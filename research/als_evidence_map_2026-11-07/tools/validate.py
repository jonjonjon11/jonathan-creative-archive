#!/usr/bin/env python3
"""Offline checks for this small, versioned evidence-map schema, not scientific review."""
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"tofersen_sod1", "ulefnersen_fus", "qrl201_stmn2", "dnl343", "relyvrio_withdrawal", "unc13a_mechanism"}
KINDS = {"clinical_primary", "clinical_supportive", "clinical_exploratory", "safety_primary", "biomarker", "regulatory", "commercial_action", "mechanistic", "hypothesis"}
SOURCE_TYPES = {"peer_reviewed_trial", "peer_reviewed_mechanistic", "regulatory_label", "regulatory_summary", "regulatory_notice", "sponsor_press_release"}
STAGES = {"randomized_trial_and_regulatory_decision", "sponsor_reported_randomized_trial", "sponsor_reported_early_trial", "peer_reviewed_randomized_trial", "negative_trial_report_and_regulatory_withdrawal", "peer_reviewed_mechanistic_research"}
REGULATORY_STATUSES = {"approved", "original_accelerated_approval", "approval_withdrawn", "investigational_in_cited_source", "not_assessed", "not_applicable"}
REGULATORY_ACTIONS = {"approved", "original_accelerated_approval", "approval_withdrawn"}
REGULATORY_SOURCE_TYPES = {"regulatory_label", "regulatory_summary", "regulatory_notice"}


class ValidationError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise ValidationError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def strings(values, allow_empty=True):
    return isinstance(values, list) and (allow_empty or bool(values)) and all(nonblank(v) for v in values)


def iso_day(value):
    need(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), "Date must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError("Invalid calendar date") from exc


def url(value):
    need(isinstance(value, str), "URL must be a string")
    parsed = urlsplit(value)
    need(parsed.scheme == "https" and bool(parsed.hostname) and parsed.username is None and parsed.password is None, "Expected public HTTPS URL without credentials")


def refs(values, sources, allow_empty=False):
    need(strings(values, allow_empty), "Missing or malformed source references")
    need(len(values) == len(set(values)), "Duplicate source reference")
    need(all(v in sources for v in values), "Unknown source reference")


def real(value):
    return type(value) in (int, float) and float("-inf") < value < float("inf")


