#!/usr/bin/env python3
"""Tests for scitex_events._schema (Event dataclass)."""

import pytest

from scitex_events._schema import Event


class TestEventDefaults:
    def test_minimal_construction_preserves_type_field(self):
        # Arrange
        type_value = "test_complete"
        # Act
        e = Event(type=type_value, project="myproj")
        # Assert
        assert e.type == type_value

    def test_minimal_construction_preserves_project_field(self):
        # Arrange
        project_value = "myproj"
        # Act
        e = Event(type="test_complete", project=project_value)
        # Assert
        assert e.project == project_value

    def test_minimal_construction_defaults_status_to_success(self):
        # Arrange
        # (no setup — defaults under test)
        # Act
        e = Event(type="test_complete", project="myproj")
        # Assert
        assert e.status == "success"

    def test_minimal_construction_defaults_source_to_local(self):
        # Arrange
        # (no setup — defaults under test)
        # Act
        e = Event(type="test_complete", project="myproj")
        # Assert
        assert e.source == "local"

    def test_minimal_construction_defaults_payload_to_empty_dict(self):
        # Arrange
        # (no setup — defaults under test)
        # Act
        e = Event(type="test_complete", project="myproj")
        # Assert
        assert e.payload == {}

    def test_timestamp_auto_generated_is_non_empty(self):
        # Arrange
        # (no setup — default factory under test)
        # Act
        e = Event(type="x", project="p")
        # Assert
        assert e.timestamp

    def test_timestamp_auto_generated_uses_iso_format(self):
        # Arrange
        # (no setup — default factory under test)
        # Act
        e = Event(type="x", project="p")
        # Assert
        # ISO 8601 contains a "T" between date and time
        assert "T" in e.timestamp

    def test_explicit_timestamp_is_preserved_verbatim(self):
        # Arrange
        explicit = "2026-05-01T12:00:00"
        # Act
        e = Event(type="x", project="p", timestamp=explicit)
        # Assert
        assert e.timestamp == explicit

    def test_payload_default_factory_isolates_instances(self):
        # Arrange
        a = Event(type="x", project="a")
        b = Event(type="x", project="b")
        # Act
        a.payload["k"] = "v"
        # Assert
        assert "k" not in b.payload  # default_factory wasn't shared


class TestSerialization:
    def test_to_dict_round_trip_preserves_full_schema(self):
        # Arrange
        e = Event(
            type="job_done",
            project="myproj",
            status="failure",
            payload={"exit_code": 1},
            source="hpc",
            timestamp="2026-05-01T10:30:00",
        )
        expected = {
            "type": "job_done",
            "project": "myproj",
            "status": "failure",
            "payload": {"exit_code": 1},
            "source": "hpc",
            "timestamp": "2026-05-01T10:30:00",
        }
        # Act
        d = e.to_dict()
        # Assert
        assert d == expected

    def test_from_dict_full_preserves_type_field(self):
        # Arrange
        d = {
            "type": "build_result",
            "project": "myproj",
            "status": "success",
            "payload": {"duration_s": 12.4},
            "source": "ci",
            "timestamp": "2026-05-01T11:00:00",
        }
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.type == "build_result"

    def test_from_dict_full_preserves_project_field(self):
        # Arrange
        d = {
            "type": "build_result",
            "project": "myproj",
            "status": "success",
            "payload": {"duration_s": 12.4},
            "source": "ci",
            "timestamp": "2026-05-01T11:00:00",
        }
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.project == "myproj"

    def test_from_dict_full_preserves_payload_field(self):
        # Arrange
        d = {
            "type": "build_result",
            "project": "myproj",
            "status": "success",
            "payload": {"duration_s": 12.4},
            "source": "ci",
            "timestamp": "2026-05-01T11:00:00",
        }
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.payload == {"duration_s": 12.4}

    def test_from_dict_full_preserves_source_field(self):
        # Arrange
        d = {
            "type": "build_result",
            "project": "myproj",
            "status": "success",
            "payload": {"duration_s": 12.4},
            "source": "ci",
            "timestamp": "2026-05-01T11:00:00",
        }
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.source == "ci"

    def test_from_dict_with_missing_optional_fields_preserves_type(self):
        # Arrange
        d = {"type": "x"}
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.type == "x"

    def test_from_dict_with_missing_optional_fields_defaults_project_empty(self):
        # Arrange
        d = {"type": "x"}
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.project == ""

    def test_from_dict_with_missing_optional_fields_defaults_status_unknown(self):
        # Arrange
        d = {"type": "x"}
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.status == "unknown"  # Event.from_dict uses unknown when omitted

    def test_from_dict_with_missing_optional_fields_defaults_source_local(self):
        # Arrange
        d = {"type": "x"}
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.source == "local"

    def test_from_dict_with_missing_optional_fields_defaults_payload_empty(self):
        # Arrange
        d = {"type": "x"}
        # Act
        e = Event.from_dict(d)
        # Assert
        assert e.payload == {}

    def test_from_dict_round_trip_equals_original_event(self):
        # Arrange
        original = Event(
            type="x",
            project="p",
            payload={"a": 1},
            timestamp="2026-05-01T00:00:00",
        )
        # Act
        round_tripped = Event.from_dict(original.to_dict())
        # Assert
        assert round_tripped == original


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
