"""Credential-free tests for schema-mismatch handling and report rendering.

These tests use fake profiling result dicts and never touch a database. They
verify that a missing table or column produces a useful partial result instead
of a crash, and that the report renders the new sections correctly.
"""

from analysis import profile
from analysis.report import render_report


def _base_results():
    return {
        "schema_comparison": {
            "missing_tables": [],
            "extra_tables": [],
            "columns": {},
        },
        "schema_problems": [],
        "columns": {},
        "tables": {},
        "joins": [],
        "ride_status": {
            "ride_flags": {"total_requests": 0, "with_accept": 0, "with_pickup": 0,
                           "with_dropoff": 0, "with_cancel": 0},
            "transactions_by_status": [],
            "reviews": {"total_reviews": 0, "distinct_rides_reviewed": 0},
        },
        "ride_timestamp_order": {},
        "ride_stage_inconsistencies": {},
        "paid_without_completion": {"approved_payment_without_dropoff": 0,
                                    "review_without_dropoff": 0,
                                    "approved_payment_on_cancelled_ride": 0},
        "transaction_multiplicity": [],
        "review_multiplicity": [],
        "date_ranges": {},
    }


def test_schema_problems_flags_missing_table():
    comparison = {"missing_tables": ["signups"], "extra_tables": [], "columns": {}}
    problems = profile.schema_problems(comparison)
    assert any("signups" in p for p in problems)


def test_schema_problems_flags_missing_column():
    comparison = {
        "missing_tables": [],
        "extra_tables": [],
        "columns": {"signups": {"missing_columns": ["age_range"], "extra_columns": []}},
    }
    problems = profile.schema_problems(comparison)
    assert any("age_range" in p for p in problems)


def test_schema_problems_empty_when_clean():
    comparison = {"missing_tables": [], "extra_tables": [], "columns": {}}
    assert profile.schema_problems(comparison) == []


def test_compare_schema_reports_extra_public_tables():
    actual = {t: [] for t in profile.EXPECTED_TABLES}
    public = list(profile.EXPECTED_TABLES) + ["unexpected_table"]
    comparison = profile.compare_schema(actual, public)
    assert "unexpected_table" in comparison["extra_tables"]


def test_profile_table_skips_missing_columns(monkeypatch):
    # Simulate a live table missing the age_range column; only existing
    # columns should be queried, and the missing one reported as skipped.
    queried = []

    def fake_rows(engine, sql, params=None):
        queried.append(sql)
        if "COUNT(*) AS n" in sql and "FILTER" not in sql:
            return [{"n": 5}]
        if "DISTINCT" in sql:
            return [{"rows": 5, "distinct_keys": 5, "null_keys": 0}]
        if "FILTER" in sql:
            return [{"n": 0}]
        if "MIN(" in sql:
            return [{"min_ts": None, "max_ts": None}]
        return []

    monkeypatch.setattr(profile, "_rows", fake_rows)
    result = profile.profile_table(
        None, "signups", available_columns=["user_id", "session_id", "signup_ts"]
    )
    assert "age_range" in result["skipped_columns"]
    assert "age_range" not in result["null_counts"]


def test_render_report_handles_missing_table():
    results = _base_results()
    results["schema_comparison"]["missing_tables"] = ["signups"]
    results["schema_problems"] = ["missing table: signups"]
    results["tables"]["signups"] = {"table": "signups", "error": "missing table"}
    md = render_report(results)
    assert "missing table: signups" in md
    assert "`signups` — missing table" in md


def test_render_report_shows_inconsistency_sections():
    results = _base_results()
    results["ride_stage_inconsistencies"] = {"pickup_without_accept": 2}
    results["paid_without_completion"] = {
        "approved_payment_without_dropoff": 1,
        "review_without_dropoff": 3,
        "approved_payment_on_cancelled_ride": 4,
    }
    md = render_report(results)
    assert "Ride-stage inconsistency checks" in md
    assert "pickup_without_accept: 2" in md
    assert "approved payment without drop-off: 1" in md
    assert "review without drop-off: 3" in md
    assert "approved payment on cancelled ride: 4" in md


def test_profile_table_does_not_query_absent_key(monkeypatch):
    # signups normally keys on user_id; simulate it missing from the live table.
    queried = []

    def fake_rows(engine, sql, params=None):
        queried.append(sql)
        if "COUNT(*) AS n" in sql and "FILTER" not in sql:
            return [{"n": 5}]
        if "FILTER" in sql:
            return [{"n": 0}]
        if "MIN(" in sql:
            return [{"min_ts": None, "max_ts": None}]
        return []

    monkeypatch.setattr(profile, "_rows", fake_rows)
    result = profile.profile_table(
        None, "signups", available_columns=["session_id", "signup_ts", "age_range"]
    )
    assert result["key"] is None
    assert result["key_stats"] is None
    assert not any("DISTINCT" in q for q in queried), "must not query an absent key"


