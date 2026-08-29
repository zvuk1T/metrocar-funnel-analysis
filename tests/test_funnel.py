"""Contract-focused tests for the Phase 2 SQL/Pandas analytical core."""

import os

import pandas as pd
import pytest

from analysis import db, funnel, reconcile

requires_db = pytest.mark.skipif(
    not os.environ.get(db.ENV_VAR, "").strip(),
    reason=f"{db.ENV_VAR} is not set; skipping database-dependent test",
)

CUTOFF = pd.Timestamp("2021-01-10 00:00:00")
PARAMETERS = funnel.AnalysisParameters(source_cutoff=CUTOFF)


def _timestamps(values):
    return pd.to_datetime(values)


def _sources() -> dict[str, pd.DataFrame]:
    """Structurally valid User Funnel sources plus Ride Funnel anomalies."""
    return {
        "downloads": pd.DataFrame(
            {
                "app_download_key": ["d1", "d2", "d3", "d4"],
                "platform": ["ios", "web", "android", None],
                "download_ts": _timestamps(
                    [
                        "2021-01-01 09:00", "2021-01-02 09:00",
                        "2021-01-03 09:00", "2021-01-04 09:00",
                    ]
                ),
            }
        ),
        "signups": pd.DataFrame(
            {
                "user_id": [1, 2, 3],
                "session_id": ["d1", "d2", "d3"],
                "signup_ts": _timestamps(
                    [
                        "2021-01-01 10:00", "2021-01-02 10:00",
                        "2021-01-03 10:00",
                    ]
                ),
                "age_range": ["25-34", "Unknown", None],
            }
        ),
        "rides": pd.DataFrame(
            {
                "ride_id": [10, 11, 12, 13],
                "user_id": [1, 2, 3, 99],
                "request_ts": _timestamps(
                    [
                        "2021-01-01 12:00", "2021-01-02 12:00",
                        "2021-01-03 12:00", "2021-01-04 12:00",
                    ]
                ),
                "accept_ts": _timestamps(
                    ["2021-01-01 12:10", None, "2021-01-03 12:10", None]
                ),
                "pickup_ts": _timestamps(
                    ["2021-01-01 12:20", None, "2021-01-03 12:20", None]
                ),
                "dropoff_ts": _timestamps(
                    ["2021-01-02 13:00", None, "2021-01-03 13:00", None]
                ),
                "cancel_ts": _timestamps([None, "2021-01-02 12:20", None, None]),
            }
        ),
        "transactions": pd.DataFrame(
            {
                "ride_id": [10, 10, 12],
                "charge_status": ["Approved", "Approved", "Decline"],
                "transaction_ts": _timestamps(
                    ["2021-01-02 13:00", "2021-01-02 13:01", "2021-01-03 13:00"]
                ),
            }
        ),
        "reviews": pd.DataFrame({"ride_id": [10, 10, 12]}),
    }


def _analysis(
    sources: dict[str, pd.DataFrame] | None = None,
    parameters: funnel.AnalysisParameters = PARAMETERS,
) -> dict:
    return funnel.run_funnel_analysis(None, parameters, sources or _sources())


# --- parameters, formulas, and subset rules --------------------------------


def test_calendar_parameters_use_half_open_end_date():
    parameters = funnel.calendar_parameters(
        "2021-01-01", "2021-01-01", source_cutoff=CUTOFF
    )
    assert parameters.cohort_start == pd.Timestamp("2021-01-01")
    assert parameters.cohort_end_exclusive == pd.Timestamp("2021-01-02")


def test_half_open_cohort_filters_entry_only():
    parameters = funnel.calendar_parameters(
        "2021-01-01", "2021-01-01", source_cutoff=CUTOFF
    )
    result = _analysis(parameters=parameters)
    assert result["user_counts"] == {
        "downloaded": 1, "signed_up": 1, "requested": 1, "completed": 1,
    }
    assert result["ride_counts"] == {
        "requested": 1, "finished": 1, "paid": 1, "reviewed": 1,
    }


