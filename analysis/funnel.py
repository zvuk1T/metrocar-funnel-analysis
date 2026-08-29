"""Canonical Pandas implementation of the locked Phase 2 funnel contract.

The two base tables use different grains: one app-download entrant and one
ride. User Funnel grain and join conditions are validated before construction;
repeated ride activity is then reduced to Boolean results per user. The Ride
Funnel retains its grain-level source aggregation. SQL/Pandas reconciliation
uses one shared cohort and source cutoff.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime
from typing import Mapping

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

USER_STAGES = ["downloaded", "signed_up", "requested", "completed"]
RIDE_STAGES = ["requested", "finished", "paid", "reviewed"]

NO_SIGNUP_AGE = "Not available — no signup"
VALID_PLATFORMS = frozenset({"ios", "android", "web"})
VALID_AGE_GROUPS = frozenset({"18-24", "25-34", "35-44", "45-54", "Unknown"})

SOURCE_CUTOFF_QUERY = """
SELECT MAX(source_timestamp)::timestamp AS source_cutoff
FROM (
  SELECT MAX(download_ts) AS source_timestamp FROM app_downloads
  UNION ALL SELECT MAX(signup_ts) FROM signups
  UNION ALL SELECT MAX(request_ts) FROM ride_requests
  UNION ALL SELECT MAX(accept_ts) FROM ride_requests
  UNION ALL SELECT MAX(pickup_ts) FROM ride_requests
  UNION ALL SELECT MAX(dropoff_ts) FROM ride_requests
  UNION ALL SELECT MAX(cancel_ts) FROM ride_requests
  UNION ALL SELECT MAX(transaction_ts) FROM transactions
) observed_timestamps
"""


@dataclass(frozen=True)
class AnalysisParameters:
    """One reproducible cohort selection and source observation cutoff.

    ``cohort_end_exclusive`` is already the day after the user-selected
    inclusive end date. ``source_cutoff`` is the maximum timestamp observed in
    the source snapshot unless the caller supplies the already-resolved value.
    Reviews have no event timestamp, so review existence is bounded by the
    source snapshot itself rather than an invented review time.
    """

    cohort_start: pd.Timestamp | None = None
    cohort_end_exclusive: pd.Timestamp | None = None
    source_cutoff: pd.Timestamp | None = None


def calendar_parameters(
    start_date: str | date | datetime | pd.Timestamp | None = None,
    end_date: str | date | datetime | pd.Timestamp | None = None,
    source_cutoff: str | datetime | pd.Timestamp | None = None,
) -> AnalysisParameters:
    """Convert inclusive calendar dates to the contract's half-open bounds."""
    start = None if start_date is None else pd.Timestamp(start_date).normalize()
    end_exclusive = (
        None
        if end_date is None
        else pd.Timestamp(end_date).normalize() + pd.Timedelta(1, unit="D")
    )
    cutoff = None if source_cutoff is None else pd.Timestamp(source_cutoff)
    return _normalise_parameters(AnalysisParameters(start, end_exclusive, cutoff))


def _normalise_timestamp(value, name: str) -> pd.Timestamp | None:
    if value is None or pd.isna(value):
        return None
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is not None:
        raise ValueError(f"{name} must be a source-local naive timestamp")
    return timestamp


def _normalise_parameters(parameters: AnalysisParameters) -> AnalysisParameters:
    normalised = AnalysisParameters(
        _normalise_timestamp(parameters.cohort_start, "cohort_start"),
        _normalise_timestamp(
            parameters.cohort_end_exclusive, "cohort_end_exclusive"
        ),
        _normalise_timestamp(parameters.source_cutoff, "source_cutoff"),
    )
    if (
        normalised.cohort_start is not None
        and normalised.cohort_end_exclusive is not None
        and normalised.cohort_start >= normalised.cohort_end_exclusive
    ):
        raise ValueError("cohort_start must be earlier than cohort_end_exclusive")
    return normalised


def _read(
    engine: Engine,
    sql: str,
    parameters: Mapping[str, object] | None = None,
) -> pd.DataFrame:
    """Run one read-only extraction query and return a DataFrame."""
    with engine.connect() as connection:
        return pd.read_sql(text(sql), connection, params=dict(parameters or {}))


