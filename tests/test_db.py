"""Tests for credential handling and connection configuration.

These tests never touch a real database and never print the URL. They verify
that a missing credential fails safely, that the URL scheme is normalized
without exposing the secret, and that connection errors are safe.
"""

import pytest

from analysis import db


def test_missing_env_var_raises_safe_error(monkeypatch):
    monkeypatch.delenv(db.ENV_VAR, raising=False)
    # Also ensure a stray .env does not supply a value during this test.
    monkeypatch.setattr(db, "load_dotenv", lambda: None)
    with pytest.raises(db.DatabaseConfigError) as excinfo:
        db.load_database_url()
    assert db.ENV_VAR in str(excinfo.value)


def test_empty_env_var_raises_safe_error(monkeypatch):
    monkeypatch.setattr(db, "load_dotenv", lambda: None)
    monkeypatch.setenv(db.ENV_VAR, "   ")
    with pytest.raises(db.DatabaseConfigError):
        db.load_database_url()


def test_scheme_normalization_rewrites_only_scheme():
    url = "postgresql://user:secret@host:5432/metrocar"
    normalized = db.normalize_url(url)
    assert normalized.startswith("postgresql+psycopg://")
    # The credential and host portion must pass through unchanged.
    assert normalized.endswith("://user:secret@host:5432/metrocar")


def test_scheme_normalization_accepts_postgres_alias():
    assert db.normalize_url("postgres://u:p@h/db").startswith("postgresql+psycopg://")


def test_scheme_normalization_leaves_correct_scheme():
    url = "postgresql+psycopg://u:p@h/db"
    assert db.normalize_url(url) == url


def test_unsupported_scheme_raises_safe_error():
    with pytest.raises(db.DatabaseConfigError):
        db.normalize_url("mysql://u:p@h/db")


def test_malformed_url_raises_safe_error():
    with pytest.raises(db.DatabaseConfigError):
        db.normalize_url("not-a-url")


def test_error_messages_do_not_contain_credentials():
    secret = "sup3r-s3cret-password"
    with pytest.raises(db.DatabaseConfigError) as excinfo:
        db.normalize_url("not-a-url")
    assert secret not in str(excinfo.value)
    with pytest.raises(db.DatabaseConfigError) as excinfo2:
        db.normalize_url(f"mysql://user:{secret}@host/db")
    assert secret not in str(excinfo2.value)


def test_get_engine_uses_normalized_scheme():
    engine = db.get_engine("postgresql://u:p@localhost:5432/metrocar")
    assert engine.url.drivername == "postgresql+psycopg"


def test_engine_registers_read_only_connect_hook():
    # The read-only enforcement is a connect event on the engine's DBAPI
    # connection. Verify it is registered without connecting.
    from sqlalchemy import event as sa_event

    engine = db.get_engine("postgresql://u:p@localhost:5432/metrocar")
    assert sa_event.contains(engine, "connect", db._set_read_only)


def test_read_only_hook_sets_flag_on_dbapi_connection():
    class FakeDBAPIConnection:
        read_only = False

    fake = FakeDBAPIConnection()
    db._set_read_only(fake, None)
    assert fake.read_only is True


def test_engine_construction_failure_redacts_secret(monkeypatch):
    secret = "sup3r-s3cret-password"
    bad_url = f"postgresql://user:{secret}@host:5432/db"

    def boom(_url):
        raise ValueError(f"bad url {bad_url}")

    monkeypatch.setattr(db, "create_engine", boom)
    with pytest.raises(db.DatabaseConfigError) as excinfo:
        db.get_engine(bad_url)
    # The safe message must not contain the secret, even though the failing
    # underlying error embedded the full URL.
    assert secret not in str(excinfo.value)


def test_redact_masks_url_sentinel():
    secret_url = "postgresql://user:sup3r-s3cret@host/db"
    masked = db._redact(f"failed for {secret_url}", secret_url)
    assert secret_url not in masked
    assert "<redacted-database-url>" in masked


def test_check_connection_failure_is_safe_and_unchained():
    secret = "sup3r-s3cret-password"
    engine = db.get_engine(f"postgresql://user:{secret}@127.0.0.1:1/nope")
    with pytest.raises(db.DatabaseConfigError) as excinfo:
        db.check_connection(engine)
    # Message must not contain the secret, and there must be no chained
    # traceback that could leak the URL or host details.
    assert secret not in str(excinfo.value)
    assert excinfo.value.__cause__ is None
    assert excinfo.value.__context__ is None or secret not in str(
        excinfo.value.__context__
    )