def test_source_cutoff_excludes_later_outcomes():
    parameters = funnel.AnalysisParameters(
        cohort_start=pd.Timestamp("2021-01-01"),
        cohort_end_exclusive=pd.Timestamp("2021-01-02"),
        source_cutoff=pd.Timestamp("2021-01-01 15:00"),
    )
    result = _analysis(parameters=parameters)
    assert result["user_counts"] == {
        "downloaded": 1, "signed_up": 1, "requested": 1, "completed": 0,
    }
    assert result["ride_counts"] == {
        "requested": 1, "finished": 0, "paid": 0, "reviewed": 0,
    }
    assert result["parameters"].source_cutoff == parameters.source_cutoff


def test_null_request_timestamp_does_not_become_a_membership_filter():
    sources = _sources()
    sources["rides"].loc[sources["rides"]["ride_id"].eq(11), "request_ts"] = pd.NaT
    user = _analysis(sources)["user_base"].set_index("app_download_key").loc["d2"]
    assert bool(user["requested"]) is True
    assert bool(user["completed"]) is False


def test_adjacent_rates_formulas_and_no_rounded_subtraction():
    rates = funnel.adjacent_rates({"a": 3, "b": 1}, ["a", "b"])
    assert rates.loc[1, "conversion_rate_pct"] == pytest.approx(100.0 / 3)
    assert rates.loc[1, "dropoff_count"] == 2
    assert rates.loc[1, "dropoff_rate_pct"] == pytest.approx(200.0 / 3)


def test_adjacent_rates_zero_denominator_returns_na():
    rates = funnel.adjacent_rates({"a": 0, "b": 0}, ["a", "b"])
    assert pd.isna(rates.loc[1, "conversion_rate_pct"])
    assert pd.isna(rates.loc[1, "dropoff_rate_pct"])
    assert rates.loc[1, "dropoff_count"] == 0


def test_subset_and_monotonicity_detect_invalid_chain():
    base = pd.DataFrame(
        {"requested": [True], "finished": [False], "paid": [True]}
    )
    assert funnel.validate_subset(base, ["requested", "finished", "paid"])
    assert funnel.validate_monotonic(
        {"requested": 1, "finished": 0, "paid": 1},
        ["requested", "finished", "paid"],
    )


# --- grain, source validity, stage membership, and attribution --------------


def test_valid_sources_preserve_base_grains():
    result = _analysis()
    user_base, ride_base = result["user_base"], result["ride_base"]
    assert user_base["app_download_key"].is_unique
    assert ride_base["ride_id"].is_unique
    assert len(user_base) == 4
    assert len(ride_base) == 4
    d1 = user_base.set_index("app_download_key").loc["d1"]
    assert d1["download_row_count"] == 1
    assert d1["signup_count"] == 1