def validate(document, register):
    need(isinstance(document, dict) and isinstance(register, dict), "Documents must be objects")
    need(document.get("schema_version") == register.get("schema_version") == "1.1.0", "Unsupported schema version")
    cutoff = iso_day(document["as_of"])
    need(iso_day(register["access_date"]) == cutoff, "Snapshot/access dates differ")
    need(document["review_status"] == "draft_research_candidate_not_independently_ALS_clinician_reviewed", "Review caveat removed")
    need(document["data_scope"] == "public_published_aggregate_only", "Data scope changed")
    need(nonblank(register["method"]), "Missing access method")
    need(isinstance(register["sources"], list) and register["sources"], "Sources must be a nonempty list")
    sources = {}
    for s in register["sources"]:
        need(isinstance(s, dict) and set(s) == {"id", "title", "creator", "type", "publication_date", "date_precision", "url", "identifiers", "access_level", "access_note", "locator", "reuse", "regulatory_assertions"}, "Unexpected source fields")
        need(nonblank(s["id"]), "Source ID must be text")
        need(s["id"] not in sources, "Duplicate source ID")
        sources[s["id"]] = s
        need(isinstance(s["type"], str) and s["type"] in SOURCE_TYPES, "Unknown source type")
        need(isinstance(s["access_level"], str) and s["access_level"] in {"body_retrieved", "indexed_abstract_only"}, "Unverified source cannot support a claim")
        need(strings(s["identifiers"]), "Source identifiers must be a list of strings")
        url(s["url"])
        for field in ("id", "title", "creator", "access_note", "locator", "reuse"):
            need(isinstance(s[field], str) and s[field].strip(), "Blank source field")
        precision, published = s["date_precision"], s["publication_date"]
        if precision == "day":
            need(iso_day(published) <= cutoff, "Source is after cutoff")
        elif precision == "month":
            need(isinstance(published, str) and bool(re.fullmatch(r"\d{4}-\d{2}", published)), "Month date must be YYYY-MM")
            need(iso_day(published + "-01") <= cutoff, "Source is after cutoff")
        else:
            need(precision == "unknown" and published is None, "Unknown source date requires null")
        need(isinstance(s["regulatory_assertions"], list), "Regulatory assertions must be a list")
        for assertion in s["regulatory_assertions"]:
            need(isinstance(assertion, dict) and set(assertion) == {"record_id", "status", "jurisdiction", "event_date", "locator"}, "Malformed regulatory assertion")
            need(nonblank(assertion["record_id"]) and assertion["record_id"] in EXPECTED, "Unknown assertion record")
            need(isinstance(assertion["status"], str) and assertion["status"] in REGULATORY_STATUSES - {"not_assessed", "not_applicable"}, "Invalid assertion status")
            need(nonblank(assertion["jurisdiction"]) and nonblank(assertion["locator"]), "Missing assertion context")
            need(iso_day(assertion["event_date"]) <= cutoff, "Assertion event after cutoff")
            if assertion["status"] in REGULATORY_ACTIONS:
                need(s["type"] in REGULATORY_SOURCE_TYPES and s["access_level"] == "body_retrieved", "Approval or withdrawal requires a retrieved regulator source")
    need(isinstance(register["unverified_navigation"], list), "Navigation must be a list")
    for item in register["unverified_navigation"]:
        need(isinstance(item, dict) and set(item) == {"url", "purpose", "access_note"}, "Malformed navigation record")
        url(item["url"])
        need(nonblank(item["access_note"]) and nonblank(item["purpose"]), "Missing navigation access caveat")
    records = document["records"]
    need(isinstance(records, list) and all(isinstance(r, dict) and nonblank(r.get("id")) for r in records), "Records must be objects with text IDs")
    need(len(records) == 6 and {r["id"] for r in records} == EXPECTED, "Exactly the six scoped records are required")
    by_id = {r["id"]: r for r in records}
    for r in records:
        need(set(r) == {"id", "title", "target", "stage", "population", "design", "trial_ids", "source_ids", "observations", "negative_evidence", "unknowns", "caveats", "regulatory_status", "scope_exclusions"}, "Unexpected record fields")
        need(isinstance(r["stage"], str) and r["stage"] in STAGES, "Unknown evidence stage")
        for field in ("title", "target", "population", "design"):
            need(isinstance(r[field], str) and r[field].strip(), "Missing record context")
        for field in ("negative_evidence", "unknowns", "caveats"):
            need(isinstance(r[field], list) and r[field] and all(isinstance(v, str) and v.strip() for v in r[field]), "Missing limitations")
        need(strings(r["trial_ids"]) and all(re.fullmatch(r"NCT\d{8}", v) for v in r["trial_ids"]), "Invalid trial identifier")
        refs(r["source_ids"], sources)
        need(isinstance(r["scope_exclusions"], list), "Scope exclusions must be a list")
        for exclusion in r["scope_exclusions"]:
            need(isinstance(exclusion, dict) and set(exclusion) == {"source_id", "reason"}, "Malformed scope exclusion")
            need(nonblank(exclusion["source_id"]) and exclusion["source_id"] in sources and nonblank(exclusion["reason"]), "Invalid scope exclusion")
            need(exclusion["source_id"] not in r["source_ids"], "Excluded source cannot also support extracted claims")
        need(isinstance(r["observations"], list) and bool(r["observations"]), "No observations")
        for o in r["observations"]:
            need(isinstance(o, dict) and set(o) == {"kind", "endpoint", "timepoint", "result", "primary_endpoint_met", "statistic", "source_ids"}, "Unexpected observation fields")
            need(isinstance(o["kind"], str) and o["kind"] in KINDS, "Unknown observation kind")
            refs(o["source_ids"], sources)
            need(set(o["source_ids"]) <= set(r["source_ids"]), "Observation source absent from parent record")
            need(all(isinstance(o[k], str) and o[k].strip() for k in ("endpoint", "timepoint", "result")), "Incomplete observation")
            met = o["primary_endpoint_met"]
            need(met is None or type(met) is bool, "Primary result must be Boolean or null")
            if o["kind"] == "clinical_primary":
                need(type(met) is bool, "Clinical primary result must be explicit")
            else:
                need(met is None, "Non-primary outcome cannot become primary efficacy success")
            stat = o["statistic"]
            if stat is not None:
                need(isinstance(stat, dict) and set(stat) == {"measure", "value", "unit", "interval", "p_value", "analysis_method", "p_value_method"}, "Unexpected statistic fields")
                need(isinstance(stat["measure"], str) and stat["measure"], "Missing statistic measure")
                need(stat["unit"] is None or nonblank(stat["unit"]), "Statistic unit must be text or null")
                need(nonblank(stat["analysis_method"]), "Missing statistical analysis method")
                need(stat["value"] is None or real(stat["value"]), "Invalid effect value")
                p = stat["p_value"]
                need(p is None or (real(p) and 0 <= p <= 1), "Invalid p-value")
                need((p is None and stat["p_value_method"] is None) or (p is not None and nonblank(stat["p_value_method"])), "P-value requires its own method, or explicit unknown method")
                interval = stat["interval"]
                if interval is not None:
                    need(isinstance(interval, dict) and set(interval) == {"type", "level", "lower", "upper"}, "Incomplete interval")
                    need(isinstance(interval["type"], str) and interval["type"] in {"confidence", "credible"}, "Unknown interval type")
                    need(real(interval["level"]) and 0 < interval["level"] < 1, "Invalid interval level")
                    need(real(interval["lower"]) and real(interval["upper"]) and interval["lower"] <= interval["upper"], "Invalid interval bounds")
                    need(stat["value"] is not None and interval["lower"] <= stat["value"] <= interval["upper"], "Estimate outside interval")
        status = r["regulatory_status"]
        need(isinstance(status, dict) and set(status) == {"jurisdiction", "status", "event_date", "source_ids"}, "Unexpected regulatory fields")
        need(isinstance(status["status"], str) and status["status"] in REGULATORY_STATUSES, "Unknown regulatory status")
        need(nonblank(status["jurisdiction"]), "Regulatory jurisdiction must be text")
        absent = status["status"] in {"not_assessed", "not_applicable"}
        refs(status["source_ids"], sources, allow_empty=absent)
        need(set(status["source_ids"]) <= set(r["source_ids"]), "Regulatory source absent from parent record")
        if absent:
            need(status["event_date"] is None and status["source_ids"] == [], "Unassessed/not-applicable status must not assert a dated event")
        else:
            need(iso_day(status["event_date"]) <= cutoff, "Regulatory event after cutoff")
            supported = False
            for sid in status["source_ids"]:
                source = sources[sid]
                if status["status"] in REGULATORY_ACTIONS and source["type"] not in REGULATORY_SOURCE_TYPES:
                    continue
                supported |= any(a["record_id"] == r["id"] and all(a[k] == status[k] for k in ("status", "jurisdiction", "event_date")) for a in source["regulatory_assertions"])
            need(supported, "Regulatory status lacks a matching dated assertion in its cited sources")

    # Explicit extraction guardrails, not independent validation of the science.
    for name in ("tofersen_sod1", "dnl343", "relyvrio_withdrawal"):
        primary = [o for o in by_id[name]["observations"] if o["kind"] == "clinical_primary"]
        need(len(primary) == 1 and primary[0]["primary_endpoint_met"] is False, "Negative primary finding was lost")
    for name in ("ulefnersen_fus", "qrl201_stmn2"):
        r = by_id[name]
        need(r["stage"].startswith("sponsor_reported_"), "Sponsor evidence was promoted")
        evidence_refs = {sid for o in r["observations"] if o["kind"] in {"clinical_primary", "clinical_supportive", "clinical_exploratory", "safety_primary", "biomarker"} for sid in o["source_ids"]}
        need(all(sources[s]["type"] == "sponsor_press_release" for s in evidence_refs), "Sponsor source classification changed")
    need(not any(o["kind"] == "clinical_primary" for o in by_id["qrl201_stmn2"]["observations"]), "QRL-201 exploratory result promoted to primary")
    mechanism = by_id["unc13a_mechanism"]
    need(mechanism["stage"] == "peer_reviewed_mechanistic_research" and not mechanism["trial_ids"], "Mechanism promoted to trial")
    need({o["kind"] for o in mechanism["observations"]} == {"mechanistic", "hypothesis"}, "Mechanism/hypothesis separation lost")
    dnl = by_id["dnl343"]["observations"][0]["statistic"]
    need(dnl["interval"]["type"] == "credible" and dnl["p_value"] is None, "Bayesian result misrepresented")
    return {"records": len(records), "sources": len(sources), "observations": sum(len(r["observations"]) for r in records)}


def load():
    with (ROOT / "data/records.json").open() as f:
        document = json.load(f)
    with (ROOT / "data/sources.json").open() as f:
        register = json.load(f)
    return document, register


if __name__ == "__main__":
    from followup import load_followup, validate_followup
    historical = load()
    print(json.dumps({"validation": "passed", **validate(*historical), "followup": validate_followup(load_followup(), historical[0])}, sort_keys=True))
