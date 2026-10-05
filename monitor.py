import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, "/home/azureuser/clouddefend/agent")
sys.path.insert(0, "/home/azureuser/clouddefend/rules")

from ssh_detector import get_ssh_logs, parse_event
from ssh_rules import detect_ssh_bruteforce

ALERT_FILE = Path("/home/azureuser/clouddefend/logs/alerts.json")


def load_alerts():
    try:
        return json.loads(ALERT_FILE.read_text())
    except Exception:
        return []


def save_alert(alert):
    alerts = load_alerts()
    alerts.append(alert)
    ALERT_FILE.write_text(json.dumps(alerts, indent=2))


def process():
    events = []

    for line in get_ssh_logs():
        event = parse_event(line)

        if event:
            events.append(event)

    alerts = detect_ssh_bruteforce(events)

    existing = load_alerts()

    for alert in alerts:
        key = (
            alert["rule"],
            alert["source_ip"],
            alert["first_event"],
        )

        duplicate = any(
            (
                a.get("rule"),
                a.get("source_ip"),
                a.get("first_event"),
            ) == key
            for a in existing
        )

        if not duplicate:
            alert["id"] = len(existing) + 1
            alert["detected_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            save_alert(alert)

            print(
                f"[ALERT] {alert['severity']} "
                f"{alert['rule']} "
                f"{alert['source_ip']}"
            )


if __name__ == "__main__":
    print("CloudDefend monitor started")

    while True:
        try:
            process()
            time.sleep(30)

        except KeyboardInterrupt:
            print("\nCloudDefend monitor stopped")
            break

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(30)
