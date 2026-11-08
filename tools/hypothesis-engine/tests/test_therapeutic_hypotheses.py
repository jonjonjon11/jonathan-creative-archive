"""Regression checks for question wording, context, identity, and exports.

Synthetic tests establish program behavior, not clinical or scientific validity.
"""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
from hypothesis_engine import HypothesisEngine, Intervention
from generate_hypotheses import (
    export_research_plan, generate_hypotheses, load_pathway_network,
    populate_engine_from_network,
)


class TherapeuticQuestionTests(unittest.TestCase):
    def setUp(self):
        self.engine = HypothesisEngine()
        self.engine.register_intervention(Intervention(
            id="INT-SYNTHETIC", name="Synthetic intervention",
            target_pathway="PATH-SYNTHETIC", mechanism_of_action="Activates a synthetic process",
            intervention_type="synthetic", evidence_level="established",
        ))

    def question(self, outcome="motor neuron survival", population="synthetic population"):
        return self.engine.generate_therapeutic_hypothesis("INT-SYNTHETIC", outcome, population)

    def test_survival_is_a_question_not_a_reduction_claim(self):
        h = self.question()
        self.assertEqual(h.statement, "Does Synthetic intervention change motor neuron survival in synthetic population?")
        self.assertIn("Test whether", h.prediction)
        self.assertNotIn("will reduce", h.prediction)
        self.assertNotIn("by blocking", h.prediction)
        self.assertNotIn("slows or reverses", h.statement)

    def test_no_direction_is_invented_for_any_outcome(self):
        for outcome in ["motor neuron survival", "neuronal death", "ATP production", "aggregate clearance"]:
            with self.subTest(outcome=outcome):
                h = self.question(outcome)
                self.assertIn(f"change {outcome}", h.statement)
                self.assertIn("direction and effect size are not inferred", h.prediction)

    def test_outcome_and_population_are_structured(self):
        h = self.question()
        self.assertEqual(h.target_outcome, "motor neuron survival")
        self.assertEqual(h.patient_population, "synthetic population")
        self.assertIn(h.patient_population, h.prediction)

    def test_unspecified_population_does_not_default_to_sod1(self):
        h = self.engine.generate_therapeutic_hypothesis("INT-SYNTHETIC", "survival")
        self.assertEqual(h.patient_population, "unspecified population")
        self.assertNotIn("SOD1", h.statement)

    def test_registry_evidence_is_not_hypothesis_confidence(self):
        self.assertEqual(self.question().confidence, "open_question")

    def test_different_outcomes_do_not_overwrite_each_other(self):
        first, second = self.question(), self.question("ATP production")
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(len(self.engine.hypotheses), 2)

    def test_different_populations_do_not_overwrite_each_other(self):
        first, second = self.question(), self.question(population="different synthetic population")
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(len(self.engine.hypotheses), 2)

    def test_same_question_is_deterministic_and_idempotent(self):
        first, second = self.question(), self.question()
        self.assertEqual(first.id, second.id)
        self.assertEqual(len(self.engine.hypotheses), 1)

    def test_id_uses_unambiguous_field_boundaries(self):
        self.assertNotEqual(self.question("ab", "c").id, self.question("a", "bc").id)

    def test_whitespace_is_normalized_and_unicode_preserved(self):
        h = self.question("  survie des neurones  ", "  groupe α  ")
        self.assertEqual(h.target_outcome, "survie des neurones")
        self.assertEqual(h.patient_population, "groupe α")
        self.assertEqual(h.id, self.question("survie des neurones", "groupe α").id)

    def test_invalid_text_is_rejected_without_registering_a_question(self):
        for value in [None, "", "   ", 1, True, [], {}]:
            for field in ("outcome", "population"):
                with self.subTest(field=field, value=value):
                    with self.assertRaisesRegex(ValueError, "nonempty text"):
                        self.question(**{field: value})
        self.assertEqual(self.engine.hypotheses, {})

    def test_unknown_intervention_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown intervention"):
            self.engine.generate_therapeutic_hypothesis("missing", "outcome", "population")

    def test_json_export_preserves_context_and_limits(self):
        h = self.question()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            output = Path(temp) / "hypotheses.json"
            self.engine.export_hypotheses_json(str(output))
            data = json.loads(output.read_text())
        self.assertEqual(data["schema_version"], "1.2")
        self.assertEqual(data["status"], "unvalidated_research_questions")
        self.assertTrue(data["limitations"])
        self.assertEqual(data["hypotheses"][0]["target_outcome"], h.target_outcome)
        self.assertEqual(data["hypotheses"][0]["patient_population"], h.patient_population)

    def test_research_plan_preserves_context_and_limits(self):
        h = self.question()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            export_research_plan(self.engine, temp)
            data = json.loads((Path(temp) / "als-aging-hypotheses.json").read_text())
            report = (Path(temp) / "HYPOTHESIS_GENERATION_REPORT.md").read_text()
        self.assertEqual(data["schema_version"], "1.2")
        self.assertEqual(data["status"], "unvalidated_research_questions")
        for name in ("top_hypotheses", "all_hypotheses"):
            self.assertEqual(data[name][0]["target_outcome"], h.target_outcome)
            self.assertEqual(data[name][0]["patient_population"], h.patient_population)
        self.assertIn("not clinical predictions", report)
        self.assertIn(h.patient_population, report)
        self.assertNotIn("Focus first on high-confidence", report)


class RepositoryGenerationTests(unittest.TestCase):
    def test_committed_outputs_match_generation_apart_from_date(self):
        engine = HypothesisEngine()
        network = load_pathway_network(str(ROOT / "data/health/als-aging-pathways.json"))
        populate_engine_from_network(engine, network)
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            generate_hypotheses(engine, network)
            export_research_plan(engine, temp)
            actual = json.loads((Path(temp) / "als-aging-hypotheses.json").read_text())
            expected = json.loads((ROOT / "data/health/als-aging-hypotheses.json").read_text())
            actual.pop("generated")
            expected.pop("generated")
            self.assertEqual(actual, expected)
            actual_report = (Path(temp) / "HYPOTHESIS_GENERATION_REPORT.md").read_text().splitlines()
            expected_report = (ROOT / "data/health/HYPOTHESIS_GENERATION_REPORT.md").read_text().splitlines()
            self.assertEqual([l for l in actual_report if not l.startswith("**Generated:**")],
                             [l for l in expected_report if not l.startswith("**Generated:**")])
        therapeutic = [h for h in engine.hypotheses.values() if h.hypothesis_type == "therapeutic"]
        self.assertEqual(len(therapeutic), 8)
        self.assertTrue(all(h.confidence == "open_question" for h in therapeutic))
        self.assertTrue(all(h.target_outcome and h.patient_population for h in therapeutic))


if __name__ == "__main__":
    unittest.main()