def test_run_profile_skips_dependent_queries_when_table_missing(monkeypatch):
    # ride_requests is absent; dependent ride queries must be skipped, not run.
    monkeypatch.setattr(profile, "list_public_tables", lambda e: ["signups"])
    monkeypatch.setattr(
        profile, "get_columns",
        lambda e: {"signups": [{"column": "user_id", "data_type": "text",
                                "is_nullable": "NO"}]},
    )
    monkeypatch.setattr(profile, "profile_table",
                        lambda e, t, a=None: {"table": t, "row_count": 1,
                                              "key": None, "key_stats": None,
                                              "null_counts": {}, "categorical": {},
                                              "timestamps": {}, "skipped_columns": []})
    monkeypatch.setattr(profile, "profile_all_joins", lambda e: [])

    def forbidden(engine, *args):
        raise AssertionError("dependent query ran despite missing table")

    for fn in ("ride_status_patterns", "ride_timestamp_order",
               "ride_stage_inconsistencies", "paid_without_completion",
               "transaction_multiplicity", "review_multiplicity",
               "date_range_evidence"):
        monkeypatch.setattr(profile, fn, forbidden)

    results = profile.run_profile(None)
    assert results["ride_status"]["skipped"] == "required schema missing"
    assert results["ride_stage_inconsistencies"]["skipped"] == "required schema missing"
    assert results["date_ranges"]["skipped"] == "required schema missing"


def test_run_profile_gates_joins_without_mocking_joins(monkeypatch):
    # Only app_downloads exists; signups/ride_requests/transactions/reviews are
    # missing. Joins referencing missing tables must be skipped, not executed.
    # profile_all_joins is NOT mocked; profile_join is stubbed to detect calls.
    monkeypatch.setattr(profile, "list_public_tables", lambda e: ["app_downloads"])
    monkeypatch.setattr(
        profile, "get_columns",
        lambda e: {"app_downloads": [
            {"column": "app_download_key", "data_type": "text", "is_nullable": "NO"},
            {"column": "platform", "data_type": "text", "is_nullable": "YES"},
            {"column": "download_ts", "data_type": "timestamp", "is_nullable": "YES"},
        ]},
    )
    monkeypatch.setattr(profile, "profile_table",
                        lambda e, t, a=None: {"table": t, "row_count": 1,
                                              "key": None, "key_stats": None,
                                              "null_counts": {}, "categorical": {},
                                              "timestamps": {}, "skipped_columns": []})

    called = []
    real_profile_join = profile.profile_join

    def spy(engine, left, left_key, right, right_key):
        called.append((left, right))
        return {"left": left, "left_key": left_key, "right": right,
                "right_key": right_key, "left_rows": 0, "right_rows": 0,
                "joined_rows": 0, "distinct_right_keys": 0,
                "orphan_right_rows": 0, "multiplies_rows": False}

    monkeypatch.setattr(profile, "profile_join", spy)
    # Stub the other dependent sections so the run completes without a DB.
    for fn in ("ride_status_patterns", "ride_timestamp_order",
               "ride_stage_inconsistencies", "paid_without_completion",
               "transaction_multiplicity", "review_multiplicity",
               "date_range_evidence"):
        monkeypatch.setattr(profile, fn, lambda e, *a: {"skipped": "required schema missing"})

    results = profile.run_profile(None)

    # Every join needs a missing right-side table, so none may execute.
    assert called == [], "profile_join ran despite missing required tables"
    assert all("skipped" in j for j in results["joins"])
    assert len(results["joins"]) == len(profile.PROVISIONAL_JOINS)


def test_render_report_completes_on_fully_skipped_profile():
    # Every dependent section is skipped (schema missing); render must not crash.
    skipped = {"skipped": "required schema missing"}
    results = {
        "schema_comparison": {
            "missing_tables": list(profile.EXPECTED_TABLES),
            "extra_tables": [],
            "columns": {},
        },
        "schema_problems": [f"missing table: {t}" for t in profile.EXPECTED_TABLES],
        "columns": {},
        "tables": {t: {"table": t, "error": "missing table"}
                   for t in profile.EXPECTED_TABLES},
        "joins": [{"left": l, "left_key": lk, "right": r, "right_key": rk,
                   "skipped": "required schema missing"}
                  for l, lk, r, rk, _ in profile.PROVISIONAL_JOINS],
        "ride_status": dict(skipped),
        "ride_timestamp_order": dict(skipped),
        "ride_stage_inconsistencies": dict(skipped),
        "paid_without_completion": dict(skipped),
        "transaction_multiplicity": dict(skipped),
        "review_multiplicity": dict(skipped),
        "date_ranges": dict(skipped),
    }
    md = render_report(results)
    assert "required schema missing" in md
    assert "Ride status and null patterns" in md
    assert "Date/cohort evidence" in md
