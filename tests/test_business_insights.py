"""Focused tests for canonical Phase 3 business evidence."""

import os

import pandas as pd
import pytest
from dotenv import load_dotenv

from analysis import business_insights, db, funnel

load_dotenv()

requires_db = pytest.mark.skipif(
    not os.environ.get(db.ENV_VAR, "").strip(),
    reason=f"{db.ENV_VAR} is not set; skipping database-dependent test",
)

CUTOFF = pd.Timestamp("2021-01-10 00:00:00")


def _timestamps(values):
    return pd.to_datetime(values, format="mixed")


def _ride_base() -> pd.DataFrame:
    """Ride-grain fixture with three distinct first-ride ambiguities."""
    return pd.DataFrame(
        {
            "ride_id": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "user_id": [1, 1, 2, 3, 4, 4, 5, 6, 7],
            "request_ts": _timestamps(
                [
                    "2021-01-01 08:00", "2021-01-02 08:00",
                    "2021-01-01 09:00", None,
                    "2021-01-01 10:00", "2021-01-01 10:00",
                    "2021-01-01 11:00", "2021-01-01 12:00",
                    "2021-01-01 13:00",
                ]
            ),
            "request_ts_missing": [
                False, False, False, True, False, False, False, False, False
            ],
            "request_ts_conflict": [
                False, False, False, False, False, False, False, True, False
            ],
            "signup_count": [1] * 9,
            "requested": [True] * 9,
            "accepted": [False, True, True, False, False, True, True, False, True],
            "pickup_ts": _timestamps(
                [
                    None, "2021-01-02 08:05", "2021-01-01 09:05", None,
                    None, "2021-01-01 10:05", None, None,
                    "2021-01-11 13:05",
                ]
            ),
            "finished": [False, True, True, False, False, True, False, False, False],
            "cancel_ts": _timestamps(
                [
                    "2021-01-01 08:05", None, None, None, None, None,
                    "2021-01-01 11:10", None, None,
                ]
            ),
            "cancel_after_accept": [
                False, False, False, False, False, False, True, False, False
            ],
            "paid": [False, True, True, False, False, True, False, False, False],
            "reviewed": [False, True, True, False, False, True, False, False, False],
            "has_review": [False, True, True, False, False, True, False, False, False],
            "tx_count": [0, 1, 1, 0, 0, 1, 0, 0, 0],
            "has_approved": [False, True, True, False, False, True, False, False, False],
            "platform": [
                "ios", "ios", "android", "web", "ios", "ios", "web",
                "android", "ios",
            ],
            "age_group": [
                "25-34", "25-34", "18-24", "Unknown", "35-44", "35-44",
                "45-54", "Unknown", "18-24",
            ],
        }
    )


def _user_base() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "app_download_key": ["d1", "d2", "d3", "d4"],
            "platform": ["ios", "android", "web", None],
            "age_group": [
                "18-24", "25-34", "Unknown", funnel.NO_SIGNUP_AGE
            ],
            "downloaded": [True, True, True, True],
            "signed_up": [True, True, True, False],
            "requested": [True, True, False, False],
            "completed": [True, False, False, False],
        }
    )


def _phase2_analysis() -> dict:
    user_base = _user_base()
    ride_base = _ride_base()
    return {
        "parameters": funnel.AnalysisParameters(source_cutoff=CUTOFF),
        "user_base": user_base,
        "ride_base": ride_base,
        "user_counts": funnel.stage_counts(user_base, funnel.USER_STAGES),
        "ride_counts": funnel.stage_counts(ride_base, funnel.RIDE_STAGES),
        "user_monotonic_violations": [],
        "ride_monotonic_violations": [],
        "user_subset_violations": [],
        "ride_subset_violations": [],
        "segment_reconciliation_errors": [],
    }


def test_overall_summary_reuses_full_precision_phase2_formulas():
    summary = business_insights.overall_transition_summary(
        {"a": 3, "b": 1}, ["a", "b"]
    )
    assert summary.loc[0, "start_count"] == 3
    assert summary.loc[0, "end_count"] == 1
    assert summary.loc[0, "conversion_rate_pct"] == pytest.approx(100 / 3)
    assert summary.loc[0, "dropoff_count"] == 2
    assert summary.loc[0, "dropoff_rate_pct"] == pytest.approx(200 / 3)


