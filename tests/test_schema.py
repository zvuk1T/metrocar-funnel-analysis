"""Schema-expectation tests against the live Metrocar database.

These tests require METROCAR_DATABASE_URL. They skip clearly when the
credential is not configured, so the suite still passes in a credential-free
environment. They verify the live schema matches Section 6.2 and that planned
joins do not multiply rows.
"""

import os

import pytest
from dotenv import load_dotenv

from analysis import db, profile
from analysis.schema import EXPECTED_TABLES, UNIQUE_KEYS

load_dotenv()

requires_db = pytest.mark.skipif(
    not os.environ.get(db.ENV_VAR, "").strip(),
    reason=f"{db.ENV_VAR} is not set; skipping database-dependent test",
)


@pytest.fixture(scope="module")
def engine():
    load_dotenv()
    if not os.environ.get(db.ENV_VAR, "").strip():
        pytest.skip(f"{db.ENV_VAR} is not set")
    eng = db.get_engine()
    db.check_connection(eng)
    yield eng
    eng.dispose()


@requires_db
def test_all_expected_tables_present(engine):
    actual = profile.get_columns(engine)
    comparison = profile.compare_schema(actual)
    assert comparison["missing_tables"] == []


@requires_db
def test_all_expected_columns_present(engine):
    actual = profile.get_columns(engine)
    comparison = profile.compare_schema(actual)
    for table in EXPECTED_TABLES:
        assert comparison["columns"][table]["missing_columns"] == [], (
            f"{table} is missing expected columns"
        )


@requires_db
def test_unique_keys_are_unique(engine):
    for table, key in UNIQUE_KEYS.items():
        p = profile.profile_table(engine, table)
        ks = p["key_stats"]
        assert ks["distinct_keys"] == ks["rows"], f"{table}.{key} is not unique"
        assert ks["null_keys"] == 0, f"{table}.{key} has null values"


@requires_db
def test_joins_do_not_multiply_rows(engine):
    for join in profile.profile_all_joins(engine):
        assert not join["multiplies_rows"], (
            f"{join['left']}→{join['right']} multiplies rows "
            f"({join['joined_rows']} joined > {join['right_rows']} right)"
        )