def test_user_funnel_outward_interfaces_remain_compatible():
    result = _analysis()
    assert list(result["user_base"].columns) == [
        "app_download_key", "download_ts", "platform", "age_group",
        "downloaded", "signed_up", "requested", "completed",
        "download_row_count", "signup_count", "signup_user_count",
        "download_ts_conflict", "download_ts_missing", "platform_conflict",
        "platform_missing", "platform_unexpected", "signup_user_missing",
        "signup_user_conflict", "age_missing", "age_conflict",
        "age_unexpected",
    ]
    assert set(result) == {
        "parameters", "user_base", "ride_base", "user_counts", "ride_counts",
        "user_rates", "ride_rates", "user_platform_counts", "user_age_counts",
        "ride_platform_counts", "ride_age_counts",
        "user_monotonic_violations", "ride_monotonic_violations",
        "user_subset_violations", "ride_subset_violations",
        "segment_reconciliation_errors", "ride_integrity",
        "validation_totals", "ride_diagnostics",
    }
    assert set(result["validation_totals"]) == {
        "user_base_rows", "user_base_distinct_ids", "ride_base_rows",
        "ride_base_distinct_ids", "downloads_without_signup",
        "user_platform_missing", "user_platform_unexpected",
        "user_platform_conflict", "user_age_missing", "user_age_unexpected",
        "user_age_conflict", "ride_signup_missing", "ride_download_missing",
        "ride_platform_missing", "ride_platform_unexpected",
        "ride_platform_conflict", "ride_age_missing", "ride_age_unexpected",
        "ride_age_conflict", "dropoff_without_pickup",
        "pickup_without_accept", "dropoff_without_accept",
        "cancel_with_pickup", "cancel_with_dropoff",
        "cancel_before_accept_anomaly", "accept_before_request",
        "pickup_before_accept", "dropoff_before_pickup",
        "approved_without_finished", "review_without_paid",
        "duplicate_app_download_keys", "duplicate_ride_ids",
        "signup_sessions_with_multiple_rows",
        "signup_sessions_with_multiple_users", "signup_users_with_multiple_rows",
        "rides_with_multiple_transactions", "rides_with_multiple_approved",
        "rides_with_multiple_reviews", "unmatched_signup_rows",
        "unmatched_ride_rows", "unmatched_transaction_rows",
        "unmatched_review_rows",
    }


def test_duplicate_download_keys_fail_before_user_base_construction():
    sources = _sources()
    sources["downloads"] = pd.concat(
        [sources["downloads"], sources["downloads"].iloc[[0]]],
        ignore_index=True,
    )
    with pytest.raises(ValueError, match="app_download_key must be unique"):
        _analysis(sources)


def test_duplicate_signup_sessions_fail_before_user_base_construction():
    sources = _sources()
    sources["signups"] = pd.concat(
        [sources["signups"], sources["signups"].iloc[[0]]],
        ignore_index=True,
    )
    with pytest.raises(ValueError, match="session_id must identify at most one"):
        _analysis(sources)


def test_duplicate_signup_users_fail_before_user_base_construction():
    sources = _sources()
    sources["downloads"] = pd.concat(
        [
            sources["downloads"],
            pd.DataFrame(
                {
                    "app_download_key": ["d5"],
                    "platform": ["ios"],
                    "download_ts": _timestamps(["2021-01-05 09:00"]),
                }
            ),
        ],
        ignore_index=True,
    )
    sources["signups"] = pd.concat(
        [
            sources["signups"],
            pd.DataFrame(
                {
                    "user_id": [1],
                    "session_id": ["d5"],
                    "signup_ts": _timestamps(["2021-01-05 10:00"]),
                    "age_range": ["25-34"],
                }
            ),
        ],
        ignore_index=True,
    )
    with pytest.raises(ValueError, match="user_id must identify at most one"):
        _analysis(sources)


def test_transaction_and_review_multiplicity_are_boolean_for_stages():
    ride = _analysis()["ride_base"].set_index("ride_id").loc[10]
    assert ride["tx_count"] == 2
    assert ride["approved_count"] == 2
    assert ride["review_count"] == 2
    assert bool(ride["paid"]) is True
    assert bool(ride["reviewed"]) is True


def test_paid_and_reviewed_require_the_contract_predecessors():
    rides = _analysis()["ride_base"].set_index("ride_id")
    assert bool(rides.loc[12, "finished"]) is True
    assert bool(rides.loc[12, "paid"]) is False
    assert bool(rides.loc[12, "has_review"]) is True
    assert bool(rides.loc[12, "reviewed"]) is False


def test_user_and_ride_platform_attribution_follow_contract_paths():
    result = _analysis()
    users = result["user_base"].set_index("app_download_key")
    rides = result["ride_base"].set_index("ride_id")
    assert users.loc["d1", "platform"] == "ios"
    assert rides.loc[10, "platform"] == "ios"
    assert rides.loc[11, "platform"] == "web"
    assert pd.isna(rides.loc[13, "platform"])
    assert bool(rides.loc[13, "platform_missing"]) is True
    assert pd.isna(users.loc["d4", "platform"])
    assert bool(users.loc["d4", "platform_missing"]) is True


