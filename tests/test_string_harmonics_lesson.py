"""Check the written companion's numbers and scope, not teaching effectiveness."""
from fractions import Fraction
import math
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "docs/lessons/string-harmonics.md"


def table(text, header):
    """Read the actual learner-facing rows, so prose/table changes are tested."""
    lines = text.splitlines()
    start = lines.index(header)
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


class StringHarmonicsLessonChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = LESSON.read_text(encoding="utf-8")
        cls.modes = table(cls.text, "| Mode n | Wavelength (m) | Frequency (Hz) | Internal nodes | All nodes, including ends (m) |")
        cls.snapshots = table(cls.text, "| Time (ms) | y at x=0 m (mm) | y at x=0.15 m (mm) | y at x=0.30 m (mm) | y at x=0.45 m (mm) | y at x=0.60 m (mm) |")
        cls.length = Fraction("0.60")
        cls.speed = Fraction(120)

    def test_model_values_and_assumptions_are_explicit(self):
        for phrase in ("L = 0.60 m", "v = 120 m/s", "chosen model values, not measurements",
                       "held fixed at both ends", "constant tension", "Displacements and slopes are small",
                       "bending stiffness, damping and changes in tension are neglected",
                       "one transverse normal mode at a time"):
            self.assertIn(phrase, self.text)

    def test_spatial_rows_use_the_fixed_end_relations(self):
        self.assertEqual(len(self.modes), 3)
        for expected_n, row in enumerate(self.modes, 1):
            self.assertEqual(len(row), 5)
            n, wavelength, frequency, internal, _ = row
            self.assertEqual(int(n), expected_n)
            self.assertEqual(Fraction(wavelength), 2 * self.length / expected_n)
            self.assertEqual(Fraction(frequency), self.speed * expected_n / (2 * self.length))
            self.assertEqual(int(internal), expected_n - 1)

    def test_spatial_rows_list_all_nodes_and_no_extra_positions(self):
        for n, _, _, _, node_text in self.modes:
            n = int(n)
            nodes = [Fraction(item.strip()) for item in node_text.split(",")]
            self.assertEqual(nodes, [j * self.length / n for j in range(n + 1)])
            self.assertEqual(len(nodes), n + 1)
            self.assertEqual(nodes[0], 0)
            self.assertEqual(nodes[-1], self.length)

    def test_each_frequency_wavelength_pair_retains_wave_speed(self):
        for _, wavelength, frequency, _, _ in self.modes:
            self.assertEqual(Fraction(wavelength) * Fraction(frequency), self.speed)

    def test_snapshot_times_are_one_quarter_period_steps_in_milliseconds(self):
        self.assertEqual(len(self.snapshots), 5)
        period_seconds = Fraction(1, 200)
        times_ms = [Fraction(row[0]) for row in self.snapshots]
        self.assertEqual(times_ms, [j * period_seconds * 1000 / 4 for j in range(5)])
        self.assertIn("1/200 s = 0.005 s = 5 ms", self.text)
        self.assertIn("One millisecond (ms) is 0.001 s", self.text)

    def test_every_snapshot_cell_matches_the_analytical_mode(self):
        positions = [Fraction(j) * self.length / 4 for j in range(5)]
        for row in self.snapshots:
            self.assertEqual(len(row), 6)
            t = float(Fraction(row[0]) / 1000)
            for x, cell in zip(positions, row[1:]):
                expected_mm = math.sin(2 * math.pi * float(x / self.length)) * math.cos(2 * math.pi * 200 * t)
                with self.subTest(time_ms=row[0], position=str(x)):
                    self.assertAlmostEqual(float(cell), expected_mm, places=12)
        self.assertIn("A = 1 mm", self.text)
        self.assertIn("y(x,t) = A sin(nπx/L) cos(2πf_n t)", self.text)
        self.assertIn("not the amplitude of each constituent travelling wave", self.text)

    def test_flat_snapshot_and_permanent_nodes_are_distinct(self):
        values = [[Fraction(cell) for cell in row[1:]] for row in self.snapshots]
        self.assertEqual(values[1], [0] * 5)
        permanent = [index for index in range(5) if all(row[index] == 0 for row in values)]
        self.assertEqual(permanent, [0, 2, 4])
        self.assertEqual([row[1] for row in values], [1, 0, -1, 0, 1])
        self.assertIn("A single photograph cannot establish that a point is a node", self.text)

    def test_shortened_string_worked_example_is_consistent(self):
        section = self.text.split("### Example 3:", 1)[1].split("## 3.", 1)[0]
        match = re.search(r"L = ([0-9.]+) m", section)
        new_length = Fraction(match.group(1))
        self.assertEqual(new_length, self.length / 2)
        self.assertEqual(2 * new_length, Fraction("0.60"))
        self.assertEqual(self.speed / (2 * new_length), 200)
        for phrase in ("keeping wave speed at **120 m/s**", "use its fundamental",
                       "only nodes are its new endpoints, 0 and 0.30 m"):
            self.assertIn(phrase, section)

    def test_exercise_one_answer_has_correct_fourth_mode_and_node_list(self):
        solutions = self.text.split("## 4. Solutions and reasons", 1)[1].split("## 5.", 1)[0]
        first = solutions.split("\n2. ", 1)[0]
        self.assertIn("**0.30 m**", first)
        self.assertIn("**400 Hz**", first)
        self.assertEqual(2 * self.length / 4, Fraction("0.30"))
        self.assertEqual(4 * self.speed / (2 * self.length), 400)
        self.assertIn("**3 internal nodes**", first)
        self.assertIn("**5 nodes including the ends**", first)
        match = re.search(r"at \*\*([0-9., ]+) m\*\*", first)
        nodes = [Fraction(value.strip()) for value in match.group(1).split(",")]
        self.assertEqual(nodes, [j * self.length / 4 for j in range(5)])

    def test_exercise_two_recalculates_mode_for_longer_string(self):
        prompt = self.text.split("2. **A frequency match.**", 1)[1].split("\n3. ", 1)[0]
        self.assertIn("length 1.20 m", prompt)
        self.assertIn("wave speed 120 m/s", prompt)
        self.assertIn("frequency 200 Hz", prompt)
        fundamental = self.speed / (2 * Fraction("1.20"))
        self.assertEqual(fundamental, 50)
        self.assertEqual(Fraction(200) / fundamental, 4)
        self.assertIn("fundamental = 120 / (2 × 1.20) = **50 Hz**", self.text)
        self.assertIn("requested mode is **n = 4**, with wavelength **0.60 m**", self.text)

    def test_amplitude_and_playback_answers_keep_model_frequency(self):
        for phrase in ("**+2 mm and -2 mm; still 200 Hz and 5 ms.**",
                       "amplitude independence belongs to the stated linear idealization",
                       "model still makes 200 cycles per model second",
                       "does not make every pair of successive harmonics an octave"):
            self.assertIn(phrase, self.text)
        self.assertEqual(2 * Fraction(self.snapshots[0][2]), 2)
        self.assertEqual(2 * Fraction(self.snapshots[0][4]), -2)

    def test_complete_readable_path_and_review_limits_are_present(self):
        self.assertEqual(len(re.findall(r"^### Example [123]:", self.text, re.M)), 3)
        questions = self.text.split("## 3. Try five questions", 1)[1].split("## 4.", 1)[0]
        solutions = self.text.split("## 4. Solutions and reasons", 1)[1].split("## 5.", 1)[0]
        self.assertEqual(re.findall(r"^([1-5])\. ", questions, re.M), list("12345"))
        self.assertEqual(re.findall(r"^([1-5])\. ", solutions, re.M), list("12345"))
        self.assertEqual(questions.count("Hint:"), 5)
        for phrase in ("Drawing is optional", "Without the table", "Read it in words",
                       "No code execution is needed", "not a validated curriculum",
                       "print-layout and assistive-technology review remain pending"):
            self.assertIn(phrase, self.text)

    def test_sources_and_prior_work_boundaries_are_preserved(self):
        source_urls = (
            "https://openstax.org/books/university-physics-volume-1/pages/16-6-standing-waves-and-resonance",
            "https://openstax.org/books/university-physics-volume-1/pages/16-3-wave-speed-on-a-stretched-string",
            "https://www.acs.psu.edu/drussell/Demos/string/Fixed.html",
            "https://openstax.org/books/chemistry-2e/pages/6-3-development-of-quantum-theory",
        )
        for index, url in enumerate(source_urls, 1):
            self.assertIn(f"**SW-0{index}:**", self.text)
            self.assertIn(url, self.text)
        self.assertIn("not three independent confirmations", self.text)
        self.assertIn("new original writing, not recovery of that lab", self.text)
        self.assertIn("exact source and current hosted behavior were not inspected", self.text)
        self.assertIn("links to it without importing its material", self.text)

    def test_orbitals_are_probability_not_paths_or_intrinsic_notes(self):
        for phrase in ("position probability density", "not a drawn route followed by an electron",
                       "governing equations and physical interpretations differ",
                       "Nothing here computes orbitals, atomic energy levels or emission spectra",
                       "does not establish an intrinsic note"):
            self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()
