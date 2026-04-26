# scitex-events

General-purpose async event bus extracted from the [SciTeX](https://github.com/ywatanabe1989/scitex-python) ecosystem as a standalone, zero-dep package.

## Install

```bash
pip install scitex-events
```

## Usage

```python
import scitex_events as ev

# Emit
ev.emit("test_complete", project="figrecipe", status="success",
        payload={"exit_code": 0, "module": "stats"})

# Read latest event of a given type
ev.latest("test_complete")
# {"type": "test_complete", "project": "figrecipe", ...}

# Recent history
list(ev.history(limit=20))

# Schemas / introspection
ev.list_types()
ev.get_type_info("test_complete")
```

Events are stored locally as JSON-Lines files (override path via `SCITEX_EVENTS_DIR`)
and can optionally be forwarded to a cloud webhook.

## Status

Standalone fork of `scitex.events`. Pure stdlib — zero runtime deps. The
umbrella package's `scitex.events` import path is preserved via a
`sys.modules`-alias bridge so existing code continues to work.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).
