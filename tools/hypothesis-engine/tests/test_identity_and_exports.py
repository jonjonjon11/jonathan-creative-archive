"""Synthetic identity and export-completeness regressions, not science tests."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hypothesis_engine import Hypothesis, HypothesisEngine, Intervention, Pathway
from generate_hypotheses import export_research_plan


class ContextIdentityTests(unittest.TestCase):
    def setUp(self):
        self.engine = HypothesisEngine()
        for pid in ("P1", "P2"):
            self.engine.register_pathway(Pathway(pid, pid, "synthetic", "Synthetic pathway"))
        for iid in ("A", "BC", "AB", "C"):
            self.engine.register_intervention(Intervention(
                iid, iid, "P1", "Synthetic action", "synthetic", "moderate"))

    def mechanism(self, pathway="P1", gap="Synthetic gap", proposal="Synthetic mechanism", confidence="moderate"):
        return self.engine.generate_mechanistic_hypothesis(pathway, gap, proposal, confidence)

    def combination(self, ids=None, rationale="Synthetic interaction"):
        return self.engine.generate_synergy_hypothesis(["A", "BC"] if ids is None else ids, rationale)

    def test_same_gap_in_different_pathways_is_preserved(self):
        self.assertNotEqual(self.mechanism().id, self.mechanism(pathway="P2").id)
        self.assertEqual(len(self.engine.hypotheses), 2)

    def test_different_mechanisms_for_same_gap_are_preserved(self):
        self.assertNotEqual(self.mechanism().id, self.mechanism(proposal="Alternative mechanism").id)
        self.assertEqual(len(self.engine.hypotheses), 2)

    def test_mechanistic_context_is_retained(self):
        h = self.mechanism()
        self.assertEqual(h.gap_description, "Synthetic gap")
        self.assertEqual(h.proposed_mechanism, "Synthetic mechanism")

    def test_mechanistic_identity_is_unambiguous(self):
        self.assertNotEqual(self.mechanism(gap="ab", proposal="c").id,
                            self.mechanism(gap="a", proposal="bc").id)

    def test_repeat_mechanism_is_idempotent_and_confidence_is_metadata(self):
        first = self.mechanism()
        second = self.mechanism(confidence="low")
        self.assertEqual(first.id, second.id)
        self.assertEqual(len(self.engine.hypotheses), 1)
        self.assertEqual(self.engine.hypotheses[first.id].confidence, "low")

    def test_mechanistic_text_normalization_and_validation(self):
        self.assertEqual(self.mechanism().id,
                         self.mechanism(gap=" Synthetic gap ", proposal=" Synthetic mechanism ").id)
        before = len(self.engine.hypotheses)
        for value in (None, "", " \n ", 42, [], {}):
            for key in ("gap", "proposal"):
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, "nonempty text"):
                        self.mechanism(**{key: value})
        self.assertEqual(len(self.engine.hypotheses), before)

    def test_combination_ids_do_not_collide_when_concatenations_match(self):
        self.assertNotEqual(self.combination(["A", "BC"]).id, self.combination(["AB", "C"]).id)
        self.assertEqual(len(self.engine.hypotheses), 2)

    def test_distinct_combination_rationales_are_preserved(self):
        first = self.combination()
        second = self.combination(rationale="Different interaction")
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(first.expected_synergy, "Synthetic interaction")
        self.assertEqual(second.expected_synergy, "Different interaction")
        self.assertIn(second.expected_synergy, second.prediction)

    def test_combination_order_is_retained_not_canonicalized(self):
        first, second = self.combination(), self.combination(["BC", "A"])
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(first.interventions_proposed, ["A", "BC"])
        self.assertEqual(second.interventions_proposed, ["BC", "A"])

    def test_repeat_combination_is_idempotent_and_text_is_normalized(self):
        first = self.combination()
        self.assertEqual(first.id, self.combination(rationale=" Synthetic interaction ").id)
        self.assertEqual(len(self.engine.hypotheses), 1)

    def test_combination_copies_input_ids(self):
        ids = ["A", "BC"]
        h = self.combination(ids)
        ids.append("C")
        self.assertEqual(h.interventions_proposed, ["A", "BC"])

    def test_unknown_combination_member_is_not_silently_dropped(self):
        with self.assertRaisesRegex(ValueError, "Unknown intervention"):
            self.combination(["A", "missing"])
        self.assertEqual(self.engine.hypotheses, {})

    def test_combination_requires_two_distinct_registered_ids(self):
        for value in ([], ["A"], ["A", "A"], "ABC", ["A", None], ["A", []], 42):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.combination(value)
        self.assertEqual(self.engine.hypotheses, {})

    def test_blank_or_nontext_rationale_is_rejected(self):
        for value in (None, "", " \t ", True, 42, [], {}):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "nonempty text"):
                    self.combination(rationale=value)
        self.assertEqual(self.engine.hypotheses, {})

    def test_combination_wording_does_not_assert_demonstrated_synergy(self):
        h = self.combination()
        self.assertEqual(h.confidence, "open_question")
        self.assertIn("Test whether", h.prediction)
        self.assertNotIn("will have greater effect", h.prediction)
        self.assertNotIn("synergizes", h.statement)


def populated_engine(count):
    engine = HypothesisEngine()
    for index in range(count):
        h = Hypothesis(
            id=f"H-{index:04d}", hypothesis_type="mechanistic",
            statement=f"Synthetic question {index}", prediction=f"Synthetic prediction {index}",
            priority_score=index / max(count, 1),
            gap_description=f"Gap {index}", proposed_mechanism=f"Mechanism {index}",
            supporting_evidence=[f"SYNTHETIC-SOURCE-{index}"],
            contradicting_evidence=[f"SYNTHETIC-CONTRADICTION-{index}"],
            experimental_approach=f"Synthetic protocol {index}",
        )
        engine.hypotheses[h.id] = h
    return engine


class CompleteExportTests(unittest.TestCase):
    def test_default_and_explicit_ranking_limits(self):
        engine = populated_engine(125)
        self.assertEqual(len(engine.rank_hypotheses_by_priority()), 20)
        self.assertEqual(len(engine.rank_hypotheses_by_priority(None)), 125)
        self.assertEqual(len(engine.rank_hypotheses_by_priority(0)), 0)
        self.assertEqual(len(engine.rank_hypotheses_by_priority(51)), 51)
        for bad in (-1, True, 2.5, "5"):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "nonnegative integer or None"):
                engine.rank_hypotheses_by_priority(bad)

    def test_both_export_paths_are_complete_at_old_boundaries(self):
        for count in (0, 1, 10, 11, 30, 31, 50, 51, 100, 101, 125):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
                engine = populated_engine(count)
                standalone = Path(temp) / "standalone.json"
                engine.export_hypotheses_json(str(standalone))
                export_research_plan(engine, temp)
                one = json.loads(standalone.read_text())
                plan = json.loads((Path(temp) / "als-aging-hypotheses.json").read_text())
                report = (Path(temp) / "HYPOTHESIS_GENERATION_REPORT.md").read_text()
                expected = [f"H-{i:04d}" for i in reversed(range(count))]
                self.assertEqual(one["schema_version"], "1.2")
                self.assertEqual(plan["schema_version"], "1.2")
                self.assertEqual(one["hypothesis_count"], count)
                self.assertEqual(len(one["hypotheses"]), count)
                self.assertEqual([h["id"] for h in one["ranked_by_priority"]], expected)
                self.assertEqual(plan["hypothesis_count"], count)
                self.assertEqual(plan["exported_hypothesis_count"], count)
                self.assertEqual([h["id"] for h in plan["all_hypotheses"]], expected)
                self.assertEqual(plan["top_hypotheses"], plan["all_hypotheses"][:30])
                self.assertEqual(plan["top_hypotheses_count"], min(count, 30))
                self.assertEqual(plan["top_hypotheses_truncated"], count > 30)
                self.assertEqual(plan["presentation_limits"], {"top_hypotheses": 30, "markdown_report": 10})
                self.assertEqual(sum(l.startswith("### ") for l in report.splitlines()), min(count, 10))
                self.assertIn(f"Showing {min(count, 10)} of {count}", report)
                self.assertIn("[Complete question records](als-aging-hypotheses.json)", report)
                if count:
                    last = plan["all_hypotheses"][-1]
                    self.assertEqual(last["prediction"], "Synthetic prediction 0")
                    self.assertEqual(last["proposed_mechanism"], "Mechanism 0")
                    self.assertEqual(last["supporting_evidence"], ["SYNTHETIC-SOURCE-0"])
                    self.assertEqual(last["contradicting_evidence"], ["SYNTHETIC-CONTRADICTION-0"])
                    self.assertEqual(last["experimental_approach"], "Synthetic protocol 0")

    def test_combination_context_survives_both_exports(self):
        fixture = ContextIdentityTests()
        fixture.setUp()
        h = fixture.combination()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            one = Path(temp) / "standalone.json"
            fixture.engine.export_hypotheses_json(str(one))
            export_research_plan(fixture.engine, temp)
            standalone = json.loads(one.read_text())
            plan = json.loads((Path(temp) / "als-aging-hypotheses.json").read_text())
        for record in (standalone["hypotheses"][0], plan["all_hypotheses"][0], plan["top_hypotheses"][0]):
            self.assertEqual(record["expected_synergy"], h.expected_synergy)
            self.assertEqual(record["prediction"], h.prediction)


if __name__ == "__main__":
    unittest.main()
