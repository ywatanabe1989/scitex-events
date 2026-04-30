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
canonical-location: scitex-events/src/scitex_events/_skills/scitex-events/SKILL.md
tags: [scitex-events, scitex-package, event-bus, async, telemetry]
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP ⭐

# scitex-events

Standalone async event bus for the SciTeX ecosystem. Zero-dep at the
core; optional webhook forwarder for cloud relay.

## Why an event bus

Pipelines and agents need to tell each other "X happened" — `print` is
not structured, log files are not queryable, and rolling your own JSON-
line append is the recipe everyone reinvents. `scitex_events` gives you
typed events with schema validation, on-disk persistence under
`$SCITEX_DIR/events/runtime/`, and a one-line read API.

## Public API

### Emit

```python
import scitex_events as ev

ev.emit(
    "test_complete",
    project="figrecipe",
    status="success",
    payload={"exit_code": 0, "module": "stats"},
)
```

The first positional arg is the event type (string). Free-form kwargs
become top-level fields; `payload=` is for nested structured data. The
event is persisted immediately and (if configured) forwarded.

### Read

```python
ev.latest("test_complete")
# {"type": "test_complete", "project": "figrecipe",
#  "status": "success", "ts": "2026-04-28T...", ...}

list(ev.history(limit=20))                          # most recent across types
list(ev.history(type="test_complete", limit=20))    # filtered
```

### Schema introspection

```python
ev.list_types()                       # ["test_complete", "agent_handoff", ...]
ev.get_type_info("test_complete")     # required fields, payload schema
```

Define types via `Event` (from `scitex_events`) for the schema-driven
flow.

## When to use

- ✅ A pipeline step succeeds/fails and a downstream agent or dashboard
  needs to know
- ✅ HPC batch script wants to broadcast progress without printing to a
  log file no one reads
- ✅ Cross-process communication where you need durability + late
  readers (vs. an in-memory queue)
- ❌ Per-call return values inside a single function — use return / raise
- ❌ High-frequency telemetry (>100 Hz) — this is on-disk JSON, not Kafka

## Local state

Events live under
`local_state.runtime_path("events", ...)` (i.e.
`$SCITEX_DIR/events/runtime/`) per the canonical local-state policy.
Rotation/cleanup is the consumer's responsibility — read and trim.

## Common mistakes

- **Treating event payloads as schemaless.** Always either define the
  type up-front or document the field set in the docstring of the
  emitter.
- **Polling `latest()` in a hot loop.** It re-reads disk; cache or use
  webhooks.
- **Hardcoding `~/.scitex/events/...`.** Use `local_state.runtime_path`
  so `$SCITEX_DIR` and project-scope overrides work.

## See also

- `scitex-orochi` — agent message bus that consumes `scitex-events`
- `scitex-notification` — outbound notifications (slack/email) often
  triggered by events
- General skill `01_arch_06_local-state-directories.md` — the canonical
  `<scitex_dir>/<pkg-short>/runtime/` layout
