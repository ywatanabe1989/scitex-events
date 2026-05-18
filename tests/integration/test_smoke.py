"""Smoke tests for scitex-events public API."""

import scitex_events as ev


def test_emit_export_is_callable():
    # Arrange
    fn = ev.emit
    # Act
    is_callable = callable(fn)
    # Assert
    assert is_callable


def test_latest_export_is_callable():
    # Arrange
    fn = ev.latest
    # Act
    is_callable = callable(fn)
    # Assert
    assert is_callable


def test_history_export_is_callable():
    # Arrange
    fn = ev.history
    # Act
    is_callable = callable(fn)
    # Assert
    assert is_callable


def test_list_types_export_is_callable():
    # Arrange
    fn = ev.list_types
    # Act
    is_callable = callable(fn)
    # Assert
    assert is_callable


def test_get_type_info_export_is_callable():
    # Arrange
    fn = ev.get_type_info
    # Act
    is_callable = callable(fn)
    # Assert
    assert is_callable


def test_event_dataclass_preserves_type_field():
    # Arrange
    type_value = "x"
    # Act
    e = ev.Event(type=type_value, project="y", status="success")
    # Assert
    assert e.type == type_value


def test_event_dataclass_preserves_project_field():
    # Arrange
    project_value = "y"
    # Act
    e = ev.Event(type="x", project=project_value, status="success")
    # Assert
    assert e.project == project_value


def test_event_dataclass_preserves_status_field():
    # Arrange
    status_value = "success"
    # Act
    e = ev.Event(type="x", project="y", status=status_value)
    # Assert
    assert e.status == status_value


def test_emit_then_latest_returns_event_with_matching_type(tmp_path, env_save_restore):
    # Arrange
    env_save_restore("SCITEX_DIR", str(tmp_path))
    ev.emit("smoke_event_type", project="proj", status="success", payload={"k": 1})
    # Act
    last = ev.latest("smoke_event_type")
    # Assert
    assert last is not None and last["type"] == "smoke_event_type"


def test_emit_then_latest_returns_event_with_matching_project(tmp_path, env_save_restore):
    # Arrange
    env_save_restore("SCITEX_DIR", str(tmp_path))
    ev.emit("smoke_event_project", project="proj", status="success", payload={"k": 1})
    # Act
    last = ev.latest("smoke_event_project")
    # Assert
    assert last is not None and last["project"] == "proj"


def test_emit_then_latest_returns_event_with_matching_payload(tmp_path, env_save_restore):
    # Arrange
    env_save_restore("SCITEX_DIR", str(tmp_path))
    ev.emit("smoke_event_payload", project="proj", status="success", payload={"k": 1})
    # Act
    last = ev.latest("smoke_event_payload")
    # Assert
    assert last is not None and last["payload"] == {"k": 1}


def test_history_returns_recent_emitted_events(tmp_path, env_save_restore):
    # Arrange
    env_save_restore("SCITEX_DIR", str(tmp_path))
    ev.emit("hist_event_type_a", project="p", status="success")
    ev.emit("hist_event_type_a", project="p", status="success")
    # Act
    items = list(ev.history(limit=20))
    # Assert
    assert len(items) >= 2


def test_list_types_returns_list_or_tuple():
    # Arrange
    # (no setup needed)
    # Act
    types = ev.list_types()
    # Assert
    assert isinstance(types, (list, tuple))


import pytest as _pytest

_REGISTERED_TYPES = ev.list_types()


@_pytest.mark.skipif(
    not _REGISTERED_TYPES, reason="no registered event types to inspect"
)
def test_get_type_info_returns_non_none_for_known_type():
    # Arrange
    known_type = _REGISTERED_TYPES[0] if _REGISTERED_TYPES else ""
    # Act
    info = ev.get_type_info(known_type)
    # Assert
    assert info is not None
