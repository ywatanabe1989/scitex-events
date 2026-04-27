"""Quickstart for scitex_events.

Emit a couple of events, then read them back from history.
"""

import scitex_events as se


def main() -> int:
    se.emit(
        event_type="test_complete",
        project="scitex-events-quickstart",
        status="success",
        payload={"passed": 42, "failed": 0, "duration_s": 3.14},
        source="local",
    )
    se.emit(
        event_type="bench_complete",
        project="scitex-events-quickstart",
        status="success",
        payload={"throughput_mbps": 128.5},
        source="local",
    )

    # Inspect known event types and recent history
    print("Known event types:", se.list_types())

    recent = se.history(limit=5)
    print(f"Last {len(recent)} events:")
    for ev in recent:
        print(
            f"  {ev.get('timestamp', '?')} "
            f"{ev.get('type', '?'):<20} "
            f"project={ev.get('project', '?'):<30} "
            f"status={ev.get('status', '?')}"
        )

    # Get the latest event for our project / type explicitly
    latest = se.latest("test_complete")
    if latest is not None:
        print("Latest test_complete payload:", latest.get("payload"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
