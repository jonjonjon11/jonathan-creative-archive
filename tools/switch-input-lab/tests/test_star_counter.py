"""Exercise/model parity and CLI regressions; no hardware or learner tests."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import star_counter as game
import switch_input as lab


def trace(observations, initial=False):
    return {
        "schema_version": "1.0",
        "metadata": {"synthetic": True, "title": "Invented test", "provenance": "Synthetic unit test"},
        "initial_pressed": initial,
        "stability_ms": 20,
        "samples": [{"timestamp_ms": t, "pressed": p} for t, p in observations],
    }


class StarCounterTests(unittest.TestCase):
    def test_bouncing_held_and_second_press(self):
        result = game.collect_stars(lab.load_trace(ROOT / "fixtures/synthetic-two-presses.json"))
        self.assertEqual(result["stars"], 2)
        self.assertEqual(result["collections"], [{"timestamp_ms": 45, "stars": 1},
                                                {"timestamp_ms": 150, "stars": 2}])
        self.assertEqual([(e["timestamp_ms"], e["event"]) for e in result["input_events"]],
                         [(45, "press"), (90, "release"), (150, "press"), (210, "release")])

    def test_held_button_does_not_repeat(self):
        result = game.collect_stars(trace([(0, True), (20, True), (30, True), (1000, True)]))
        self.assertEqual(result["stars"], 1)

    def test_unfinished_press_and_initially_held_do_not_award(self):
        self.assertEqual(game.collect_stars(trace([(0, False), (20, True)]))["stars"], 0)
        self.assertEqual(game.collect_stars(trace([(0, True), (20, True)], initial=True))["stars"], 0)
        self.assertEqual(game.collect_stars(trace([(0, False), (20, False)], initial=True))["stars"], 0)

    def test_initially_held_then_released_and_pressed(self):
        result = game.collect_stars(trace([(0, False), (20, False), (30, True), (50, True)], initial=True))
        self.assertEqual(result["collections"], [{"timestamp_ms": 50, "stars": 1}])

    def test_double_reward_changes_points_not_event_times(self):
        fixture = lab.load_trace(ROOT / "fixtures/synthetic-two-presses.json")
        result = game.collect_stars(fixture, stars_per_press=2)
        self.assertEqual(result["stars"], 4)
        self.assertEqual(result["collections"], [{"timestamp_ms": 45, "stars": 2},
                                                {"timestamp_ms": 150, "stars": 4}])
        self.assertEqual(fixture, lab.load_trace(ROOT / "fixtures/synthetic-two-presses.json"))

    def test_reward_bounds_and_type(self):
        for value in [True, False, 0, -1, 101, 1.5, "2", None]:
            with self.subTest(value=value), self.assertRaises(lab.TraceError):
                game.collect_stars(trace([(0, True), (20, True)]), value)
        self.assertEqual(game.collect_stars(trace([(0, True), (20, True)]), 100)["stars"], 100)

    def test_sparse_sample_pair_cannot_prove_continuity(self):
        sparse = trace([(10, True), (1000, True)])
        hidden_release = trace([(10, True), (500, False), (1000, True)])
        self.assertEqual(game.collect_stars(sparse)["stars"], 1)
        self.assertEqual(game.collect_stars(hidden_release)["stars"], 0)
        self.assertIn("not established", game.collect_stars(sparse)["limitations"][0])

    def test_unconfirmed_release_does_not_rearm(self):
        observations = [(0, True), (20, True), (30, False), (35, True), (55, True)]
        self.assertEqual(game.collect_stars(trace(observations))["stars"], 1)

    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, "-B", str(ROOT / "star_counter.py"), *map(str, args)],
                              capture_output=True, text=True, cwd=cwd, check=False)

    def test_cli_documented_output_and_json_from_other_directory(self):
        fixture = ROOT / "fixtures/synthetic-two-presses.json"
        result = self.run_cli(fixture, cwd=ROOT.parent)
        expected = ("One press, one star: synthetic text-only game\n"
                    "45 ms: total stars = 1\n150 ms: total stars = 2\nFinal stars: 2\n"
                    "Only confirmed sampled press events award points; releases and held states do not.\n"
                    "Educational simulation; no hardware or clinical validation.\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, expected)
        lesson = (ROOT.parents[1] / "docs/lessons/one-press-one-star.md").read_text(encoding="utf-8")
        self.assertIn("```text\n" + expected + "```", lesson)
        first = self.run_cli(fixture, "--json")
        second = self.run_cli(fixture, "--json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["stars"], 2)
        doubled = self.run_cli(fixture, "--stars-per-press", 2, "--json")
        self.assertEqual(doubled.returncode, 0, doubled.stderr)
        self.assertEqual(json.loads(doubled.stdout)["stars"], 4)

    def test_cli_errors_are_nonzero_without_game_output(self):
        for args, code in [([], 2), ([ROOT / "missing.json"], 1),
                           ([ROOT / "fixtures/synthetic-bounce.json", "--stars-per-press", 0], 1),
                           ([ROOT / "fixtures/synthetic-bounce.json", "--stars-per-press", "abc"], 2)]:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, code)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_surrogate_duplicate_key_and_control_diagnostics(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text('{"\\ud800\\n":1,"\\ud800\\n":2}', encoding="utf-8")
            env = dict(os.environ, PYTHONIOENCODING="ascii:strict")
            for script in ["switch_input.py", "star_counter.py"]:
                result = subprocess.run([sys.executable, "-B", str(ROOT / script), str(path)],
                                        capture_output=True, text=True, env=env, check=False)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("Invalid trace: Duplicate JSON key:", result.stderr)
                self.assertIn(r"\ud800\n", result.stderr)
                self.assertEqual(len(result.stderr.splitlines()), 1)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_lesson_table_and_loop_match_fixture_and_code(self):
        lesson = (ROOT.parents[1] / "docs/lessons/one-press-one-star.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| (\d+) \| (true|false) \| (true|false) \| (\d+|—) \| (none|press|release) \|$",
                          lesson, flags=re.MULTILINE)
        fixture = lab.load_trace(ROOT / "fixtures/synthetic-two-presses.json")
        self.assertEqual(len(rows), len(fixture["samples"]))
        self.assertEqual(sum(sample["pressed"] for sample in fixture["samples"]), 12)
        for index, (timestamp, pressed, accepted, candidate, event) in enumerate(rows):
            self.assertEqual(fixture["samples"][index], {"timestamp_ms": int(timestamp), "pressed": pressed == "true"})
            prefix = dict(fixture, samples=fixture["samples"][:index + 1])
            result = lab.simulate(prefix)
            self.assertEqual(result["final_pressed"], accepted == "true")
            current_event = result["events"][-1] if result["events"] else None
            actual_event = current_event["event"] if current_event and current_event["timestamp_ms"] == int(timestamp) else "none"
            self.assertEqual(actual_event, event)
        loop = re.search(r"```python\n(.*?)```", lesson, flags=re.DOTALL).group(1)
        self.assertIn(loop, (ROOT / "star_counter.py").read_text(encoding="utf-8"))

    def test_many_cycles_and_maximum_reward(self):
        observations = [(n * 20, n % 4 in (0, 1)) for n in range(10000)]
        result = game.collect_stars(trace(observations), stars_per_press=100)
        self.assertEqual(len(result["collections"]), 2500)
        self.assertEqual(result["stars"], 250000)


if __name__ == "__main__":
    unittest.main()
