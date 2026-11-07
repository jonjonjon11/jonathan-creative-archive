#!/usr/bin/env python3
"""Educational sampled-switch debouncer. No hardware, network, or device control."""
import argparse
import json
import math
from pathlib import Path
import sys

MAX_BYTES = 2 * 1024 * 1024
MAX_SAMPLES = 10_000
MAX_TIMESTAMP_MS = 2**53 - 1


class TraceError(ValueError):
    """A trace cannot be interpreted under the supported educational format."""


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise TraceError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise TraceError(f"Non-finite JSON number is unsupported: {value}")


def _integer(value):
    # Bound before int() so Python versions with different digit limits agree.
    if len(value.lstrip("-")) > 32:
        raise TraceError("JSON integer exceeds the 32-digit parsing limit")
    return int(value)


def _float(value):
    result = float(value)
    if not math.isfinite(result):
        raise TraceError("Non-finite JSON number is unsupported")
    return result


def validate_trace(trace):
    """Check the complete trace before calculating any events."""
    if not isinstance(trace, dict):
        raise TraceError("Trace must be a JSON object")
    if trace.get("schema_version") != "1.0":
        raise TraceError("Unsupported schema_version; expected '1.0'")
    metadata = trace.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("synthetic") is not True:
        raise TraceError("metadata.synthetic must be true; this lab accepts invented examples only")
    for name in ("title", "provenance"):
        if not isinstance(metadata.get(name), str) or not metadata[name].strip():
            raise TraceError(f"metadata.{name} must be nonempty text")
    interval = trace.get("stability_ms")
    if type(interval) is not int or not 1 <= interval <= 60_000:
        raise TraceError("stability_ms must be an integer from 1 to 60000")
    if type(trace.get("initial_pressed")) is not bool:
        raise TraceError("initial_pressed must be a boolean")
    samples = trace.get("samples")
    if not isinstance(samples, list) or not 1 <= len(samples) <= MAX_SAMPLES:
        raise TraceError(f"samples must contain 1 to {MAX_SAMPLES} observations")
    previous = -1
    for index, sample in enumerate(samples):
        if not isinstance(sample, dict):
            raise TraceError(f"samples[{index}] must be an object")
        timestamp = sample.get("timestamp_ms")
        if type(timestamp) is not int or not 0 <= timestamp <= MAX_TIMESTAMP_MS:
            raise TraceError(f"samples[{index}].timestamp_ms must be a nonnegative integer <= {MAX_TIMESTAMP_MS}")
        if timestamp <= previous:
            raise TraceError(f"samples[{index}].timestamp_ms must be strictly increasing")
        if type(sample.get("pressed")) is not bool:
            raise TraceError(f"samples[{index}].pressed must be a boolean")
        previous = timestamp
    return trace


def load_trace(path):
    """Read bounded UTF-8 JSON. File content is data and is never executed."""
    try:
        with Path(path).open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise TraceError(f"Trace exceeds {MAX_BYTES} bytes")
        trace = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant,
                           parse_int=_integer, parse_float=_float)
    except TraceError:
        raise
    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise TraceError(f"Cannot read trace: {exc}") from exc
    return validate_trace(trace)


def simulate(trace):
    """Emit changes at confirming sample times, using elapsed milliseconds.

    Opposite-state observations start a candidate. Returning to the accepted
    state cancels it. A later observation of the candidate at >= stability_ms
    accepts the change. Unobserved intervals are unknown, not proven stable.
    """
    validate_trace(trace)
    stable = trace["initial_pressed"]
    interval = trace["stability_ms"]
    candidate_since = None
    events = []
    for sample in trace["samples"]:
        timestamp, pressed = sample["timestamp_ms"], sample["pressed"]
        if pressed == stable:
            candidate_since = None
        elif candidate_since is None:
            candidate_since = timestamp
        elif timestamp - candidate_since >= interval:
            stable = pressed
            events.append({"timestamp_ms": timestamp, "event": "press" if stable else "release", "pressed": stable})
            candidate_since = None
    return {
        "schema_version": "1.0",
        "synthetic": True,
        "stability_ms": interval,
        "initial_pressed": trace["initial_pressed"],
        "sample_count": len(trace["samples"]),
        "final_pressed": stable,
        "events": events,
        "limitations": [
            "Only sampled observations are known; physical stability between samples is not established.",
            "No event is predicted after the last sample, including an unfinished candidate.",
            "Educational synthetic simulation; no hardware or clinical suitability is established.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", help="Path to a synthetic JSON trace")
    parser.add_argument("--json", action="store_true", help="Print the complete deterministic result as JSON")
    args = parser.parse_args(argv)
    try:
        result = simulate(load_trace(args.trace))
    except TraceError as exc:
        print(f"Invalid trace: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print(f"Synthetic trace: {result['sample_count']} samples; stability interval {result['stability_ms']} ms")
        for event in result["events"]:
            print(f"{event['timestamp_ms']} ms: {event['event']}")
        if not result["events"]:
            print("No confirmed state changes.")
        print("Only sample-time observations are modeled; unobserved intervals remain unknown.")
        print("Educational simulation; no hardware or clinical validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
