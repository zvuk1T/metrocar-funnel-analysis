"""Regression tests for the aggregate-only Phase 4A public-data boundary."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from analysis import funnel, public_data

ACCEPTED_SOURCE_CUTOFF = pd.Timestamp("2022-04-24 20:00:00")
ACCEPTED_COUNTS = {
    "user": {
        "downloaded": 23_608,
        "signed_up": 17_623,
        "requested": 12_406,
        "completed": 6_233,
    },
    "ride": {
        "requested": 385_477,
        "finished": 223_652,
        "paid": 212_628,
        "reviewed": 148_464,
    },
}
FORBIDDEN_PUBLIC_KEYS = {
    "app_download_key",
    "session_id",
    "user_id",
    "ride_id",
    "transaction_id",
    "review_id",
    "email",
    "password",
    "database_url",
}


def _accepted_reconciliation() -> dict[str, object]:
    user_counts = ACCEPTED_COUNTS["user"]
    ride_counts = ACCEPTED_COUNTS["ride"]
    return {
        "all_match": True,
        "analysis": {
            "parameters": funnel.AnalysisParameters(
                source_cutoff=ACCEPTED_SOURCE_CUTOFF
            ),
            "user_counts": user_counts,
            "ride_counts": ride_counts,
            "user_rates": funnel.adjacent_rates(user_counts, funnel.USER_STAGES),
            "ride_rates": funnel.adjacent_rates(ride_counts, funnel.RIDE_STAGES),
            "user_monotonic_violations": [],
            "ride_monotonic_violations": [],
            "user_subset_violations": [],
            "ride_subset_violations": [],
            "segment_reconciliation_errors": [],
        },
    }


def _collect_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            child_key
            for child in value.values()
            for child_key in _collect_keys(child)
        }
    if isinstance(value, list):
        return {key for child in value for key in _collect_keys(child)}
    return set()


def test_public_payload_matches_the_accepted_full_snapshot():
    payload = public_data.build_public_payload(_accepted_reconciliation())

    assert payload["scope"] == {
        "kind": "full_snapshot",
        "sourceCutoff": "2022-04-24T20:00:00",
        "cohortStart": None,
        "cohortEndExclusive": None,
    }
    for funnel_key, expected_counts in ACCEPTED_COUNTS.items():
        stages = payload["funnels"][funnel_key]["stages"]
        assert {stage["key"]: stage["count"] for stage in stages} == expected_counts


def test_public_payload_contains_only_two_small_aggregate_funnels():
    payload = public_data.build_public_payload(_accepted_reconciliation())

    assert set(payload["funnels"]) == {"user", "ride"}
    assert all(len(item["stages"]) == 4 for item in payload["funnels"].values())
    assert not (_collect_keys(payload) & FORBIDDEN_PUBLIC_KEYS)
    text = public_data.serialise_payload(payload).lower()
    assert "postgresql://" not in text
    assert "postgresql+psycopg://" not in text
    assert "metrocar_database_url" not in text


def test_public_serialisation_is_deterministic_and_valid_json():
    first = public_data.build_public_payload(_accepted_reconciliation())
    second = public_data.build_public_payload(_accepted_reconciliation())

    first_text = public_data.serialise_payload(first)
    assert first_text == public_data.serialise_payload(second)
    assert json.loads(first_text) == first


def test_export_fails_closed_for_filters_or_failed_reconciliation():
    filtered = _accepted_reconciliation()
    filtered["analysis"]["parameters"] = funnel.calendar_parameters(
        "2022-01-01", "2022-01-31", ACCEPTED_SOURCE_CUTOFF
    )
    with pytest.raises(ValueError, match="full snapshot"):
        public_data.build_public_payload(filtered)

    failed = _accepted_reconciliation()
    failed["all_match"] = False
    with pytest.raises(ValueError, match="reconciliation"):
        public_data.build_public_payload(failed)


def test_checked_in_artifact_is_the_deterministic_accepted_payload():
    expected = public_data.serialise_payload(
        public_data.build_public_payload(_accepted_reconciliation())
    )
    assert public_data.DEFAULT_OUTPUT_PATH.read_text(encoding="utf-8") == expected
