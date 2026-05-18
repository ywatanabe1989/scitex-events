"""Pytest fixtures and rootdir marker for this package.

An empty conftest.py at tests/ is the canonical SciTeX
convention (audit-project PS208) — it pins the pytest
rootdir and gives downstream fixtures a home.

Also performs module-import-time coverage wiring (parallel +
subprocess support). `os.environ.setdefault` would be a no-op
here because pytest-cov has already set ``COVERAGE_FILE`` to a
tmp dir by the time conftest is loaded — so we force-set.

See ``scitex_dev._skills.general.05_development_06_subprocess-coverage``.
"""
from __future__ import annotations

import os
import sysconfig
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Pin coverage's data file at the repo root and point process_startup
# at our pyproject so child interpreters configure themselves correctly.
os.environ["COVERAGE_PROCESS_START"] = str(_PROJECT_ROOT / "pyproject.toml")
os.environ["COVERAGE_FILE"] = str(_PROJECT_ROOT / ".coverage")


def _ensure_subprocess_coverage_shim() -> None:
    """Drop an idempotent ``.pth`` file in site-packages that auto-starts
    coverage in every child Python interpreter via
    ``coverage.process_startup()``.
    """
    purelib = Path(sysconfig.get_paths()["purelib"])
    pth = purelib / "_scitex_events_subprocess_coverage.pth"
    shim = (
        "import os, coverage\n"
        "if os.environ.get('COVERAGE_PROCESS_START'):\n"
        "    coverage.process_startup()\n"
    )
    try:
        if not pth.exists() or pth.read_text() != shim:
            pth.write_text(shim)
    except OSError:
        # site-packages may be read-only (e.g. system Python); silently
        # skip — local dev venvs are writable and that's where this matters.
        pass


_ensure_subprocess_coverage_shim()


@pytest.fixture
def env_save_restore():
    """Snapshot and restore ``os.environ`` mutations across a test.

    Replacement for the banned ``monkeypatch`` fixture (PA-306). Yields
    a callable that sets an env var; on teardown, every variable the
    fixture set is removed and any pre-existing value is restored.
    """
    saved: dict[str, str | None] = {}

    def _setenv(key: str, value: str) -> None:
        if key not in saved:
            saved[key] = os.environ.get(key)
        os.environ[key] = value

    try:
        yield _setenv
    finally:
        for key, prev in saved.items():
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev
