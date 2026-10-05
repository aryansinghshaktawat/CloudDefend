import subprocess
import re
from collections import Counter
from datetime import datetime


def get_ssh_logs():
    command = [
        "sudo",
        "journalctl",
        "-u",
        "ssh",
        "--since",
        "1 hour ago",
        "--no-pager",
        "-o",
        "short-iso",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.splitlines()


def parse_event(line):
    # Extract timestamp from journalctl short-iso output.
    timestamp_match = re.match(
        r"^(\S+)",
        line,
    )

    if not timestamp_match:
        return None

    timestamp = timestamp_match.group(1)

    # Invalid user <username> from <IP>
    match = re.search(
        r"Invalid user\s*(\S*)\s+from\s+(\d+\.\d+\.\d+\.\d+)",
        line,
    )

    if match:
        username = match.group(1) or "unknown"
        ip = match.group(2)

        return {
            "timestamp": timestamp,
            "ip": ip,
            "username": username,
            "type": "invalid_user",
        }

    # Connection reset/closed by authenticating user <username> <IP>
    match = re.search(
        r"Connection (?:reset|closed) by authenticating user\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)",
        line,
    )

    if match:
        username = match.group(1)
        ip = match.group(2)

        return {
            "timestamp": timestamp,
            "ip": ip,
            "username": username,
            "type": "failed_auth",
        }

    return None


def main():
    lines = get_ssh_logs()

    events = []

    for line in lines:
        event = parse_event(line)

        if event:
            events.append(event)

    print(f"Suspicious SSH events: {len(events)}")
    print()

    counts = Counter(event["ip"] for event in events)

    print("Events by source IP:")
    print("-" * 40)

    for ip, count in counts.most_common():
        print(f"{ip:20} {count}")


if __name__ == "__main__":
    main()
