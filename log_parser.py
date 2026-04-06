#!/usr/bin/env python3

from collections import Counter
from datetime import datetime
import sys


def parse_log_file(filename):
    level_counts = Counter()
    error_messages = Counter()
    error_timestamps = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 2)
            if len(parts) < 3:
                continue

            ts_str, level, message = parts
            level_counts[level] += 1

            if level == "ERROR":
                error_messages[message] += 1
                try:
                    error_timestamps.append(datetime.fromisoformat(ts_str))
                except ValueError:
                    continue

    return level_counts, error_messages, error_timestamps


def detect_error_spike(timestamps, window_seconds=60, threshold=10):
    if not timestamps:
        return False

    timestamps.sort()
    left = 0

    for right in range(len(timestamps)):
        while (timestamps[right] - timestamps[left]).total_seconds() > window_seconds:
            left += 1

        if (right - left + 1) > threshold:
            return True

    return False


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "app.log"

    level_counts, error_messages, error_timestamps = parse_log_file(filename)

    print("=== Log Level Counts ===")
    print(f"INFO : {level_counts.get('INFO', 0)}")
    print(f"WARN : {level_counts.get('WARN', 0)}")
    print(f"ERROR: {level_counts.get('ERROR', 0)}")

    print("\n=== Top 5 Error Messages ===")
    for message, count in error_messages.most_common(5):
        print(f"{count}x - {message}")

    print("\n=== Error Spike Detection ===")
    if detect_error_spike(error_timestamps):
        print("⚠️  Detected more than 10 ERRORs within 60 seconds")
    else:
        print("No error spike detected")


if __name__ == "__main__":
    main()