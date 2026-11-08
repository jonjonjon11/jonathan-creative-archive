#!/usr/bin/env python3
"""Deterministic, offline Markdown views. Does not fetch or reinterpret evidence."""
import argparse
from pathlib import Path
from validate import ROOT, load, validate
from followup import load_followup, validate_followup, render_followup


def render(document, register):
    sources = {s["id"]: s for s in register["sources"]}
    def citations(ids):
        return "; ".join(f"[{i}]({sources[i]['url']})" for i in ids)
    lines = ["# ALS evidence map", "", f"Snapshot: {document['as_of']}. Six purposively selected records. Not comprehensive.", "", "**Draft research candidate. Not independently reviewed by an ALS clinician. No patient predictions or treatment recommendations.**", "", "Read README.md for selection, interpretation, reproducibility, and limitations. Source dates and access caveats are in SOURCE_ACCESS.md. A separately dated [VALOR/OLE follow-up](VALOR_OLE_FOLLOWUP.md) adds later evidence without changing the historical primary result.", ""]
    for r in document["records"]:
        lines += [f"## {r['title']}", "", f"- Record: `{r['id']}`", f"- Stage: {r['stage'].replace('_', ' ')}", f"- Target: {r['target']}", f"- Population: {r['population']}", f"- Design: {r['design']}", f"- Trial identifiers: {', '.join(r['trial_ids']) or 'None asserted in this record'}", f"- Context sources: {citations(r['source_ids'])}", ""]
        for o in r["observations"]:
            lines += [f"### {o['kind'].replace('_', ' ').capitalize()}", "", f"{o['endpoint']}. Timepoint: {o['timepoint']}.", "", o["result"]]
            if o["statistic"] is not None:
                s = o["statistic"]
                numeric = f"Measure: {s['measure']}. Analysis: {s['analysis_method']}."
                if s["value"] is not None:
                    numeric += f" Estimate: {s['value']} {s['unit'] or ''}."
                if s["interval"] is not None:
                    i = s["interval"]
                    numeric += f" {i['level'] * 100:g}% {i['type']} interval: {i['lower']} to {i['upper']}."
                if s["p_value"] is not None:
                    numeric += f" Reported p-value: {s['p_value']} ({s['p_value_method']})."
                lines += ["", numeric]
            lines += ["", f"Sources: {citations(o['source_ids'])}", ""]
        for field, heading in [("negative_evidence", "Negative or absent evidence"), ("unknowns", "Unknowns"), ("caveats", "Caveats")]:
            lines += [f"**{heading}**"] + [f"- {x}" for x in r[field]] + [""]
        s = r["regulatory_status"]
        lines += [f"Regulatory field: {s['status'].replace('_', ' ')}; jurisdiction: {s['jurisdiction']}; event date: {s['event_date'] or 'not asserted'}.", ""]
        if s["source_ids"]:
            lines += [f"Regulatory sources: {citations(s['source_ids'])}", ""]
        if r["scope_exclusions"]:
            lines += ["**Named scope exclusions**", ""]
            for exclusion in r["scope_exclusions"]:
                lines += [f"- {citations([exclusion['source_id']])}: {exclusion['reason']}"]
            lines += [""]
    access = ["# Source and access register", "", f"Access date: {register['access_date']}", "", register["method"], "", "URLs below are the source references. No source document bytes are included in this package. 'Body retrieved' does not mean every supplement was reviewed. Indexed-only access is explicitly labeled.", ""]
    for s in register["sources"]:
        access += [f"## {s['id']}", "", f"[{s['title']}]({s['url']})", "", f"- Creator: {s['creator']}", f"- Type: {s['type']}", f"- Publication date: {s['publication_date'] or 'not established'} ({s['date_precision']} precision)", f"- Identifiers: {', '.join(s['identifiers']) or 'none recorded'}", f"- Access: {s['access_level']}", f"- Access note: {s['access_note']}", f"- Relevant location: {s['locator']}", f"- Reuse: {s['reuse']}", ""]
        for a in s["regulatory_assertions"]:
            access += [f"- Curated regulatory assertion: {a['record_id']}; {a['status']}; {a['jurisdiction']}; {a['event_date']}. Source location: {a['locator']}."]
        if s["regulatory_assertions"]:
            access += [""]
    access += ["## Unverified navigation and retrieval gaps", "", "These URLs do not supply verified claim evidence in this map.", ""]
    for s in register["unverified_navigation"]:
        access += [f"- [{s['purpose']}]({s['url']}): {s['access_note']}"]
    return {"EVIDENCE_MAP.md": "\n".join(lines).rstrip() + "\n", "SOURCE_ACCESS.md": "\n".join(access).rstrip() + "\n"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document, register = load()
    validate(document, register)
    followup = load_followup()
    validate_followup(followup, document)
    views = render(document, register)
    views["VALOR_OLE_FOLLOWUP.md"] = render_followup(followup)
    for filename, content in views.items():
        path = ROOT / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Stale or missing generated view: {filename}")
        else:
            path.write_text(content, encoding="utf-8")
    print("Generated views verified" if args.check else "Generated views written")


if __name__ == "__main__":
    main()