def test_unexpected_user_platform_remains_visible_and_flagged():
    sources = _sources()
    sources["downloads"].loc[
        sources["downloads"]["app_download_key"].eq("d2"), "platform"
    ] = "mystery"
    user = _analysis(sources)["user_base"].set_index("app_download_key").loc["d2"]
    assert user["platform"] == "mystery"
    assert bool(user["platform_unexpected"]) is True


def test_age_categories_preserve_unknown_null_and_no_signup():
    result = _analysis()
    users = result["user_base"].set_index("app_download_key")
    rides = result["ride_base"].set_index("ride_id")
    assert users.loc["d2", "age_group"] == "Unknown"
    assert pd.isna(users.loc["d3", "age_group"])
    assert bool(users.loc["d3", "age_missing"]) is True
    assert users.loc["d4", "age_group"] == funnel.NO_SIGNUP_AGE
    assert rides.loc[13, "age_group"] == funnel.NO_SIGNUP_AGE


def test_unexpected_age_remains_visible_and_flagged():
    sources = _sources()
    sources["signups"].loc[sources["signups"]["user_id"].eq(2), "age_range"] = "mystery"
    user = _analysis(sources)["user_base"].set_index("app_download_key").loc["d2"]
    assert user["age_group"] == "mystery"
    assert bool(user["age_unexpected"]) is True


def test_conflicting_ride_attribution_is_explicit_without_fanout():
    sources = _sources()
    sources["downloads"] = pd.concat(
        [
            sources["downloads"],
            pd.DataFrame(
                {
                    "app_download_key": ["d5"],
                    "platform": ["android"],
                    "download_ts": _timestamps(["2021-01-01 08:00"]),
                }
            ),
        ],
        ignore_index=True,
    )
    sources["signups"] = pd.concat(
        [
            sources["signups"],
            pd.DataFrame(
                {
                    "user_id": [1], "session_id": ["d5"],
                    "signup_ts": _timestamps(["2021-01-01 08:30"]),
                    "age_range": ["25-34"],
                }
            ),
        ],
        ignore_index=True,
    )
    rides = funnel.build_ride_base_from_frames(
        sources["rides"],
        sources["signups"],
        sources["downloads"],
        sources["transactions"],
        sources["reviews"],
        PARAMETERS,
    ).set_index("ride_id")
    assert len(rides) == 4
    assert pd.isna(rides.loc[10, "platform"])
    assert bool(rides.loc[10, "platform_conflict"]) is True


def test_segmented_outputs_include_missing_categories_and_reconcile():
    result = _analysis()
    assert result["segment_reconciliation_errors"] == []
    assert result["user_platform_counts"]["downloaded"].sum() == 4
    assert result["ride_age_counts"]["requested"].sum() == 4


def test_source_validation_reports_multiplicity_and_unmatched_paths():
    validation = _analysis()["validation_totals"]
    assert validation["duplicate_app_download_keys"] == 0
    assert validation["signup_sessions_with_multiple_rows"] == 0
    assert validation["signup_users_with_multiple_rows"] == 0
    assert validation["rides_with_multiple_transactions"] == 1
    assert validation["rides_with_multiple_approved"] == 1
    assert validation["rides_with_multiple_reviews"] == 1
    assert validation["unmatched_ride_rows"] == 1
    assert validation["review_without_paid"] == 1


# --- canonical SQL and reconciliation helpers ------------------------------


def test_canonical_sql_contains_all_named_queries():
    queries = reconcile.load_canonical_queries()
    assert reconcile.REQUIRED_QUERIES <= queries.keys()


