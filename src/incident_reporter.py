# src/incident_reporter.py

import csv
from datetime import datetime
import os

LOG_PATH = "logs/events.csv"
OUTPUT_PATH = "logs/incident_summary.txt"

def generate_summary():
    if not os.path.exists(LOG_PATH):
        print("No event log found.")
        return

    events = []
    with open(LOG_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append(row)

    if not events:
        print("Event log is empty.")
        return

    summary = {}
    for e in events:
        key = e["event_type"].lower()
        summary.setdefault(key, []).append(e)

    with open(OUTPUT_PATH, "w") as f:
        f.write(f"INCIDENT REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 40 + "\n")

        for category, entries in summary.items():
            icon = {
                "face": "🧑",
                "plate": "🚘",
                "behavior": "👀"
            }.get(category, "•")

            f.write(f"{icon} {category.title()} Events ({len(entries)}):\n")
            for e in entries:
                detail = f"    - {e['identifier']} | Confidence: {e['confidence']} | Time: {e['timestamp']}"
                f.write(detail + "\n")
            f.write("\n")

    print(f"✅ Incident summary written to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_summary()
