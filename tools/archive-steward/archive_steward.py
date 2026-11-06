#!/usr/bin/env python3
"""Archive Steward 0.1: deterministic, read-only, offline archive review aid."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

VERSION = "0.1.0"
NO_HASH = object()
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_HASH_BYTES = 64 * 1024 * 1024
STATUSES = {
    "idea", "documented_design", "artifact_delivery_record", "source_inspected",
    "historical_test_report", "runtime_verified", "review_gap", "editorial_proposal",
}
# This is a fixed, documented local-cache exclusion, not input-controlled globbing.
SKIP_DIRS = {".git", "__pycache__"}
SKIP_FILES = {".DS_Store"}
LIMITS = [
    "Metadata and license declarations are reported, not independently established.",
    "Hashes establish byte agreement with local records, not authenticity or safety.",
    "No network, subprocesses, source execution, edits or publication.",
    "No legal clearance, comprehensive secret scan, science review or runtime verification.",
]


class InputError(ValueError):
    """An input cannot be interpreted safely."""


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be nonempty text")
    return value


def require_list(value, label):
    if not isinstance(value, list):
        raise InputError(f"{label} must be a list")
    return value


def safe_path(root, value):
    """Reject traversal, platform-ambiguous names, and every symlink component."""
    require_text(value, "path")
    if "\\" in value or ":" in value or "\x00" in value:
        raise InputError("path contains unsupported characters")
    parts = value.split("/")
    if PurePosixPath(value).is_absolute() or any(p in {"", ".", ".."} for p in parts):
        raise InputError("path must be a normalized relative path without traversal")
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise InputError("symlink paths are not followed")
    return path


def regular_file(path):
    if not stat.S_ISREG(path.stat().st_mode):
        raise InputError("input is not a regular file")


def unique_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise InputError("duplicate JSON object key")
        obj[key] = value
    return obj


def read_json(root, rel):
    path = safe_path(root, rel)
    regular_file(path)
    if path.stat().st_size > MAX_JSON_BYTES:
        raise InputError(f"{rel}: JSON exceeds 4 MiB limit")
    try:
        result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError(f"{rel}: invalid UTF-8 JSON or excessive nesting") from exc
    if not isinstance(result, dict):
        raise InputError(f"{rel}: top level must be an object")
    return result


def digest(root, rel):
    path = safe_path(root, rel)
    regular_file(path)
    if path.stat().st_size > MAX_HASH_BYTES:
        raise InputError("file exceeds 64 MiB hash limit")
    total = 0
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(128 * 1024), b""):
            total += len(block)
            if total > MAX_HASH_BYTES:
                raise InputError("file exceeds 64 MiB hash limit")
            result.update(block)
    return result.hexdigest()


def record_map(data, key):
    records = require_list(data.get(key), key)
    result = {}
    for record in records:
        if not isinstance(record, dict):
            raise InputError(f"{key} entries must be objects")
        ident = require_text(record.get("id"), f"{key} ID")
        if ident in result:
            raise InputError(f"duplicate {key} ID: {ident}")
        require_text(record.get("title"), f"{ident} title")
        result[ident] = record
    return result


def inspect(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise InputError("archive root must be a directory")
    sources = record_map(read_json(root, "sources/manifest.json"), "sources")
    concepts = record_map(read_json(root, "data/concepts.json"), "concepts")
    registry = read_json(root, "data/artifacts.json")
    if registry.get("schema_version") != "1.0":
        raise InputError("data/artifacts.json: unsupported schema_version")
    artifacts = record_map(registry, "artifacts")
    baseline = read_json(root, "data/checksums.json")
    if baseline.get("algorithm") != "sha256" or not isinstance(baseline.get("files"), dict):
        raise InputError("data/checksums.json: expected sha256 files object")
    # No input-controlled exclusions: an altered baseline cannot silently hide files.
    if baseline.get("excluded") != ["data/checksums.json", ".git/**"]:
        raise InputError("data/checksums.json: unsupported exclusion list")
    findings = []
    checks = Counter()

    def issue(level, code, subject, message):
        findings.append({"level": level, "code": code, "subject": subject, "message": message})

    def check_file(rel, expected=NO_HASH, origin="file"):
        try:
            if expected is NO_HASH:
                path = safe_path(root, rel)
                regular_file(path)
                return True
            if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
                raise InputError("expected hash must be 64 lowercase hexadecimal characters")
            actual = digest(root, rel)
            checks[origin] += 1
            if actual != expected:
                issue("error", "hash_mismatch", rel, f"Bytes differ from {origin} record.")
                return False
            return True
        except (InputError, OSError, ValueError) as exc:
            # Avoid echoing file contents or absolute exception paths.
            detail = str(exc) if isinstance(exc, InputError) else "File is missing or unreadable."
            issue("error", "unreadable_file", str(rel), detail)
            return False

    expected_files = baseline["files"]
    for rel, expected in sorted(expected_files.items()):
        check_file(rel, expected, "archive_checksum")
    present = set()
    def walk_error(_):
        issue("error", "unreadable_directory", ".", "A directory could not be inventoried.")
    for base, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        for name in sorted(dirs[:]):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                issue("error", "symlink", rel, "Directory symlinks are not followed.")
                dirs.remove(name)
            elif name in SKIP_DIRS:
                dirs.remove(name)
        for name in sorted(names):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                issue("error", "symlink", rel, "File symlinks are not followed.")
                continue
            if name in SKIP_FILES or name.endswith(".pyc") or rel == "data/checksums.json":
                continue
            present.add(rel)
            if rel not in expected_files:
                issue("error", "unlisted_file", rel, "File has no archive checksum; review before adding it.")

    used_sources = set()
    statuses = Counter()
    queue = []
    for ident, concept in sorted(concepts.items()):
        status_value = require_text(concept.get("artifact_status"), f"{ident} artifact_status")
        if status_value not in STATUSES:
            issue("error", "unknown_status", ident, "Artifact status is not in the archive vocabulary.")
        statuses[status_value] += 1
        refs = require_list(concept.get("source_ids"), f"{ident} source_ids")
        if not refs:
            issue("error", "missing_sources", ident, "Concept has no source references.")
        for ref in refs:
            require_text(ref, f"{ident} source ID")
            if ref not in sources:
                issue("error", "unknown_source", ident, f"Unknown source ID: {ref}")
            else:
                used_sources.add(ref)
        included = concept.get("included_artifact")
        if included is not None:
            check_file(included)
        next_step = require_text(concept.get("next_step"), f"{ident} next_step")
        limitation = require_text(concept.get("limitations"), f"{ident} limitations")
        if status_value == "runtime_verified" and not concept.get("limited_verification"):
            issue("warning", "verification_record_needed", ident,
                  "Runtime label needs a separately reviewable exact-version test record.")
        category = "evidence_gap" if status_value in {"review_gap", "artifact_delivery_record", "historical_test_report"} else "next_experiment"
        queue.append({"id": ident, "title": concept["title"], "category": category,
                      "artifact_status": status_value, "next_step": next_step, "limitations": limitation})

    inventory = []
    for ident, artifact in sorted(artifacts.items()):
        prefix = require_text(artifact.get("path"), f"{ident} path")
        directory = safe_path(root, prefix)
        if not directory.is_dir():
            issue("error", "missing_artifact_directory", ident, "Registered artifact directory is missing or unreadable.")
        refs = require_list(artifact.get("source_ids"), f"{ident} source_ids")
        if not refs:
            issue("error", "missing_sources", ident, "Artifact has no source references.")
        for ref in refs:
            require_text(ref, f"{ident} source ID")
            if ref not in sources:
                issue("error", "unknown_source", ident, f"Unknown source ID: {ref}")
            else:
                used_sources.add(ref)
        rights = artifact.get("rights")
        verification = artifact.get("verification")
        if not isinstance(rights, dict) or not isinstance(verification, dict):
            raise InputError(f"{ident}: rights and verification must be objects")
        for key in ("license_declared", "license_path", "scope", "review_record"):
            require_text(rights.get(key), f"{ident} rights.{key}")
        for key in ("status", "record", "limitations"):
            require_text(verification.get(key), f"{ident} verification.{key}")
        check_file(rights["license_path"])
        check_file(rights["review_record"])
        check_file(verification["record"])
        if rights["license_declared"] == "unknown":
            issue("warning", "rights_review_needed", ident, "No license declaration recorded; human review needed.")
        independent_kinds = ("preserved_source", "generated_build", "pinned_artifact")
        checks_before = sum(checks[kind] for kind in independent_kinds)
        manifest_rel = artifact.get("preserved_manifest")
        if manifest_rel is not None:
            try:
                manifest = read_json(root, manifest_rel)
            except (InputError, OSError) as exc:
                raise InputError(f"{ident}: cannot read preserved manifest") from exc
            if manifest.get("license") != rights["license_declared"]:
                issue("error", "license_disagreement", ident, "Registry and preserved manifest declarations differ.")
            entries = manifest.get("files")
            if isinstance(entries, dict):
                for rel, entry in sorted(entries.items()):
                    if not isinstance(entry, dict):
                        raise InputError(f"{ident}: malformed preserved file entry")
                    check_file(prefix + "/" + rel, entry.get("sha256", ""), "preserved_source")
            elif isinstance(entries, list):
                for entry in entries:
                    if not isinstance(entry, dict) or type(entry.get("included")) is not bool:
                        raise InputError(f"{ident}: malformed included file entry")
                    if entry["included"]:
                        rel = require_text(entry.get("archive_path"), f"{ident} archive_path")
                        check_file(prefix + "/" + rel, entry.get("sha256", ""), "preserved_source")
                build = manifest.get("generated_build")
                if build is not None:
                    if not isinstance(build, dict):
                        raise InputError(f"{ident}: malformed generated_build")
                    rel = require_text(build.get("path"), f"{ident} generated path")
                    check_file(prefix + "/" + rel, build.get("sha256", ""), "generated_build")
            else:
                raise InputError(f"{ident}: unsupported preserved manifest format")
        for entry in require_list(artifact.get("pinned_files", []), f"{ident} pinned_files"):
            if not isinstance(entry, dict):
                raise InputError(f"{ident}: malformed pinned file entry")
            check_file(entry.get("path"), entry.get("sha256", ""), "pinned_artifact")
        if sum(checks[kind] for kind in independent_kinds) == checks_before:
            issue("warning", "independent_hashes_missing", ident,
                  "No preserved-source or pinned-file hashes were checked for this artifact.")
        inventory.append({"id": ident, "title": artifact["title"], "path": prefix,
                          "rights": rights, "verification": verification})

    access = Counter()
    for ident, source in sorted(sources.items()):
        access[require_text(source.get("access"), f"{ident} access")] += 1
    findings.sort(key=lambda x: (x["level"], x["code"], x["subject"], x["message"]))
    queue.sort(key=lambda x: (x["category"] != "evidence_gap", x["id"]))
    return {"tool": "Archive Steward", "version": VERSION,
            "summary": {"sources": len(sources), "concepts": len(concepts),
                        "registered_artifacts": len(artifacts), "inventoried_files": len(present),
                        "errors": sum(f["level"] == "error" for f in findings),
                        "warnings": sum(f["level"] == "warning" for f in findings)},
            "hash_checks": dict(sorted(checks.items())),
            "status_counts": dict(sorted(statuses.items())),
            "source_access_counts": dict(sorted(access.items())),
            "sources_without_concept_or_artifact_references": sorted(set(sources) - used_sources),
            "artifacts": inventory, "review_queue": queue, "findings": findings, "limitations": LIMITS}


def line(value):
    """Keep human-readable output one line; neutralize terminal control characters."""
    return str(value).encode("unicode_escape").decode("ascii")


def render(report):
    s = report["summary"]
    out = [f"Archive Steward {VERSION} | offline review report",
           f"{s['concepts']} concepts; {s['sources']} sources; {s['registered_artifacts']} registered artifacts; {s['inventoried_files']} inventoried files.",
           f"{s['errors']} errors; {s['warnings']} warnings. No files changed.", "", "Integrity checks:"]
    out.extend(f"- {key}: {value} files hashed" for key, value in report["hash_checks"].items())
    out.append("\nFindings:")
    out.extend(f"- {f['level'].upper()} {line(f['code'])}: {line(f['subject'])}: {line(f['message'])}" for f in report["findings"])
    if not report["findings"]:
        out.append("- No configured integrity/metadata problems found. This is not publication clearance.")
    out.append("\nDeclared rights and verification (not independently established):")
    for item in report["artifacts"]:
        out.append(f"- {line(item['title'])}: {line(item['rights']['license_declared'])}; {line(item['verification']['status'])}")
        out.append(f"  Scope: {line(item['rights']['scope'])}")
        out.append(f"  Limit: {line(item['verification']['limitations'])}")
    out.append("\nConcept status counts:")
    out.extend(f"- {line(key)}: {value}" for key, value in report["status_counts"].items())
    out.append("\nSource access counts (not live-checked):")
    out.extend(f"- {line(key)}: {value}" for key, value in report["source_access_counts"].items())
    orphaned = report["sources_without_concept_or_artifact_references"]
    out.append("Sources with no concept/artifact reference: " + (", ".join(map(line, orphaned)) or "none") + ". They may still be cited in prose.")
    out.append("\nReview queue (evidence gaps first, then stable ID; not a quality score):")
    for item in report["review_queue"]:
        out.append(f"- {line(item['id'])} [{line(item['category'])}] {line(item['title'])}: {line(item['next_step'])}")
        out.append(f"  Known limit: {line(item['limitations'])}")
    out.append("\nLimits:")
    out.extend("- " + value for value in report["limitations"])
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="local archive root (required; no home-directory search)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        report = inspect(args.root)
    except (InputError, OSError, ValueError) as exc:
        detail = str(exc) if isinstance(exc, InputError) else "Archive root or required input is missing or unreadable."
        print("Archive Steward input error: " + line(detail), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(render(report), end="")
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
