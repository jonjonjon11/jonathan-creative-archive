#!/usr/bin/env python3
"""Validate/render the bounded follow-up companion without rewriting historical results."""
import json
from validate import ROOT, need, nonblank, strings, iso_day, url, real, refs

OBSERVATIONS = {'function_ancova', 'function_jrt', 'function_alternative_jrt', 'survival_death_pv', 'survival_death', 'biomarkers', 'neurological_safety'}
ANALYSES = {
    'function_ancova': 'ANCOVA with multiple imputation',
    'function_jrt': 'Post hoc joint-rank ANCOVA with multiple imputation',
    'function_alternative_jrt': 'Post hoc alternative joint-rank ANCOVA with ranked covariates and multiple imputation',
    'survival_death_pv': 'Cox regression adjusted for baseline NfL and riluzole/edaravone use',
    'survival_death': 'Cox regression adjusted for baseline NfL and riluzole/edaravone use',
}


def load_followup():
    return json.loads((ROOT / 'data/valor_ole_followup.json').read_text(encoding='utf-8'))


def validate_followup(doc, historical):
    need(isinstance(doc, dict) and set(doc) == {'schema_version', 'as_of', 'parent_record_id', 'title', 'review_status', 'data_scope', 'design', 'sources', 'observations', 'methods_and_limits', 'unverified', 'review'}, 'Unexpected follow-up fields')
    need(doc['schema_version'] == '1.0.0', 'Unsupported follow-up schema')
    cutoff = iso_day(doc['as_of'])
    need(cutoff >= iso_day(historical['as_of']), 'Follow-up predates historical snapshot')
    parents = {r['id']: r for r in historical['records']}
    need(nonblank(doc['parent_record_id']) and doc['parent_record_id'] in parents and doc['parent_record_id'] == 'tofersen_sod1', 'Unknown follow-up parent')
    need(doc['review_status'] == historical['review_status'] == 'draft_research_candidate_not_independently_ALS_clinician_reviewed', 'Clinical review caveat removed')
    need(doc['data_scope'] == 'public_published_aggregate_only' and nonblank(doc['title']), 'Missing follow-up scope')
    sources = {}
    need(isinstance(doc['sources'], list) and len(doc['sources']) >= 2, 'Missing follow-up sources')
    for s in doc['sources']:
        need(isinstance(s, dict) and set(s) == {'id', 'title', 'url', 'identifiers', 'publication_date', 'publication_note', 'access_date', 'access_level', 'access_note', 'locator', 'reuse'}, 'Unexpected follow-up source fields')
        need(all(nonblank(s[k]) for k in ('id', 'title', 'publication_note', 'access_note', 'locator', 'reuse')), 'Blank source context')
        need(s['id'] not in sources, 'Duplicate follow-up source')
        need(s['access_level'] == 'body_retrieved', 'Follow-up requires retrieved primary text')
        need(strings(s['identifiers'], False), 'Missing follow-up identifiers')
        need(iso_day(s['publication_date']) <= iso_day(s['access_date']) <= cutoff, 'Invalid follow-up source dates')
        url(s['url'])
        sources[s['id']] = s

    def citations(entries):
        need(isinstance(entries, list) and entries, 'Missing claim-level source locators')
        need(all(isinstance(e, dict) and set(e) == {'source_id', 'locator'} and nonblank(e['locator']) for e in entries), 'Malformed claim locator')
        refs([e['source_id'] for e in entries], sources)

    design = doc['design']
    need(isinstance(design, dict) and set(design) == {'classification', 'description', 'comparison', 'population', 'trial_ids', 'randomized', 'ole_entered', 'ole_completed', 'tofersen_exposed', 'source_refs'}, 'Unexpected follow-up design')
    need(design['classification'] == 'integrated_delayed_start_open_label_followup', 'Follow-up cannot become a placebo-controlled trial')
    need(all(nonblank(design[k]) for k in ('description', 'comparison', 'population')), 'Missing study context')
    need(strings(design['trial_ids'], False), 'Missing trial IDs')
    for field in ('randomized', 'ole_completed'):
        value = design[field]
        need(isinstance(value, dict) and set(value) == {'early_start', 'delayed_start'}, 'Missing group denominators')
        need(all(type(n) is int and n >= 0 for n in value.values()), 'Invalid group denominator')
    randomized = sum(design['randomized'].values())
    need(all(n > 0 for n in design['randomized'].values()), 'Both randomized comparison groups must be positive')
    need(all(design['ole_completed'][g] <= design['randomized'][g] for g in design['randomized']), 'Completions exceed randomized group')
    need(type(design['ole_entered']) is int and sum(design['ole_completed'].values()) <= design['ole_entered'] <= randomized, 'Inconsistent OLE attrition')
    need(type(design['tofersen_exposed']) is int and design['ole_entered'] <= design['tofersen_exposed'] <= randomized, 'Inconsistent exposed denominator')
    citations(design['source_refs'])
    observations = doc['observations']
    need(isinstance(observations, list) and all(isinstance(o, dict) and nonblank(o.get('id')) for o in observations), 'Malformed follow-up observations')
    need(len(observations) == len(OBSERVATIONS) and {o['id'] for o in observations} == OBSERVATIONS, 'Bounded follow-up observations missing or duplicated')
    for o in observations:
        need(set(o) == {'id', 'kind', 'endpoint', 'timepoint', 'result', 'primary_endpoint_met', 'statistic', 'count', 'source_refs'}, 'Unexpected follow-up observation fields')
        expected_kind = 'biomarker_followup' if o['id'] == 'biomarkers' else 'safety_followup' if o['id'] == 'neurological_safety' else 'clinical_followup'
        need(o['kind'] == expected_kind and o['primary_endpoint_met'] is None, 'Follow-up outcome promoted or reclassified')
        need(all(nonblank(o[k]) for k in ('endpoint', 'timepoint', 'result')), 'Missing follow-up endpoint context')
        citations(o['source_refs'])
        need('valor_ole_final_2025' in [e['source_id'] for e in o['source_refs']], 'Outcome lacks main primary-paper citation')
        if o['id'] not in {'biomarkers', 'neurological_safety'}:
            need('valor_ole_supplement_1' in [e['source_id'] for e in o['source_refs']], 'Analysis lacks supplemental methods citation')
        s = o['statistic']
        if expected_kind == 'clinical_followup':
            need(isinstance(s, dict) and set(s) == {'measure', 'value', 'unit', 'interval', 'p_value', 'p_value_type', 'analysis_method', 'p_value_method'}, 'Malformed follow-up statistic')
            need(s['analysis_method'] == s['p_value_method'] == ANALYSES[o['id']], 'Different analysis identity or post hoc status conflated')
            need(s['p_value_type'] == 'nominal' and real(s['p_value']) and 0 <= s['p_value'] <= 1, 'Nominal inference label missing or invalid p-value')
            need(s['unit'] is None or nonblank(s['unit']), 'Invalid statistic unit')
            expected_measure = 'joint_rank_test' if o['id'] in {'function_jrt', 'function_alternative_jrt'} else 'adjusted_mean_difference' if o['id'] == 'function_ancova' else 'hazard_ratio'
            need(s['measure'] == expected_measure, 'Different follow-up analyses conflated')
            if expected_measure == 'joint_rank_test':
                need(s['value'] is None and s['interval'] is None and s['unit'] is None, 'Rank analysis cannot inherit mean difference or CI')
            else:
                i = s['interval']
                need(isinstance(i, dict) and set(i) == {'type', 'level', 'lower', 'upper'}, 'Missing interval')
                need(i['type'] == 'confidence' and i['level'] == .95, 'Follow-up interval misclassified')
                need(all(real(v) for v in (i['lower'], s['value'], i['upper'])) and i['lower'] <= s['value'] <= i['upper'], 'Invalid estimate/interval')
                if expected_measure == 'adjusted_mean_difference':
                    need(s['unit'] == 'ALSFRS-R points', 'Function estimate has wrong units')
                if expected_measure == 'hazard_ratio':
                    need(i['lower'] > 0 and s['unit'] == 'ratio', 'Hazard ratio must be positive')
        else:
            need(s is None, 'Unextracted statistic asserted')
        count = o['count']
        if o['id'] == 'neurological_safety':
            need(isinstance(count, dict) and set(count) == {'numerator', 'denominator', 'unit', 'reported_percent'}, 'Missing safety denominator')
            need(type(count['numerator']) is int and type(count['denominator']) is int and count['denominator'] > 0 and 0 <= count['numerator'] <= count['denominator'] == design['tofersen_exposed'], 'Invalid exposed safety count')
            need(count['unit'] == 'participants' and real(count['reported_percent']) and abs(100 * count['numerator'] / count['denominator'] - count['reported_percent']) < .051, 'Safety proportion inconsistent')
        else:
            need(count is None, 'Count attached to wrong observation')
    need(isinstance(doc['methods_and_limits'], list) and doc['methods_and_limits'], 'Missing methods/limitations')
    for m in doc['methods_and_limits']:
        need(isinstance(m, dict) and set(m) == {'topic', 'text', 'source_refs'} and nonblank(m['topic']) and nonblank(m['text']), 'Malformed methodological note')
        citations(m['source_refs'])
    need(strings(doc['unverified'], False), 'Missing verification limits')
    review = doc['review']
    need(isinstance(review, dict) and set(review) == {'source_double_extraction', 'software_review', 'record'}, 'Malformed review record')
    need(review['record'] == 'REVIEW_VALOR_OLE.md' and all(nonblank(review[k]) and review[k] in {'pending', 'independent_ai_review_completed'} for k in ('source_double_extraction', 'software_review')), 'Unsupported review claim')
    return {'followups': 1, 'sources': len(sources), 'observations': len(observations)}


