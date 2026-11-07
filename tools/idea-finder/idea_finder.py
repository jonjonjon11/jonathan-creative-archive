#!/usr/bin/env python3
"""Idea Finder 0.1: search the archive's public metadata, entirely offline."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import stat
import sys
import unicodedata

VERSION = "0.1.0"
MAX_JSON_BYTES = 4 * 1024 * 1024
STATUSES = ("idea", "documented_design", "artifact_delivery_record", "source_inspected",
            "historical_test_report", "runtime_verified", "review_gap", "editorial_proposal")
SCIENCE_STANDINGS = ("established_model_scoped", "design_mapping", "speculative_unvalidated",
                     "not_a_scientific_claim", "insufficient_evidence")
RIGHTS_FIELDS = ("license_declared", "license_path", "scope", "review_record")
VERIFICATION_FIELDS = ("status", "record", "limitations")
WEIGHTS = {"id": 5, "title": 5, "tags": 4, "summary": 2, "next_step": 1}
LIMITS = [
    "Search covers concept IDs, titles, tags, summaries and next steps, not full documents or source code.",
    "Matches use literal case-insensitive substrings, not semantic search or independent fact checking.",
    "Ranking measures text matches, not quality, evidence strength, urgency or scientific confidence.",
    "Source access, rights and verification claims are copied from local metadata, not freshly verified.",
    "Related artifacts share source IDs; that does not prove they implement the matched concept.",
    "No network, credentials, source execution, edits, scheduling or publication.",
]


class InputError(ValueError):
    pass


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be nonempty text")
    return value


def text_list(value, label):
    if not isinstance(value, list) or not value:
        raise InputError(f"{label} must be a nonempty list")
    for item in value:
        text(item, label)
    if len(value) != len(set(value)):
        raise InputError(f"{label} contains duplicates")
    return value


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("duplicate JSON object key")
        result[key] = value
    return result


def read_records(root, relative, key):
    path = root
    for part in relative.split("/"):
        path = path / part
        if path.is_symlink():
            raise InputError(f"{relative}: symbolic links are not followed")
    if not stat.S_ISREG(path.stat().st_mode):
        raise InputError(f"{relative}: not a regular file")
    # Read a bounded amount even if a file grows after the initial size check.
    with path.open("rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise InputError(f"{relative}: exceeds 4 MiB input limit")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_keys)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError(f"{relative}: invalid UTF-8 JSON or excessive nesting") from exc
    if not isinstance(data, dict) or data.get("schema_version") != "1.0" or not isinstance(data.get(key), list):
        raise InputError(f"{relative}: expected schema 1.0 and a {key} list")
    result = {}
    for record in data[key]:
        if not isinstance(record, dict):
            raise InputError(f"{key} entries must be objects")
        ident = text(record.get("id"), f"{key} ID")
        text(record.get("title"), f"{ident} title")
        if ident in result:
            raise InputError(f"duplicate {key} ID")
        result[ident] = record
    return result


def load_archive(root):
    try:
        root = Path(root).resolve(strict=True)
    except RuntimeError as exc:
        raise InputError("archive root cannot be resolved, possibly due to a symlink loop") from exc
    if not root.is_dir():
        raise InputError("archive root must be a directory")
    concepts = read_records(root, "data/concepts.json", "concepts")
    sources = read_records(root, "sources/manifest.json", "sources")
    artifacts = read_records(root, "data/artifacts.json", "artifacts")
    for ident, source in sources.items():
        for key in ("evidence_class", "access", "findings", "limitations"):
            text(source.get(key), f"{ident} {key}")
    for ident, concept in concepts.items():
        for key in ("summary", "artifact_status", "scientific_standing", "limitations", "next_step"):
            text(concept.get(key), f"{ident} {key}")
        if concept["artifact_status"] not in STATUSES:
            raise InputError(f"{ident}: unknown artifact status")
        if concept["scientific_standing"] not in SCIENCE_STANDINGS:
            raise InputError(f"{ident}: unknown scientific standing")
        text_list(concept.get("tags"), f"{ident} tags")
        refs = text_list(concept.get("source_ids"), f"{ident} source_ids")
        if any(ref not in sources for ref in refs):
            raise InputError(f"{ident}: unresolved source reference")
    for ident, artifact in artifacts.items():
        text(artifact.get("path"), f"{ident} path")
        refs = text_list(artifact.get("source_ids"), f"{ident} source_ids")
        if any(ref not in sources for ref in refs):
            raise InputError(f"{ident}: unresolved source reference")
        for group, fields in (("rights", RIGHTS_FIELDS), ("verification", VERIFICATION_FIELDS)):
            value = artifact.get(group)
            if not isinstance(value, dict):
                raise InputError(f"{ident}: {group} must be an object")
            for key in fields:
                text(value.get(key), f"{ident} {group}.{key}")
    return concepts, sources, artifacts


def normalize(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def find(root, query="", tags=(), status=None, limit=5):
    if not isinstance(query, str) or len(query) > 500:
        raise InputError("query must be text of at most 500 characters")
    terms = list(dict.fromkeys(normalize(query).split()))
    if len(terms) > 16:
        raise InputError("query may contain at most 16 distinct terms")
    if type(limit) is not int or not 1 <= limit <= 20:
        raise InputError("limit must be between 1 and 20")
    if status is not None and status not in STATUSES:
        raise InputError("unknown status filter")
    if not isinstance(tags, (list, tuple)):
        raise InputError("tag filters must be a list or tuple")
    wanted_tags = {normalize(text(tag, "tag filter")) for tag in tags}
    concepts, sources, artifacts = load_archive(root)
    matches = []
    for ident, concept in concepts.items():
        actual_tags = {normalize(tag) for tag in concept["tags"]}
        if not wanted_tags <= actual_tags or status is not None and concept["artifact_status"] != status:
            continue
        fields = {key: [normalize(value) for value in concept[key]] if key == "tags" else [normalize(concept[key])]
                  for key in WEIGHTS}
        score, matched_fields = 0, set()
        for term in terms:
            hits = [key for key, values in fields.items() if any(term in value for value in values)]
            if not hits:
                break
            matched_fields.update(hits)
            score += max(WEIGHTS[key] for key in hits)
        else:
            matches.append((score, ident, concept, sorted(matched_fields)))
    matches.sort(key=lambda item: (-item[0], item[1]))
    results = []
    for score, ident, concept, matched_fields in matches[:limit]:
        entry = {key: concept[key] for key in ("id", "title", "tags", "summary", "artifact_status",
                                                "scientific_standing", "limitations", "next_step", "source_ids")}
        entry["match"] = {"text_score": score, "matched_fields": matched_fields}
        entry["sources"] = [{key: sources[ref][key] for key in ("id", "title", "evidence_class", "access", "findings", "limitations")}
                            for ref in sorted(concept["source_ids"])]
        entry["related_artifacts"] = []
        for artifact_id, artifact in sorted(artifacts.items()):
            common = sorted(set(concept["source_ids"]) & set(artifact["source_ids"]))
            if common:
                # Paths and statements here are copied as data, never opened or executed.
                entry["related_artifacts"].append({"id": artifact_id, "title": artifact["title"], "path": artifact["path"],
                                                   "shared_source_ids": common,
                                                   "rights": {key: artifact["rights"][key] for key in RIGHTS_FIELDS},
                                                   "verification": {key: artifact["verification"][key] for key in VERIFICATION_FIELDS}})
        results.append(entry)
    return {"tool": "Idea Finder", "version": VERSION, "query": query,
            "filters": {"tags": sorted(wanted_tags), "status": status, "limit": limit}, "terms": terms,
            "total_matches": len(matches), "returned": len(results), "omitted": max(0, len(matches) - limit),
            "available_tags": sorted({tag for concept in concepts.values() for tag in concept["tags"]}),
            "status_counts": dict(sorted(Counter(c["artifact_status"] for c in concepts.values()).items())),
            "results": results, "limitations": LIMITS}


def line(value):
    return str(value).encode("unicode_escape").decode("ascii")


def render(report):
    out = [f"Idea Finder {VERSION} | offline concept search",
           f"{report['total_matches']} matches; showing {report['returned']}; omitted {report['omitted']}.",
           "Read-only metadata search; no implementation or rights clearance is implied."]
    if report["terms"]:
        out.append("Required text terms: " + ", ".join(map(line, report["terms"])))
    if report["filters"]["tags"] or report["filters"]["status"]:
        out.append("Filters: " + line(json.dumps(report["filters"], sort_keys=True)))
    for result in report["results"]:
        out.extend(["", f"{line(result['id'])}: {line(result['title'])}",
                    f"Status: {line(result['artifact_status'])}; science: {line(result['scientific_standing'])}",
                    "Tags: " + ", ".join(map(line, result["tags"])),
                    "Summary: " + line(result["summary"]), "Next step: " + line(result["next_step"]),
                    "Known limits: " + line(result["limitations"]),
                    "Matched fields: " + (", ".join(result["match"]["matched_fields"]) or "browse/filter only"),
                    "Source records (not live-checked):"])
        for source in result["sources"]:
            out.extend([f"- {line(source['id'])}: {line(source['title'])} [{line(source['evidence_class'])}; {line(source['access'])}]",
                        "  Recorded finding: " + line(source["findings"]), "  Source limit: " + line(source["limitations"])])
        out.append("Related included artifacts (shared source IDs, not proof of implementation):")
        for artifact in result["related_artifacts"]:
            out.extend([f"- {line(artifact['title'])}: {line(artifact['path'])}",
                        f"  Declared license: {line(artifact['rights']['license_declared'])}; scope: {line(artifact['rights']['scope'])}",
                        "  Shared source IDs: " + ", ".join(map(line, artifact["shared_source_ids"])),
                        "  License record: " + line(artifact["rights"]["license_path"]),
                        "  Rights review record: " + line(artifact["rights"]["review_record"]),
                        f"  Verification declaration: {line(artifact['verification']['status'])}; limit: {line(artifact['verification']['limitations'])}",
                        "  Verification record: " + line(artifact["verification"]["record"])])
        if not result["related_artifacts"]:
            out.append("- None registered through this concept's source IDs; this does not prove no implementation exists elsewhere.")
    if not report["results"]:
        out.append("\nNo metadata matches. Try fewer terms, a different tag, or omit the query to browse.")
    if report["omitted"]:
        out.append("\nSome matches are omitted. Narrow the query/filters or raise --limit (maximum 20).")
    out.append("\nAvailable tags: " + ", ".join(map(line, report["available_tags"])))
    out.append("\nLimits:")
    out.extend("- " + value for value in report["limitations"])
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="explicit local archive root")
    parser.add_argument("query", nargs="?", default="", help="all whitespace-separated terms must match")
    parser.add_argument("--tag", action="append", default=[], help="exact tag; repeat to require multiple tags")
    parser.add_argument("--status", choices=STATUSES)
    parser.add_argument("--limit", type=int, default=5, help="maximum results, from 1 to 20")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        report = find(args.root, args.query, args.tag, args.status, args.limit)
    except (InputError, OSError, ValueError) as exc:
        detail = str(exc) if isinstance(exc, InputError) else "Required local input is missing or unreadable."
        print("Idea Finder input error: " + line(detail), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) if args.format == "json" else render(report),
          end="\n" if args.format == "json" else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
