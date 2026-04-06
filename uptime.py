from typing import Iterable


def uptime_percentage(total_minutes: int, downtimes: Iterable[int]) -> float:
    if total_minutes <= 0:
        raise ValueError("total_minutes must be greater than 0")

    total_downtime = 0

    for d in downtimes:
        if d < 0:
            raise ValueError("downtime values must be non-negative")
        total_downtime += d

    if total_downtime > total_minutes:
        total_downtime = total_minutes

    uptime = ((total_minutes - total_downtime) / total_minutes) * 100
    return round(uptime, 2)


def run_tests():
    print("=== Running uptime tests ===\n")

    # Test 1
    result = uptime_percentage(1440, [5, 10, 20])
    print("Test 1:", result, "✅" if result == 97.57 else "❌")

    # Test 2
    result = uptime_percentage(60, [0])
    print("Test 2:", result, "✅" if result == 100.0 else "❌")

    # Test 3
    result = uptime_percentage(60, [60])
    print("Test 3:", result, "✅" if result == 0.0 else "❌")

    # Test 4
    result = uptime_percentage(100, [10, 10])
    print("Test 4:", result, "✅" if result == 80.0 else "❌")

    # Test 5 (no downtime)
    result = uptime_percentage(100, [])
    print("Test 5:", result, "✅" if result == 100.0 else "❌")

    # Test 6 (downtime > total)
    result = uptime_percentage(100, [200])
    print("Test 6:", result, "✅" if result == 0.0 else "❌")

    # Test 7 (invalid total_minutes)
    try:
        uptime_percentage(0, [10])
        print("Test 7: ❌ (should fail)")
    except ValueError:
        print("Test 7: ✅ (caught error)")

    # Test 8 (negative downtime)
    try:
        uptime_percentage(100, [-5])
        print("Test 8: ❌ (should fail)")
    except ValueError:
        print("Test 8: ✅ (caught error)")


if __name__ == "__main__":
    run_tests()