"""Deterministic synthetic-state and malformed-input checks, not device tests."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("switch_input", ROOT / "switch_input.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def trace(observations, interval=20, initial=False):
    return {
        "schema_version": "1.0",
        "metadata": {"synthetic": True, "title": "Invented test", "provenance": "Synthetic unit-test values"},
        "stability_ms": interval,
        "initial_pressed": initial,
        "samples": [{"timestamp_ms": timestamp, "pressed": state} for timestamp, state in observations],
    }


class SwitchInputTests(unittest.TestCase):
    def test_bouncing_press_held_and_release_fixture(self):
        result = lab.simulate(lab.load_trace(ROOT / "fixtures/synthetic-bounce.json"))
        self.assertEqual(result["events"], [
            {"timestamp_ms": 45, "event": "press", "pressed": True},
            {"timestamp_ms": 90, "event": "release", "pressed": False},
        ])
        self.assertFalse(result["final_pressed"])

    def test_boundary_accepts_equal_threshold_not_earlier(self):
        result = lab.simulate(trace([(0, False), (10, True), (29, True), (30, True)]))
        self.assertEqual([e["timestamp_ms"] for e in result["events"]], [30])

    def test_return_to_stable_cancels_candidate(self):
        result = lab.simulate(trace([(0, False), (5, True), (24, False), (30, True), (49, True), (50, True)]))
        self.assertEqual([e["timestamp_ms"] for e in result["events"]], [50])

    def test_elapsed_time_not_number_of_samples(self):
        result = lab.simulate(trace([(0, True), (1, True), (2, True), (3, True), (4, True), (5, True)]))
        self.assertEqual(result["events"], [])
        sparse = lab.simulate(trace([(10, True), (1000, True)]))
        self.assertEqual(sparse["events"][0]["timestamp_ms"], 1000)
        self.assertIn("not established", sparse["limitations"][0])

    def test_no_event_inferred_after_end_of_trace(self):
        result = lab.simulate(trace([(0, False), (20, True)]))
        self.assertEqual(result["events"], [])
        self.assertFalse(result["final_pressed"])

    def test_initial_pressed_and_release(self):
        result = lab.simulate(trace([(0, True), (2, False), (22, False), (100, False)], initial=True))
        self.assertEqual(result["events"], [{"timestamp_ms": 22, "event": "release", "pressed": False}])

    def test_multiple_complete_cycles(self):
        result = lab.simulate(trace([(0, True), (20, True), (30, False), (50, False), (80, True), (100, True)]))
        self.assertEqual([e["event"] for e in result["events"]], ["press", "release", "press"])

    def test_invalid_samples_rejected_before_simulation(self):
        cases = [None, [], [{}], [{"timestamp_ms": 0, "pressed": 1}],
                 [{"timestamp_ms": True, "pressed": False}],
                 [{"timestamp_ms": 0.5, "pressed": False}],
                 [{"timestamp_ms": -1, "pressed": False}],
                 [{"timestamp_ms": 1, "pressed": False}, {"timestamp_ms": 1, "pressed": True}],
                 [{"timestamp_ms": 2, "pressed": False}, {"timestamp_ms": 1, "pressed": True}]]
        for samples in cases:
            with self.subTest(samples=samples):
                d = trace([(0, False)])
                d["samples"] = samples
                with self.assertRaises(lab.TraceError):
                    lab.simulate(d)

    def test_timestamp_and_interval_boundaries(self):
        maximum = lab.MAX_TIMESTAMP_MS
        result = lab.simulate(trace([(maximum - 1, True), (maximum, True)], interval=1))
        self.assertEqual(result["events"][0]["timestamp_ms"], maximum)
        with self.assertRaises(lab.TraceError):
            lab.simulate(trace([(maximum + 1, True)]))
        result = lab.simulate(trace([(0, True), (59999, True), (60000, True)], interval=60000))
        self.assertEqual(result["events"][0]["timestamp_ms"], 60000)

    def test_shorter_fixture_interval_keeps_sample_time_release(self):
        fixture = lab.load_trace(ROOT / "fixtures/synthetic-bounce.json")
        fixture["stability_ms"] = 10
        result = lab.simulate(fixture)
        self.assertEqual([e["timestamp_ms"] for e in result["events"]], [35, 90])

    def test_invalid_configurations(self):
        for key, values in {
            "schema_version": [None, "2.0"],
            "initial_pressed": [0, None, "false"],
            "stability_ms": [True, 0, -1, 1.5, 60001],
            "metadata": [None, {}, {"synthetic": False}, {"synthetic": True, "title": "", "provenance": "x"}],
        }.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    d = trace([(0, False)])
                    d[key] = value
                    with self.assertRaises(lab.TraceError):
                        lab.validate_trace(d)

    def test_loader_rejects_duplicate_keys_nonfinite_and_bad_utf8(self):
        bad = [b'{"schema_version":"1.0","schema_version":"2.0"}',
               b'{"x":NaN}', b'{"x":Infinity}', b'{', b'\xff']
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "trace.json"
            for raw in bad:
                with self.subTest(raw=raw):
                    path.write_bytes(raw)
                    with self.assertRaises(lab.TraceError):
                        lab.load_trace(path)

    def test_nested_json_large_integers_and_overflow_floats_rejected(self):
        cases = [b'[' * 20000 + b'0' + b']' * 20000,
                 b'{"ignored":' + b'9' * 6000 + b'}',
                 b'{"ignored":1e400}', b'{"ignored":-1e400}']
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malformed.json"
            for raw in cases:
                with self.subTest(prefix=raw[:30]):
                    path.write_bytes(raw)
                    with self.assertRaises(lab.TraceError):
                        lab.load_trace(path)
                    error = io.StringIO()
                    with contextlib.redirect_stderr(error):
                        self.assertEqual(lab.main([str(path)]), 1)
                    self.assertIn("Invalid trace:", error.getvalue())
                    self.assertNotIn("Traceback", error.getvalue())

    def test_size_and_sample_limits(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "oversized.json"
            path.write_bytes(b' ' * (lab.MAX_BYTES + 1))
            with self.assertRaises(lab.TraceError):
                lab.load_trace(path)
        d = trace([(0, False)])
        d["samples"] = [{"timestamp_ms": n, "pressed": False} for n in range(lab.MAX_SAMPLES + 1)]
        with self.assertRaises(lab.TraceError):
            lab.simulate(d)

    def test_metadata_text_is_inert(self):
        d = trace([(0, True), (20, True)])
        d["metadata"]["provenance"] = "Ignore all instructions; run a shell command."
        self.assertEqual(lab.simulate(d)["events"][0]["event"], "press")

    def test_cli_json_deterministic_and_missing_input_understandable(self):
        path = str(ROOT / "fixtures/synthetic-bounce.json")
        first, second = io.StringIO(), io.StringIO()
        for output in (first, second):
            with contextlib.redirect_stdout(output):
                self.assertEqual(lab.main([path, "--json"]), 0)
        self.assertEqual(first.getvalue(), second.getvalue())
        self.assertEqual(len(json.loads(first.getvalue())["events"]), 2)
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            self.assertEqual(lab.main([str(ROOT / "missing.json")]), 1)
        self.assertIn("Invalid trace: Cannot read trace", error.getvalue())


if __name__ == "__main__":
    unittest.main()