def resolve_parameters(
    engine: Engine,
    parameters: AnalysisParameters | None = None,
) -> AnalysisParameters:
    """Resolve one cutoff once so SQL and Pandas never derive separate values."""
    resolved = _normalise_parameters(parameters or AnalysisParameters())
    if resolved.source_cutoff is None:
        cutoff_frame = _read(engine, SOURCE_CUTOFF_QUERY)
        if cutoff_frame.empty or pd.isna(cutoff_frame.loc[0, "source_cutoff"]):
            raise ValueError("source snapshot has no timestamp for a reproducible cutoff")
        resolved = replace(
            resolved,
            source_cutoff=pd.Timestamp(cutoff_frame.loc[0, "source_cutoff"]),
        )
    return _normalise_parameters(resolved)


def sql_parameter_values(parameters: AnalysisParameters) -> dict[str, object]:
    """Return DBAPI-friendly values for the canonical SQL bind parameters."""
    resolved = _normalise_parameters(parameters)
    if resolved.source_cutoff is None:
        raise ValueError("source_cutoff must be resolved before SQL execution")

    def value(timestamp: pd.Timestamp | None):
        return None if timestamp is None else timestamp.to_pydatetime()

    return {
        "cohort_start": value(resolved.cohort_start),
        "cohort_end_exclusive": value(resolved.cohort_end_exclusive),
        "source_cutoff": value(resolved.source_cutoff),
    }


def load_source_frames(engine: Engine) -> dict[str, pd.DataFrame]:
    """Load only fields required by the locked Phase 2 definitions."""
    return {
        "downloads": _read(
            engine,
            "SELECT app_download_key, platform, download_ts FROM app_downloads",
        ),
        "signups": _read(
            engine,
            "SELECT user_id, session_id, signup_ts, age_range FROM signups",
        ),
        "rides": _read(
            engine,
            "SELECT ride_id, user_id, request_ts, accept_ts, pickup_ts, "
            "dropoff_ts, cancel_ts FROM ride_requests",
        ),
        "transactions": _read(
            engine,
            "SELECT ride_id, charge_status, transaction_ts FROM transactions",
        ),
        "reviews": _read(engine, "SELECT ride_id FROM reviews"),
    }


def _first_non_null(series: pd.Series):
    values = series.dropna()
    return pd.NA if values.empty else values.iloc[0]


def _source_row_mask(timestamp: pd.Series, cutoff: pd.Timestamp) -> pd.Series:
    """Keep snapshot rows with a null or not-later-than-cutoff timestamp."""
    return timestamp.isna() | timestamp.le(cutoff)


def _event_observed(timestamp: pd.Series, cutoff: pd.Timestamp) -> pd.Series:
    return timestamp.notna() & timestamp.le(cutoff)


def _cohort_mask(
    entry_timestamp: pd.Series,
    parameters: AnalysisParameters,
) -> pd.Series:
    mask = _source_row_mask(entry_timestamp, parameters.source_cutoff)
    if parameters.cohort_start is not None:
        mask &= entry_timestamp.notna() & entry_timestamp.ge(parameters.cohort_start)
    if parameters.cohort_end_exclusive is not None:
        mask &= entry_timestamp.notna() & entry_timestamp.lt(
            parameters.cohort_end_exclusive
        )
    return mask


def _require_non_null_identifier(frame: pd.DataFrame, column: str) -> None:
    if frame[column].isna().any():
        raise ValueError(f"{column} contains null grain identifiers")


def _assert_unique_base(frame: pd.DataFrame, identifier: str) -> None:
    if frame[identifier].isna().any() or not frame[identifier].is_unique:
        raise ValueError(f"{identifier} does not define one base row per entity")


