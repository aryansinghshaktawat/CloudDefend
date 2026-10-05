from collections import defaultdict
from datetime import datetime, timedelta

THRESHOLD = 5
WINDOW_MINUTES = 10


def detect_ssh_bruteforce(events):
    alerts = []

    events_by_ip = defaultdict(list)

    for event in events:
        if event["type"] in {"failed_auth", "invalid_user"}:
            timestamp = datetime.fromisoformat(event["timestamp"])
            events_by_ip[event["ip"]].append((timestamp, event))

    for ip, ip_events in events_by_ip.items():
        ip_events.sort(key=lambda x: x[0])

        for i in range(len(ip_events)):
            window_start = ip_events[i][0]
            window_end = window_start + timedelta(minutes=WINDOW_MINUTES)

            window_events = [
                event
                for timestamp, event in ip_events[i:]
                if timestamp <= window_end
            ]

            if len(window_events) >= THRESHOLD:
                alerts.append({
                    "rule": "SSH_BRUTE_FORCE",
                    "severity": "HIGH",
                    "source_ip": ip,
                    "event_count": len(window_events),
                    "window_minutes": WINDOW_MINUTES,
                    "first_event": window_events[0]["timestamp"],
                    "last_event": window_events[-1]["timestamp"],
                })

                break

    return alerts
