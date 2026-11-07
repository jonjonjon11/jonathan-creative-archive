"""Synthetic and adversarial tests. No real participants or clinical claims."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit", ROOT / "audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def fixture():
    return {
        "evidence": {"schema_version": "1.0", "sources": [{"id": "S1", "url": "https://example.org/synthetic"}],
                     "claims": [{"id": "C1", "source_ids": ["S1"], "statement": "Invented fixture; no biomedical meaning."}]},
        "network": {"schema_version": "1.0", "pathways": [{"id": "P1", "source_ids": ["S1"],
            "als_relevance": 0.2, "aging_relevance": 0.3,
            "score_provenance": {k: {"method": "Invented test coefficient; not empirical."} for k in ("als_relevance", "aging_relevance")},
            "literature_count": 1, "literature_source_ids": ["S1"],
            "mechanisms": [{"id": "M1", "evidence_confidence": "low", "supporting_sources": ["S1"]}]}],
            "interventions": [{"id": "I1", "target_pathway": "P1", "evidence_level": "low", "source_ids": ["S1"],
                "known_effects": {"P1": 0.123},
                "effect_provenance": {"P1": {"kind": "illustrative", "note": "Invented coefficient for software tests only."}}}],
            "pathway_count": 1, "intervention_count": 1},
        "hypotheses": {"schema_version": "1.0", "hypothesis_count": 1, "pathways_analyzed": 1, "interventions_reviewed": 1,
            "all_hypotheses": [{"id": "H1", "type": "mechanistic", "statement": "Invented fixture.", "confidence": "low", "priority_score": 0.25}],
            "top_hypotheses": [{"id": "H1", "type": "mechanistic", "statement": "Invented fixture.", "confidence": "low", "priority_score": 0.25,
                "score_provenance": {"priority_score": {"method": "Fixed synthetic test value."}},
                "supporting_evidence": ["C1"], "contradicting_evidence": [], "experimental_approach": "Synthetic software-only fixture check.",
                "pathways": ["P1"], "interventions": ["I1"]}]}
    }


def run(data):
    return audit.Audit().run(**data)


def codes(data):
    return {f["code"] for f in run(data)["findings"]}


class Rules(unittest.TestCase):
    def setUp(self):
        self.d = fixture()
        self.p = self.d["network"]["pathways"][0]
        self.i = self.d["network"]["interventions"][0]
        self.h = self.d["hypotheses"]["top_hypotheses"][0]

    def test_clean_is_explicitly_limited_not_scientific_pass(self):
        report = run(self.d)
        self.assertEqual(report["status"], "no_findings_within_scope")
        self.assertEqual(report["findings"], [])
        self.assertGreater(len(report["limitations"]), 5)

    def test_citations_do_not_establish_truth(self):
        self.h["statement"] = "A knowingly invented and scientifically meaningless sentence."
        self.d["hypotheses"]["all_hypotheses"][0]["statement"] = self.h["statement"]
        self.assertEqual(run(self.d)["findings"], [])  # prose intentionally outside scope

    def test_missing_source_url(self):
        del self.d["evidence"]["sources"][0]["url"]
        self.assertIn("SOURCE_URL_MISSING_OR_INVALID", codes(self.d))
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))

    def test_urls_reject_malformed_and_credentials_without_requests(self):
        bad = ["", None, 4, "relative", "javascript:alert(1)", "file:///tmp/a", "https://", "https://example.org:bad", "https://a:70000", "https://u:p@example.org", "https://exa mple.org", "https://example.org/\n", "https://example.org/%Q0", "https://example.org\\evil", "https://[broken"]
        for value in bad:
            with self.subTest(value=value):
                self.assertFalse(audit.valid_url(value))
        for value in ("https://example.org/a", "http://example.org:80", "https://例え.テスト/例"):
            self.assertTrue(audit.valid_url(value))

    def test_dangling_source_claim_and_path_references(self):
        self.h["supporting_evidence"] = ["MISSING"]
        self.h["pathways"] = ["MISSING"]
        self.assertIn("UNKNOWN_REFERENCE", codes(self.d))
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))

    def test_duplicate_source_not_counted_as_support(self):
        self.d["evidence"]["sources"] *= 2
        self.assertIn("DUPLICATE_ID", codes(self.d))
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))

    def test_duplicate_claim_not_counted_as_support(self):
        self.d["evidence"]["claims"] *= 2
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))

    def test_ambiguous_source_claim_id(self):
        self.d["evidence"]["claims"][0]["id"] = "S1"
        self.assertIn("AMBIGUOUS_EVIDENCE_ID", codes(self.d))

    def test_empty_or_absent_support_not_disproof(self):
        for value in ([], None, [""], [{}]):
            self.h["supporting_evidence"] = value
            self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))
        del self.h["supporting_evidence"]
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))

    def test_empty_contradictions_are_not_called_contradictions(self):
        self.assertNotIn("CONTRADICTION_REVIEW_UNDOCUMENTED", codes(self.d))
        del self.h["contradicting_evidence"]
        self.assertIn("CONTRADICTION_REVIEW_UNDOCUMENTED", codes(self.d))

    def test_undocumented_scores_and_effects(self):
        del self.p["score_provenance"]
        del self.i["effect_provenance"]
        self.assertIn("SCORE_METHOD_UNDOCUMENTED", codes(self.d))
        self.assertIn("EFFECT_PROVENANCE_INCOMPLETE", codes(self.d))

    def test_empirical_provenance_shape(self):
        self.i["effect_provenance"]["P1"] = {"source_ids": ["S1"], "unit": "synthetic", "population": "no participants", "endpoint": "toy", "timepoint": "toy"}
        self.assertNotIn("EFFECT_PROVENANCE_INCOMPLETE", codes(self.d))
        self.i["effect_provenance"]["P1"]["source_ids"] = ["missing"]
        self.assertIn("EFFECT_PROVENANCE_INCOMPLETE", codes(self.d))

    def test_boolean_nan_infinity_and_out_of_bounds_score(self):
        for value in (True, False, "0.1", None, float("nan"), float("inf"), -0.1, 1.1, [], {}):
            self.h["priority_score"] = value
            self.assertIn("INVALID_SCORE", codes(self.d))

    def test_numeric_equal_scores_do_not_conflict(self):
        self.h["priority_score"] = 1
        self.d["hypotheses"]["all_hypotheses"][0]["priority_score"] = 1.0
        self.assertNotIn("HYPOTHESIS_FIELD_CONFLICT", codes(self.d))

    def test_exact_export_conflict(self):
        self.h["priority_score"] = 0.9
        self.assertIn("HYPOTHESIS_FIELD_CONFLICT", codes(self.d))

    def test_internal_count_mismatch(self):
        self.d["hypotheses"]["hypothesis_count"] = 2
        self.assertIn("COUNT_MISMATCH", codes(self.d))

    def test_boolean_count_not_one(self):
        self.d["hypotheses"]["hypothesis_count"] = True
        self.assertIn("INVALID_COUNT", codes(self.d))

    def test_truncated_top_list_is_not_total_count_mismatch(self):
        extra = copy.deepcopy(self.h)
        extra["id"] = "H2"
        self.d["hypotheses"]["all_hypotheses"].append(extra)
        self.d["hypotheses"]["hypothesis_count"] = 2
        self.assertEqual(run(self.d)["findings"], [])

    def test_literature_sum_is_not_unique_reference_count(self):
        second = copy.deepcopy(self.p)
        second["id"] = "P2"
        second["mechanisms"] = []
        self.d["network"]["pathways"].append(second)
        report = run(self.d)
        self.assertEqual(report["metrics"]["literature_count_field_sum"], 2)
        self.assertEqual(report["metrics"]["source_records"], 1)

    def test_unenumerated_literature_not_false_reference_count(self):
        self.p["literature_count"] = 500
        del self.p["literature_source_ids"]
        self.assertIn("LITERATURE_COUNT_UNENUMERATED", codes(self.d))
        self.assertNotIn("LITERATURE_COUNT_UNRECONCILED", codes(self.d))

    def test_duplicate_literature_not_counted_twice(self):
        self.p["literature_count"] = 2
        self.p["literature_source_ids"] = ["S1", "S1"]
        self.assertIn("LITERATURE_COUNT_UNRECONCILED", codes(self.d))

    def test_unknown_effect_target(self):
        self.i["known_effects"]["missing"] = 0.5
        self.assertIn("UNKNOWN_EFFECT_TARGET", codes(self.d))

    def test_missing_experiment(self):
        self.h["experimental_approach"] = "  "
        self.assertIn("EXPERIMENT_UNDOCUMENTED", codes(self.d))

    def test_source_inputs_not_mutated(self):
        before = copy.deepcopy(self.d)
        run(self.d)
        self.assertEqual(before, self.d)

    def test_stable_report(self):
        self.h.pop("supporting_evidence")
        self.assertEqual(run(self.d), run(self.d))

    def test_no_network(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("Network forbidden")), mock.patch.object(socket, "create_connection", side_effect=AssertionError("Network forbidden")):
            run(self.d)

    def test_unsupported_schema_flagged(self):
        self.d["hypotheses"]["schema_version"] = "2.0"
        self.assertIn("UNSUPPORTED_VERSION", codes(self.d))

    def test_present_summary_score_provenance_references_are_checked(self):
        self.d["hypotheses"]["all_hypotheses"][0]["score_provenance"] = {"priority_score": {"method": "Synthetic", "source_ids": ["MISSING"]}}
        self.assertIn("UNKNOWN_REFERENCE", codes(self.d))

    def test_summary_boolean_score_not_masked_by_top_numeric_score(self):
        self.d["hypotheses"]["all_hypotheses"][0]["priority_score"] = True
        self.h["priority_score"] = 1
        self.assertIn("INVALID_SCORE", codes(self.d))
        self.assertIn("HYPOTHESIS_FIELD_CONFLICT", codes(self.d))

    def test_non_top_optional_details_are_checked(self):
        extra = copy.deepcopy(self.h)
        extra.update(id="H2", pathways=["missing"], interventions=["missing"], contradicting_evidence=["missing"], experimental_approach="")
        self.d["hypotheses"]["all_hypotheses"].append(extra)
        self.d["hypotheses"]["hypothesis_count"] = 2
        self.assertIn("UNKNOWN_REFERENCE", codes(self.d))
        self.assertIn("EXPERIMENT_UNDOCUMENTED", codes(self.d))

    def test_ambiguous_source_invalidates_earlier_claim(self):
        self.d["evidence"]["claims"].append({"id": "S1", "source_ids": ["S1"]})
        self.assertIn("HYPOTHESIS_WITHOUT_CITATION", codes(self.d))
        before = codes(self.d)
        self.d["evidence"]["claims"].reverse()
        self.assertEqual(before, codes(self.d))

    def test_confidence_enum_is_validated(self):
        for value in (True, [], {}, "", "proven", 1):
            self.h["confidence"] = value
            self.assertIn("INVALID_CONFIDENCE", codes(self.d))

    def test_each_existing_field_handles_adversarial_json_types(self):
        # Every node below each document root is replaced with wrong-type values.
        def paths(value, path=()):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield path + (key,)
                    yield from paths(child, path + (key,))
            elif isinstance(value, list):
                for i, child in enumerate(value):
                    yield path + (i,)
                    yield from paths(child, path + (i,))
        mutations = (None, False, 0, "", "x", [], {}, [None, {}, []])
        count = 0
        for role, doc in self.d.items():
            for path in paths(doc):
                for value in mutations:
                    data = copy.deepcopy(self.d)
                    node = data[role]
                    for part in path[:-1]:
                        node = node[part]
                    node[path[-1]] = copy.deepcopy(value)
                    with self.subTest(role=role, path=path, value=value):
                        report = run(data)
                        json.dumps(report, allow_nan=False)
                        count += 1
        self.assertGreater(count, 500)


class InputsAndCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / "input.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_reject_duplicate_keys_nan_and_invalid_json(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e999}', '[1]', '{bad', '\ufeff{}'):
            self.path.write_text(raw)
            with self.subTest(raw=raw), self.assertRaises(audit.InputError):
                audit.load_json(self.path)

    def test_reject_invalid_utf8(self):
        self.path.write_bytes(b'\xff')
        with self.assertRaises(audit.InputError):
            audit.load_json(self.path)

    def test_file_byte_depth_and_node_limits(self):
        self.path.write_text('{"x":"1234567890"}')
        with mock.patch.object(audit, "MAX_BYTES", 5), self.assertRaises(audit.InputError):
            audit.load_json(self.path)
        self.path.write_text('{"x":[[[[1]]]]}')
        with mock.patch.object(audit, "MAX_DEPTH", 2), self.assertRaises(audit.InputError):
            audit.load_json(self.path)
        with mock.patch.object(audit, "MAX_NODES", 3), self.assertRaises(audit.InputError):
            audit.load_json(self.path)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX test")
    def test_fifo_does_not_block(self):
        os.mkfifo(self.path)
        with self.assertRaises(audit.InputError):
            audit.load_json(self.path)

    def write_fixture(self, data):
        folder = self.root / "data" / "health"
        folder.mkdir(parents=True, exist_ok=True)
        for role, filename in (("evidence", "als-evidence.json"), ("network", "als-aging-pathways.json"), ("hypotheses", "als-aging-hypotheses.json")):
            (folder / filename).write_text(json.dumps(data[role]))
        return folder

    def cli(self, output="json"):
        return subprocess.run([sys.executable, "-B", str(ROOT / "audit.py"), "--repo", str(self.root), "--format", output], capture_output=True, text=True, timeout=10)

    def test_cli_exit_codes_0_1_2_and_read_only(self):
        d = fixture()
        folder = self.write_fixture(d)
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()}
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["inputs"]), 3)
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()})
        del d["hypotheses"]["top_hypotheses"][0]["supporting_evidence"]
        self.write_fixture(d)
        self.assertEqual(self.cli().returncode, 1)
        (folder / "als-evidence.json").write_text('{')
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "input_error")
        self.assertNotIn("Traceback", result.stderr)

    def test_terminal_escape_characters_are_quoted(self):
        d = fixture()
        d["network"]["interventions"][0]["known_effects"] = {"\x1b[31mBAD": 1}
        self.write_fixture(d)
        result = self.cli("text")
        self.assertNotIn("\x1b", result.stdout)
        self.assertIn("\\u001b", result.stdout)

    def test_symlink_outside_selected_root_is_refused(self):
        self.write_fixture(fixture())
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external) / "external.json"
            outside.write_text(json.dumps(fixture()["evidence"]))
            target = self.root / "data/health/als-evidence.json"
            target.unlink()
            target.symlink_to(outside)
            result = self.cli()
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "input_error")

    def test_file_symlink_loop_gets_structured_input_error(self):
        self.write_fixture(fixture())
        target = self.root / "data/health/als-evidence.json"
        target.unlink()
        target.symlink_to("als-evidence.json")
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "input_error")
        self.assertNotIn("Traceback", result.stderr)

    def test_root_symlink_loop_gets_structured_input_error(self):
        root = self.root / "loop"
        root.symlink_to("loop")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "audit.py"), "--repo", str(root), "--format", "json"], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "input_error")
        self.assertNotIn("Traceback", result.stderr)

    def test_no_file_output_flag(self):
        result = subprocess.run([sys.executable, str(ROOT / "audit.py"), "--output", str(self.path)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