def _aggregate_downloads(
    downloads: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    observed = downloads.loc[
        _source_row_mask(downloads["download_ts"], parameters.source_cutoff)
    ].copy()
    _require_non_null_identifier(observed, "app_download_key")
    grouped = observed.groupby("app_download_key", as_index=False, sort=False)
    result = grouped.agg(
        download_row_count=("app_download_key", "size"),
        download_ts=("download_ts", "min"),
        download_ts_value_count=("download_ts", lambda s: s.nunique(dropna=True)),
        download_ts_missing=("download_ts", lambda s: bool(s.isna().any())),
        platform=("platform", _first_non_null),
        platform_value_count=("platform", lambda s: s.nunique(dropna=True)),
        platform_source_missing=("platform", lambda s: bool(s.isna().any())),
    )
    result["download_ts_conflict"] = result["download_ts_value_count"].gt(1)
    result["platform_conflict"] = result["platform_value_count"].gt(1)
    unsafe_platform = (
        result["platform_value_count"].ne(1)
        | result["platform_source_missing"]
    )
    result.loc[unsafe_platform, "platform"] = pd.NA
    return result.drop(columns=["download_ts_value_count", "platform_value_count"])


def _aggregate_user_ride_flags(
    rides: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    """Reduce repeated observed rides to Requested/Completed flags per user."""
    observed = rides.loc[
        _source_row_mask(rides["request_ts"], parameters.source_cutoff)
        & rides["user_id"].notna()
    ].copy()
    if observed.empty:
        return pd.DataFrame(columns=["user_id", "requested", "completed"])
    observed["requested"] = True
    observed["completed"] = _event_observed(
        observed["dropoff_ts"], parameters.source_cutoff
    )
    return (
        observed.groupby("user_id", as_index=False, sort=False)
        .agg(requested=("requested", "any"), completed=("completed", "any"))
    )


def _observed_signups(
    signups: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    return signups.loc[
        _source_row_mask(signups["signup_ts"], parameters.source_cutoff)
    ].copy()


def _validate_user_source_conditions(
    downloads: pd.DataFrame,
    signups: pd.DataFrame,
    parameters: AnalysisParameters,
) -> None:
    """Fail before construction when User Funnel join keys are ambiguous."""
    observed_downloads = downloads.loc[
        _source_row_mask(downloads["download_ts"], parameters.source_cutoff)
    ]
    _require_non_null_identifier(observed_downloads, "app_download_key")
    duplicate_downloads = observed_downloads["app_download_key"].duplicated(
        keep=False
    )
    if duplicate_downloads.any():
        duplicate_groups = observed_downloads.loc[
            duplicate_downloads, "app_download_key"
        ].nunique()
        raise ValueError(
            "app_download_key must be unique before User Funnel construction; "
            f"found {duplicate_groups} duplicate key group(s)"
        )

    linked_signups = _observed_signups(signups, parameters).loc[
        lambda frame: frame["session_id"].notna()
    ]
    duplicate_sessions = linked_signups["session_id"].duplicated(keep=False)
    if duplicate_sessions.any():
        duplicate_groups = linked_signups.loc[
            duplicate_sessions, "session_id"
        ].nunique()
        raise ValueError(
            "session_id must identify at most one signup before User Funnel "
            f"construction; found {duplicate_groups} duplicate session group(s)"
        )

    known_users = linked_signups.loc[
        linked_signups["user_id"].notna(), "user_id"
    ]
    duplicate_users = known_users.duplicated(keep=False)
    if duplicate_users.any():
        duplicate_groups = known_users.loc[duplicate_users].nunique()
        raise ValueError(
            "user_id must identify at most one signup-linked entrant before "
            f"User Funnel construction; found {duplicate_groups} duplicate "
            "user group(s)"
        )


def build_user_base_from_frames(
    downloads: pd.DataFrame,
    signups: pd.DataFrame,
    rides: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    """Build one row per selected download through two preserving LEFT joins.

    Material download/signup cardinality failures are rejected first. Missing
    or unexpected platform and age values remain visible in the returned base.
    """
    parameters = _normalise_parameters(parameters)
    if parameters.source_cutoff is None:
        raise ValueError("source_cutoff is required")

    _validate_user_source_conditions(downloads, signups, parameters)

    observed_downloads = downloads.loc[
        _source_row_mask(downloads["download_ts"], parameters.source_cutoff)
    ].copy()
    download_cohort = observed_downloads.loc[
        _cohort_mask(observed_downloads["download_ts"], parameters)
    ].copy()

    user_ride_flags = _aggregate_user_ride_flags(rides, parameters)
    signup_details = _observed_signups(signups, parameters).loc[
        lambda frame: frame["session_id"].notna(),
        ["session_id", "user_id", "age_range"],
    ].merge(
        user_ride_flags,
        how="left",
        on="user_id",
        validate="many_to_one",
    )

    base = download_cohort.merge(
        signup_details,
        how="left",
        left_on="app_download_key",
        right_on="session_id",
        validate="one_to_one",
    )

    base["downloaded"] = True
    base["signed_up"] = base["session_id"].notna()
    base["requested"] = base["signed_up"] & (
        base["requested"].astype("boolean").fillna(False).astype(bool)
    )
    base["completed"] = base["requested"] & (
        base["completed"].astype("boolean").fillna(False).astype(bool)
    )
    base["age_group"] = base["age_range"].astype("object")
    base.loc[~base["signed_up"], "age_group"] = NO_SIGNUP_AGE

    base["download_row_count"] = 1
    base["signup_count"] = base["signed_up"].astype("int64")
    base["signup_user_count"] = (
        base["signed_up"] & base["user_id"].notna()
    ).astype("int64")
    base["download_ts_conflict"] = False
    base["download_ts_missing"] = base["download_ts"].isna()
    base["platform_conflict"] = False
    base["platform_missing"] = base["platform"].isna()
    base["platform_unexpected"] = (
        base["platform"].notna() & ~base["platform"].isin(VALID_PLATFORMS)
    )
    base["signup_user_missing"] = (
        base["signed_up"] & base["user_id"].isna()
    )
    base["signup_user_conflict"] = False
    base["age_missing"] = (
        base["signed_up"] & base["age_group"].isna()
    )
    base["age_conflict"] = False
    base["age_unexpected"] = (
        base["signed_up"]
        & base["age_group"].notna()
        & ~base["age_group"].isin(VALID_AGE_GROUPS)
    )
    _assert_unique_base(base, "app_download_key")
    columns = [
        "app_download_key", "download_ts", "platform", "age_group",
        *USER_STAGES,
        "download_row_count", "signup_count", "signup_user_count",
        "download_ts_conflict", "download_ts_missing", "platform_conflict",
        "platform_missing", "platform_unexpected", "signup_user_missing",
        "signup_user_conflict", "age_missing", "age_conflict",
        "age_unexpected",
    ]
    return base[columns].sort_values("app_download_key").reset_index(drop=True)


def _aggregate_ride_source(
    rides: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    observed = rides.loc[
        _source_row_mask(rides["request_ts"], parameters.source_cutoff)
    ].copy()
    _require_non_null_identifier(observed, "ride_id")
    observed["finished"] = _event_observed(
        observed["dropoff_ts"], parameters.source_cutoff
    )
    observed["accepted"] = _event_observed(
        observed["accept_ts"], parameters.source_cutoff
    )
    observed["cancel_after_accept"] = (
        _event_observed(observed["accept_ts"], parameters.source_cutoff)
        & _event_observed(observed["cancel_ts"], parameters.source_cutoff)
        & observed["cancel_ts"].ge(observed["accept_ts"])
    )
    observed["dropoff_without_pickup"] = (
        observed["dropoff_ts"].notna() & observed["pickup_ts"].isna()
    )
    observed["pickup_without_accept"] = (
        observed["pickup_ts"].notna() & observed["accept_ts"].isna()
    )
    observed["dropoff_without_accept"] = (
        observed["dropoff_ts"].notna() & observed["accept_ts"].isna()
    )
    observed["cancel_with_pickup"] = (
        observed["cancel_ts"].notna() & observed["pickup_ts"].notna()
    )
    observed["cancel_with_dropoff"] = (
        observed["cancel_ts"].notna() & observed["dropoff_ts"].notna()
    )
    observed["cancel_before_accept_anomaly"] = (
        observed["accept_ts"].notna()
        & observed["cancel_ts"].notna()
        & observed["cancel_ts"].lt(observed["accept_ts"])
    )
    observed["accept_before_request"] = observed["accept_ts"].lt(
        observed["request_ts"]
    )
    observed["pickup_before_accept"] = observed["pickup_ts"].lt(
        observed["accept_ts"]
    )
    observed["dropoff_before_pickup"] = observed["dropoff_ts"].lt(
        observed["pickup_ts"]
    )
    grouped = observed.groupby("ride_id", as_index=False, sort=False)
    result = grouped.agg(
        ride_row_count=("ride_id", "size"),
        user_id=("user_id", _first_non_null),
        user_id_value_count=("user_id", lambda s: s.nunique(dropna=True)),
        ride_user_missing=("user_id", lambda s: bool(s.isna().any())),
        request_ts=("request_ts", "min"),
        request_ts_value_count=("request_ts", lambda s: s.nunique(dropna=True)),
        request_ts_missing=("request_ts", lambda s: bool(s.isna().any())),
        accept_ts=("accept_ts", "min"),
        pickup_ts=("pickup_ts", "min"),
        dropoff_ts=("dropoff_ts", "min"),
        cancel_ts=("cancel_ts", "min"),
        finished=("finished", "any"),
        accepted=("accepted", "any"),
        cancel_after_accept=("cancel_after_accept", "any"),
        dropoff_without_pickup=("dropoff_without_pickup", "any"),
        pickup_without_accept=("pickup_without_accept", "any"),
        dropoff_without_accept=("dropoff_without_accept", "any"),
        cancel_with_pickup=("cancel_with_pickup", "any"),
        cancel_with_dropoff=("cancel_with_dropoff", "any"),
        cancel_before_accept_anomaly=("cancel_before_accept_anomaly", "any"),
        accept_before_request=("accept_before_request", "any"),
        pickup_before_accept=("pickup_before_accept", "any"),
        dropoff_before_pickup=("dropoff_before_pickup", "any"),
    )
    result["ride_user_conflict"] = result["user_id_value_count"].gt(1)
    result["request_ts_conflict"] = result["request_ts_value_count"].gt(1)
    unsafe_user = result["ride_user_conflict"] | result["ride_user_missing"]
    result.loc[unsafe_user, "user_id"] = pd.NA
    result["requested"] = True
    return result.drop(columns=["user_id_value_count", "request_ts_value_count"])


def _aggregate_attribution_by_user(
    signups: pd.DataFrame,
    download_by_key: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    observed = _observed_signups(signups, parameters)
    observed = observed.loc[observed["user_id"].notna()].copy()
    download_links = download_by_key[
        [
            "app_download_key", "platform", "platform_conflict",
            "platform_source_missing",
        ]
    ].rename(columns={"app_download_key": "matched_download_key"})
    rows = observed.merge(
        download_links,
        how="left",
        left_on="session_id",
        right_on="matched_download_key",
        validate="many_to_one",
    )
    if rows.empty:
        return pd.DataFrame(columns=["user_id"])
    rows["source_platform_conflict"] = rows["platform_conflict"].fillna(False)
    rows["source_platform_missing"] = rows[
        "platform_source_missing"
    ].fillna(False)
    grouped = rows.groupby("user_id", as_index=False, sort=False)
    result = grouped.agg(
        signup_count=("user_id", "size"),
        signup_session_count=("session_id", lambda s: s.nunique(dropna=True)),
        signup_session_missing=("session_id", lambda s: bool(s.isna().any())),
        download_missing=("matched_download_key", lambda s: bool(s.isna().any())),
        platform=("platform", _first_non_null),
        platform_value_count=("platform", lambda s: s.nunique(dropna=True)),
        platform_source_missing=("platform", lambda s: bool(s.isna().any())),
        source_platform_conflict=("source_platform_conflict", "any"),
        source_download_platform_missing=("source_platform_missing", "any"),
        age_range=("age_range", _first_non_null),
        age_value_count=("age_range", lambda s: s.nunique(dropna=True)),
        age_source_missing=("age_range", lambda s: bool(s.isna().any())),
    )
    result["platform_conflict"] = (
        result["platform_value_count"].gt(1)
        | result["source_platform_conflict"]
    )
    result["platform_source_missing"] = (
        result["platform_source_missing"]
        | result["source_download_platform_missing"]
    )
    unsafe_platform = (
        result["platform_value_count"].ne(1)
        | result["platform_source_missing"]
        | result["platform_conflict"]
    )
    result.loc[unsafe_platform, "platform"] = pd.NA
    result["age_conflict"] = result["age_value_count"].gt(1)
    unsafe_age = result["age_value_count"].ne(1) | result["age_source_missing"]
    result.loc[unsafe_age, "age_range"] = pd.NA
    return result.drop(
        columns=[
            "platform_value_count", "source_platform_conflict",
            "source_download_platform_missing", "age_value_count",
        ]
    )


def _aggregate_transactions(
    transactions: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    observed = transactions.loc[
        _source_row_mask(transactions["transaction_ts"], parameters.source_cutoff)
        & transactions["ride_id"].notna()
    ].copy()
    if observed.empty:
        return pd.DataFrame(
            columns=["ride_id", "tx_count", "approved_count", "has_approved"]
        )
    observed["is_approved"] = observed["charge_status"].eq("Approved")
    return observed.groupby("ride_id", as_index=False, sort=False).agg(
        tx_count=("ride_id", "size"),
        approved_count=("is_approved", "sum"),
        has_approved=("is_approved", "any"),
    )


def _aggregate_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    observed = reviews.loc[reviews["ride_id"].notna()].copy()
    if observed.empty:
        return pd.DataFrame(columns=["ride_id", "review_count", "has_review"])
    result = observed.groupby("ride_id", as_index=False, sort=False).agg(
        review_count=("ride_id", "size")
    )
    result["has_review"] = True
    return result


def build_ride_base_from_frames(
    rides: pd.DataFrame,
    signups: pd.DataFrame,
    downloads: pd.DataFrame,
    transactions: pd.DataFrame,
    reviews: pd.DataFrame,
    parameters: AnalysisParameters,
) -> pd.DataFrame:
    """Build one row per distinct ride with stage and attribution evidence."""
    parameters = _normalise_parameters(parameters)
    if parameters.source_cutoff is None:
        raise ValueError("source_cutoff is required")
    ride_source = _aggregate_ride_source(rides, parameters)
    ride_source = ride_source.loc[
        _cohort_mask(ride_source["request_ts"], parameters)
    ].copy()
    attribution = _aggregate_attribution_by_user(
        signups,
        _aggregate_downloads(downloads, parameters),
        parameters,
    )
    base = ride_source.merge(
        attribution,
        how="left",
        on="user_id",
        validate="many_to_one",
    ).merge(
        _aggregate_transactions(transactions, parameters),
        how="left",
        on="ride_id",
        validate="one_to_one",
    ).merge(
        _aggregate_reviews(reviews),
        how="left",
        on="ride_id",
        validate="one_to_one",
    )

    has_signup = base["signup_count"].notna()
    for column in (
        "signup_count", "signup_session_count", "tx_count", "approved_count",
        "review_count",
    ):
        base[column] = base[column].astype("Int64").fillna(0).astype("int64")
    for column in (
        "signup_session_missing", "download_missing", "platform_conflict",
        "platform_source_missing", "age_source_missing", "age_conflict",
        "has_approved", "has_review",
    ):
        base[column] = base[column].astype("boolean").fillna(False).astype(bool)

    base["age_group"] = base["age_range"].astype("object")
    no_signup = ~has_signup & ~base["ride_user_conflict"]
    base.loc[no_signup, "age_group"] = NO_SIGNUP_AGE
    base["paid"] = base["finished"] & base["has_approved"]
    base["reviewed"] = base["paid"] & base["has_review"]
    base["signup_missing"] = no_signup
    base["download_missing"] = base["download_missing"] | ~has_signup
    base["platform_missing"] = (
        base["platform"].isna() | base["platform_source_missing"]
    )
    base["platform_unexpected"] = (
        base["platform"].notna() & ~base["platform"].isin(VALID_PLATFORMS)
    )
    base["age_missing"] = has_signup & (
        base["age_source_missing"] | base["age_group"].isna()
    )
    base["age_unexpected"] = (
        has_signup
        & base["age_group"].notna()
        & ~base["age_group"].isin(VALID_AGE_GROUPS)
    )
    _assert_unique_base(base, "ride_id")
    columns = [
        "ride_id", "user_id", "request_ts", "accept_ts", "pickup_ts",
        "dropoff_ts", "cancel_ts", "platform", "age_group", *RIDE_STAGES,
        "accepted", "cancel_after_accept", "has_approved", "has_review",
        "ride_row_count", "signup_count", "signup_session_count", "tx_count",
        "approved_count", "review_count", "ride_user_conflict",
        "ride_user_missing", "request_ts_conflict", "request_ts_missing",
        "signup_missing", "signup_session_missing", "download_missing",
        "platform_conflict", "platform_missing", "platform_unexpected",
        "age_missing", "age_conflict", "age_unexpected",
        "dropoff_without_pickup", "pickup_without_accept",
        "dropoff_without_accept", "cancel_with_pickup", "cancel_with_dropoff",
        "cancel_before_accept_anomaly", "accept_before_request",
        "pickup_before_accept", "dropoff_before_pickup",
    ]
    return base[columns].sort_values("ride_id").reset_index(drop=True)


def build_user_base(
    engine: Engine,
    parameters: AnalysisParameters | None = None,
) -> pd.DataFrame:
    resolved = resolve_parameters(engine, parameters)
    sources = load_source_frames(engine)
    return build_user_base_from_frames(
        sources["downloads"], sources["signups"], sources["rides"], resolved
    )


def build_ride_base(
    engine: Engine,
    parameters: AnalysisParameters | None = None,
) -> pd.DataFrame:
    resolved = resolve_parameters(engine, parameters)
    sources = load_source_frames(engine)
    return build_ride_base_from_frames(
        sources["rides"], sources["signups"], sources["downloads"],
        sources["transactions"], sources["reviews"], resolved,
    )


def stage_counts(base: pd.DataFrame, stages: list[str]) -> dict[str, int]:
    """Return exact integer stage counts at the base table's grain."""
    return {stage: int(base[stage].sum()) for stage in stages}


def adjacent_rates(counts: dict[str, int], stages: list[str]) -> pd.DataFrame:
    """Return full-precision adjacent conversion and drop-off calculations."""
    rows = []
    for index, stage in enumerate(stages):
        count = counts[stage]
        if index == 0:
            rows.append(
                {
                    "stage": stage, "count": count, "previous_count": None,
                    "conversion_rate_pct": None, "dropoff_count": None,
                    "dropoff_rate_pct": None,
                }
            )
            continue
        previous = counts[stages[index - 1]]
        dropoff = previous - count
        rows.append(
            {
                "stage": stage,
                "count": count,
                "previous_count": previous,
                "conversion_rate_pct": (
                    None if previous == 0 else 100.0 * count / previous
                ),
                "dropoff_count": dropoff,
                "dropoff_rate_pct": (
                    None if previous == 0 else 100.0 * dropoff / previous
                ),
            }
        )
    return pd.DataFrame(rows)


def segment_counts(
    base: pd.DataFrame,
    segment: str,
    stages: list[str],
) -> pd.DataFrame:
    """Return exact stage counts for every explicit segment, including null."""
    return (
        base.groupby(segment, dropna=False, sort=True)[stages]
        .sum()
        .astype("int64")
        .reset_index()
    )


def validate_monotonic(counts: dict[str, int], stages: list[str]) -> list[str]:
    violations = []
    for index in range(1, len(stages)):
        previous, current = stages[index - 1], stages[index]
        if counts[current] > counts[previous]:
            violations.append(
                f"{current} ({counts[current]}) exceeds "
                f"{previous} ({counts[previous]})"
            )
    return violations


def validate_subset(base: pd.DataFrame, stages: list[str]) -> list[str]:
    violations = []
    for index in range(1, len(stages)):
        earlier, later = stages[index - 1], stages[index]
        invalid = base[later] & ~base[earlier]
        if invalid.any():
            violations.append(
                f"{int(invalid.sum())} records in {later} but not {earlier}"
            )
    return violations


def validate_segment_reconciliation(
    base: pd.DataFrame,
    stages: list[str],
    segments: tuple[str, ...] = ("platform", "age_group"),
) -> list[str]:
    errors = []
    overall = stage_counts(base, stages)
    for segment in segments:
        segmented = segment_counts(base, segment, stages)
        for stage in stages:
            if int(segmented[stage].sum()) != overall[stage]:
                errors.append(f"{segment}.{stage} does not reconcile to overall")
    return errors


def ride_integrity_checks(base: pd.DataFrame) -> dict[str, int]:
    keys = (
        "dropoff_without_pickup", "pickup_without_accept",
        "dropoff_without_accept", "cancel_with_pickup", "cancel_with_dropoff",
        "cancel_before_accept_anomaly", "accept_before_request",
        "pickup_before_accept", "dropoff_before_pickup",
    )
    result = {key: int(base[key].sum()) for key in keys}
    result["approved_without_finished"] = int(
        (base["has_approved"] & ~base["finished"]).sum()
    )
    result["review_without_paid"] = int(
        (base["has_review"] & ~base["paid"]).sum()
    )
    return result


def base_validation_totals(
    user_base: pd.DataFrame,
    ride_base: pd.DataFrame,
) -> dict[str, int]:
    result = {
        "user_base_rows": len(user_base),
        "user_base_distinct_ids": user_base["app_download_key"].nunique(),
        "ride_base_rows": len(ride_base),
        "ride_base_distinct_ids": ride_base["ride_id"].nunique(),
        "downloads_without_signup": int((~user_base["signed_up"]).sum()),
        "user_platform_missing": int(user_base["platform_missing"].sum()),
        "user_platform_unexpected": int(user_base["platform_unexpected"].sum()),
        "user_platform_conflict": int(user_base["platform_conflict"].sum()),
        "user_age_missing": int(user_base["age_missing"].sum()),
        "user_age_unexpected": int(user_base["age_unexpected"].sum()),
        "user_age_conflict": int(user_base["age_conflict"].sum()),
        "ride_signup_missing": int(ride_base["signup_missing"].sum()),
        "ride_download_missing": int(ride_base["download_missing"].sum()),
        "ride_platform_missing": int(ride_base["platform_missing"].sum()),
        "ride_platform_unexpected": int(ride_base["platform_unexpected"].sum()),
        "ride_platform_conflict": int(ride_base["platform_conflict"].sum()),
        "ride_age_missing": int(ride_base["age_missing"].sum()),
        "ride_age_unexpected": int(ride_base["age_unexpected"].sum()),
        "ride_age_conflict": int(ride_base["age_conflict"].sum()),
    }
    result.update(ride_integrity_checks(ride_base))
    return {key: int(value) for key, value in result.items()}


def source_validation_totals(
    sources: Mapping[str, pd.DataFrame],
    parameters: AnalysisParameters,
) -> dict[str, int]:
    downloads = sources["downloads"].loc[
        _source_row_mask(
            sources["downloads"]["download_ts"], parameters.source_cutoff
        )
    ]
    signups = _observed_signups(sources["signups"], parameters)
    rides = sources["rides"].loc[
        _source_row_mask(sources["rides"]["request_ts"], parameters.source_cutoff)
    ]
    transactions = sources["transactions"].loc[
        _source_row_mask(
            sources["transactions"]["transaction_ts"], parameters.source_cutoff
        )
    ]
    reviews = sources["reviews"]

    def duplicate_groups(frame: pd.DataFrame, key: str) -> int:
        return int((frame.groupby(key, dropna=False).size() > 1).sum())

    session_rows = signups.loc[signups["session_id"].notna()]
    user_rows = signups.loc[signups["user_id"].notna()]
    return {
        "duplicate_app_download_keys": duplicate_groups(
            downloads, "app_download_key"
        ),
        "duplicate_ride_ids": duplicate_groups(rides, "ride_id"),
        "signup_sessions_with_multiple_rows": duplicate_groups(
            session_rows, "session_id"
        ),
        "signup_sessions_with_multiple_users": int(
            (
                session_rows.groupby("session_id")["user_id"]
                .nunique(dropna=True)
                .gt(1)
            ).sum()
        ),
        "signup_users_with_multiple_rows": duplicate_groups(user_rows, "user_id"),
        "rides_with_multiple_transactions": duplicate_groups(
            transactions, "ride_id"
        ),
        "rides_with_multiple_approved": duplicate_groups(
            transactions.loc[transactions["charge_status"].eq("Approved")],
            "ride_id",
        ),
        "rides_with_multiple_reviews": duplicate_groups(reviews, "ride_id"),
        "unmatched_signup_rows": int(
            (~signups["session_id"].isin(downloads["app_download_key"])).sum()
        ),
        "unmatched_ride_rows": int(
            (~rides["user_id"].isin(signups["user_id"].dropna())).sum()
        ),
        "unmatched_transaction_rows": int(
            (~transactions["ride_id"].isin(rides["ride_id"])).sum()
        ),
        "unmatched_review_rows": int(
            (~reviews["ride_id"].isin(rides["ride_id"])).sum()
        ),
    }


def run_funnel_analysis(
    engine: Engine,
    parameters: AnalysisParameters | None = None,
    sources: Mapping[str, pd.DataFrame] | None = None,
) -> dict:
    """Build both bases, governed outputs, and complete validation evidence."""
    resolved = resolve_parameters(engine, parameters)
    source_frames = dict(sources) if sources is not None else load_source_frames(engine)
    user_base = build_user_base_from_frames(
        source_frames["downloads"], source_frames["signups"],
        source_frames["rides"], resolved,
    )
    ride_base = build_ride_base_from_frames(
        source_frames["rides"], source_frames["signups"],
        source_frames["downloads"], source_frames["transactions"],
        source_frames["reviews"], resolved,
    )
    user_counts = stage_counts(user_base, USER_STAGES)
    ride_counts = stage_counts(ride_base, RIDE_STAGES)
    validation = base_validation_totals(user_base, ride_base)
    validation.update(source_validation_totals(source_frames, resolved))
    return {
        "parameters": resolved,
        "user_base": user_base,
        "ride_base": ride_base,
        "user_counts": user_counts,
        "ride_counts": ride_counts,
        "user_rates": adjacent_rates(user_counts, USER_STAGES),
        "ride_rates": adjacent_rates(ride_counts, RIDE_STAGES),
        "user_platform_counts": segment_counts(user_base, "platform", USER_STAGES),
        "user_age_counts": segment_counts(user_base, "age_group", USER_STAGES),
        "ride_platform_counts": segment_counts(ride_base, "platform", RIDE_STAGES),
        "ride_age_counts": segment_counts(ride_base, "age_group", RIDE_STAGES),
        "user_monotonic_violations": validate_monotonic(user_counts, USER_STAGES),
        "ride_monotonic_violations": validate_monotonic(ride_counts, RIDE_STAGES),
        "user_subset_violations": validate_subset(user_base, USER_STAGES),
        "ride_subset_violations": validate_subset(ride_base, RIDE_STAGES),
        "segment_reconciliation_errors": (
            validate_segment_reconciliation(user_base, USER_STAGES)
            + validate_segment_reconciliation(ride_base, RIDE_STAGES)
        ),
        "ride_integrity": ride_integrity_checks(ride_base),
        "validation_totals": validation,
        "ride_diagnostics": {
            "accepted": int(ride_base["accepted"].sum()),
            "cancel_after_accept": int(ride_base["cancel_after_accept"].sum()),
        },
    }
