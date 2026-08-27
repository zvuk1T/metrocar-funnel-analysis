"""Contract-focused tests for the Phase 2 SQL/Pandas analytical core."""

import os

import pandas as pd
import pytest
from dotenv import load_dotenv

from analysis import db, funnel, reconcile

load_dotenv()

requires_db = pytest.mark.skipif(
    not os.environ.get(db.ENV_VAR, "").strip(),
    reason=f"{db.ENV_VAR} is not set; skipping database-dependent test",
)

CUTOFF = pd.Timestamp("2021-01-10 00:00:00")
PARAMETERS = funnel.AnalysisParameters(source_cutoff=CUTOFF)


def _timestamps(values):
    return pd.to_datetime(values)


def _sources() -> dict[str, pd.DataFrame]:
    """Small snapshot with safe duplicates, missing attribution, and anomalies."""
    return {
        "downloads": pd.DataFrame(
            {
                "app_download_key": ["d1", "d1", "d2", "d3", "d4"],
                "platform": ["ios", "ios", "web", "android", None],
                "download_ts": _timestamps(
                    [
                        "2021-01-01 09:00", "2021-01-01 09:00",
                        "2021-01-02 09:00", "2021-01-03 09:00",
                        "2021-01-04 09:00",
                    ]
                ),
            }
        ),
        "signups": pd.DataFrame(
            {
                "user_id": [1, 1, 2, 3],
                "session_id": ["d1", "d1", "d2", "d3"],
                "signup_ts": _timestamps(
                    [
                        "2021-01-01 10:00", "2021-01-01 10:00",
                        "2021-01-02 10:00", "2021-01-03 10:00",
                    ]
                ),
                "age_range": ["25-34", "25-34", "Unknown", None],
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


# --- grain, multiplicity, stage membership, and attribution -----------------


def test_duplicate_sources_do_not_multiply_base_grains():
    result = _analysis()
    user_base, ride_base = result["user_base"], result["ride_base"]
    assert user_base["app_download_key"].is_unique
    assert ride_base["ride_id"].is_unique
    assert len(user_base) == 4
    assert len(ride_base) == 4
    d1 = user_base.set_index("app_download_key").loc["d1"]
    assert d1["download_row_count"] == 2
    assert d1["signup_count"] == 2


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
    rides = _analysis(sources)["ride_base"].set_index("ride_id")
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
    assert validation["duplicate_app_download_keys"] == 1
    assert validation["signup_sessions_with_multiple_rows"] == 1
    assert validation["signup_users_with_multiple_rows"] == 1
    assert validation["rides_with_multiple_transactions"] == 1
    assert validation["rides_with_multiple_approved"] == 1
    assert validation["rides_with_multiple_reviews"] == 1
    assert validation["unmatched_ride_rows"] == 1
    assert validation["review_without_paid"] == 1


# --- canonical SQL and reconciliation helpers ------------------------------


def test_canonical_sql_contains_all_named_queries_and_no_correlated_exists():
    queries = reconcile.load_canonical_queries()
    assert reconcile.REQUIRED_QUERIES <= queries.keys()
    assert "EXISTS" not in queries["user_base"].upper()
    assert "EXISTS" not in queries["ride_base"].upper()


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
    load_dotenv()
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
