# scitex-events

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-events.svg)](https://pypi.org/project/scitex-events/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-events.svg)](https://pypi.org/project/scitex-events/)
[![Tests](https://github.com/ywatanabe1989/scitex-events/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-events/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-events/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-events/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-events/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-events)
[![Docs](https://readthedocs.org/projects/scitex-events/badge/?version=latest)](https://scitex-events.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Zero-dep async event bus for the SciTeX ecosystem.</b></p>

<p align="center">
  <a href="https://scitex-events.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-events</code>
</p>

---

## Installation

```bash
pip install scitex-events
```

## Quick Start

```python
import scitex_events as ev

ev.emit("test_complete", project="figrecipe", status="success",
        payload={"exit_code": 0, "module": "stats"})

ev.latest("test_complete")     # most recent event of this type
list(ev.history(limit=20))     # recent history
```

## 1 Interfaces

<details>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_events as ev

# Emit an event (any kwargs become payload fields).
ev.emit("test_complete", project="figrecipe", status="success",
        payload={"exit_code": 0, "module": "stats"})

# Latest event of a given type.
ev.latest("test_complete")

# Recent history (newest first).
list(ev.history(limit=20))

# Schemas / introspection.
ev.list_types()
ev.get_type_info("test_complete")
```

Events are stored locally as JSON-Lines files (override path via `SCITEX_EVENTS_DIR`)
and can optionally be forwarded to a cloud webhook.

</details>

## Status

Standalone fork of `scitex.events`. Pure stdlib — zero runtime deps. The
umbrella package's `scitex.events` import path is preserved via a
`sys.modules`-alias bridge so existing code continues to work.

## Part of SciTeX

`scitex-events` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[events]` to use as
`scitex.events` (Python).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
