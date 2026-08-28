"""Canonical Phase 3 business evidence built from accepted Phase 2 bases.

The module does not redefine either governed funnel. It reuses Phase 2 stage
counts and formulas, then adds only the approved diagnostics needed for the
nine business questions: first ride, segmentation, request hour, and the
review-without-Paid anomaly.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from analysis import funnel

PLATFORMS = ("ios", "android", "web")
SOURCE_RECORDED_HOUR = "source-recorded hour"
MISSING_SEGMENT_LABEL = "<missing>"

CANONICAL_SQL_PATH = (
    Path(__file__).resolve().parents[1]
    / "sql"
    / "production"
    / "03_business_insights.sql"
)
REQUIRED_SQL_QUERIES = {"first_ride_diagnostic"}
_QUERY_PATTERN = re.compile(
    r"^-- name: (?P<name>[a-z0-9_]+)\s*$\n(?P<sql>.*?)^-- end\s*$",
    re.MULTILINE | re.DOTALL,
)


def _percentage(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else 100.0 * numerator / denominator


def overall_transition_summary(
    counts: dict[str, int],
    stages: list[str],
) -> pd.DataFrame:
    """Return adjacent transitions using the accepted Phase 2 formulas."""
    rates = funnel.adjacent_rates(counts, stages)
    rows = []
    for index in range(1, len(stages)):
        current = rates.iloc[index]
        rows.append(
            {
                "transition": f"{stages[index - 1]} -> {stages[index]}",
                "start_count": int(current["previous_count"]),
                "end_count": int(current["count"]),
                "conversion_rate_pct": current["conversion_rate_pct"],
                "dropoff_count": int(current["dropoff_count"]),
                "dropoff_rate_pct": current["dropoff_rate_pct"],
            }
        )
    return pd.DataFrame(rows)


def overall_transition_summaries(phase2_analysis: dict) -> dict[str, pd.DataFrame]:
    """Build the two approved funnel summaries without mixing their grains."""
    return {
        "user": overall_transition_summary(
            phase2_analysis["user_counts"], funnel.USER_STAGES
        ),
        "ride": overall_transition_summary(
            phase2_analysis["ride_counts"], funnel.RIDE_STAGES
        ),
    }


def _observed_timestamp(
    values: pd.Series,
    source_cutoff: pd.Timestamp | None,
) -> pd.Series:
    observed = values.notna()
    if source_cutoff is not None:
        observed &= values.le(pd.Timestamp(source_cutoff))
    return observed


def first_ride_diagnostic(
    ride_base: pd.DataFrame,
    source_cutoff: pd.Timestamp | None = None,
) -> dict[str, object]:
    """Select one first ride only after checking every ambiguity condition.

    The diagnostic operates at registered-user grain within the supplied ride
    cohort. A missing or conflicting request timestamp, or more than one ride
    at the earliest timestamp, excludes that user from first-ride selection.
    No ride identifier or input row order is used as a tie-break.
    """
    required = {
        "ride_id", "user_id", "request_ts", "request_ts_missing",
        "request_ts_conflict", "signup_count", "accepted", "pickup_ts",
        "finished", "cancel_ts", "cancel_after_accept",
    }
    missing_columns = required - set(ride_base.columns)
    if missing_columns:
        raise ValueError(
            f"ride_base is missing first-ride fields: {sorted(missing_columns)}"
        )

    registered = ride_base.loc[
        ride_base["user_id"].notna() & ride_base["signup_count"].gt(0)
    ].copy()
    registered["_request_missing"] = (
        registered["request_ts"].isna()
        | registered["request_ts_missing"].astype(bool)
    )

    user_checks = registered.groupby("user_id", sort=False).agg(
        missing_request_ts=("_request_missing", "any"),
        conflicting_request_ts=("request_ts_conflict", "any"),
        earliest_request_ts=("request_ts", "min"),
        ever_finished=("finished", "any"),
    )

    candidates = registered.merge(
        user_checks[["earliest_request_ts"]],
        left_on="user_id",
        right_index=True,
        how="left",
        validate="many_to_one",
    )
    candidates["_is_earliest"] = (
        candidates["request_ts"].notna()
        & candidates["request_ts"].eq(candidates["earliest_request_ts"])
    )
    earliest_counts = (
        candidates.loc[candidates["_is_earliest"]]
        .groupby("user_id")
        .size()
    )
    user_checks["earliest_candidate_count"] = (
        earliest_counts.reindex(user_checks.index).fillna(0).astype("int64")
    )
    user_checks["earliest_timestamp_tie"] = user_checks[
        "earliest_candidate_count"
    ].gt(1)
    user_checks["ambiguous"] = (
        user_checks["missing_request_ts"]
        | user_checks["conflicting_request_ts"]
        | user_checks["earliest_timestamp_tie"]
    )

    eligible_users = user_checks.index[~user_checks["ambiguous"]]
    first_rides = candidates.loc[
        candidates["user_id"].isin(eligible_users)
        & candidates["_is_earliest"]
    ].copy()
    if first_rides["user_id"].duplicated().any():
        raise ValueError("more than one first ride was selected for a user")
    if len(first_rides) != len(eligible_users):
        raise ValueError("an eligible user did not resolve to exactly one first ride")

    first_rides = first_rides.merge(
        user_checks[["ever_finished"]],
        left_on="user_id",
        right_index=True,
        how="left",
        validate="one_to_one",
        suffixes=("", "_user"),
    )
    first_rides["first_requested"] = True
    first_rides["first_accepted"] = first_rides["accepted"].astype(bool)
    first_rides["first_picked_up"] = _observed_timestamp(
        first_rides["pickup_ts"], source_cutoff
    )
    first_rides["first_finished"] = first_rides["finished"].astype(bool)
    first_rides["cancellation_observed"] = _observed_timestamp(
        first_rides["cancel_ts"], source_cutoff
    )

    stage_columns = {
        "requested": "first_requested",
        "accepted": "first_accepted",
        "picked_up": "first_picked_up",
        "finished": "first_finished",
    }
    stage_counts = {
        stage: int(first_rides[column].sum())
        for stage, column in stage_columns.items()
    }
    progression = funnel.adjacent_rates(
        stage_counts, ["requested", "accepted", "picked_up", "finished"]
    )

    totals = {
        "registered_users_with_request": len(user_checks),
        "users_with_missing_request_ts": int(
            user_checks["missing_request_ts"].sum()
        ),
        "users_with_conflicting_request_ts": int(
            user_checks["conflicting_request_ts"].sum()
        ),
        "users_with_earliest_tie": int(
            user_checks["earliest_timestamp_tie"].sum()
        ),
        "ambiguous_users": int(user_checks["ambiguous"].sum()),
        "unambiguous_users": int((~user_checks["ambiguous"]).sum()),
        "selected_first_rides": len(first_rides),
        "requested_first_rides": stage_counts["requested"],
        "accepted_first_rides": stage_counts["accepted"],
        "picked_up_first_rides": stage_counts["picked_up"],
        "finished_first_rides": stage_counts["finished"],
        "any_cancellation_evidence": int(
            first_rides["cancellation_observed"].sum()
        ),
        "cancel_after_accept_first_rides": int(
            first_rides["cancel_after_accept"].sum()
        ),
        "cancelled_without_recorded_acceptance": int(
            (
                first_rides["cancellation_observed"]
                & ~first_rides["first_accepted"]
            ).sum()
        ),
        "first_unfinished_but_later_finished": int(
            (
                ~first_rides["first_finished"]
                & first_rides["ever_finished"].astype(bool)
            ).sum()
        ),
    }
    return {
        "totals": {key: int(value) for key, value in totals.items()},
        "progression": progression,
        "ambiguity_by_user": user_checks.reset_index(),
        "first_rides": first_rides.drop(
            columns=["_request_missing", "_is_earliest"], errors="ignore"
        ).reset_index(drop=True),
    }


def _segment_label(value: object) -> str:
    return MISSING_SEGMENT_LABEL if pd.isna(value) else str(value)


def _segment_stage_counts(
    base: pd.DataFrame,
    segment: str,
    stages: list[str],
    preferred_values: tuple[str, ...],
) -> pd.DataFrame:
    counts = funnel.segment_counts(base, segment, stages).copy()
    counts[segment] = [
        _segment_label(value) for value in counts[segment].astype("object")
    ]
    present = set(counts[segment])
    missing_rows = [
        {segment: value, **{stage: 0 for stage in stages}}
        for value in preferred_values
        if value not in present
    ]
    if missing_rows:
        counts = pd.concat([counts, pd.DataFrame(missing_rows)], ignore_index=True)
    order = {value: index for index, value in enumerate(preferred_values)}
    counts["_order"] = counts[segment].map(
        lambda value: order.get(value, len(order))
    )
    return (
        counts.sort_values(["_order", segment], kind="stable")
        .drop(columns="_order")
        .reset_index(drop=True)
    )


def _segment_transition_summary(
    stage_counts: pd.DataFrame,
    segment: str,
    stages: list[str],
) -> pd.DataFrame:
    overall = {
        stage: int(stage_counts[stage].sum()) for stage in stages
    }
    overall_rates = funnel.adjacent_rates(overall, stages).set_index("stage")
    rows = []
    for _, segment_row in stage_counts.iterrows():
        segment_counts = {
            stage: int(segment_row[stage]) for stage in stages
        }
        segment_rates = funnel.adjacent_rates(
            segment_counts, stages
        ).set_index("stage")
        for index in range(1, len(stages)):
            previous, current = stages[index - 1], stages[index]
            segment_rate = segment_rates.loc[current, "conversion_rate_pct"]
            overall_rate = overall_rates.loc[current, "conversion_rate_pct"]
            rows.append(
                {
                    segment: segment_row[segment],
                    "transition": f"{previous} -> {current}",
                    "start_count": segment_counts[previous],
                    "end_count": segment_counts[current],
                    "conversion_rate_pct": segment_rate,
                    "dropoff_count": int(
                        segment_rates.loc[current, "dropoff_count"]
                    ),
                    "dropoff_rate_pct": segment_rates.loc[
                        current, "dropoff_rate_pct"
                    ],
                    "overall_conversion_rate_pct": overall_rate,
                    "difference_from_overall_pp": (
                        None
                        if pd.isna(segment_rate) or pd.isna(overall_rate)
                        else float(segment_rate - overall_rate)
                    ),
                    "volume_share_pct": _percentage(
                        segment_counts[stages[0]], overall[stages[0]]
                    ),
                }
            )
    return pd.DataFrame(rows)


def platform_comparison(
    user_base: pd.DataFrame,
    ride_base: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Compare named platforms while keeping explicit extra categories."""
    user_counts = _segment_stage_counts(
        user_base, "platform", funnel.USER_STAGES, PLATFORMS
    )
    ride_counts = _segment_stage_counts(
        ride_base, "platform", funnel.RIDE_STAGES, PLATFORMS
    )
    return {
        "user_stage_counts": user_counts,
        "user_transitions": _segment_transition_summary(
            user_counts, "platform", funnel.USER_STAGES
        ),
        "ride_stage_counts": ride_counts,
        "ride_transitions": _segment_transition_summary(
            ride_counts, "platform", funnel.RIDE_STAGES
        ),
    }


