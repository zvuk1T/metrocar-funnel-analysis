"""Safe command-line runner for the Phase 1 structural profile.

This is the single documented entry point for regenerating the data-quality
report. It loads the credential, verifies the connection, runs the read-only
profile, and writes the Markdown report. Every failure path exits with a
credential-free message instead of a traceback that could expose the URL.

Usage:
    python -m analysis.run
"""

from __future__ import annotations

import sys

from analysis import db
from analysis.report import write_report

OUTPUT_PATH = "docs/data_quality_report.md"


def main() -> int:
    """Run the profile and write the report. Returns a process exit code."""
    engine = None
    try:
        engine = db.get_engine()
        db.check_connection(engine)
        path = write_report(engine, OUTPUT_PATH)
    except db.DatabaseConfigError as exc:
        # Safe message only; never echo the URL or a chained exception.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - profiling/report failure
        print(
            f"ERROR: profiling failed ({type(exc).__name__}). "
            "No report was written.",
            file=sys.stderr,
        )
        return 1
    finally:
        if engine is not None:
            engine.dispose()

    print(f"Data-quality report written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
