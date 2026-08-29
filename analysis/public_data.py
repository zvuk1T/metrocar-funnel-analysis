"""Generate the small, browser-safe Phase 4A funnel artifact.

The exporter runs the accepted SQL/Pandas reconciliation first. Only after
that succeeds does it reduce the canonical full-snapshot analysis to four
aggregate stages per funnel. No entrant, user, ride, or source rows cross the
public-data boundary.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Mapping

import pandas as pd

from analysis import db, funnel, reconcile

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT / "web" / "public" / "data" / "metrocar-funnels.json"
)

FUNNEL_PRESENTATION = {
    "user": {
        "label": "User Funnel",
        "grain": "One recorded app-download entrant",
        "unit": "download entrants",
        "stages": {
            "downloaded": "Downloaded",
            "signed_up": "Signed Up",
            "requested": "Requested",
            "completed": "Completed",
        },
    },
    "ride": {
        "label": "Ride Funnel",
        "grain": "One distinct requested ride",
        "unit": "rides",
        "stages": {
            "requested": "Requested",
            "finished": "Finished",
            "paid": "Paid",
            "reviewed": "Reviewed",
        },
    },
}


def _validate_reconciliation(result: Mapping[str, object]) -> Mapping[str, object]:
    """Fail closed when the canonical full-snapshot evidence is not publishable."""
    if result.get("all_match") is not True:
        raise ValueError("SQL/Pandas reconciliation did not pass")

    analysis = result.get("analysis")
    if not isinstance(analysis, Mapping):
        raise ValueError("reconciliation is missing its canonical analysis result")

    parameters = analysis.get("parameters")
    if not isinstance(parameters, funnel.AnalysisParameters):
        raise ValueError("analysis parameters are missing or invalid")
    if parameters.cohort_start is not None or parameters.cohort_end_exclusive is not None:
        raise ValueError("Phase 4A public data must use the unfiltered full snapshot")
    if parameters.source_cutoff is None:
        raise ValueError("source cutoff must be resolved before public export")

    validation_keys = (
        "user_monotonic_violations",
        "ride_monotonic_violations",
        "user_subset_violations",
        "ride_subset_violations",
        "segment_reconciliation_errors",
    )
    failed = [key for key in validation_keys if analysis.get(key) != []]
    if failed:
        raise ValueError(f"canonical validations failed: {', '.join(failed)}")

    return analysis


def _stage_rows(
    counts: Mapping[str, int],
    rates: pd.DataFrame,
    stage_labels: Mapping[str, str],
) -> list[dict[str, object]]:
    """Reduce canonical counts and rates to the three approved label modes."""
    stages = list(stage_labels)
    if set(counts) != set(stages):
        raise ValueError("canonical stage keys do not match the public schema")
    if rates["stage"].tolist() != stages:
        raise ValueError("canonical rate rows do not match the governed stage order")

    exact_counts = {stage: int(counts[stage]) for stage in stages}
    if any(value < 0 for value in exact_counts.values()):
        raise ValueError("stage counts must be non-negative")
    monotonic_errors = funnel.validate_monotonic(exact_counts, stages)
    if monotonic_errors:
        raise ValueError("stage counts are not monotonic")

    top_count = exact_counts[stages[0]]
    rows: list[dict[str, object]] = []
    for index, stage in enumerate(stages):
        count = exact_counts[stage]
        rate_value = rates.iloc[index]["conversion_rate_pct"]
        percent_of_previous = None if pd.isna(rate_value) else float(rate_value)

        if index > 0:
            previous_count = exact_counts[stages[index - 1]]
            expected_rate = (
                None if previous_count == 0 else 100.0 * count / previous_count
            )
            if expected_rate is None and percent_of_previous is not None:
                raise ValueError("zero-denominator rate must remain unavailable")
            if expected_rate is not None and (
                percent_of_previous is None
                or not math.isclose(
                    percent_of_previous,
                    expected_rate,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                )
            ):
                raise ValueError("canonical adjacent rate does not match exact counts")

        percent_of_top = (
            100.0
            if index == 0
            else None if top_count == 0 else 100.0 * count / top_count
        )
        rows.append(
            {
                "key": stage,
                "label": stage_labels[stage],
                "count": count,
                "percentOfTop": percent_of_top,
                "percentOfPrevious": percent_of_previous,
            }
        )
    return rows


def build_public_payload(result: Mapping[str, object]) -> dict[str, object]:
    """Build the deterministic Phase 4A schema from reconciled canonical output."""
    analysis = _validate_reconciliation(result)
    parameters = analysis["parameters"]
    assert isinstance(parameters, funnel.AnalysisParameters)

    funnels: dict[str, object] = {}
    for funnel_key in ("user", "ride"):
        presentation = FUNNEL_PRESENTATION[funnel_key]
        funnels[funnel_key] = {
            "label": presentation["label"],
            "grain": presentation["grain"],
            "unit": presentation["unit"],
            "stages": _stage_rows(
                analysis[f"{funnel_key}_counts"],
                analysis[f"{funnel_key}_rates"],
                presentation["stages"],
            ),
        }

    return {
        "schemaVersion": 1,
        "scope": {
            "kind": "full_snapshot",
            "sourceCutoff": parameters.source_cutoff.isoformat(timespec="seconds"),
            "cohortStart": None,
            "cohortEndExclusive": None,
        },
        "funnels": funnels,
        "traceability": {
            "metricContract": "docs/METRIC_DEFINITION_CONTRACT.md",
            "python": "analysis.funnel.run_funnel_analysis",
            "sql": "sql/production/02_funnel_analysis.sql",
        },
    }


def serialise_payload(payload: Mapping[str, object]) -> str:
    """Return stable bytes: sorted keys, fixed indentation, and no NaN values."""
    return json.dumps(
        payload,
        allow_nan=False,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def write_public_payload(payload: Mapping[str, object], output_path: Path) -> None:
    """Atomically replace the artifact only after the payload is fully validated."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            dir=output_path.parent,
            encoding="utf-8",
            delete=False,
        ) as temporary_file:
            temporary_file.write(serialise_payload(payload))
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, output_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def generate_public_data(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    """Reconcile the live snapshot and write its aggregate-only public artifact."""
    engine = db.get_engine()
    try:
        result = reconcile.reconcile(engine)
        payload = build_public_payload(result)
        write_public_payload(payload, output_path)
    finally:
        engine.dispose()
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and export the full-snapshot public funnel data."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    arguments = parser.parse_args(argv)

    try:
        output_path = generate_public_data(arguments.output)
    except db.DatabaseConfigError as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001 - never expose connection details
        print(
            "ERROR: public-data generation failed safely "
            f"({type(exc).__name__}). No artifact was published."
        )
        return 1

    print(f"Public funnel data written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
