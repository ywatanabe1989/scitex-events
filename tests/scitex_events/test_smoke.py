"""Smoke tests for scitex-events public API."""

import scitex_events as ev


def test_exports_are_callable():
    assert callable(ev.emit)
    assert callable(ev.latest)
    assert callable(ev.history)
    assert callable(ev.list_types)
    assert callable(ev.get_type_info)


def test_event_dataclass():
    e = ev.Event(type="x", project="y", status="success")
    assert e.type == "x"
    assert e.project == "y"
    assert e.status == "success"


def test_emit_and_latest_roundtrip(tmp_path, monkeypatch):
    # Direct event store at tmp_path so test is hermetic
    monkeypatch.setenv("SCITEX_EVENTS_DIR", str(tmp_path))
    ev.emit("smoke_event", project="proj", status="success", payload={"k": 1})
    last = ev.latest("smoke_event")
    assert last is not None
    assert last["type"] == "smoke_event"
    assert last["project"] == "proj"
    assert last["payload"] == {"k": 1}


def test_history(tmp_path, monkeypatch):
    monkeypatch.setenv("SCITEX_EVENTS_DIR", str(tmp_path))
    ev.emit("hist_event", project="p", status="success")
    ev.emit("hist_event", project="p", status="success")
    items = list(ev.history(limit=20))
    assert len(items) >= 2


def test_list_types_and_get_type_info():
    types = ev.list_types()
    assert isinstance(types, (list, tuple))
    if types:
        info = ev.get_type_info(types[0])
        assert info is not None
