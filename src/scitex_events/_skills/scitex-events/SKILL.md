---
name: scitex-events
description: General-purpose async event bus. Emit typed events (`scitex_events.emit("test_complete", project="...", status="success", payload={...})`) from any CLI/HPC/Python process; events persist as local state files under `<scitex_dir>/events/runtime/` and can be forwarded to a cloud webhook. Read with `latest(type)` or `history(limit=N)`. Schema-introspect with `list_types()` / `get_type_info(name)`. Drop-in replacement for ad-hoc JSON-line append loggers, scattered `print(json.dumps({...}))` status messages, and one-off webhook posts. Use whenever a pipeline step needs to record a structured outcome that another process (dashboard, scheduler, agent) reads later.
primary_interface: python
interfaces:
  python: 3
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 1
tags: [scitex-events, scitex-package, event-bus, async, telemetry]
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI ⭐ · Skills ⭐⭐ · HTTP ⭐

# scitex-events

Standalone async event bus for SciTeX. Zero-dep core; optional webhook
forwarder.

## Why

Pipelines and agents need to tell each other "X happened" — `print` is
not structured, log files are not queryable, and rolling your own JSON-
line append is the recipe everyone reinvents.

## Public API

```python
import scitex_events as ev

# Emit — type, then free-form kwargs + structured payload
ev.emit("test_complete", project="figrecipe",
        status="success", payload={"exit_code": 0, "module": "stats"})

# Read
ev.latest("test_complete")
list(ev.history(limit=20))
list(ev.history(type="test_complete", limit=20))

# Schema introspection
ev.list_types()
ev.get_type_info("test_complete")
```

Events persist under `local_state.runtime_path("events", ...)` and are
forwarded if `SCITEX_API_KEY` is set. Define types via `Event` for the
schema-driven flow.

## When to use

- ✅ Pipeline step succeeds/fails and a downstream agent needs to know
- ✅ HPC batch script broadcasting progress for late readers
- ❌ In-function return values — use return / raise
- ❌ High-frequency telemetry (>100 Hz) — this is on-disk JSON, not Kafka

## Pitfalls

- **Schemaless payloads** — define the type or document fields in the
  emitter docstring.
- **Polling `latest()` in a hot loop** — cache or use webhooks.
- **Hardcoding `~/.scitex/events/...`** — use `local_state.runtime_path`.

## See also

- `scitex-orochi` — agent message bus that consumes events
- `scitex-notification` — slack/email triggered by events
- General `01_arch_06_local-state-directories.md` — runtime path policy
