"""Safe, read-only PostgreSQL access for the Metrocar analysis.

This module is the single place that touches the database credential. It loads
the connection URL from the ``METROCAR_DATABASE_URL`` environment variable,
normalizes only the URL scheme in memory when needed, and builds a synchronous
SQLAlchemy 2.x engine using the psycopg 3 driver. No ORM and no async code.

Security rules enforced here:
- the URL is never printed, logged, or included in error messages;
- errors are raised as safe messages that cannot contain the credential.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine

ENV_VAR = "METROCAR_DATABASE_URL"

# Schemes we accept from the environment, mapped to the scheme the engine needs.
# Only the scheme is rewritten; the credentials and host are never modified.
_SCHEME_NORMALIZATION = {
    "postgresql": "postgresql+psycopg",
    "postgres": "postgresql+psycopg",
}


class DatabaseConfigError(RuntimeError):
    """Raised for missing or invalid database configuration.

    Messages are written by us and never include the connection URL, so the
    credential cannot leak through an exception.
    """


def _redact(message: str, url: str | None) -> str:
    """Return ``message`` with the raw URL replaced by a sentinel.

    Defense in depth: even if an unexpected error text somehow embeds the
    credential, it is masked before the message is shown or raised.
    """
    if url:
        return message.replace(url, "<redacted-database-url>")
    return message


def _set_read_only(dbapi_connection, _connection_record):
    """Put a new DBAPI connection into read-only mode.

    Registered as a SQLAlchemy ``connect`` listener so every connection is
    read-only at the database level, not only by convention in query text.
    Defined at module level so tests can call it directly.
    """
    dbapi_connection.read_only = True


def load_database_url() -> str:
    """Return the raw database URL from the environment.

    Loads a local ``.env`` file if present. Raises a safe error when the
    variable is missing or empty, without revealing any value.
    """
    load_dotenv()
    url = os.environ.get(ENV_VAR, "").strip()
    if not url:
        raise DatabaseConfigError(
            f"Environment variable {ENV_VAR} is not set. "
            "Add it to a local .env file (see .env.example) or export it in "
            "your shell. Never commit the real URL."
        )
    return url


def normalize_url(url: str) -> str:
    """Return the URL with the scheme SQLAlchemy + psycopg 3 expects.

    Only the scheme portion before ``://`` is changed. The historical
    MasterSchool URL uses the generic ``postgresql://`` scheme; SQLAlchemy
    needs ``postgresql+psycopg://`` to select the psycopg 3 driver. The
    credential and host parts are passed through unchanged.
    """
    if "://" not in url:
        raise DatabaseConfigError(
            f"{ENV_VAR} is not a valid connection URL (missing '://')."
        )
    scheme, rest = url.split("://", 1)
    target_scheme = _SCHEME_NORMALIZATION.get(scheme, scheme)
    if target_scheme != "postgresql+psycopg":
        raise DatabaseConfigError(
            f"{ENV_VAR} uses an unsupported URL scheme. "
            "Expected a PostgreSQL connection URL."
        )
    return f"{target_scheme}://{rest}"


def get_engine(url: str | None = None) -> Engine:
    """Create a synchronous SQLAlchemy engine for read-only queries.

    Accepts an optional URL for testing; otherwise loads it from the
    environment. The engine is created lazily and does not connect until a
    query is executed. Engine construction is wrapped so a malformed URL
    cannot leak the credential through a chained traceback.
    """
    raw = url if url is not None else load_database_url()
    try:
        engine = create_engine(normalize_url(raw))
    except Exception as exc:  # noqa: BLE001 - re-raised as a safe message
        raise DatabaseConfigError(
            _redact(
                "Could not configure the database engine. Check that "
                f"{ENV_VAR} is a valid PostgreSQL URL. "
                f"Underlying error type: {type(exc).__name__}.",
                raw,
            )
        ) from None

    # Enforce read-only at the connection level for every new connection.
    event.listen(engine, "connect", _set_read_only)

    return engine


def check_connection(engine: Engine) -> None:
    """Run a trivial read-only query to confirm the connection works.

    Raises a safe error on failure. The underlying driver error is NOT
    chained, so a full traceback cannot expose the URL or host details.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except DatabaseConfigError:
        raise
    except Exception as exc:  # noqa: BLE001 - re-raised as a safe message
        raise DatabaseConfigError(
            "Could not connect to the Metrocar database. Check that "
            f"{ENV_VAR} is correct and the database is reachable. "
            f"Underlying error type: {type(exc).__name__}."
        ) from None