def test_first_ride_selects_exactly_one_ride_for_each_eligible_user():
    result = business_insights.first_ride_diagnostic(_ride_base(), CUTOFF)
    assert set(result["first_rides"]["ride_id"]) == {1, 3, 7, 9}
    assert result["first_rides"]["user_id"].is_unique
    assert result["totals"]["unambiguous_users"] == 4
    assert result["totals"]["selected_first_rides"] == 4


def test_missing_and_conflicting_request_timestamps_are_ambiguous():
    result = business_insights.first_ride_diagnostic(_ride_base(), CUTOFF)
    totals = result["totals"]
    assert totals["users_with_missing_request_ts"] == 1
    assert totals["users_with_conflicting_request_ts"] == 1
    assert not result["first_rides"]["user_id"].isin([3, 6]).any()


def test_tied_earliest_requests_are_not_broken_by_ride_id_or_row_order():
    rides = _ride_base()
    first = business_insights.first_ride_diagnostic(rides, CUTOFF)
    reversed_first = business_insights.first_ride_diagnostic(
        rides.iloc[::-1].reset_index(drop=True), CUTOFF
    )
    assert first["totals"]["users_with_earliest_tie"] == 1
    assert first["totals"]["ambiguous_users"] == 3
    assert 4 not in set(first["first_rides"]["user_id"])
    assert set(first["first_rides"]["ride_id"]) == set(
        reversed_first["first_rides"]["ride_id"]
    )


def test_first_ride_progression_uses_observed_timestamps_at_cutoff():
    result = business_insights.first_ride_diagnostic(_ride_base(), CUTOFF)
    progression = result["progression"].set_index("stage")
    assert progression["count"].to_dict() == {
        "requested": 4,
        "accepted": 3,
        "picked_up": 1,
        "finished": 1,
    }
    assert progression.loc["accepted", "conversion_rate_pct"] == 75.0
    assert progression.loc["picked_up", "conversion_rate_pct"] == pytest.approx(
        100 / 3
    )


def test_first_ride_cancellation_diagnostics_remain_distinct():
    totals = business_insights.first_ride_diagnostic(
        _ride_base(), CUTOFF
    )["totals"]
    assert totals["any_cancellation_evidence"] == 2
    assert totals["cancelled_without_recorded_acceptance"] == 1
    assert totals["cancel_after_accept_first_rides"] == 1
    assert totals["first_unfinished_but_later_finished"] == 1


def test_phase3_sql_surfaces_ties_without_a_ride_id_tiebreak():
    query = business_insights.load_canonical_queries()["first_ride_diagnostic"]
    upper = query.upper()
    assert "EARLIEST_CANDIDATE_COUNT" in upper
    assert "ROW_NUMBER" not in upper
    assert "ORDER BY RIDE_ID" not in upper


def test_request_hour_uses_recorded_hour_and_explicit_missing_population():
    result = business_insights.request_hour_summary(_ride_base())
    hourly = result["hourly"].set_index(business_insights.SOURCE_RECORDED_HOUR)
    assert hourly.loc[8, "requested_count"] == 2
    assert hourly.loc[8, "request_share_pct"] == pytest.approx(200 / 9)
    assert hourly.loc[8, "accepted_rate_pct"] == 50.0
    assert hourly.loc[8, "finished_rate_pct"] == 50.0
    assert result["missing_request_timestamp_count"] == 1
    assert result["request_timestamp_missing_evidence_count"] == 1
    assert result["hourly_requested_count"] == 8
    assert result["reconciles_to_timestamped_requests"] is True
    assert result["reconciles_to_ride_population"] is True
    assert result["timezone_note"] == (
        "source-recorded hour; timezone unavailable"
    )


def test_request_hour_rejects_timezone_conversion_input():
    rides = _ride_base()
    rides["request_ts"] = pd.to_datetime(rides["request_ts"], utc=True)
    with pytest.raises(ValueError, match="source-local naive"):
        business_insights.request_hour_summary(rides)


def test_platform_counts_include_missing_and_reconcile_to_phase2_bases():
    result = business_insights.platform_comparison(_user_base(), _ride_base())
    for prefix, base, stages in (
        ("user", _user_base(), funnel.USER_STAGES),
        ("ride", _ride_base(), funnel.RIDE_STAGES),
    ):
        counts = result[f"{prefix}_stage_counts"]
        if base["platform"].isna().any():
            assert business_insights.MISSING_SEGMENT_LABEL in set(
                counts["platform"]
            )
        assert {"ios", "android", "web"} <= set(counts["platform"])
        for stage in stages:
            assert int(counts[stage].sum()) == int(base[stage].sum())


