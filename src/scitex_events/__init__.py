#!/usr/bin/env python3
# Timestamp: 2026-02-14
# File: scitex/events/__init__.py

"""scitex-events — general-purpose async event bus (standalone).

Emit events from CLI, HPC, or any process. Events are stored locally
as state files and optionally forwarded to the cloud API via webhook.

Usage
-----
>>> from scitex_events import emit, latest
>>> emit("test_complete", project="figrecipe", status="success",
...      payload={"exit_code": 0, "module": "stats"})
>>> latest("test_complete")
{"type": "test_complete", "project": "figrecipe", ...}
"""

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("scitex-events")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"
from ._emit import emit, history, latest
from ._schema import Event
from ._types import get_type_info, list_types

__all__ = [
    "Event",
    "emit",
    "latest",
    "history",
    "list_types",
    "get_type_info",
]

# EOF
