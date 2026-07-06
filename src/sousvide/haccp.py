"""HACCP cook-safety check: was the temperature held at or above a threshold for long enough?

Pure function over readings (`t` in minutes, `temp_c`). Measures the longest CONTIGUOUS stretch at
or above `min_temp_c`; any dip below resets the clock.
"""


def cook_safety(readings, min_temp_c, hold_minutes):
    ordered = sorted(readings, key=lambda r: r["t"])
    longest = 0.0
    run_start = None
    for r in ordered:
        if r["temp_c"] >= min_temp_c:
            if run_start is None:
                run_start = r["t"]
            longest = max(longest, r["t"] - run_start)
        else:
            run_start = None
    return {
        "pass": longest >= hold_minutes,
        "held_minutes": longest,
        "required_minutes": hold_minutes,
        "min_temp_c": min_temp_c,
    }
