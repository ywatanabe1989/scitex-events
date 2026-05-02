# scitex-events

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Zero-dep async event bus for the SciTeX ecosystem.</b></p>

<p align="center">
  <a href="https://scitex-events.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-events</code>
</p>

<!-- scitex-badges:start -->
<p align="center">
  <a href="https://pypi.org/project/scitex-events/"><img src="https://img.shields.io/pypi/v/scitex-events.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/scitex-events/"><img src="https://img.shields.io/pypi/pyversions/scitex-events.svg" alt="Python"></a>
  <a href="https://github.com/ywatanabe1989/scitex-events/actions/workflows/test.yml"><img src="https://github.com/ywatanabe1989/scitex-events/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="https://github.com/ywatanabe1989/scitex-events/actions/workflows/install-test.yml"><img src="https://github.com/ywatanabe1989/scitex-events/actions/workflows/install-test.yml/badge.svg" alt="Install Test"></a>
  <a href="https://codecov.io/gh/ywatanabe1989/scitex-events"><img src="https://codecov.io/gh/ywatanabe1989/scitex-events/graph/badge.svg" alt="Coverage"></a>
  <a href="https://scitex-events.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/scitex-events/badge/?version=latest" alt="Docs"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/license-AGPL_v3-blue.svg" alt="License: AGPL v3"></a>
</p>
<!-- scitex-badges:end -->

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

<details open>
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
`scitex.events` (Python) or `scitex events ...` (CLI).

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
