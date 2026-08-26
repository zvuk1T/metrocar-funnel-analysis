"""Credential-free tests for the safe profiling runner.

These tests never touch a database. They verify that profiling/report failures
are handled safely and that the engine is always disposed.
"""

from analysis import run


class _FakeEngine:
    def __init__(self):
        self.disposed = False

    def dispose(self):
        self.disposed = True


def test_main_disposes_engine_on_success(monkeypatch):
    engine = _FakeEngine()
    monkeypatch.setattr(run.db, "get_engine", lambda: engine)
    monkeypatch.setattr(run.db, "check_connection", lambda e: None)
    monkeypatch.setattr(run, "write_report", lambda e, p: p)
    assert run.main() == 0
    assert engine.disposed is True


def test_main_disposes_engine_on_profile_failure(monkeypatch, capsys):
    engine = _FakeEngine()
    monkeypatch.setattr(run.db, "get_engine", lambda: engine)
    monkeypatch.setattr(run.db, "check_connection", lambda e: None)

    def boom(e, p):
        raise RuntimeError("profiling exploded")

    monkeypatch.setattr(run, "write_report", boom)
    assert run.main() == 1
    assert engine.disposed is True
    err = capsys.readouterr().err
    assert "profiling failed" in err
    assert "profiling exploded" not in err  # no chained detail leaked


def test_main_returns_1_on_config_error_without_engine(monkeypatch, capsys):
    def raise_config():
        raise run.db.DatabaseConfigError("no credential")

    monkeypatch.setattr(run.db, "get_engine", raise_config)
    assert run.main() == 1
    assert "no credential" in capsys.readouterr().err