def test_compare_bases_detects_membership_mismatch():
    sql = pd.DataFrame({"id": [1], "stage": [True], "category": ["x"]})
    pandas = pd.DataFrame({"id": [1], "stage": [False], "category": ["x"]})
    comparison = reconcile.compare_bases(
        sql, pandas, "id", ["stage", "category"]
    )
    assert comparison["identifiers_match"] is True
    assert comparison["column_mismatches"]["stage"] == 1
    assert comparison["all_match"] is False


def test_compare_rates_uses_tolerance_only_for_float_representation():
    left = funnel.adjacent_rates({"a": 3, "b": 1}, ["a", "b"])
    right = left.copy()
    right.loc[1, "conversion_rate_pct"] += 1e-13
    assert reconcile.compare_rates(left, right)["match"] is True
    right.loc[1, "conversion_rate_pct"] += 0.1
    assert reconcile.compare_rates(left, right)["match"] is False


def test_reconciliation_reports_material_failure(monkeypatch):
    pandas_result = _analysis()
    sql_result = {
        "source_cutoff": CUTOFF,
        "user_base": pandas_result["user_base"].copy(),
        "ride_base": pandas_result["ride_base"].copy(),
        "user_counts": dict(pandas_result["user_counts"]),
        "ride_counts": dict(pandas_result["ride_counts"]),
        "user_rates": pandas_result["user_rates"].copy(),
        "ride_rates": pandas_result["ride_rates"].copy(),
        "validation_totals": dict(pandas_result["validation_totals"]),
        "ride_diagnostics": dict(pandas_result["ride_diagnostics"]),
    }
    sql_result["ride_counts"]["paid"] += 1
    monkeypatch.setattr(funnel, "resolve_parameters", lambda engine, parameters: PARAMETERS)
    monkeypatch.setattr(funnel, "run_funnel_analysis", lambda engine, parameters: pandas_result)
    monkeypatch.setattr(reconcile, "run_canonical_sql", lambda engine, parameters: sql_result)
    result = reconcile.reconcile(None, PARAMETERS)
    assert result["ride_funnel"]["paid"]["match"] is False
    assert result["all_match"] is False


# --- live Phase 2 acceptance checks ----------------------------------------


@pytest.fixture(scope="module")
def engine():
    if not os.environ.get(db.ENV_VAR, "").strip():
        pytest.skip(f"{db.ENV_VAR} is not set")
    created = db.get_engine()
    db.check_connection(created)
    yield created
    created.dispose()


@pytest.fixture(scope="module")
def live_reconciliation(engine):
    """Run both live implementations once; the checks inspect shared evidence."""
    return reconcile.reconcile(engine)


@requires_db
def test_live_canonical_sql_executes_at_both_grains(live_reconciliation):
    result = live_reconciliation["sql"]
    assert result["user_base"]["app_download_key"].is_unique
    assert result["ride_base"]["ride_id"].is_unique
    assert len(result["user_base"]) > 0
    assert len(result["ride_base"]) > 0


@requires_db
def test_live_pandas_contract_validations(live_reconciliation):
    analysis = live_reconciliation["analysis"]
    assert analysis["user_monotonic_violations"] == []
    assert analysis["ride_monotonic_violations"] == []
    assert analysis["user_subset_violations"] == []
    assert analysis["ride_subset_violations"] == []
    assert analysis["segment_reconciliation_errors"] == []
    assert analysis["validation_totals"]["user_base_rows"] == analysis[
        "validation_totals"
    ]["user_base_distinct_ids"]
    assert analysis["validation_totals"]["ride_base_rows"] == analysis[
        "validation_totals"
    ]["ride_base_distinct_ids"]


@requires_db
def test_live_sql_pandas_reconcile(live_reconciliation):
    result = live_reconciliation
    assert result["user_base"]["identifiers_match"]
    assert result["ride_base"]["identifiers_match"]
    assert result["platform_segments"]["user"]["match"]
    assert result["platform_segments"]["ride"]["match"]
    assert result["age_segments"]["user"]["match"]
    assert result["age_segments"]["ride"]["match"]
    assert all(item["match"] for item in result["validation_totals"].values())
    assert result["all_match"]