def render_followup(doc):
    sources = {s['id']: s for s in doc['sources']}
    def cites(entries):
        return '; '.join(f"[{e['source_id']}]({sources[e['source_id']]['url']}) ({e['locator']})" for e in entries)
    lines = [f"# {doc['title']}", '', f"Extraction date: {doc['as_of']}. Companion to the unchanged historical findings in [the six-record map](EVIDENCE_MAP.md).", '', '**Draft research candidate. No independent ALS clinician review, patient predictions, treatment recommendations, or regulatory-status update.**', '', '[Review and test record](REVIEW_VALOR_OLE.md). This is not a comprehensive current evidence synthesis.', '', '## Design and denominators', '']
    d = doc['design']
    lines += [d['description'], '', f"Population: {d['population']}. Comparison: {d['comparison']}.", '', f"Randomized early/delayed: {d['randomized']['early_start']}/{d['randomized']['delayed_start']}; entered OLE: {d['ole_entered']}; completed early/delayed: {d['ole_completed']['early_start']}/{d['ole_completed']['delayed_start']}; tofersen-exposed safety population: {d['tofersen_exposed']}.", '', f"Trials: {', '.join(d['trial_ids'])}.", '', cites(d['source_refs']), '']
    for o in doc['observations']:
        lines += [f"## {o['endpoint']}", '', f"Evidence type: {o['kind']}. Timepoint: {o['timepoint']}.", '', o['result']]
        s = o['statistic']
        if s:
            numeric = f"Analysis: {s['analysis_method']}."
            if s['value'] is not None:
                i = s['interval']
                numeric += f" Estimate: {s['value']} {s['unit']}; 95% confidence interval {i['lower']} to {i['upper']}."
            numeric += f" Nominal p = {s['p_value']} ({s['p_value_method']})."
            lines += ['', numeric]
        if o['count']:
            c = o['count']
            lines += ['', f"Reported count: {c['numerator']}/{c['denominator']} {c['unit']} ({c['reported_percent']}%)."]
        lines += ['', cites(o['source_refs']), '']
    lines += ['## Methods and limitations', '']
    for m in doc['methods_and_limits']:
        lines += [f"- **{m['topic']}:** {m['text']} {cites(m['source_refs'])}"]
    lines += ['', '## Unverified or outside scope', ''] + ['- ' + s for s in doc['unverified']]
    lines += ['', '## Source access and rights', '']
    for s in doc['sources']:
        lines += [f"### {s['id']}", '', f"[{s['title']}]({s['url']})", '', f"Publication: {s['publication_date']}. {s['publication_note']}", '', f"Access: {s['access_date']}; {s['access_level']}. {s['access_note']}", '', f"Location: {s['locator']}. Identifiers: {', '.join(s['identifiers'])}.", '', s['reuse'], '']
    return '\n'.join(lines).rstrip() + '\n'
