"""Synthetic fixtures only; never read private accounts or execute archive code."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("finder", Path(__file__).parents[1] / "idea_finder.py")
finder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(finder)


class FinderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        common = {"source_ids": ["S-1"], "artifact_status": "source_inspected",
                  "scientific_standing": "design_mapping", "limitations": "Not independently verified.",
                  "next_step": "Try a bounded experiment."}
        self.concepts = [dict(common, id="C-2", title="Ratio lesson", tags=["music", "math"], summary="Explore light and rhythm."),
                         dict(common, id="C-1", title="Light atlas", tags=["physics", "math"], summary="Compare measured motion.")]
        self.sources = [{"id": "S-1", "title": "Fixture source", "evidence_class": "repository_inspection",
                         "access": "private_source", "findings": "Historical work was found.", "limitations": "Original is private."}]
        self.artifacts = [{"id": "A-1", "title": "Fixture artifact", "path": "tools/example", "source_ids": ["S-1"],
                           "rights": {"license_declared": "unknown", "license_path": "tools/example/LICENSE",
                                      "scope": "No clearance inferred.", "review_record": "tools/example/README.md"},
                           "verification": {"status": "not_run", "record": "tools/example/README.md", "limitations": "Never runtime verified."}}]
        self.persist()

    def save(self, rel, value):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def persist(self):
        for rel, key, values in (("data/concepts.json", "concepts", self.concepts),
                                 ("sources/manifest.json", "sources", self.sources),
                                 ("data/artifacts.json", "artifacts", self.artifacts)):
            self.save(rel, {"schema_version": "1.0", key: values})

    def find(self, query="", **kwargs):
        return finder.find(self.root, query, **kwargs)

    def invoke(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = finder.main([str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_case_insensitive_unicode_normalization(self):
        self.assertEqual(self.find("ＬＩＧＨＴ")["results"][0]["id"], "C-1")
        self.assertEqual(self.find("LIGHT"), self.find("LIGHT"))

    def test_all_terms_must_match_across_fields(self):
        report = self.find("light physics")
        self.assertEqual([r["id"] for r in report["results"]], ["C-1"])
        self.assertEqual(self.find("light absent")["total_matches"], 0)

    def test_title_ranks_above_summary_and_has_match_reasons(self):
        report = self.find("light")
        self.assertEqual([r["id"] for r in report["results"]], ["C-1", "C-2"])
        self.assertEqual(report["results"][0]["match"], {"text_score": 5, "matched_fields": ["title"]})
        self.assertEqual(report["results"][1]["match"]["text_score"], 2)

    def test_no_query_browses_stable_ids(self):
        self.assertEqual([r["id"] for r in self.find()["results"]], ["C-1", "C-2"])

    def test_duplicate_terms_do_not_inflate_score(self):
        first = self.find("light")["results"]
        repeated = self.find("light light LIGHT")["results"]
        self.assertEqual(first, repeated)

    def test_literal_query_never_becomes_regex(self):
        self.assertEqual(self.find(".*")["total_matches"], 0)
        self.assertEqual(self.find("[light")["total_matches"], 0)

    def test_tag_filters_are_exact_and_all_required(self):
        report = self.find(tags=["MUSIC", "math"])
        self.assertEqual([r["id"] for r in report["results"]], ["C-2"])
        self.assertEqual(self.find(tags=["mus"])["total_matches"], 0)
        self.assertEqual(self.find(tags=["music", "physics"])["total_matches"], 0)

    def test_status_filter(self):
        self.concepts[1]["artifact_status"] = "idea"
        self.persist()
        self.assertEqual([r["id"] for r in self.find(status="idea")["results"]], ["C-1"])

    def test_explicit_truncation(self):
        report = self.find(limit=1)
        self.assertEqual((report["total_matches"], report["returned"], report["omitted"]), (2, 1, 1))
        self.assertIn("Some matches are omitted", finder.render(report))

    def test_sources_and_limits_remain_explicit(self):
        result = self.find("C-1")["results"][0]
        self.assertEqual(result["scientific_standing"], "design_mapping")
        self.assertEqual(result["limitations"], "Not independently verified.")
        self.assertEqual(result["sources"][0]["access"], "private_source")
        self.assertEqual(result["sources"][0]["limitations"], "Original is private.")

    def test_related_artifact_is_source_link_not_implementation_claim(self):
        result = self.find("C-1")["results"][0]
        self.assertEqual(result["related_artifacts"][0]["shared_source_ids"], ["S-1"])
        self.assertEqual(result["related_artifacts"][0]["rights"]["license_declared"], "unknown")
        self.assertIn("not proof of implementation", finder.render(self.find("C-1")))

    def test_metadata_paths_remain_inert_and_are_not_opened(self):
        self.artifacts[0]["path"] = "../../outside"
        self.artifacts[0]["rights"]["license_path"] = "https://example.invalid/no-fetch"
        self.persist()
        # No such artifact files exist; only the three fixed JSON inputs are read.
        self.assertEqual(self.find("light")["returned"], 2)

    def test_source_findings_and_limits_are_not_search_fields(self):
        self.sources[0]["findings"] = "unique_unindexed_term"
        self.concepts[0]["limitations"] = "other_unindexed_term"
        self.persist()
        self.assertEqual(self.find("unique_unindexed_term")["total_matches"], 0)
        self.assertEqual(self.find("other_unindexed_term")["total_matches"], 0)

    def test_next_step_is_searchable(self):
        self.assertEqual(self.find("bounded")["total_matches"], 2)
        self.assertEqual(self.find("bounded")["results"][0]["match"]["matched_fields"], ["next_step"])

    def test_unrelated_artifact_not_attached(self):
        self.sources.append(dict(self.sources[0], id="S-2"))
        self.artifacts[0]["source_ids"] = ["S-2"]
        self.persist()
        self.assertEqual(self.find("light")["results"][0]["related_artifacts"], [])

    def test_missing_reference_rejected(self):
        self.concepts[0]["source_ids"] = ["missing"]
        self.persist()
        self.assertEqual(self.invoke("light")[0], 2)

    def test_duplicate_ids_or_source_references_rejected(self):
        self.concepts.append(copy.deepcopy(self.concepts[0]))
        self.persist()
        self.assertEqual(self.invoke()[0], 2)
        self.concepts.pop()
        self.concepts[0]["source_ids"] = ["S-1", "S-1"]
        self.persist()
        self.assertEqual(self.invoke()[0], 2)

    def test_empty_or_bad_tags_rejected(self):
        for tags in ([], {}, [None], ["math", "math"]):
            with self.subTest(tags=tags):
                self.concepts[0]["tags"] = tags
                self.persist()
                self.assertEqual(self.invoke()[0], 2)

    def test_malformed_fields_and_schema_rejected(self):
        self.save("data/artifacts.json", {"schema_version": "2.0", "artifacts": self.artifacts})
        self.assertEqual(self.invoke()[0], 2)
        self.artifacts[0]["verification"] = []
        self.persist()
        self.assertEqual(self.invoke()[0], 2)

    def test_duplicate_json_keys_and_deep_json_rejected(self):
        path = self.root / "data/concepts.json"
        for payload in ('{"schema_version":"1.0","concepts":[],"concepts":[]}',
                        '{"x":' + '[' * 10000 + ']' * 10000 + '}'):
            with self.subTest(size=len(payload)):
                path.write_text(payload)
                code, _, error = self.invoke()
                self.assertEqual(code, 2)
                self.assertNotIn("Traceback", error)

    def test_size_limit_and_non_utf8(self):
        with patch.object(finder, "MAX_JSON_BYTES", 1):
            self.assertEqual(self.invoke()[0], 2)
        (self.root / "data/concepts.json").write_bytes(b"\xff")
        self.assertEqual(self.invoke()[0], 2)

    def test_metadata_symlink_rejected(self):
        path = self.root / "data/concepts.json"
        original = self.root / "copy.json"
        path.rename(original)
        path.symlink_to(original)
        self.assertEqual(self.invoke()[0], 2)

    def test_metadata_directory_symlink_rejected(self):
        (self.root / "data").rename(self.root / "actual-data")
        (self.root / "data").symlink_to(self.root / "actual-data", target_is_directory=True)
        self.assertEqual(self.invoke()[0], 2)

    @unittest.skipUnless(hasattr(__import__("os"), "mkfifo"), "FIFO support required")
    def test_nonregular_input_rejected_before_open(self):
        import os
        path = self.root / "data/concepts.json"
        path.unlink()
        os.mkfifo(path)
        self.assertEqual(self.invoke()[0], 2)

    def test_query_and_result_limits(self):
        for query in ("x" * 501, " ".join(f"t{i}" for i in range(17)), None):
            with self.subTest(query=query), self.assertRaises(finder.InputError):
                self.find(query)
        for limit in (0, 21, True, "5"):
            with self.subTest(limit=limit), self.assertRaises(finder.InputError):
                self.find(limit=limit)

    def test_cli_success_no_matches_and_no_writes(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        code, out, err = self.invoke("light", "--format", "json")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(json.loads(out)["total_matches"], 2)
        self.assertEqual(snapshot(), before)
        code, out, _ = self.invoke("no-such-concept")
        self.assertEqual(code, 0)
        self.assertIn("No metadata matches", out)

    def test_missing_input_is_controlled_error(self):
        (self.root / "sources/manifest.json").unlink()
        code, _, err = self.invoke()
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)

    def test_output_escapes_terminal_control_characters(self):
        self.concepts[0]["title"] = "Injected\n\x1b[31m"
        self.persist()
        out = finder.render(self.find("injected"))
        self.assertNotIn("\x1b", out)
        self.assertIn("Injected\\n\\x1b[31m", out)


    def test_unknown_extra_fields_are_not_exported(self):
        marker = "unneeded_fixture_field"
        self.concepts[0]["extra"] = marker
        self.sources[0]["extra"] = marker
        self.artifacts[0]["rights"]["extra"] = marker
        self.artifacts[0]["verification"]["extra"] = marker
        self.persist()
        self.assertNotIn(marker, json.dumps(self.find()))

    def test_unknown_science_and_status_labels_rejected(self):
        self.concepts[0]["scientific_standing"] = "proven_everything"
        self.persist()
        self.assertEqual(self.invoke()[0], 2)
        self.concepts[0]["scientific_standing"] = "design_mapping"
        self.concepts[0]["artifact_status"] = "complete_forever"
        self.persist()
        self.assertEqual(self.invoke()[0], 2)


    def test_root_symlink_loop_is_controlled_error(self):
        loop = self.root / "loop"
        loop.symlink_to(loop)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = finder.main([str(loop)])
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err.getvalue())

    def test_distinct_rights_and_verification_records_are_both_shown(self):
        self.artifacts[0]["rights"]["review_record"] = "rights-review.md"
        self.artifacts[0]["verification"]["record"] = "tests-review.md"
        self.persist()
        report = finder.render(self.find("light"))
        self.assertIn("Rights review record: rights-review.md", report)
        self.assertIn("Verification record: tests-review.md", report)


if __name__ == "__main__":
    unittest.main()
