#!/usr/bin/env python3
"""Offline, read-only structural audit. Does not establish scientific truth or safety."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

VERSION = "0.1.0"
MAX_BYTES = 5 * 1024 * 1024
MAX_NODES = 100_000
MAX_DEPTH = 40
LIMITATIONS = [
    "Local JSON structure and explicitly documented provenance only; not scientific validation.",
    "Links are checked for HTTP(S) syntax only. No DNS, network, source-content, license, or retraction checks occur.",
    "A resolvable citation or documented score is not proof of relevance, support, reproducibility, or efficacy.",
    "Missing provenance means not documented in the audited fields, not that evidence does not exist elsewhere.",
    "Empty contradicting evidence does not mean no contradictory research exists. Prose contradictions are not assessed.",
    "No clinical recommendations, efficacy predictions, treatment rankings, or patient-data processing are provided.",
    "Not a complete JSON Schema validator. Only the documented rules and input files are covered.",
]


class InputError(ValueError):
    pass


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def finite(value):
    return type(value) in (int, float) and (isinstance(value, int) or math.isfinite(value))


def pointer(base, key):
    return base + "/" + str(key).replace("~", "~0").replace("/", "~1")


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("Duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(_):
    raise InputError("Non-finite JSON number")


def load_json(path):
    # Open nonblocking before inspecting the descriptor: a FIFO/device cannot hang the audit.
    import os
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise InputError("Input must be a regular file")
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise InputError("Input exceeds 5 MiB limit")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs,
                          parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise InputError("Invalid UTF-8 JSON, duplicate key, or non-finite number") from exc
    todo, nodes = [(data, 0)], 0
    while todo:
        value, depth = todo.pop()
        nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            raise InputError("Input exceeds node/depth limit")
        if isinstance(value, dict):
            todo.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            todo.extend((v, depth + 1) for v in value)
        elif type(value) is float and not math.isfinite(value):
            raise InputError("Non-finite JSON number")
    if not isinstance(data, dict):
        raise InputError("Root must be an object")
    return data, hashlib.sha256(raw).hexdigest()


def valid_url(value):
    """Syntax only; never dereferences a URL and does not certify a public/safe host."""
    if not nonblank(value) or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value):
        return False
    if "\\" in value or re.search(r"%(?![0-9a-fA-F]{2})", value):
        return False
    try:
        url = urlsplit(value)
        return (url.scheme in ("http", "https") and bool(url.hostname)
                and url.username is None and url.password is None
                and (url.port is None or 1 <= url.port <= 65535)
                and all(c not in url.netloc for c in '<>"{}|^`'))
    except ValueError:
        return False


class Audit:
    def __init__(self):
        self.findings = []
        self.metrics = {}
        self.sources = {}
        self.claims = {}

    def add(self, severity, code, location, message):
        self.findings.append(dict(severity=severity, code=code, location=location, message=message))

    def objects(self, obj, key, loc, required=True):
        where = pointer(loc, key)
        value = obj.get(key)
        if value is None and not required and key not in obj:
            return []
        if not isinstance(value, list):
            self.add("error", "INVALID_COLLECTION", where, "Expected an array of objects.")
            return []
        if required and not value:
            self.add("warning", "EMPTY_COLLECTION", where, "Required collection contains no records to inspect.")
        rows = []
        seen = set()
        for i, row in enumerate(value):
            here = pointer(where, i)
            if not isinstance(row, dict):
                self.add("error", "INVALID_RECORD", here, "Expected an object.")
                continue
            ident = row.get("id")
            if not nonblank(ident):
                self.add("error", "MISSING_ID", here, "Expected a nonempty string id.")
            elif ident in seen:
                self.add("error", "DUPLICATE_ID", here, "Duplicate id in this collection.")
            else:
                seen.add(ident)
            rows.append((row, here))
        return rows

    def refs(self, obj, field, loc, registry):
        """Return distinct valid references. Every malformed/unknown reference is reported."""
        if field not in obj:
            return set()
        value, found = obj[field], set()
        here = pointer(loc, field)
        if not isinstance(value, list):
            self.add("error", "INVALID_REFERENCES", here, "Expected an array of nonempty string IDs.")
            return found
        seen = set()
        for i, ident in enumerate(value):
            at = pointer(here, i)
            if not nonblank(ident):
                self.add("error", "INVALID_REFERENCE", at, "Expected a nonempty string ID.")
            elif ident in seen:
                self.add("error", "DUPLICATE_REFERENCE", at, "Repeated reference must not inflate evidence counts.")
            else:
                seen.add(ident)
                if ident not in registry:
                    self.add("error", "UNKNOWN_REFERENCE", at, "ID does not resolve in the audited registry.")
                elif registry[ident]:
                    found.add(ident)
        return found

    def sources_for(self, obj, loc):
        direct = self.refs(obj, "source_ids", loc, self.sources)
        direct |= self.refs(obj, "supporting_sources", loc, self.sources)
        evidence = self.refs(obj, "supporting_evidence", loc, {**self.sources, **self.claims})
        return direct | evidence

    def count(self, obj, key, actual, loc):
        if key not in obj:
            return
        value = obj[key]
        if type(value) is not int or value < 0:
            self.add("error", "INVALID_COUNT", pointer(loc, key), "Count must be a nonnegative integer, not a boolean.")
        elif value != actual:
            self.add("error", "COUNT_MISMATCH", pointer(loc, key),
                     f"Declared {value}; corresponding complete array contains {actual} records.")

    def score(self, obj, key, loc, require_method=True):
        if key not in obj:
            return
        value = obj[key]
        if not finite(value) or not 0 <= value <= 1:
            self.add("error", "INVALID_SCORE", pointer(loc, key), "Expected a finite number in [0, 1], not a boolean.")
        provenance = obj.get("score_provenance", {})
        record = provenance.get(key) if isinstance(provenance, dict) else None
        if "score_provenance" in obj and not isinstance(provenance, dict):
            self.add("error", "INVALID_SCORE_PROVENANCE", pointer(loc, "score_provenance"), "Expected an object of score fields to provenance records.")
        if (require_method or record is not None) and (not isinstance(record, dict) or not nonblank(record.get("method"))):
            self.add("warning", "SCORE_METHOD_UNDOCUMENTED", pointer(loc, key),
                     "No nonempty score_provenance method is documented for this numeric score. A score is not an effect estimate.")
        if isinstance(record, dict) and "source_ids" in record:
            self.refs(record, "source_ids", pointer(pointer(loc, "score_provenance"), key), self.sources)

    def confidence(self, obj, field, loc, refs):
        if field in obj and (not isinstance(obj[field], str) or obj[field] not in {"established", "high", "moderate", "low", "open_question"}):
            self.add("error", "INVALID_CONFIDENCE", pointer(loc, field), "Expected established, high, moderate, low, or open_question.")
        if field in obj and obj[field] != "open_question" and not refs:
            self.add("warning", "CONFIDENCE_WITHOUT_CITATION", pointer(loc, field),
                     "Confidence label has no resolvable source/claim link in the audited citation fields.")

    def evidence(self, pack):
        rows = self.objects(pack, "sources", "evidence")
        ids = Counter(r.get("id") for r, _ in rows if nonblank(r.get("id")))
        for row, loc in rows:
            valid = any(valid_url(row.get(k)) for k in ("url", "source_url"))
            if not valid:
                self.add("error", "SOURCE_URL_MISSING_OR_INVALID", loc,
                         "Source needs a syntactically valid HTTP(S) url or source_url without credentials.")
            # An additional malformed URL is not hidden by a second valid URL.
            for key in ("url", "source_url"):
                if key in row and not valid_url(row[key]) and valid:
                    self.add("error", "INVALID_SOURCE_URL", pointer(loc, key), "Malformed HTTP(S) source URL.")
            ident = row.get("id")
            if nonblank(ident):
                self.sources[ident] = valid and ids[ident] == 1
        claims = self.objects(pack, "claims", "evidence")
        counts = Counter(r.get("id") for r, _ in claims if nonblank(r.get("id")))
        collisions = {row["id"] for row, _ in claims if nonblank(row.get("id")) and row["id"] in self.sources}
        for ident in collisions:
            self.sources[ident] = False
        for row, loc in claims:
            links = self.refs(row, "source_ids", loc, self.sources)
            if not links:
                self.add("warning", "CLAIM_WITHOUT_CITATION", loc, "Claim has no resolvable source link with a valid URL.")
            ident = row.get("id")
            if nonblank(ident):
                if ident in self.sources:
                    self.add("error", "AMBIGUOUS_EVIDENCE_ID", loc, "Claim and source share an ID.")
                    self.sources[ident] = False
                self.claims[ident] = bool(links) and counts[ident] == 1 and ident not in self.sources
        self.metrics.update(source_records=len(rows), claim_records=len(claims))

    def network(self, network):
        pathways = self.objects(network, "pathways", "network")
        interventions = self.objects(network, "interventions", "network")
        pids = {r["id"]: True for r, _ in pathways if nonblank(r.get("id"))}
        iids = {r["id"]: True for r, _ in interventions if nonblank(r.get("id"))}
        mechanism_count = effects_count = literature_sum = 0
        mechanism_ids = set()
        for row, loc in pathways:
            links = self.sources_for(row, loc)
            for field in ("als_relevance", "aging_relevance"):
                self.score(row, field, loc)
            if not links:
                self.add("warning", "PATHWAY_WITHOUT_CITATION", loc, "No resolvable pathway-level citation is documented.")
            if "literature_count" in row:
                count = row["literature_count"]
                if type(count) is not int or count < 0:
                    self.add("error", "INVALID_COUNT", pointer(loc, "literature_count"), "Expected a nonnegative integer.")
                else:
                    literature_sum += count
                    refs = self.refs(row, "literature_source_ids", loc, self.sources)
                    if "literature_source_ids" not in row and count > 0:
                        self.add("warning", "LITERATURE_COUNT_UNENUMERATED", pointer(loc, "literature_count"),
                                 "Nonzero count has no literature_source_ids list. The selected evidence pack is not assumed exhaustive.")
                    elif "literature_source_ids" in row and len(refs) != count:
                        self.add("error", "LITERATURE_COUNT_UNRECONCILED", pointer(loc, "literature_count"),
                                 f"Count {count} does not reconcile with {len(refs)} distinct resolvable literature_source_ids.")
            mechanisms = self.objects(row, "mechanisms", loc, required=False)
            mechanism_count += len(mechanisms)
            for mechanism, mloc in mechanisms:
                ident = mechanism.get("id")
                if nonblank(ident):
                    if ident in mechanism_ids:
                        self.add("error", "DUPLICATE_MECHANISM_ID", mloc, "Mechanism ID repeats across pathways.")
                    mechanism_ids.add(ident)
                refs = self.sources_for(mechanism, mloc)
                if not refs:
                    self.add("warning", "MECHANISM_WITHOUT_CITATION", mloc, "No resolvable mechanism-level citation is documented.")
                self.confidence(mechanism, "evidence_confidence", mloc, refs)
        for row, loc in interventions:
            links = self.sources_for(row, loc)
            self.confidence(row, "evidence_level", loc, links)
            self.refs({"target_pathway": [row.get("target_pathway")]}, "target_pathway", loc, pids)
            effects = row.get("known_effects", {})
            if not isinstance(effects, dict):
                self.add("error", "INVALID_EFFECTS", pointer(loc, "known_effects"), "Expected an object of pathway IDs to numbers.")
                continue
            provenance = row.get("effect_provenance", {})
            for target, value in effects.items():
                effects_count += 1
                where = pointer(pointer(loc, "known_effects"), target)
                if target not in pids:
                    self.add("error", "UNKNOWN_EFFECT_TARGET", where, "Effect target does not resolve to a pathway.")
                if not finite(value):
                    self.add("error", "INVALID_EFFECT_NUMBER", where, "Expected a finite number, not a boolean.")
                doc = provenance.get(target) if isinstance(provenance, dict) else None
                at = pointer(pointer(loc, "effect_provenance"), target)
                refs = self.refs(doc, "source_ids", at, self.sources) if isinstance(doc, dict) else set()
                illustrative = (isinstance(doc, dict) and doc.get("kind") == "illustrative" and nonblank(doc.get("note")))
                complete = (isinstance(doc, dict) and bool(refs)
                            and all(nonblank(doc.get(k)) for k in ("unit", "population", "endpoint", "timepoint")))
                if not illustrative and not complete:
                    self.add("warning", "EFFECT_PROVENANCE_INCOMPLETE", where,
                             "Coefficient lacks linked sources plus unit/population/endpoint/timepoint, or an explicit illustrative label and note. No efficacy meaning is inferred.")
        self.count(network, "pathway_count", len(pathways), "network")
        self.count(network, "intervention_count", len(interventions), "network")
        self.metrics.update(pathway_records=len(pathways), mechanism_records=mechanism_count,
                            intervention_records=len(interventions), effect_coefficients=effects_count,
                            literature_count_field_sum=literature_sum)
        return pids, iids

    def hypotheses(self, plan, pids, iids):
        # Only the current research-plan export shape is supported; do not silently audit the other exporter.
        rows = self.objects(plan, "all_hypotheses", "hypotheses")
        top = self.objects(plan, "top_hypotheses", "hypotheses")
        full = {r["id"]: r for r, _ in rows if nonblank(r.get("id"))}
        self.count(plan, "hypothesis_count", len(rows), "hypotheses")
        self.count(plan, "pathways_analyzed", self.metrics["pathway_records"], "hypotheses")
        self.count(plan, "interventions_reviewed", self.metrics["intervention_records"], "hypotheses")
        # Top list is allowed to be truncated. Never compare its length with total hypothesis_count.
        top_ids = {r.get("id") for r, _ in top if nonblank(r.get("id"))}
        for row, loc in rows:
            in_top = isinstance(row.get("id"), str) and row["id"] in top_ids
            self.score(row, "priority_score", loc, require_method=not in_top)
            # Summary rows need not duplicate top-detail provenance. Validate any details they do carry.
            links = self.sources_for(row, loc)
            if not in_top:
                self.confidence(row, "confidence", loc, links)
            elif "confidence" in row and (not isinstance(row["confidence"], str) or row["confidence"] not in {"established", "high", "moderate", "low", "open_question"}):
                self.add("error", "INVALID_CONFIDENCE", pointer(loc, "confidence"), "Invalid confidence label in summary row.")
            self.refs(row, "pathways", loc, pids)
            self.refs(row, "interventions", loc, iids)
            self.refs(row, "contradicting_evidence", loc, {**self.sources, **self.claims})
            if "experimental_approach" in row and not nonblank(row["experimental_approach"]):
                self.add("warning", "EXPERIMENT_UNDOCUMENTED", loc, "Present experimental_approach is empty in summary row.")
        for row, loc in top:
            ident = row.get("id")
            original = full.get(ident) if isinstance(ident, str) else None
            if original is None:
                self.add("error", "TOP_ID_NOT_IN_ALL", loc, "Top hypothesis ID is absent from all_hypotheses.")
            else:
                for field in ("type", "statement", "confidence", "priority_score"):
                    if field in row and field in original and (row[field] != original[field] or ((isinstance(row[field], bool) or isinstance(original[field], bool)) and type(row[field]) != type(original[field]))):
                        self.add("error", "HYPOTHESIS_FIELD_CONFLICT", pointer(loc, field),
                                 "Top and all_hypotheses representations disagree on this exact field.")
            self.score(row, "priority_score", loc)
            refs = self.sources_for(row, loc)
            if not refs:
                self.add("warning", "HYPOTHESIS_WITHOUT_CITATION", loc,
                         "No resolvable supporting source/claim link is exported. Evidence may have been omitted by the exporter.")
            self.confidence(row, "confidence", loc, refs)
            if "contradicting_evidence" not in row:
                self.add("warning", "CONTRADICTION_REVIEW_UNDOCUMENTED", loc, "Contradicting-evidence field is absent; review status cannot be inferred.")
            else:
                self.refs(row, "contradicting_evidence", loc, {**self.sources, **self.claims})
            if not nonblank(row.get("experimental_approach")):
                self.add("warning", "EXPERIMENT_UNDOCUMENTED", loc, "No nonempty experimental_approach is exported; no protocol has been assessed.")
            self.refs(row, "pathways", loc, pids)
            self.refs(row, "interventions", loc, iids)
        self.metrics.update(hypothesis_records=len(rows), top_hypothesis_records=len(top))

    def run(self, evidence, network, hypotheses):
        for name, doc in (("evidence", evidence), ("network", network), ("hypotheses", hypotheses)):
            if doc.get("schema_version") != "1.0":
                self.add("error", "UNSUPPORTED_VERSION", name + "/schema_version", "Expected schema_version string 1.0.")
        self.evidence(evidence)
        pids, iids = self.network(network)
        self.hypotheses(hypotheses, pids, iids)
        self.findings.sort(key=lambda f: (f["location"], f["code"], f["message"]))
        counts = Counter(f["severity"] for f in self.findings)
        return {"audit_version": VERSION,
                "status": "needs_review" if self.findings else "no_findings_within_scope",
                "summary": {"errors": counts["error"], "warnings": counts["warning"]},
                "metrics": self.metrics, "findings": self.findings, "limitations": LIMITATIONS}


def display_text(report):
    print("Evidence integrity audit: " + report["status"])
    print("STRUCTURE/PROVENANCE ONLY. Not scientific validation or clinical guidance.")
    for role, item in report.get("inputs", {}).items():
        print(f"Input {role}: {json.dumps(item['path'])}; SHA-256 {item['sha256']}")
    print("Summary: " + json.dumps(report["summary"], sort_keys=True))
    if "metrics" in report:
        print("Observed metrics: " + json.dumps(report["metrics"], sort_keys=True))
        print("literature_count_field_sum sums declared fields; it is NOT a verified or deduplicated reference count.")
    for item in report["findings"]:
        # JSON quoting escapes terminal control characters in paths/IDs from untrusted JSON.
        print(f"[{item['severity'].upper()}] {item['code']} {json.dumps(item['location'])}: {item['message']}")
    print("Limitations:")
    for item in report["limitations"]:
        print("- " + item)


def resolved(path):
    try:
        return path.resolve()
    except RuntimeError as exc:
        raise InputError("Cannot resolve input path, possibly a symlink loop") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Local repository or snapshot root (default: current directory)")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    names = {"evidence": "als-evidence.json", "network": "als-aging-pathways.json", "hypotheses": "als-aging-hypotheses.json"}
    docs, inputs = {}, {}
    role = "repository"
    try:
        root = resolved(args.repo)
        for role, name in names.items():
            path = root / "data" / "health" / name
            if not resolved(path).is_relative_to(root):
                raise InputError("Input symlink escapes the selected root")
            docs[role], digest = load_json(path)
            inputs[role] = {"path": str(path), "sha256": digest}
        report = Audit().run(**docs)
        code = 1 if report["findings"] else 0
    except (OSError, InputError, RecursionError) as exc:
        report = {"audit_version": VERSION, "status": "input_error", "summary": {"errors": 1, "warnings": 0},
                  "findings": [{"severity": "error", "code": "INPUT_ERROR", "location": role,
                                "message": f"Cannot audit input ({type(exc).__name__}); check file presence, regular-file type, JSON validity and documented size/depth limits."}],
                  "limitations": LIMITATIONS}
        code = 2
    report["inputs"] = inputs
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False))
    else:
        display_text(report)
    return code


if __name__ == "__main__":
    sys.exit(main())
