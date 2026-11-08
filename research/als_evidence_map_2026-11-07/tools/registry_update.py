"""Dated registry provenance only; never promotes registration to efficacy evidence."""
import json
from validate import ROOT, need, nonblank, strings, iso_day, url, refs

SOURCE_IDS = {'anqur_registry_v24', 'anqur_registry_v1', 'anqur_registry_v15_v16', 'anqur_registry_v23_v24'}
HISTORY_REFS = {'original_registration': 'anqur_registry_v1', 'safety_window_amendment': 'anqur_registry_v15_v16', 'extended_dosing_amendment': 'anqur_registry_v23_v24'}


def load_registry_update():
    return json.loads((ROOT / 'data/anqur_registry_update.json').read_text(encoding='utf-8'))


def validate_registry_update(doc, historical, register):
    need(isinstance(doc, dict) and set(doc) == {'schema_version', 'as_of', 'parent_record_id', 'trial_id', 'scope', 'review_status', 'title', 'sources', 'current_registration', 'history', 'phase_discrepancy', 'limits', 'reuse'}, 'Unexpected registry-update fields')
    need(doc['schema_version'] == '1.0.0' and doc['scope'] == 'registry_provenance_only', 'Registry-update scope changed')
    cutoff = iso_day(doc['as_of'])
    need(cutoff >= iso_day(historical['as_of']), 'Registry update predates snapshot')
    parents = {r['id']: r for r in historical['records']}
    need(doc['parent_record_id'] == 'qrl201_stmn2' and doc['trial_id'] == 'NCT05633459' and doc['trial_id'] in parents['qrl201_stmn2']['trial_ids'], 'Registry parent mismatch')
    need(doc['review_status'] == historical['review_status'], 'Registry clinical-review caveat changed')
    need(all(nonblank(doc[k]) for k in ('title', 'reuse')) and strings(doc['limits'], False), 'Missing registry interpretation limits')
    sources = {s['id']: s for s in register['sources']}
    need(isinstance(doc['sources'], list) and len(doc['sources']) == 4, 'Missing bounded registry sources')
    seen = set()
    for s in doc['sources']:
        need(isinstance(s, dict) and set(s) == {'id', 'title', 'url', 'type', 'record_posted_date', 'version_submitted_dates', 'access_date', 'access_level', 'locator', 'access_note'}, 'Unexpected registry source fields')
        need(nonblank(s['id']) and s['id'] in SOURCE_IDS and s['id'] not in seen and s['id'] not in sources, 'Unknown or duplicate registry source')
        seen.add(s['id'])
        need(s['type'] == 'trial_registry' and s['access_level'] == 'body_retrieved', 'Registry source misclassified')
        need(all(nonblank(s[k]) for k in ('title', 'locator', 'access_note')), 'Missing registry source context')
        url(s['url'])
        need(strings(s['version_submitted_dates'], False), 'Missing submitted dates')
        posted, accessed = iso_day(s['record_posted_date']), iso_day(s['access_date'])
        dates = [iso_day(v) for v in s['version_submitted_dates']]
        need(dates == sorted(dates) and dates[-1] <= posted <= accessed <= cutoff, 'Registry dates out of order')
        sources[s['id']] = s

    def citations(entries, required):
        need(isinstance(entries, list) and entries, 'Missing registry claim references')
        need(all(isinstance(e, dict) and set(e) == {'source_id', 'locator'} and nonblank(e['locator']) for e in entries), 'Malformed registry claim locator')
        ids = [e['source_id'] for e in entries]
        refs(ids, sources)
        need(set(required) <= set(ids), 'Registry claim lacks required source')

    current = doc['current_registration']
    need(isinstance(current, dict) and set(current) == {'version', 'submitted_date', 'posted_date', 'verified_month', 'phase', 'enrollment', 'primary_outcome', 'secondary_outcomes', 'results_posted', 'full_protocol_or_sap_posted_in_reviewed_record', 'source_refs'}, 'Unexpected current-registry fields')
    # Snapshot-specific transcription safeguards, not a truth oracle or future schema.
    need(type(current['version']) is int and current['version'] == 24 and current['phase'] == 'Phase 1', 'Reviewed registry phase/version changed')
    need(current['submitted_date'] == sources['anqur_registry_v24']['version_submitted_dates'][-1] and current['posted_date'] == sources['anqur_registry_v24']['record_posted_date'], 'Current registry dates lack matching source')
    need(current['verified_month'] == '2026-05', 'Reviewed verification month changed')
    enrollment = current['enrollment']
    need(isinstance(enrollment, dict) and set(enrollment) == {'count', 'type'}, 'Malformed enrollment')
    need(type(enrollment['count']) is int and enrollment['count'] == 69 and enrollment['type'] == 'actual', 'Reviewed enrollment changed')
    need(current['results_posted'] is False and current['full_protocol_or_sap_posted_in_reviewed_record'] is False, 'Registry availability cannot become outcome evidence')
    primary = current['primary_outcome']
    need(isinstance(primary, dict) and set(primary) == {'measure', 'time_frame'}, 'Malformed primary registry endpoint')
    need(primary['measure'] == 'Number of participants with one or more treatment emergent adverse events and serious adverse events' and primary['time_frame'] == 'Baseline through Day 421 [End of Study Visit', 'Registered safety endpoint/window changed')
    secondary = current['secondary_outcomes']
    need(isinstance(secondary, list) and len(secondary) == 3, 'Missing registered PK endpoints')
    expected = ('Pharmacokinetics (plasma): Maximum observed concentration of QRL-201 (Cmax)', 'Pharmacokinetics (plasma): Area under the concentration time curve from zero to infinity (AUCinf) of QRL-201', 'Pharmacokinetics (plasma): Time of maximum concentration (Tmax) of QRL-201')
    for i, outcome in enumerate(secondary):
        need(isinstance(outcome, dict) and set(outcome) == {'measure', 'time_frame'}, 'Malformed secondary registry endpoint')
        need(outcome['measure'] == expected[i] and outcome['time_frame'] == ('Predose up to 24 hours postdose' if i == 2 else 'Predose up to 24 hours post dose'), 'Registered PK endpoint/window changed')
    citations(current['source_refs'], ['anqur_registry_v24'])
    need(isinstance(doc['history'], list) and len(doc['history']) == 3, 'Missing registry history')
    history_seen = set()
    for entry in doc['history']:
        need(isinstance(entry, dict) and set(entry) == {'id', 'text', 'source_refs'} and nonblank(entry['id']) and entry['id'] in HISTORY_REFS and nonblank(entry['text']), 'Malformed registry history entry')
        need(entry['id'] not in history_seen, 'Duplicate registry history')
        history_seen.add(entry['id'])
        citations(entry['source_refs'], [HISTORY_REFS[entry['id']]])
    discrepancy = doc['phase_discrepancy']
    need(isinstance(discrepancy, dict) and set(discrepancy) == {'text', 'source_refs'} and nonblank(discrepancy['text']), 'Missing phase discrepancy')
    citations(discrepancy['source_refs'], ['anqur_design_2024', 'anqur_interim_2026', 'anqur_registry_v24', 'anqur_registry_v23_v24'])
    return {'registry_updates': 1, 'sources': 4, 'history_entries': 3}


