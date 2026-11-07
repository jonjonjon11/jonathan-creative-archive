#!/usr/bin/env python3
"""Read, inspect, and search a bounded local evidence pack without executing it.

This checks record consistency. It does not validate scientific truth or advise care.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

MAX_BYTES = 2 * 1024 * 1024
SCHEMA_VERSION = '1.0'
SOURCE_TYPES = {'primary_trial', 'regulatory', 'government_education', 'registry', 'methods', 'sponsor_report'}
EVIDENCE_TYPES = {'randomized_trial', 'regulatory_decision', 'established_background',
                  'methodological', 'open_question', 'open_label_followup',
                  'trial_design', 'sponsor_report', 'study_safety'}
DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}\Z')
YEAR_PATTERN = re.compile(r'\d{4}\Z')


class EvidenceError(ValueError):
    """An understandable local data/read failure."""


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceError(f'Duplicate JSON key: {key!r}')
        result[key] = value
    return result


def _reject_constant(value):
    raise EvidenceError(f'Non-finite JSON number is not permitted: {value}')


def _finite_float(token):
    value = float(token)
    if not math.isfinite(value):
        raise EvidenceError('Non-finite or overflowing JSON number is not permitted.')
    return value


def load_pack(path):
    """Read at most MAX_BYTES from an explicit local regular, nonsymlink file.

    No data-provided path, URL, code, or command is opened or executed.
    This is not a filesystem sandbox; callers choose a trusted stationary file.
    """
    file_path = Path(path)
    try:
        if file_path.is_symlink() or not file_path.is_file():
            raise EvidenceError('Pack must be a regular local file, not a symbolic link.')
        with file_path.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
    except OSError as exc:
        raise EvidenceError(f'Cannot read pack: {exc.strerror or str(exc)}') from None
    if len(raw) > MAX_BYTES:
        raise EvidenceError(f'Pack exceeds the {MAX_BYTES}-byte input limit.')
    try:
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_pairs,
                          parse_constant=_reject_constant, parse_float=_finite_float)
    except EvidenceError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f'Invalid UTF-8 JSON: {exc}') from None
    except ValueError as exc:
        raise EvidenceError(f'Unsupported JSON number: {exc}') from None
    except RecursionError:
        raise EvidenceError('JSON nesting exceeds the supported input depth.') from None
    errors = validate(data)
    if errors:
        raise EvidenceError('\n'.join(errors))
    return data


def validate(data):
    """Return structural/reference errors; never establish evidence quality."""
    errors = []
    if not isinstance(data, dict):
        return ['Record must be a JSON object.']
    if data.get('schema_version') != SCHEMA_VERSION:
        errors.append(f'Unsupported schema_version; expected {SCHEMA_VERSION!r}.')

    def text_at(obj, field, path):
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{path}.{field}: expected a nonempty string.')
            return None
        return value

    def text_list_at(obj, field, path):
        value = obj.get(field)
        if (not isinstance(value, list) or not value or
                any(not isinstance(item, str) or not item.strip() for item in value)):
            errors.append(f'{path}.{field}: expected a nonempty list of nonempty strings.')
            return []
        return value

    def iso_date(value, path):
        if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
            errors.append(f'{path}: expected a YYYY-MM-DD date.')
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            errors.append(f'{path}: invalid calendar date.')
            return None

    def object_list(field):
        value = data.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f'{field}: expected a nonempty array of objects.')
            return []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f'{field}[{index}]: expected an object.')
        return [(index, item) for index, item in enumerate(value) if isinstance(item, dict)]

    pack = data.get('pack')
    if not isinstance(pack, dict):
        errors.append('pack: expected an object.')
        pack = {}
    for field in ('id', 'title', 'version', 'review_status', 'scope', 'license'):
        text_at(pack, field, 'pack')
    if pack.get('review_status') != 'draft_pending_qualified_review':
        errors.append('pack.review_status: this format supports draft_pending_qualified_review only; validation does not grant approval.')
    text_list_at(pack, 'limits', 'pack')
    as_of = iso_date(pack.get('as_of'), 'pack.as_of')

    seen_ids = set()

    def check_id(obj, path):
        value = text_at(obj, 'id', path)
        if value is not None:
            if value in seen_ids:
                errors.append(f'{path}.id: duplicate record ID {value!r}.')
            seen_ids.add(value)
        return value

    check_id(pack, 'pack')
    source_items = object_list('sources')
    source_types = {}
    for index, source in source_items:
        path = f'sources[{index}]'
        source_id = check_id(source, path)
        for field in ('title', 'rights_note', 'inspection'):
            text_at(source, field, path)
        url = text_at(source, 'url', path)
        if url is not None:
            try:
                location = urlsplit(url)
                valid_url = (location.scheme == 'https' and location.hostname and
                             location.username is None and location.password is None and
                             not any(char.isspace() for char in url))
                # Accessing port also rejects malformed/non-numeric values.
                location.port
            except ValueError:
                valid_url = False
            if not valid_url:
                errors.append(f'{path}.url: expected an absolute HTTPS URL without credentials or whitespace.')
        kind = source.get('source_type')
        if not isinstance(kind, str) or kind not in SOURCE_TYPES:
            errors.append(f'{path}.source_type: unsupported source type.')
        elif source_id is not None:
            source_types[source_id] = kind
        checked = iso_date(source.get('checked'), f'{path}.checked')
        if checked is not None and as_of is not None and checked > as_of:
            errors.append(f'{path}.checked: date is after pack.as_of.')
        if 'published' not in source:
            errors.append(f'{path}.published: required; use null if unknown.')
        else:
            published = source['published']
            published_year = None
            if published is None:
                pass
            elif isinstance(published, int) and not isinstance(published, bool) and 1 <= published <= 9999:
                published_year = published
            elif isinstance(published, str) and YEAR_PATTERN.fullmatch(published):
                published_year = int(published)
                if published_year == 0:
                    errors.append(f'{path}.published: invalid year.')
            elif isinstance(published, str):
                pub_date = iso_date(published, f'{path}.published')
                if pub_date is not None and as_of is not None and pub_date > as_of:
                    errors.append(f'{path}.published: date is after pack.as_of.')
            else:
                errors.append(f'{path}.published: expected a year, YYYY-MM-DD date, or null.')
            if published_year is not None and as_of is not None and published_year > as_of.year:
                errors.append(f'{path}.published: year is after pack.as_of.')

    for index, claim in object_list('claims'):
        path = f'claims[{index}]'
        check_id(claim, path)
        for field in ('topic', 'statement', 'population'):
            text_at(claim, field, path)
        text_list_at(claim, 'limitations', path)
        refs = text_list_at(claim, 'source_ids', path)
        if len(refs) != len(set(refs)):
            errors.append(f'{path}.source_ids: duplicate source reference.')
        for source_id in refs:
            if source_id not in source_types:
                errors.append(f'{path}.source_ids: missing or invalid source {source_id!r}.')
        evidence_type = claim.get('evidence_type')
        if not isinstance(evidence_type, str) or evidence_type not in EVIDENCE_TYPES:
            errors.append(f'{path}.evidence_type: unsupported evidence type.')
        required_type = {'randomized_trial': 'primary_trial',
                         'open_label_followup': 'primary_trial',
                         'trial_design': 'primary_trial',
                         'study_safety': 'primary_trial',
                         'regulatory_decision': 'regulatory',
                         'sponsor_report': 'sponsor_report'}.get(
            evidence_type if isinstance(evidence_type, str) else '')
        if required_type and not any(source_types.get(ref) == required_type for ref in refs):
            errors.append(f'{path}: {evidence_type} requires a {required_type} source.')
        if 'quantitative' in claim:
            quantitative = claim['quantitative']
            qpath = f'{path}.quantitative'
            if not isinstance(quantitative, dict):
                errors.append(f'{qpath}: expected an object.')
                continue
            for field in ('outcome', 'unit', 'timepoint', 'interpretation'):
                text_at(quantitative, field, qpath)
            numbers = {}
            for field in ('estimate', 'ci95_low', 'ci95_high'):
                value = quantitative.get(field)
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    errors.append(f'{qpath}.{field}: expected a finite number, not a boolean.')
                else:
                    try:
                        finite = math.isfinite(value)
                    except OverflowError:
                        finite = False
                    if not finite:
                        errors.append(f'{qpath}.{field}: expected a finite number.')
                    else:
                        numbers[field] = value
            if len(numbers) == 3 and not numbers['ci95_low'] <= numbers['estimate'] <= numbers['ci95_high']:
                errors.append(f'{qpath}: expected ci95_low <= estimate <= ci95_high.')
    return errors


def search(data, query, topic=None):
    """Case-insensitive OR substring search; source order is preserved."""
    terms = query.casefold().split()
    if not terms:
        return []
    matches = []
    for claim in data['claims']:
        if topic is not None and topic.casefold() not in claim['topic'].casefold():
            continue
        haystack = ' '.join([claim['topic'], claim['statement'], claim['population'],
                             *claim['limitations']]).casefold()
        if any(term in haystack for term in terms):
            matches.append(claim)
    return matches


def report(data, topic=None):
    """Select claims and relevant sources while retaining all pack limits."""
    claims = [claim for claim in data['claims'] if topic is None or
              topic.casefold() in claim['topic'].casefold()]
    refs = {ref for claim in claims for ref in claim['source_ids']}
    return {'schema_version': data['schema_version'], 'pack': data['pack'],
            'claims': claims, 'sources': [s for s in data['sources'] if s['id'] in refs]}


def _display(value):
    # Escape control characters so a source cannot inject terminal escape sequences.
    return json.dumps(value, ensure_ascii=False)[1:-1]


def _print_report(result, concise=False):
    pack = result['pack']
    print(f"{_display(pack['id'])}: {_display(pack['title'])}")
    print(f"As of: {_display(pack['as_of'])}; status: {_display(pack['review_status'])}")
    print(f"Scope: {_display(pack['scope'])}")
    print('Limits:')
    for limit in pack['limits']:
        print(f'  - {_display(limit)}')
    print(f"Claims: {len(result['claims'])}")
    for claim in result['claims']:
        print(f"\n{_display(claim['id'])} [{_display(claim['evidence_type'])}] {_display(claim['topic'])}")
        print(_display(claim['statement']))
        print('Population: ' + _display(claim['population']))
        for limit in claim['limitations']:
            print('Limit: ' + _display(limit))
        print('Sources: ' + ', '.join(_display(ref) for ref in claim['source_ids']))
        if not concise and 'quantitative' in claim:
            q = claim['quantitative']
            print(f"Outcome: {_display(q['outcome'])}; time: {_display(q['timepoint'])}")
            print(f"Estimate: {q['estimate']}; 95% CI [{q['ci95_low']}, {q['ci95_high']}]; unit: {_display(q['unit'])}")
            print('Interpretation: ' + _display(q['interpretation']))
    if not concise:
        print('\nSource records (links are displayed, never opened):')
        for source in result['sources']:
            print(f"{_display(source['id'])}: {_display(source['title'])}")
            print(f"  {_display(source['url'])}; checked {_display(source['checked'])}")
            print('  Inspection: ' + _display(source['inspection']))
            print('  Rights: ' + _display(source['rights_note']))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pack', help='Explicit local evidence-pack JSON file')
    subparsers = parser.add_subparsers(dest='command', required=True)
    for command in ('validate', 'report', 'search'):
        sub = subparsers.add_parser(command)
        sub.add_argument('--json', action='store_true', help='Output deterministic JSON')
        if command in ('report', 'search'):
            sub.add_argument('--topic', help='Case-insensitive substring filter on topic')
        if command == 'search':
            sub.add_argument('query', help='Space-separated OR substring terms')
    args = parser.parse_args(argv)
    if args.command == 'search' and not args.query.strip():
        parser.error('Search query must contain at least one non-whitespace character.')
    if getattr(args, 'topic', None) is not None and not args.topic.strip():
        parser.error('Topic filter must not be empty.')
    try:
        data = load_pack(args.pack)
    except EvidenceError as exc:
        if args.json:
            print(json.dumps({'ok': False, 'errors': str(exc).splitlines()}, ensure_ascii=False, sort_keys=True))
        else:
            print('Invalid evidence pack:', file=sys.stderr)
            for error in str(exc).splitlines():
                print('  ' + _display(error), file=sys.stderr)
        return 1
    if args.command == 'validate':
        result = {'ok': True, 'pack_id': data['pack']['id'], 'sources': len(data['sources']),
                  'claims': len(data['claims']),
                  'limitation': 'Structural consistency only; no scientific, clinical, rights, or approval certification.'}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        else:
            print(f"Valid record structure: {_display(data['pack']['id'])} ({len(data['sources'])} sources, {len(data['claims'])} claims).")
            print(result['limitation'])
    else:
        result = report(data, getattr(args, 'topic', None))
        if args.command == 'search':
            result['claims'] = search(data, args.query, args.topic)
            refs = {ref for claim in result['claims'] for ref in claim['source_ids']}
            result['sources'] = [s for s in data['sources'] if s['id'] in refs]
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
        else:
            _print_report(result, concise=args.command == 'search')
    return 0


if __name__ == '__main__':
    sys.exit(main())
