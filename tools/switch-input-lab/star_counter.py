#!/usr/bin/env python3
"""One press, one star: a text-only programming exercise, not a device driver."""
import argparse
import json
import sys

from switch_input import TraceError, load_trace, report_trace_error, simulate


def collect_stars(trace, stars_per_press=1):
    """Count confirmed press events, not every raw pressed observation."""
    if type(stars_per_press) is not int or not 1 <= stars_per_press <= 100:
        raise TraceError("stars_per_press must be an integer from 1 to 100")
    result = simulate(trace)
    stars = 0
    collections = []
    for event in result["events"]:
        if event["event"] == "press":
            stars = stars + stars_per_press
            collections.append({"timestamp_ms": event["timestamp_ms"], "stars": stars})
    return {
        "schema_version": "1.0",
        "synthetic": True,
        "stars_per_press": stars_per_press,
        "stars": stars,
        "collections": collections,
        "input_events": result["events"],
        "limitations": result["limitations"] + [
            "Stars are invented game points; no real device, person, or outcome is modeled."
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", help="Path to a synthetic JSON trace")
    parser.add_argument("--stars-per-press", type=int, default=1,
                        help="Points awarded per confirmed press, from 1 to 100 (default 1)")
    parser.add_argument("--json", action="store_true", help="Print the deterministic result as JSON")
    args = parser.parse_args(argv)
    try:
        result = collect_stars(load_trace(args.trace), args.stars_per_press)
    except TraceError as exc:
        report_trace_error(exc)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))
    else:
        print("One press, one star: synthetic text-only game")
        for collection in result["collections"]:
            print(f"{collection['timestamp_ms']} ms: total stars = {collection['stars']}")
        print(f"Final stars: {result['stars']}")
        print("Only confirmed sampled press events award points; releases and held states do not.")
        print("Educational simulation; no hardware or clinical validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
