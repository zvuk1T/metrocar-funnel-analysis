"""Structural profiling of the Metrocar database (Phase 1).

This module runs read-only metadata and ``SELECT`` queries to document the
actual shape of the data before any metric is defined. It answers: what tables
and columns exist, are keys unique, where are the nulls, what are the timestamp
ranges, and do the planned joins multiply rows.

It deliberately does NOT compute funnel stages, conversion rates, or any
business insight. Those belong to later phases.

Output grain: one plain-Python dict per check, so results are easy to print,
test, and write into the data-quality report without a formatting layer.
"""

from __future__ import annotations

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from analysis.schema import EXPECTED_TABLES, PROVISIONAL_JOINS, UNIQUE_KEYS


def _rows(engine: Engine, sql: str, params: dict | None = None) -> list[dict]:
    """Run a read-only query and return rows as a list of dicts."""
    with engine.connect() as connection:
        result = connection.execute(text(sql), params or {})
        return [dict(row) for row in result.mappings()]


def list_public_tables(engine: Engine) -> list[str]:
    """Return every table in the public schema, sorted.

    Grain: one row per table. This lets the report genuinely list extra tables
    instead of only checking the five expected ones.
    """
    rows = _rows(
        engine,
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """,
    )
    return [r["table_name"] for r in rows]


def get_columns(engine: Engine) -> dict[str, list[dict]]:
    """Return actual columns per table from information_schema.

    Grain: one row per (table, column). Only the five expected tables are
    returned, so the result stays focused on the planned schema.
    """
    sql = """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = ANY(:tables)
        ORDER BY table_name, ordinal_position
    """
    rows = _rows(engine, sql, {"tables": list(EXPECTED_TABLES)})
    columns: dict[str, list[dict]] = {}
    for row in rows:
        columns.setdefault(row["table_name"], []).append(
            {
                "column": row["column_name"],
                "data_type": row["data_type"],
                "is_nullable": row["is_nullable"],
            }
        )
    return columns


def compare_schema(actual: dict[str, list[dict]],
                   public_tables: list[str] | None = None) -> dict:
    """Compare live columns to the expected schema.

    Returns a dict with missing/extra tables and per-table missing/extra
    columns. ``public_tables`` should come from ``list_public_tables`` so that
    extra tables anywhere in the schema are reported, not just expected ones.
    """
    expected_tables = set(EXPECTED_TABLES)
    actual_tables = set(public_tables) if public_tables is not None else set(actual)
    per_table = {}
    for table in sorted(expected_tables & set(actual)):
        expected_cols = set(EXPECTED_TABLES[table])
        actual_cols = {c["column"] for c in actual[table]}
        per_table[table] = {
            "missing_columns": sorted(expected_cols - actual_cols),
            "extra_columns": sorted(actual_cols - expected_cols),
        }
    return {
        "missing_tables": sorted(expected_tables - actual_tables),
        "extra_tables": sorted(actual_tables - expected_tables),
        "columns": per_table,
    }


def schema_problems(comparison: dict) -> list[str]:
    """Return a human-readable list of schema mismatches, empty when clean."""
    problems = [f"missing table: {t}" for t in comparison["missing_tables"]]
    for table, cols in comparison["columns"].items():
        problems += [f"{table}: missing column {c}" for c in cols["missing_columns"]]
    return problems


def profile_table(engine: Engine, table: str,
                  available_columns: list[str] | None = None) -> dict:
    """Profile one table: row count, key uniqueness, nulls, categories, timestamps.

    Grain: a single summary dict for the table. ``available_columns`` should be
    the live column list; when provided, only columns that actually exist are
    queried, so a schema mismatch produces a partial result instead of a crash.
    """
    key = UNIQUE_KEYS.get(table)
    planned = EXPECTED_TABLES[table]
    columns = [c for c in planned if available_columns is None or c in available_columns]
    skipped = [c for c in planned if c not in columns]

    row_count = _rows(engine, f'SELECT COUNT(*) AS n FROM "{table}"')[0]["n"]

    # Only query the candidate key when it actually exists in the live table.
    key_present = key is not None and (available_columns is None or key in available_columns)
    key_stats = None
    if key_present:
        key_stats = _rows(
            engine,
            f'SELECT COUNT(*) AS rows, COUNT(DISTINCT "{key}") AS distinct_keys, '
            f'COUNT(*) FILTER (WHERE "{key}" IS NULL) AS null_keys FROM "{table}"',
        )[0]

    null_counts = {}
    for column in columns:
        null_counts[column] = _rows(
            engine,
            f'SELECT COUNT(*) FILTER (WHERE "{column}" IS NULL) AS n FROM "{table}"',
        )[0]["n"]

    # Categorical columns: distinct values with counts, capped for safety.
    categorical = {}
    for column in ("platform", "age_range", "charge_status", "rating"):
        if column in columns:
            categorical[column] = _rows(
                engine,
                f'SELECT "{column}" AS value, COUNT(*) AS n FROM "{table}" '
                f'GROUP BY "{column}" ORDER BY n DESC LIMIT 50',
            )

    # Timestamp columns: min/max range.
    timestamps = {}
    for column in columns:
        if column.endswith("_ts"):
            timestamps[column] = _rows(
                engine,
                f'SELECT MIN("{column}") AS min_ts, MAX("{column}") AS max_ts '
                f'FROM "{table}"',
            )[0]

    return {
        "table": table,
        "row_count": row_count,
        "key": key if key_present else None,
        "key_stats": key_stats,
        "null_counts": null_counts,
        "categorical": categorical,
        "timestamps": timestamps,
        "skipped_columns": skipped,
    }


def profile_join(engine: Engine, left: str, left_key: str,
                 right: str, right_key: str) -> dict:
    """Measure cardinality and referential coverage for one relationship.

    Grain: one summary dict per planned join. We count rows on each side, how
    many right-side keys match a left-side key, and whether any right-side key
    is orphaned. Comparing joined row count to the right-side row count shows
    whether the join multiplies rows (a fan-out that would inflate metrics).
    """
    left_rows = _rows(engine, f'SELECT COUNT(*) AS n FROM "{left}"')[0]["n"]
    right_rows = _rows(engine, f'SELECT COUNT(*) AS n FROM "{right}"')[0]["n"]

    stats = _rows(
        engine,
        f"""
        SELECT
          COUNT(*) AS joined_rows,
          COUNT(DISTINCT r."{right_key}") AS distinct_right_keys,
          COUNT(*) FILTER (WHERE l."{left_key}" IS NULL) AS unmatched_right_rows
        FROM "{right}" r
        LEFT JOIN "{left}" l ON l."{left_key}" = r."{right_key}"
        """,
    )[0]

    # Rows on the right whose key does not appear on the left (orphans).
    orphans = _rows(
        engine,
        f"""
        SELECT COUNT(*) AS n
        FROM "{right}" r
        WHERE NOT EXISTS (
          SELECT 1 FROM "{left}" l WHERE l."{left_key}" = r."{right_key}"
        )
        """,
    )[0]["n"]

    return {
        "left": left,
        "left_key": left_key,
        "right": right,
        "right_key": right_key,
        "left_rows": left_rows,
        "right_rows": right_rows,
        "joined_rows": stats["joined_rows"],
        "distinct_right_keys": stats["distinct_right_keys"],
        "orphan_right_rows": orphans,
        "multiplies_rows": stats["joined_rows"] > right_rows,
    }


def profile_all_joins(engine: Engine) -> list[dict]:
    """Profile every provisional relationship from Section 6.3."""
    return [
        profile_join(engine, left, left_key, right, right_key)
        for left, left_key, right, right_key, _ in PROVISIONAL_JOINS
    ]


def ride_status_patterns(engine: Engine) -> dict:
    """Document null/status patterns that define ride outcomes.

    Grain: one summary dict. These counts are evidence for later metric
    definitions (requested/accepted/completed/paid/reviewed); they are NOT yet
    funnel numbers. We count non-null timestamps and distinct rides per
    outcome to see how the data represents each stage.
    """
    ride_flags = _rows(
        engine,
        """
        SELECT
          COUNT(*) AS total_requests,
          COUNT(*) FILTER (WHERE accept_ts IS NOT NULL) AS with_accept,
          COUNT(*) FILTER (WHERE pickup_ts IS NOT NULL) AS with_pickup,
          COUNT(*) FILTER (WHERE dropoff_ts IS NOT NULL) AS with_dropoff,
          COUNT(*) FILTER (WHERE cancel_ts IS NOT NULL) AS with_cancel
        FROM ride_requests
        """,
    )[0]

    tx = _rows(
        engine,
        """
        SELECT
          charge_status,
          COUNT(*) AS transactions,
          COUNT(DISTINCT ride_id) AS distinct_rides
        FROM transactions
        GROUP BY charge_status
        ORDER BY charge_status
        """,
    )

    reviews = _rows(
        engine,
        """
        SELECT
          COUNT(*) AS total_reviews,
          COUNT(DISTINCT ride_id) AS distinct_rides_reviewed
        FROM reviews
        """,
    )[0]

    return {"ride_flags": ride_flags, "transactions_by_status": tx, "reviews": reviews}


def ride_timestamp_order(engine: Engine) -> dict:
    """Check the chronological order of ride timestamps.

    Grain: one summary dict. Confirms request <= accept <= pickup <= dropoff
    holds, which matters for duration math and for trusting the stage sequence.
    """
    return _rows(
        engine,
        """
        SELECT
          COUNT(*) FILTER (WHERE accept_ts < request_ts) AS accept_before_request,
          COUNT(*) FILTER (WHERE pickup_ts < accept_ts) AS pickup_before_accept,
          COUNT(*) FILTER (WHERE dropoff_ts < pickup_ts) AS dropoff_before_pickup,
          COUNT(*) FILTER (
            WHERE cancel_ts IS NOT NULL AND dropoff_ts IS NOT NULL
          ) AS cancelled_and_dropped_off
        FROM ride_requests
        """,
    )[0]


def transaction_multiplicity(engine: Engine) -> list[dict]:
    """Count how many rides have 0, 1, or many transactions.

    Grain: one row per transaction-count bucket. Shows whether a ride can have
    more than one transaction, which would inflate revenue if joined naively.
    """
    return _rows(
        engine,
        """
        SELECT tx_count, COUNT(*) AS rides
        FROM (
          SELECT r.ride_id, COUNT(t.ride_id) AS tx_count
          FROM ride_requests r
          LEFT JOIN transactions t ON t.ride_id = r.ride_id
          GROUP BY r.ride_id
        ) s
        GROUP BY tx_count
        ORDER BY tx_count
        """,
    )


def review_multiplicity(engine: Engine) -> list[dict]:
    """Count how many rides have 0, 1, or many reviews.

    Grain: one row per review-count bucket. Same fan-out concern as
    transactions, for the reviewed-rides stage.
    """
    return _rows(
        engine,
        """
        SELECT review_count, COUNT(*) AS rides
        FROM (
          SELECT r.ride_id, COUNT(rv.review_id) AS review_count
          FROM ride_requests r
          LEFT JOIN reviews rv ON rv.ride_id = r.ride_id
          GROUP BY r.ride_id
        ) s
        GROUP BY review_count
        ORDER BY review_count
        """,
    )


def date_range_evidence(engine: Engine) -> dict:
    """Gather timestamp ranges relevant to date/cohort attribution.

    Grain: one summary dict. Comparing download, signup, and request time
    ranges shows whether events cluster in the same window, which informs the
    date-filter rule decided in a later phase.
    """
    downloads = _rows(
        engine,
        "SELECT MIN(download_ts) AS min_ts, MAX(download_ts) AS max_ts FROM app_downloads",
    )[0]
    signups = _rows(
        engine,
        "SELECT MIN(signup_ts) AS min_ts, MAX(signup_ts) AS max_ts FROM signups",
    )[0]
    requests = _rows(
        engine,
        "SELECT MIN(request_ts) AS min_ts, MAX(request_ts) AS max_ts FROM ride_requests",
    )[0]
    return {"downloads": downloads, "signups": signups, "requests": requests}


def ride_stage_inconsistencies(engine: Engine) -> dict:
    """Count structurally inconsistent ride-stage combinations.

    Grain: one summary dict. These are data-quality signals, not funnel
    metrics. Each count isolates a combination that should be impossible or
    rare if the stage sequence is clean (e.g. a drop-off with no pickup).
    """
    return _rows(
        engine,
        """
        SELECT
          COUNT(*) FILTER (
            WHERE pickup_ts IS NOT NULL AND accept_ts IS NULL
          ) AS pickup_without_accept,
          COUNT(*) FILTER (
            WHERE dropoff_ts IS NOT NULL AND pickup_ts IS NULL
          ) AS dropoff_without_pickup,
          COUNT(*) FILTER (
            WHERE dropoff_ts IS NOT NULL AND accept_ts IS NULL
          ) AS dropoff_without_accept,
          COUNT(*) FILTER (
            WHERE cancel_ts IS NOT NULL AND accept_ts IS NOT NULL
          ) AS cancelled_with_accept,
          COUNT(*) FILTER (
            WHERE cancel_ts IS NOT NULL AND pickup_ts IS NOT NULL
          ) AS cancelled_with_pickup,
          COUNT(*) FILTER (
            WHERE cancel_ts IS NOT NULL AND dropoff_ts IS NOT NULL
          ) AS cancelled_with_dropoff
        FROM ride_requests
        """,
    )[0]


def paid_without_completion(engine: Engine) -> dict:
    """Count approved payments and reviews attached to incomplete rides.

    Grain: one summary dict. A completed ride is provisionally identified by a
    non-null dropoff_ts. These counts flag rows that would break the rides
    funnel order if treated as valid later-stage events.
    """
    paid = _rows(
        engine,
        """
        SELECT COUNT(*) AS n
        FROM transactions t
        JOIN ride_requests r ON r.ride_id = t.ride_id
        WHERE t.charge_status = 'Approved' AND r.dropoff_ts IS NULL
        """,
    )[0]["n"]
    reviewed = _rows(
        engine,
        """
        SELECT COUNT(*) AS n
        FROM reviews rv
        JOIN ride_requests r ON r.ride_id = rv.ride_id
        WHERE r.dropoff_ts IS NULL
        """,
    )[0]["n"]
    paid_cancelled = _rows(
        engine,
        """
        SELECT COUNT(*) AS n
        FROM transactions t
        JOIN ride_requests r ON r.ride_id = t.ride_id
        WHERE t.charge_status = 'Approved' AND r.cancel_ts IS NOT NULL
        """,
    )[0]["n"]
    return {
        "approved_payment_without_dropoff": paid,
        "review_without_dropoff": reviewed,
        "approved_payment_on_cancelled_ride": paid_cancelled,
    }


def run_profile(engine: Engine) -> dict:
    """Run the full Phase 1 structural profile and return all results.

    Grain: one dict of sections. Schema validation runs first. Dependent
    queries are gated: a section runs only when every table and column it
    needs is present, so a schema mismatch yields a useful partial report
    instead of crashing on a missing relation or column.
    """
    public_tables = list_public_tables(engine)
    actual_columns = get_columns(engine)
    comparison = compare_schema(actual_columns, public_tables)
    problems = schema_problems(comparison)

    def has(table: str, *cols: str) -> bool:
        """True when a table and all named columns exist in the live schema."""
        if table not in actual_columns:
            return False
        present = {c["column"] for c in actual_columns[table]}
        return all(c in present for c in cols)

    tables = {}
    for table in EXPECTED_TABLES:
        if table in actual_columns:
            available = [c["column"] for c in actual_columns[table]]
            tables[table] = profile_table(engine, table, available)
        else:
            tables[table] = {"table": table, "error": "missing table"}

    def run_if(condition: bool, fn, *args):
        """Run a dependent query only when its required schema is present."""
        return fn(engine, *args) if condition else {"skipped": "required schema missing"}

    ride_cols = has("ride_requests", "ride_id", "request_ts", "accept_ts",
                    "pickup_ts", "dropoff_ts", "cancel_ts")

    # Gate each provisional join on its required tables and key columns.
    joins = []
    for left, left_key, right, right_key, _desc in PROVISIONAL_JOINS:
        if has(left, left_key) and has(right, right_key):
            joins.append(profile_join(engine, left, left_key, right, right_key))
        else:
            joins.append({
                "left": left, "left_key": left_key,
                "right": right, "right_key": right_key,
                "skipped": "required schema missing",
            })

    return {
        "schema_comparison": comparison,
        "schema_problems": problems,
        "columns": actual_columns,
        "tables": tables,
        "joins": joins,
        "ride_status": run_if(
            ride_cols and has("transactions", "ride_id", "charge_status")
            and has("reviews", "ride_id"),
            ride_status_patterns,
        ),
        "ride_timestamp_order": run_if(ride_cols, ride_timestamp_order),
        "ride_stage_inconsistencies": run_if(ride_cols, ride_stage_inconsistencies),
        "paid_without_completion": run_if(
            ride_cols and has("transactions", "ride_id", "charge_status")
            and has("reviews", "ride_id"),
            paid_without_completion,
        ),
        "transaction_multiplicity": run_if(
            has("ride_requests", "ride_id") and has("transactions", "ride_id"),
            transaction_multiplicity,
        ),
        "review_multiplicity": run_if(
            has("ride_requests", "ride_id") and has("reviews", "ride_id"),
            review_multiplicity,
        ),
        "date_ranges": run_if(
            has("app_downloads", "download_ts") and has("signups", "signup_ts")
            and has("ride_requests", "request_ts"),
            date_range_evidence,
        ),
    }
