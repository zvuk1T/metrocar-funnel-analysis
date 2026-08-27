"""Exact reconciliation of canonical SQL and independent Pandas outputs."""

from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from analysis import funnel

CANONICAL_SQL_PATH = (
    Path(__file__).resolve().parents[1]
    / "sql"
    / "production"
    / "02_funnel_analysis.sql"
)
REQUIRED_QUERIES = {"source_cutoff", "user_base", "ride_base", "source_validation"}
_QUERY_PATTERN = re.compile(
    r"^-- name: (?P<name>[a-z0-9_]+)\s*$\n(?P<sql>.*?)^-- end\s*$",
    re.MULTILINE | re.DOTALL,
)


def load_canonical_queries(path: Path = CANONICAL_SQL_PATH) -> dict[str, str]:
    """Load named executable statements from the sole analytical SQL file."""
    contents = path.read_text(encoding="utf-8")
    queries = {
        match.group("name"): match.group("sql").strip()
        for match in _QUERY_PATTERN.finditer(contents)
    }
    missing = REQUIRED_QUERIES - queries.keys()
    if missing:
        raise ValueError(f"canonical SQL is missing named queries: {sorted(missing)}")
    return queries


def run_canonical_sql(
    engine: Engine,
    parameters: funnel.AnalysisParameters,
) -> dict[str, object]:
    """Execute every canonical SQL result with one shared parameter mapping."""
    queries = load_canonical_queries()
    sql_parameters = funnel.sql_parameter_values(parameters)
    with engine.connect() as connection:
        cutoff = pd.read_sql(text(queries["source_cutoff"]), connection)
        user_base = pd.read_sql(
            text(queries["user_base"]), connection, params=sql_parameters
        )
        ride_base = pd.read_sql(
            text(queries["ride_base"]), connection, params=sql_parameters
        )
        source_validation = pd.read_sql(
            text(queries["source_validation"]), connection, params=sql_parameters
        )
    if source_validation.empty:
        raise ValueError("canonical source_validation returned no row")
    source_totals = {
        key: int(value) for key, value in source_validation.iloc[0].items()
    }
    validation_totals = funnel.base_validation_totals(user_base, ride_base)
    validation_totals.update(source_totals)
    return {
        "source_cutoff": pd.Timestamp(cutoff.loc[0, "source_cutoff"]),
        "user_base": user_base,
        "ride_base": ride_base,
        "user_counts": funnel.stage_counts(user_base, funnel.USER_STAGES),
        "ride_counts": funnel.stage_counts(ride_base, funnel.RIDE_STAGES),
        "user_rates": funnel.adjacent_rates(
            funnel.stage_counts(user_base, funnel.USER_STAGES), funnel.USER_STAGES
        ),
        "ride_rates": funnel.adjacent_rates(
            funnel.stage_counts(ride_base, funnel.RIDE_STAGES), funnel.RIDE_STAGES
        ),
        "validation_totals": validation_totals,
        "ride_diagnostics": {
            "accepted": int(ride_base["accepted"].sum()),
            "cancel_after_accept": int(ride_base["cancel_after_accept"].sum()),
        },
    }


def _compare_counts(
    sql_counts: dict[str, int],
    pandas_counts: dict[str, int],
) -> dict[str, dict[str, object]]:
    return {
        metric: {
            "sql": int(sql_counts[metric]),
            "pandas": int(pandas_counts[metric]),
            "match": int(sql_counts[metric]) == int(pandas_counts[metric]),
        }
        for metric in sql_counts.keys() | pandas_counts.keys()
    }


def compare_bases(
    sql_base: pd.DataFrame,
    pandas_base: pd.DataFrame,
    identifier: str,
    columns: list[str],
) -> dict[str, object]:
    """Compare grain identifiers and material membership/attribution columns."""
    sql_unique = sql_base[identifier].notna().all() and sql_base[identifier].is_unique
    pandas_unique = (
        pandas_base[identifier].notna().all()
        and pandas_base[identifier].is_unique
    )
    sql_ids = set(sql_base[identifier].dropna().tolist())
    pandas_ids = set(pandas_base[identifier].dropna().tolist())
    identifiers_match = sql_unique and pandas_unique and sql_ids == pandas_ids
    if not sql_unique or not pandas_unique:
        return {
            "identifiers_match": False,
            "sql_only_identifiers": len(sql_ids - pandas_ids),
            "pandas_only_identifiers": len(pandas_ids - sql_ids),
            "column_mismatches": {column: None for column in columns},
            "all_match": False,
        }

    merged = sql_base[[identifier, *columns]].merge(
        pandas_base[[identifier, *columns]],
        how="outer",
        on=identifier,
        suffixes=("_sql", "_pandas"),
        indicator=True,
        validate="one_to_one",
    )
    mismatches: dict[str, int] = {}
    both = merged["_merge"].eq("both")
    for column in columns:
        left = merged[f"{column}_sql"]
        right = merged[f"{column}_pandas"]
        both_missing = left.isna() & right.isna()
        comparable = left.notna() & right.notna()
        equal = both_missing.copy()
        equal.loc[comparable] = (
            left.loc[comparable].astype("object").to_numpy()
            == right.loc[comparable].astype("object").to_numpy()
        )
        mismatches[column] = int((~both | ~equal).sum())
    return {
        "identifiers_match": identifiers_match,
        "sql_only_identifiers": len(sql_ids - pandas_ids),
        "pandas_only_identifiers": len(pandas_ids - sql_ids),
        "column_mismatches": mismatches,
        "all_match": identifiers_match and all(value == 0 for value in mismatches.values()),
    }