def test_age_counts_preserve_categories_and_skip_download_signup_interpretation():
    result = business_insights.age_comparison(_user_base(), _ride_base())
    user_counts = result["user_stage_counts"]
    assert "Unknown" in set(user_counts["age_group"])
    assert funnel.NO_SIGNUP_AGE in set(user_counts["age_group"])
    assert not result["user_transitions"]["transition"].str.contains(
        "downloaded"
    ).any()
    for stage in funnel.USER_STAGES:
        assert int(user_counts[stage].sum()) == int(_user_base()[stage].sum())


def test_review_without_paid_categories_reconcile_without_reclassification():
    rides = _ride_base()
    rides.loc[rides["ride_id"].eq(1), "has_review"] = True
    rides.loc[rides["ride_id"].eq(2), ["paid", "reviewed", "has_approved"]] = [
        False, False, False
    ]
    before = rides[["paid", "reviewed"]].copy()
    result = business_insights.review_without_paid_decomposition(rides)
    assert result["population_count"] == 2
    assert int(result["decomposition"]["count"].sum()) == 2
    assert set(result["decomposition"]["finish_status"]) == {
        "Finished", "Did not Finish"
    }
    pd.testing.assert_frame_equal(rides[["paid", "reviewed"]], before)


def test_orchestrator_preserves_supplied_phase2_counts_and_bases():
    phase2 = _phase2_analysis()
    user_before = phase2["user_base"].copy(deep=True)
    ride_before = phase2["ride_base"].copy(deep=True)
    result = business_insights.run_business_insights(
        None,
        phase2_analysis=phase2,
        include_sql_crosscheck=False,
    )
    assert result["phase2_counts"]["user"] == phase2["user_counts"]
    assert result["phase2_counts"]["ride"] == phase2["ride_counts"]
    pd.testing.assert_frame_equal(phase2["user_base"], user_before)
    pd.testing.assert_frame_equal(phase2["ride_base"], ride_before)


@pytest.fixture(scope="module")
def live_insights():
    load_dotenv()
    if not os.environ.get(db.ENV_VAR, "").strip():
        pytest.skip(f"{db.ENV_VAR} is not set")
    engine = db.get_engine()
    db.check_connection(engine)
    try:
        yield business_insights.run_business_insights(engine)
    finally:
        engine.dispose()


@requires_db
def test_live_phase3_sql_pandas_and_accepted_snapshot_reconcile(live_insights):
    assert live_insights["phase2_counts"] == {
        "user": {
            "downloaded": 23608,
            "signed_up": 17623,
            "requested": 12406,
            "completed": 6233,
        },
        "ride": {
            "requested": 385477,
            "finished": 223652,
            "paid": 212628,
            "reviewed": 148464,
        },
    }
    totals = live_insights["first_ride"]["totals"]
    assert totals["registered_users_with_request"] == 12406
    assert totals["ambiguous_users"] == 0
    assert totals["accepted_first_rides"] == 7205
    assert totals["picked_up_first_rides"] == 6233
    assert totals["finished_first_rides"] == 6233
    assert totals["cancelled_without_recorded_acceptance"] == 5201
    assert totals["cancel_after_accept_first_rides"] == 972
    assert totals["first_unfinished_but_later_finished"] == 0
    assert live_insights["first_ride_reconciliation"]["all_match"] is True

    hourly = live_insights["request_hour"]
    assert hourly["reconciles_to_ride_population"] is True
    assert hourly["top_six_hours"] == [8, 9, 16, 17, 18, 19]
    assert hourly["top_six_request_share_pct"] == pytest.approx(82.197122)

    anomaly = live_insights["review_without_paid"]
    assert anomaly["population_count"] == 7747
    assert int(anomaly["decomposition"]["count"].sum()) == 7747
    assert anomaly["anomaly_share_of_all_review_evidence_pct"] == pytest.approx(
        4.959318
    )
    assert anomaly["canonical_paid_to_reviewed_pct"] == pytest.approx(69.823353)