def registry_notice(doc):
    current = doc['current_registration']
    return (f"**Registry correction checked {doc['as_of']}:** The registration posted {current['posted_date']} lists {current['phase']}, "
            f"{current['enrollment']['count']} actual participants, a primary safety endpoint through Day 421 and three plasma-PK secondary endpoints. "
            'This resolves the registry-access/window gap below, not the unexplained sponsor Phase 1/2 terminology. '
            '[Dated extraction, amendment comparisons and limits](ANQUR_REGISTRY_UPDATE.md). No efficacy inference or posted registry results.')


def render_registry_update(doc, register):
    sources = {s['id']: s for s in register['sources'] + doc['sources']}
    def cites(entries):
        return '; '.join(f"[{e['source_id']}]({sources[e['source_id']]['url']}) ({e['locator']})" for e in entries)
    current = doc['current_registration']
    lines = [f"# {doc['title']}", '', f"Access/correction date: {doc['as_of']}. Trial: {doc['trial_id']}.", '', '**Registry design/provenance only. No efficacy conclusion, regulatory-status update or independent ALS clinician review.**', '', 'This corrects the access gap in the [historical six-record map](EVIDENCE_MAP.md), whose November 7 source snapshot and sponsor-reported results remain unchanged. [Review and test record](REVIEW_ANQUR_REGISTRY.md).', '', '## Current reviewed registration', '', f"Version {current['version']}: submitted {current['submitted_date']}; posted {current['posted_date']}; record verified {current['verified_month']}. Phase: {current['phase']}. Enrollment: {current['enrollment']['count']} ({current['enrollment']['type']}).", '', f"Primary: {current['primary_outcome']['measure']}. Registered time frame (verbatim): {current['primary_outcome']['time_frame']}", '', 'Secondary plasma-PK endpoints:', '']
    lines += [f"- {o['measure']}; {o['time_frame']}." for o in current['secondary_outcomes']]
    lines += ['', 'No results, full protocol or SAP are posted in the reviewed registry record.', '', cites(current['source_refs']), '', '## Inspected amendment history', '']
    for entry in doc['history']:
        lines += [entry['text'], '', cites(entry['source_refs']), '']
    lines += ['## Phase terminology remains discrepant', '', doc['phase_discrepancy']['text'], '', cites(doc['phase_discrepancy']['source_refs']), '', '## Limits and unknowns', '']
    lines += ['- ' + entry for entry in doc['limits']]
    lines += ['', '## Source access', '']
    for s in doc['sources']:
        lines += [f"### {s['id']}", '', f"[{s['title']}]({s['url']})", '', f"Registry source; submitted version dates: {', '.join(s['version_submitted_dates'])}; latest compared record posted: {s['record_posted_date']}; accessed: {s['access_date']}.", '', s['access_note'], '', f"Location: {s['locator']}.", '']
    lines += ['The two sponsor sources retain their original November 7 access metadata in [SOURCE_ACCESS.md](SOURCE_ACCESS.md).', '', doc['reuse'], '']
    return '\n'.join(lines).rstrip() + '\n'
