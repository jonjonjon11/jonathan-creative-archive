"""Synthetic fixtures only. No credentials, network, or real user files."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("steward", Path(__file__).parents[1] / "archive_steward.py")
steward = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(steward)


class StewardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("LICENSE", "fixture declaration only\n")
        self.write("tools/example/file.txt", "preserved bytes\n")
        self.write("tools/example/README.md", "fixture review\n")
        self.save("sources/manifest.json", {"sources": [
            {"id": "S-1", "title": "Fixture source", "access": "private_source"}]})
        self.save("data/concepts.json", {"concepts": [
            {"id": "C-1", "title": "Fixture concept", "source_ids": ["S-1"],
             "artifact_status": "source_inspected", "next_step": "Run a bounded test.",
             "limitations": "No runtime verification.", "included_artifact": "tools/example/file.txt"}]})
        self.save("tools/example/source-manifest.json", {
            "license": "CC0-1.0", "files": {"file.txt": {"sha256": self.hash("tools/example/file.txt")}}})
        self.save("data/artifacts.json", {"schema_version": "1.0", "artifacts": [
            {"id": "A-1", "title": "Fixture artifact", "path": "tools/example", "source_ids": ["S-1"],
             "rights": {"license_declared": "CC0-1.0", "license_path": "LICENSE", "scope": "Fixture only.",
                        "review_record": "tools/example/README.md"},
             "verification": {"status": "not_run", "record": "tools/example/README.md", "limitations": "Fixture only."},
             "preserved_manifest": "tools/example/source-manifest.json", "pinned_files": []}]})
        self.refresh()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def save(self, rel, value):
        self.write(rel, json.dumps(value))

    def read(self, rel):
        return json.loads((self.root / rel).read_text())

    def hash(self, rel):
        return hashlib.sha256((self.root / rel).read_bytes()).hexdigest()

    def refresh(self):
        hashes = {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.root.rglob("*") if p.is_file() and p.relative_to(self.root).as_posix() != "data/checksums.json"}
        self.save("data/checksums.json", {"algorithm": "sha256", "excluded": ["data/checksums.json", ".git/**"], "files": hashes})

    def report(self):
        return steward.inspect(self.root)

    def codes(self):
        return {f["code"] for f in self.report()["findings"]}

    def invoke(self, *options):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = steward.main([str(self.root), *options])
        return result, out.getvalue(), err.getvalue()

    def test_clean_archive_is_deterministic(self):
        first = self.report()
        self.assertEqual(first, self.report())
        self.assertEqual(first["summary"]["errors"], 0)
        self.assertEqual(first["hash_checks"]["preserved_source"], 1)
        self.assertEqual(first["review_queue"][0]["next_step"], "Run a bounded test.")

    def test_changed_preserved_file_detected_even_after_refresh(self):
        self.write("tools/example/file.txt", "changed\n")
        self.refresh()
        findings = self.report()["findings"]
        self.assertTrue(any(f["code"] == "hash_mismatch" and "preserved_source" in f["message"] for f in findings))

    def test_archive_hash_drift(self):
        self.write("LICENSE", "different declaration\n")
        self.assertIn("hash_mismatch", self.codes())

    def test_missing_file(self):
        (self.root / "tools/example/file.txt").unlink()
        self.assertIn("unreadable_file", self.codes())

    def test_unlisted_file(self):
        self.write("unexpected.txt", "review me")
        self.assertIn("unlisted_file", self.codes())

    def test_cache_directories_ignored(self):
        for rel in (".git/config", "nested/__pycache__/x.pyc", ".DS_Store", "x.pyc"):
            self.write(rel, "cache")
        self.assertEqual(self.report()["summary"]["errors"], 0)

    def test_symlinks_never_followed(self):
        (self.root / "linked-file").symlink_to(self.root / "LICENSE")
        (self.root / "linked-dir").symlink_to(self.root / "tools", target_is_directory=True)
        self.assertIn("symlink", self.codes())
        with self.assertRaises(steward.InputError):
            steward.safe_path(self.root, "linked-dir/example/file.txt")

    def test_traversal_and_platform_paths_rejected(self):
        for rel in ("../outside", "/absolute", "tools/../LICENSE", "tools//file", "./LICENSE", "C:/file", "a\\b"):
            with self.subTest(rel=rel), self.assertRaises(steward.InputError):
                steward.safe_path(self.root, rel)

    def test_traversal_in_hash_manifest_is_reported(self):
        data = self.read("data/checksums.json")
        data["files"]["../outside"] = "a" * 64
        self.save("data/checksums.json", data)
        self.assertIn("unreadable_file", self.codes())

    def test_source_reference_must_resolve(self):
        data = self.read("data/concepts.json")
        data["concepts"][0]["source_ids"] = ["S-missing"]
        self.save("data/concepts.json", data)
        self.refresh()
        self.assertIn("unknown_source", self.codes())

    def test_empty_source_references(self):
        data = self.read("data/concepts.json")
        data["concepts"][0]["source_ids"] = []
        self.save("data/concepts.json", data)
        self.refresh()
        self.assertIn("missing_sources", self.codes())

    def test_missing_artifact_directory(self):
        data = self.read("data/artifacts.json")
        data["artifacts"][0]["path"] = "missing-directory"
        data["artifacts"][0]["preserved_manifest"] = None
        self.save("data/artifacts.json", data)
        self.refresh()
        self.assertIn("missing_artifact_directory", self.codes())

    def test_empty_artifact_source_references(self):
        data = self.read("data/artifacts.json")
        data["artifacts"][0]["source_ids"] = []
        self.save("data/artifacts.json", data)
        self.refresh()
        self.assertIn("missing_sources", self.codes())

    def test_duplicate_ids_rejected(self):
        data = self.read("data/concepts.json")
        data["concepts"].append(data["concepts"][0])
        self.save("data/concepts.json", data)
        with self.assertRaises(steward.InputError):
            self.report()

    def test_duplicate_json_keys_rejected(self):
        self.write("data/concepts.json", '{"concepts": [], "concepts": []}')
        self.assertEqual(self.invoke()[0], 2)

    def test_invalid_json_no_traceback(self):
        self.write("data/concepts.json", "not JSON")
        status, out, err = self.invoke()
        self.assertEqual((status, out), (2, ""))
        self.assertIn("invalid UTF-8 JSON", err)
        self.assertNotIn("Traceback", err)

    def test_deeply_nested_json_no_traceback(self):
        self.write("data/concepts.json", '{"concepts":' + '[' * 10000 + ']' * 10000 + '}')
        status, _, err = self.invoke()
        self.assertEqual(status, 2)
        self.assertNotIn("Traceback", err)

    def test_no_independent_hashes_warns(self):
        data = self.read("data/artifacts.json")
        data["artifacts"][0]["preserved_manifest"] = None
        self.save("data/artifacts.json", data)
        self.refresh()
        self.assertIn("independent_hashes_missing", self.codes())

    def test_empty_preserved_manifest_warns(self):
        self.save("tools/example/source-manifest.json", {"license": "CC0-1.0", "files": {}})
        self.refresh()
        self.assertIn("independent_hashes_missing", self.codes())

    def test_unknown_status(self):
        data = self.read("data/concepts.json")
        data["concepts"][0]["artifact_status"] = "perfect"
        self.save("data/concepts.json", data)
        self.refresh()
        self.assertIn("unknown_status", self.codes())

    def test_runtime_claim_requires_record_warning(self):
        data = self.read("data/concepts.json")
        data["concepts"][0]["artifact_status"] = "runtime_verified"
        self.save("data/concepts.json", data)
        self.refresh()
        report = self.report()
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertIn("verification_record_needed", self.codes())
        self.assertEqual(self.invoke()[0], 0)

    def test_evidence_gaps_sort_first(self):
        data = self.read("data/concepts.json")
        item = dict(data["concepts"][0], id="C-9", artifact_status="review_gap")
        data["concepts"].append(item)
        self.save("data/concepts.json", data)
        self.refresh()
        self.assertEqual([q["id"] for q in self.report()["review_queue"]], ["C-9", "C-1"])

    def test_license_disagreement(self):
        data = self.read("data/artifacts.json")
        data["artifacts"][0]["rights"]["license_declared"] = "unknown"
        self.save("data/artifacts.json", data)
        self.refresh()
        self.assertTrue({"license_disagreement", "rights_review_needed"} <= self.codes())

    def test_list_manifest_and_generated_build(self):
        self.save("tools/example/source-manifest.json", {"license": "CC0-1.0", "files": [
            {"included": True, "archive_path": "file.txt", "sha256": self.hash("tools/example/file.txt")},
            {"included": False, "archive_path": None}],
            "generated_build": {"path": "file.txt", "sha256": self.hash("tools/example/file.txt")}})
        self.refresh()
        report = self.report()
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["hash_checks"]["generated_build"], 1)

    def test_null_or_malformed_hash_is_not_presence_check(self):
        for bad in (None, "xyz", 42):
            with self.subTest(hash=bad):
                data = self.read("tools/example/source-manifest.json")
                data["files"]["file.txt"]["sha256"] = bad
                self.save("tools/example/source-manifest.json", data)
                self.refresh()
                self.assertIn("unreadable_file", self.codes())

    def test_invalid_included_flag_rejected(self):
        self.save("tools/example/source-manifest.json", {"license": "CC0-1.0", "files": [{"included": "false"}]})
        self.refresh()
        self.assertEqual(self.invoke()[0], 2)

    def test_pinned_file_hash(self):
        data = self.read("data/artifacts.json")
        data["artifacts"][0]["pinned_files"] = [{"path": "tools/example/file.txt", "sha256": "0" * 64}]
        self.save("data/artifacts.json", data)
        self.refresh()
        self.assertIn("hash_mismatch", self.codes())

    def test_unknown_schema_or_exclusions_rejected(self):
        data = self.read("data/artifacts.json")
        data["schema_version"] = "9.0"
        self.save("data/artifacts.json", data)
        self.assertEqual(self.invoke()[0], 2)
        data["schema_version"] = "1.0"
        self.save("data/artifacts.json", data)
        hashes = self.read("data/checksums.json")
        hashes["excluded"].append("everything/**")
        self.save("data/checksums.json", hashes)
        self.assertEqual(self.invoke()[0], 2)

    def test_file_and_json_size_limits(self):
        with patch.object(steward, "MAX_JSON_BYTES", 1), self.assertRaises(steward.InputError):
            self.report()
        with patch.object(steward, "MAX_HASH_BYTES", 1):
            self.assertIn("unreadable_file", self.codes())

    @unittest.skipUnless(hasattr(__import__("os"), "mkfifo"), "FIFO support required")
    def test_nonregular_file_rejected_without_open(self):
        import os
        os.mkfifo(self.root / "pipe")
        with self.assertRaises(steward.InputError):
            steward.digest(self.root, "pipe")

    def test_cli_success_json_error_and_no_writes(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        status, out, err = self.invoke("--format", "json")
        self.assertEqual((status, err), (0, ""))
        self.assertEqual(json.loads(out)["tool"], "Archive Steward")
        self.assertEqual(before, snapshot())
        self.write("unlisted.txt", "new")
        self.assertEqual(self.invoke()[0], 1)

    def test_terminal_control_characters_escaped(self):
        self.assertEqual(steward.line("title\n\x1b[31m"), "title\\n\\x1b[31m")

    def test_invalid_required_field_no_traceback(self):
        data = self.read("data/concepts.json")
        data["concepts"][0]["source_ids"] = [{}]
        self.save("data/concepts.json", data)
        status, _, err = self.invoke()
        self.assertEqual(status, 2)
        self.assertNotIn("Traceback", err)


    def test_compare_same_report_has_no_changes(self):
        report = self.report()
        diff = steward.compare_reports(report, report)
        for key in ("review_queue", "artifacts", "sources", "files", "findings"):
            self.assertFalse(any(diff[key].values()))

    def test_compare_changed_next_step_and_limit(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["review_queue"][0]["next_step"] = "Try one documented experiment."
        after["review_queue"][0]["limitations"] = "Scope remains narrow."
        fields = steward.compare_reports(before, after)["review_queue"]["changed"][0]["fields"]
        self.assertEqual([f["field"] for f in fields], ["limitations", "next_step"])
        self.assertEqual(fields[1]["before"], "Run a bounded test.")

    def test_compare_rights_and_verification_fields(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["artifacts"][0]["rights"]["license_declared"] = "unknown"
        after["artifacts"][0]["rights"]["scope"] = "New limited scope."
        after["artifacts"][0]["verification"]["status"] = "historical_only"
        fields = steward.compare_reports(before, after)["artifacts"]["changed"][0]["fields"]
        self.assertEqual([f["field"] for f in fields], ["rights.license_declared", "rights.scope", "verification.status"])

    def test_compare_added_removed_concepts(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["review_queue"][0]["id"] = "C-2"
        diff = steward.compare_reports(before, after)["review_queue"]
        self.assertEqual(diff["added"][0]["id"], "C-2")
        self.assertEqual(diff["removed"][0]["id"], "C-1")
        self.assertEqual(diff["changed"], [])

    def test_compare_per_source_and_access_counts(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["source_inventory"][0]["access"] = "public_source"
        after["source_access_counts"] = {"public_source": 1}
        diff = steward.compare_reports(before, after)
        self.assertEqual(diff["sources"]["changed"][0]["fields"][0]["field"], "access")
        self.assertEqual(len(diff["source_access_counts"]), 2)

    def test_compare_changed_bytes_after_baseline_refresh(self):
        before = self.report()
        self.write("tools/example/README.md", "updated review record")
        self.refresh()
        after = self.report()
        self.assertEqual(after["summary"]["errors"], 0)
        self.assertIn("tools/example/README.md", steward.compare_reports(before, after)["files"]["changed"])

    def test_compare_added_removed_files(self):
        before = self.report()
        self.write("new.txt", "new bytes")
        (self.root / "tools/example/file.txt").unlink()
        diff = steward.compare_reports(before, self.report())["files"]
        self.assertEqual(diff["added"], ["new.txt"])
        self.assertEqual(diff["removed"], ["tools/example/file.txt"])

    def test_compare_hashes_unlisted_files(self):
        self.write("new.txt", "first")
        before = self.report()
        self.write("new.txt", "second")
        after = self.report()
        self.assertIn("new.txt", steward.compare_reports(before, after)["files"]["changed"])
        self.assertEqual(after["hash_checks"]["unlisted_snapshot"], 1)

    def test_compare_unreadable_files_are_not_unchanged(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["file_snapshot"]["LICENSE"] = None
        diff = steward.compare_reports(before, after)
        self.assertEqual(diff["files"]["uncompared"], ["LICENSE"])
        self.assertTrue(any("could not be hashed" in item for item in diff["limitations"]))

    def test_compare_findings_introduced_and_no_longer_reported(self):
        before = self.report()
        self.write("new.txt", "new")
        after = self.report()
        forward = steward.compare_reports(before, after)
        reverse = steward.compare_reports(after, before)
        self.assertEqual(forward["findings"]["introduced"][0]["code"], "unlisted_file")
        self.assertEqual(reverse["findings"]["no_longer_reported"][0]["code"], "unlisted_file")

    def test_compare_legacy_report_reports_missing_coverage(self):
        after = self.report()
        before = copy.deepcopy(after)
        before["version"] = "0.1.0"
        for key in ("report_schema_version", "file_snapshot", "source_inventory"):
            before.pop(key)
        diff = steward.compare_reports(before, after)
        self.assertIsNone(diff["files"])
        self.assertIsNone(diff["sources"])
        self.assertTrue(any("Version 0.1" in item for item in diff["limitations"]))

    def test_compare_rejects_unknown_schema_or_non_report(self):
        report = self.report()
        for bad in ({}, dict(report, report_schema_version="999"), dict(report, tool="other")):
            with self.subTest(bad=bad.get("tool")), self.assertRaises(steward.InputError):
                steward.compare_reports(bad, report)

    def test_compare_rejects_malformed_records(self):
        report = self.report()
        bad_records = [dict(report, review_queue=[{}]), dict(report, file_snapshot={"a": "not-a-hash"}),
                       dict(report, source_access_counts={"private": True}), dict(report, findings=[{"level": "info"}])]
        for bad in bad_records:
            with self.subTest(keys=list(bad)), self.assertRaises(steward.InputError):
                steward.compare_reports(bad, report)

    def test_compare_never_opens_paths_from_report(self):
        before = self.report()
        before["file_snapshot"]["../../do-not-open"] = "0" * 64
        after = self.report()
        with patch.object(steward, "digest", side_effect=AssertionError("unexpected file access")):
            diff = steward.compare_reports(before, after)
        self.assertIn("../../do-not-open", diff["files"]["removed"])

    def test_compare_cli_json_can_be_compared_again_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = Path(directory) / "previous.json"
            previous.write_text(json.dumps(self.report()))
            original = previous.read_bytes()
            status, out, err = self.invoke("--compare", str(previous), "--format", "json")
            self.assertEqual((status, err), (0, ""))
            current = json.loads(out)
            self.assertIn("comparison", current)
            self.assertEqual(previous.read_bytes(), original)
            self.assertEqual(steward.compare_reports(current, self.report())["files"]["changed"], [])

    def test_compare_cli_text_keeps_persistent_errors_visible(self):
        self.write("unlisted.txt", "unlisted")
        with tempfile.TemporaryDirectory() as directory:
            previous = Path(directory) / "previous.json"
            previous.write_text(json.dumps(self.report()))
            status, out, _ = self.invoke("--compare", str(previous))
            self.assertEqual(status, 1)
            self.assertIn("All current findings", out)
            self.assertIn("unlisted_file: unlisted.txt", out)
            self.assertIn("No finding changes.", out)

    def test_compare_cli_missing_or_bad_report_returns_two(self):
        self.assertEqual(self.invoke("--compare", str(self.root / "absent.json"))[0], 2)
        self.write("invalid.json", "{}")
        status, _, err = self.invoke("--compare", str(self.root / "invalid.json"))
        self.assertEqual(status, 2)
        self.assertNotIn("Traceback", err)

    def test_compare_selected_report_allows_explicit_parent_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "child").mkdir()
            (root / "previous.json").write_text(json.dumps(self.report()))
            self.assertEqual(steward.read_selected_report(root / "child/../previous.json")["tool"], "Archive Steward")

    def test_compare_selected_report_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "previous.json").write_text(json.dumps(self.report()))
            (root / "link.json").symlink_to(root / "previous.json")
            with self.assertRaises(steward.InputError):
                steward.read_selected_report(root / "link.json")

    def test_comparison_text_escapes_control_characters(self):
        before = self.report()
        after = copy.deepcopy(before)
        after["review_queue"][0]["next_step"] = "Injected\n\x1b[31m"
        after["comparison"] = steward.compare_reports(before, after)
        rendered = steward.render_comparison(after)
        self.assertNotIn("\x1b", rendered)
        self.assertIn("Injected\\n\\x1b[31m", rendered)


    def test_compare_invalid_finding_level_returns_two(self):
        for level in ([], {}):
            with self.subTest(level=level), tempfile.TemporaryDirectory() as directory:
                report = self.report()
                report["findings"] = [{"level": level, "code": "x", "subject": "x", "message": "x"}]
                previous = Path(directory) / "previous.json"
                previous.write_text(json.dumps(report))
                status, _, err = self.invoke("--compare", str(previous))
                self.assertEqual(status, 2)
                self.assertNotIn("Traceback", err)

    def test_incomplete_walk_withholds_added_removed_file_claims(self):
        before = self.report()
        real_walk = steward.os.walk
        def incomplete_walk(root, *, followlinks, onerror):
            for base, dirs, names in real_walk(root, followlinks=followlinks, onerror=onerror):
                if Path(base) == self.root:
                    dirs.remove("tools")
                    onerror(PermissionError("fixture unreadable directory"))
                yield base, dirs, names
        with patch.object(steward.os, "walk", incomplete_walk):
            after = self.report()
        self.assertFalse(after["file_inventory_complete"])
        diff = steward.compare_reports(before, after)
        self.assertEqual(diff["files"]["removed"], [])
        self.assertIn("tools/example/file.txt", diff["files"]["uncompared_presence"])
        # Reversing the comparison must not invent new additions either.
        reverse = steward.compare_reports(after, before)
        self.assertEqual(reverse["files"]["added"], [])
        self.assertIn("tools/example/file.txt", reverse["files"]["uncompared_presence"])

    def test_directory_symlink_marks_inventory_incomplete(self):
        (self.root / "linked-dir").symlink_to(self.root / "tools", target_is_directory=True)
        self.assertFalse(self.report()["file_inventory_complete"])

    def test_compare_requires_inventory_coverage_flag(self):
        report = self.report()
        for flag in (None, "true", 1):
            with self.subTest(flag=flag), self.assertRaises(steward.InputError):
                steward.compare_reports(dict(report, file_inventory_complete=flag), report)


if __name__ == "__main__":
    unittest.main()