def age_comparison(
    user_base: pd.DataFrame,
    ride_base: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Compare age from signup onward and preserve unavailable categories."""
    preferred = (
        "18-24", "25-34", "35-44", "45-54", "Unknown",
        funnel.NO_SIGNUP_AGE,
    )
    user_counts = _segment_stage_counts(
        user_base, "age_group", funnel.USER_STAGES, preferred
    )
    ride_counts = _segment_stage_counts(
        ride_base, "age_group", funnel.RIDE_STAGES, preferred
    )
    user_interpretable = user_counts[
        ["age_group", "signed_up", "requested", "completed"]
    ].copy()
    return {
        "user_stage_counts": user_counts,
        "user_transitions": _segment_transition_summary(
            user_interpretable,
            "age_group",
            ["signed_up", "requested", "completed"],
        ),
        "ride_stage_counts": ride_counts,
        "ride_transitions": _segment_transition_summary(
            ride_counts, "age_group", funnel.RIDE_STAGES
        ),
    }


def request_hour_summary(ride_base: pd.DataFrame) -> dict[str, object]:
    """Summarize request activity without assigning or converting a timezone."""
    request_ts = pd.to_datetime(ride_base["request_ts"], errors="raise")
    if request_ts.dt.tz is not None:
        raise ValueError("request_ts must remain a source-local naive timestamp")

    working = ride_base.copy()
    working["_request_ts"] = request_ts
    timestamped = working.loc[working["_request_ts"].notna()].copy()
    timestamped[SOURCE_RECORDED_HOUR] = timestamped["_request_ts"].dt.hour
    hourly = (
        timestamped.groupby(SOURCE_RECORDED_HOUR)
        .agg(
            requested_count=("ride_id", "size"),
            accepted_count=("accepted", "sum"),
            finished_count=("finished", "sum"),
            cancel_after_accept_count=("cancel_after_accept", "sum"),
        )
        .reindex(range(24), fill_value=0)
        .reset_index()
    )
    population = len(working)
    hourly["request_share_pct"] = hourly["requested_count"].map(
        lambda value: _percentage(int(value), population)
    )
    for count_column, rate_column in (
        ("accepted_count", "accepted_rate_pct"),
        ("finished_count", "finished_rate_pct"),
        ("cancel_after_accept_count", "cancel_after_accept_rate_pct"),
    ):
        hourly[rate_column] = [
            _percentage(int(numerator), int(denominator))
            for numerator, denominator in zip(
                hourly[count_column], hourly["requested_count"]
            )
        ]

    missing_count = int(working["_request_ts"].isna().sum())
    missing_evidence_count = (
        int(working["request_ts_missing"].astype(bool).sum())
        if "request_ts_missing" in working
        else missing_count
    )
    hourly_count = int(hourly["requested_count"].sum())
    top_three_hours = hourly.nlargest(3, "requested_count")[
        SOURCE_RECORDED_HOUR
    ].astype(int).tolist()
    top_six_hours = sorted(
        hourly.nlargest(6, "requested_count")[SOURCE_RECORDED_HOUR]
        .astype(int)
        .tolist()
    )
    top_three_rides = timestamped.loc[
        timestamped[SOURCE_RECORDED_HOUR].isin(top_three_hours)
    ]
    overall_rates = {
        "accepted_rate_pct": _percentage(
            int(working["accepted"].sum()), population
        ),
        "finished_rate_pct": _percentage(
            int(working["finished"].sum()), population
        ),
        "cancel_after_accept_rate_pct": _percentage(
            int(working["cancel_after_accept"].sum()), population
        ),
    }
    top_three_rates = {
        "accepted_rate_pct": _percentage(
            int(top_three_rides["accepted"].sum()), len(top_three_rides)
        ),
        "finished_rate_pct": _percentage(
            int(top_three_rides["finished"].sum()), len(top_three_rides)
        ),
        "cancel_after_accept_rate_pct": _percentage(
            int(top_three_rides["cancel_after_accept"].sum()),
            len(top_three_rides),
        ),
    }
    return {
        "hourly": hourly,
        "ride_population": population,
        "timestamped_request_count": len(timestamped),
        "missing_request_timestamp_count": missing_count,
        "request_timestamp_missing_evidence_count": missing_evidence_count,
        "hourly_requested_count": hourly_count,
        "reconciles_to_timestamped_requests": hourly_count == len(timestamped),
        "reconciles_to_ride_population": hourly_count + missing_count == population,
        "top_three_hours": top_three_hours,
        "top_six_hours": top_six_hours,
        "top_six_request_share_pct": _percentage(
            int(
                hourly.loc[
                    hourly[SOURCE_RECORDED_HOUR].isin(top_six_hours),
                    "requested_count",
                ].sum()
            ),
            population,
        ),
        "overall_rates_pct": overall_rates,
        "top_three_rates_pct": top_three_rates,
        "top_three_minus_overall_pp": {
            key: (
                None
                if top_three_rates[key] is None or overall_rates[key] is None
                else top_three_rates[key] - overall_rates[key]
            )
            for key in overall_rates
        },
        "timezone_note": "source-recorded hour; timezone unavailable",
    }


def review_without_paid_decomposition(
    ride_base: pd.DataFrame,
) -> dict[str, object]:
    """Decompose the anomaly without changing Paid or Reviewed membership."""
    anomaly = ride_base.loc[
        ride_base["has_review"].astype(bool) & ~ride_base["paid"].astype(bool)
    ].copy()
    anomaly["finish_status"] = anomaly["finished"].map(
        {True: "Finished", False: "Did not Finish"}
    )
    anomaly["transaction_evidence"] = anomaly["tx_count"].gt(0).map(
        {True: "Has transaction", False: "No transaction"}
    )
    anomaly["approved_transaction"] = anomaly["has_approved"].map(
        {True: "Has Approved", False: "No Approved"}
    )
    decomposition = (
        anomaly.groupby(
            ["finish_status", "transaction_evidence", "approved_transaction"],
            dropna=False,
        )
        .size()
        .rename("count")
        .reset_index()
    )
    population = len(anomaly)
    decomposition["population_share_pct"] = decomposition["count"].map(
        lambda value: _percentage(int(value), population)
    )
    if int(decomposition["count"].sum()) != population:
        raise ValueError("review-without-Paid categories do not reconcile")
    all_review_evidence = int(ride_base["has_review"].sum())
    paid_count = int(ride_base["paid"].sum())
    reviewed_count = int(ride_base["reviewed"].sum())
    return {
        "population_count": population,
        "decomposition": decomposition,
        "all_review_evidence_count": all_review_evidence,
        "anomaly_share_of_all_review_evidence_pct": _percentage(
            population, all_review_evidence
        ),
        "canonical_paid_count": paid_count,
        "canonical_reviewed_count": reviewed_count,
        "canonical_paid_to_reviewed_pct": _percentage(
            reviewed_count, paid_count
        ),
    }


def load_canonical_queries(
    path: Path = CANONICAL_SQL_PATH,
) -> dict[str, str]:
    """Load the named Phase 3 production SQL statements."""
    contents = path.read_text(encoding="utf-8")
    queries = {
        match.group("name"): match.group("sql").strip()
        for match in _QUERY_PATTERN.finditer(contents)
    }
    missing = REQUIRED_SQL_QUERIES - queries.keys()
    if missing:
        raise ValueError(f"Phase 3 SQL is missing named queries: {sorted(missing)}")
    return queries


def run_first_ride_sql(
    engine: Engine,
    parameters: funnel.AnalysisParameters,
) -> dict[str, int]:
    """Execute the independent SQL first-ride diagnostic cross-check."""
    query = load_canonical_queries()["first_ride_diagnostic"]
    with engine.connect() as connection:
        result = pd.read_sql(
            text(query),
            connection,
            params=funnel.sql_parameter_values(parameters),
        )
    if len(result) != 1:
        raise ValueError("first_ride_diagnostic SQL must return exactly one row")
    return {column: int(result.loc[0, column]) for column in result.columns}


def reconcile_first_ride_totals(
    pandas_totals: dict[str, int],
    sql_totals: dict[str, int],
) -> dict[str, object]:
    """Compare every first-ride diagnostic total exactly."""
    keys = pandas_totals.keys() | sql_totals.keys()
    comparisons = {
        key: {
            "pandas": pandas_totals.get(key),
            "sql": sql_totals.get(key),
            "match": pandas_totals.get(key) == sql_totals.get(key),
        }
        for key in sorted(keys)
    }
    return {
        "comparisons": comparisons,
        "all_match": all(item["match"] for item in comparisons.values()),
    }


def _validate_phase2_analysis(phase2_analysis: dict) -> None:
    expected_user = funnel.stage_counts(
        phase2_analysis["user_base"], funnel.USER_STAGES
    )
    expected_ride = funnel.stage_counts(
        phase2_analysis["ride_base"], funnel.RIDE_STAGES
    )
    if expected_user != phase2_analysis["user_counts"]:
        raise ValueError("Phase 2 user counts do not match the accepted base")
    if expected_ride != phase2_analysis["ride_counts"]:
        raise ValueError("Phase 2 ride counts do not match the accepted base")
    validation_keys = (
        "user_monotonic_violations", "ride_monotonic_violations",
        "user_subset_violations", "ride_subset_violations",
        "segment_reconciliation_errors",
    )
    failures = {
        key: phase2_analysis[key]
        for key in validation_keys
        if phase2_analysis.get(key)
    }
    if failures:
        raise ValueError(f"Phase 2 base validation failed: {failures}")


def run_business_insights(
    engine: Engine | None,
    parameters: funnel.AnalysisParameters | None = None,
    phase2_analysis: dict | None = None,
    include_sql_crosscheck: bool = True,
) -> dict[str, object]:
    """Run all approved Phase 3 evidence from one accepted Phase 2 result."""
    if phase2_analysis is None:
        if engine is None:
            raise ValueError("engine is required when phase2_analysis is not supplied")
        resolved = funnel.resolve_parameters(engine, parameters)
        phase2_analysis = funnel.run_funnel_analysis(engine, resolved)
    else:
        resolved = phase2_analysis["parameters"]
        if parameters is not None and parameters != resolved:
            raise ValueError("parameters must match the supplied Phase 2 analysis")

    _validate_phase2_analysis(phase2_analysis)
    user_base = phase2_analysis["user_base"]
    ride_base = phase2_analysis["ride_base"]
    first_ride = first_ride_diagnostic(ride_base, resolved.source_cutoff)

    sql_totals = None
    first_ride_reconciliation = None
    if include_sql_crosscheck:
        if engine is None:
            raise ValueError("engine is required for the SQL cross-check")
        sql_totals = run_first_ride_sql(engine, resolved)
        first_ride_reconciliation = reconcile_first_ride_totals(
            first_ride["totals"], sql_totals
        )

    return {
        "parameters": resolved,
        "phase2_counts": {
            "user": dict(phase2_analysis["user_counts"]),
            "ride": dict(phase2_analysis["ride_counts"]),
        },
        "overall_transitions": overall_transition_summaries(phase2_analysis),
        "first_ride": first_ride,
        "platform": platform_comparison(user_base, ride_base),
        "age": age_comparison(user_base, ride_base),
        "request_hour": request_hour_summary(ride_base),
        "review_without_paid": review_without_paid_decomposition(ride_base),
        "sql_first_ride_totals": sql_totals,
        "first_ride_reconciliation": first_ride_reconciliation,
    }
