#!/usr/bin/env python3
"""Tests for scitex_events._schema (Event dataclass)."""

import pytest

from scitex_events._schema import Event


class TestEventDefaults:
    def test_minimal_construction(self):
        e = Event(type="test_complete", project="myproj")
        assert e.type == "test_complete"
        assert e.project == "myproj"
        assert e.status == "success"
        assert e.source == "local"
        assert e.payload == {}

    def test_timestamp_auto_generated(self):
        e = Event(type="x", project="p")
        assert e.timestamp  # non-empty
        # ISO 8601 contains a "T" between date and time
        assert "T" in e.timestamp

    def test_explicit_timestamp_preserved(self):
        e = Event(type="x", project="p", timestamp="2026-05-01T12:00:00")
        assert e.timestamp == "2026-05-01T12:00:00"

    def test_payload_isolation_between_instances(self):
        a = Event(type="x", project="a")
        b = Event(type="x", project="b")
        a.payload["k"] = "v"
        assert "k" not in b.payload  # default_factory wasn't shared


class TestSerialization:
    def test_to_dict_round_trip(self):
        e = Event(
            type="job_done",
            project="myproj",
            status="failure",
            payload={"exit_code": 1},
            source="hpc",
            timestamp="2026-05-01T10:30:00",
        )
        d = e.to_dict()
        assert d == {
            "type": "job_done",
            "project": "myproj",
            "status": "failure",
            "payload": {"exit_code": 1},
            "source": "hpc",
            "timestamp": "2026-05-01T10:30:00",
        }

    def test_from_dict_full(self):
        d = {
            "type": "build_result",
            "project": "myproj",
            "status": "success",
            "payload": {"duration_s": 12.4},
            "source": "ci",
            "timestamp": "2026-05-01T11:00:00",
        }
        e = Event.from_dict(d)
        assert e.type == "build_result"
        assert e.project == "myproj"
        assert e.payload == {"duration_s": 12.4}
        assert e.source == "ci"

    def test_from_dict_with_missing_optional_fields_uses_defaults(self):
        e = Event.from_dict({"type": "x"})
        assert e.type == "x"
        assert e.project == ""
        assert e.status == "unknown"  # Event.from_dict uses unknown when omitted
        assert e.source == "local"
        assert e.payload == {}

    def test_from_dict_round_trip(self):
        original = Event(
            type="x",
            project="p",
            payload={"a": 1},
            timestamp="2026-05-01T00:00:00",
        )
        round_tripped = Event.from_dict(original.to_dict())
        assert round_tripped == original


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