def _segment_mapping(
    base: pd.DataFrame,
    segment: str,
    stages: list[str],
) -> dict[tuple[object, str], int]:
    segmented = funnel.segment_counts(base, segment, stages)
    result = {}
    for _, row in segmented.iterrows():
        category = None if pd.isna(row[segment]) else row[segment]
        for stage in stages:
            result[(category, stage)] = int(row[stage])
    return result


def compare_segments(
    sql_base: pd.DataFrame,
    pandas_base: pd.DataFrame,
    segment: str,
    stages: list[str],
) -> dict[str, object]:
    sql_values = _segment_mapping(sql_base, segment, stages)
    pandas_values = _segment_mapping(pandas_base, segment, stages)
    keys = sql_values.keys() | pandas_values.keys()
    mismatches = sum(sql_values.get(key) != pandas_values.get(key) for key in keys)
    return {
        "match": mismatches == 0,
        "mismatch_count": int(mismatches),
        "category_stage_values": len(keys),
    }


def compare_rates(
    sql_rates: pd.DataFrame,
    pandas_rates: pd.DataFrame,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    columns = ("conversion_rate_pct", "dropoff_rate_pct")
    left = sql_rates.set_index("stage")
    right = pandas_rates.set_index("stage")
    stages_match = set(left.index) == set(right.index)
    mismatches = 0
    if stages_match:
        for stage in left.index:
            for column in columns:
                sql_value, pandas_value = left.loc[stage, column], right.loc[stage, column]
                if pd.isna(sql_value) and pd.isna(pandas_value):
                    continue
                if pd.isna(sql_value) or pd.isna(pandas_value) or not math.isclose(
                    float(sql_value), float(pandas_value), rel_tol=tolerance,
                    abs_tol=tolerance,
                ):
                    mismatches += 1
    return {
        "match": stages_match and mismatches == 0,
        "mismatch_count": mismatches,
    }


def reconcile(
    engine: Engine,
    parameters: funnel.AnalysisParameters | None = None,
) -> dict[str, object]:
    """Reconcile grain, membership, attribution, segments, rates, and checks."""
    resolved = funnel.resolve_parameters(engine, parameters)
    pandas_result = funnel.run_funnel_analysis(engine, resolved)
    sql_result = run_canonical_sql(engine, resolved)

    user_counts = _compare_counts(
        sql_result["user_counts"], pandas_result["user_counts"]
    )
    ride_counts = _compare_counts(
        sql_result["ride_counts"], pandas_result["ride_counts"]
    )
    diagnostics = _compare_counts(
        sql_result["ride_diagnostics"], pandas_result["ride_diagnostics"]
    )

    user_base = compare_bases(
        sql_result["user_base"],
        pandas_result["user_base"],
        "app_download_key",
        ["platform", "age_group", *funnel.USER_STAGES],
    )
    ride_base = compare_bases(
        sql_result["ride_base"],
        pandas_result["ride_base"],
        "ride_id",
        [
            "platform", "age_group", *funnel.RIDE_STAGES, "accepted",
            "cancel_after_accept", "has_approved", "has_review", "tx_count",
            "approved_count", "review_count",
        ],
    )
    platform_segments = {
        "user": compare_segments(
            sql_result["user_base"], pandas_result["user_base"],
            "platform", funnel.USER_STAGES,
        ),
        "ride": compare_segments(
            sql_result["ride_base"], pandas_result["ride_base"],
            "platform", funnel.RIDE_STAGES,
        ),
    }
    age_segments = {
        "user": compare_segments(
            sql_result["user_base"], pandas_result["user_base"],
            "age_group", funnel.USER_STAGES,
        ),
        "ride": compare_segments(
            sql_result["ride_base"], pandas_result["ride_base"],
            "age_group", funnel.RIDE_STAGES,
        ),
    }
    rates = {
        "user": compare_rates(sql_result["user_rates"], pandas_result["user_rates"]),
        "ride": compare_rates(sql_result["ride_rates"], pandas_result["ride_rates"]),
    }
    validation = _compare_counts(
        sql_result["validation_totals"], pandas_result["validation_totals"]
    )

    sections_match = (
        all(item["match"] for item in user_counts.values())
        and all(item["match"] for item in ride_counts.values())
        and all(item["match"] for item in diagnostics.values())
        and user_base["all_match"]
        and ride_base["all_match"]
        and all(item["match"] for item in platform_segments.values())
        and all(item["match"] for item in age_segments.values())
        and all(item["match"] for item in rates.values())
        and all(item["match"] for item in validation.values())
    )
    return {
        "parameters": resolved,
        "user_funnel": user_counts,
        "ride_funnel": ride_counts,
        "diagnostics": diagnostics,
        "user_base": user_base,
        "ride_base": ride_base,
        "platform_segments": platform_segments,
        "age_segments": age_segments,
        "rates": rates,
        "validation_totals": validation,
        "all_match": sections_match,
        "analysis": pandas_result,
        "sql": sql_result,
    }
