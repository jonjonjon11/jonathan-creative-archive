#!/usr/bin/env python3
"""Offline structural checks, not proof of correctness, safety or accessibility."""
import json
import math
import sys
from pathlib import Path

PROJECT_STATUSES = {'planning', 'in_progress', 'first_pathway_complete_validation_pending',
                    'complete', 'paused', 'archived'}
TASK_STATUSES = {'open', 'in_progress', 'pending_review', 'approved', 'blocked', 'cancelled'}


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def _read(path):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'),
                          object_pairs_hook=_pairs, parse_constant=_constant)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        return None, [f"Cannot read record: {exc}"]
    if not isinstance(data, dict):
        return None, ['Record must be a JSON object']
    return data, []


def _text(value):
    return (isinstance(value, str) and bool(value.strip())
            and not any(0xD800 <= ord(c) <= 0xDFFF for c in value))


def _strings(record, fields, errors, prefix=''):
    for field in fields:
        if not _text(record.get(field)):
            errors.append(f'{prefix}{field} must be a non-empty string')


def _list(record, field, errors, prefix='', minimum=0, item_type=None):
    value = record.get(field)
    if not isinstance(value, list):
        errors.append(f'{prefix}{field} must be an array')
        return []
    if len(value) < minimum:
        errors.append(f'{prefix}{field} needs at least {minimum} entries; found {len(value)}')
    for i, item in enumerate(value):
        if item_type is str and not _text(item):
            errors.append(f'{prefix}{field}[{i}] must be a non-empty string')
        elif item_type is dict and not isinstance(item, dict):
            errors.append(f'{prefix}{field}[{i}] must be an object')
    return value


def _unique_ids(items, errors, prefix):
    seen = set()
    for i, item in enumerate(items):
        if not isinstance(item, dict) or 'id' not in item:
            continue
        identifier = item['id']
        if not _text(identifier):
            errors.append(f'{prefix}[{i}].id must be a non-empty string')
        elif identifier.strip() in seen:
            errors.append(f'{prefix}[{i}].id duplicates {identifier.strip()}')
        else:
            seen.add(identifier.strip())


def _module(data):
    errors = []
    if data.get('schema_version') != '1.0':
        errors.append('schema_version must be "1.0"')
    module = data.get('module')
    if not isinstance(module, dict):
        return errors + ['module must be an object']
    _strings(module, ('id', 'version', 'title', 'license'), errors, 'module.')
    _list(module, 'learning_objectives', errors, 'module.', 1, str)
    _list(module, 'prerequisites', errors, 'module.', item_type=dict)
    content = module.get('content')
    if not isinstance(content, dict):
        return errors + ['module.content must be an object']
    # Preserve the legacy top-level location, but never fall back from a malformed
    # canonical content field to a second, potentially different copy.
    for key, minimum in (('worked_examples', 3), ('exercises', 5)):
        owner = content if key in content else module
        items = _list(owner, key, errors, 'module.content.' if owner is content else 'module.', minimum, dict)
        _unique_ids(items, errors, key)
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            if key == 'worked_examples':
                if not any(_text(item.get(k)) for k in ('id', 'title')):
                    errors.append(f'{key}[{i}] needs a non-empty id or title')
            else:
                if not any(_text(item.get(k)) for k in ('prompt', 'problem_statement')):
                    errors.append(f'{key}[{i}] needs a non-empty prompt or problem_statement')
                if not any(_text(item.get(k)) for k in ('solution_guidance', 'solution')):
                    errors.append(f'{key}[{i}] needs a non-empty solution_guidance or solution')
    return errors


def _project(project):
    errors = []
    _strings(project, ('project_id', 'version', 'title', 'purpose', 'status', 'license'), errors)
    if not isinstance(project.get('status'), str) or project['status'] not in PROJECT_STATUSES:
        errors.append('Invalid project status')
    return errors


def _task(task):
    errors = []
    _strings(task, ('task_id', 'project_id', 'title', 'objective', 'status'), errors)
    _list(task, 'scope', errors, minimum=1, item_type=str)
    deliverables = _list(task, 'deliverables', errors, minimum=1)
    for i, item in enumerate(deliverables):
        if isinstance(item, dict):
            _strings(item, ('name', 'format'), errors, f'deliverables[{i}].')
        elif not _text(item):
            errors.append(f'deliverables[{i}] must be text or a named object with a format')
    if not isinstance(task.get('status'), str) or task['status'] not in TASK_STATUSES:
        errors.append('Invalid task status')
    hours = task.get('time_estimate_hours')
    if isinstance(hours, bool) or not isinstance(hours, (int, float)):
        errors.append('time_estimate_hours must be a positive finite number')
    elif hours <= 0 or (isinstance(hours, float) and not math.isfinite(hours)):
        errors.append('time_estimate_hours must be a positive finite number')
    difficulty = task.get('difficulty')
    if not isinstance(difficulty, str) or difficulty not in {'beginner', 'intermediate', 'advanced'}:
        errors.append('difficulty must be beginner, intermediate or advanced')
    return errors


VALIDATORS = {'module': _module, 'project': _project, 'task': _task}
ID_FIELDS = {'module': 'id', 'project': 'project_id', 'task': 'task_id'}


def _validate_file(path, kind):
    data, errors = _read(path)
    return errors if errors else VALIDATORS[kind](data)


def validate_module(module_file):
    return _validate_file(module_file, 'module')


def validate_project(project_file):
    return _validate_file(project_file, 'project')


def validate_task(task_file):
    return _validate_file(task_file, 'task')


def _emit(text):
    # Escaped JSON strings and filesystem names may contain lone surrogates.
    # Diagnostics must not abort the batch on a terminal encoding error.
    encoding = getattr(sys.stdout, 'encoding', None) or 'utf-8'
    print(text.encode(encoding, errors='backslashreplace').decode(encoding))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args or args == ['--help']:
        print('Usage: python3 tools/validate.py <module|project|task> <file.json> [<file2.json> ...]')
        print('Offline structural checks only; not correctness, safety, rights or accessibility approval.')
        return 0
    kind, *files = args
    if kind not in VALIDATORS or not files:
        print('Error: specify module, project or task and at least one JSON file')
        return 1
    failed = False
    seen = {}
    for path in files:
        data, errors = _read(path)
        if not errors:
            errors = VALIDATORS[kind](data)
            record = data.get('module', {}) if kind == 'module' else data
            identifier = record.get(ID_FIELDS[kind]) if isinstance(record, dict) else None
            if _text(identifier):
                identifier = identifier.strip()
                if identifier in seen:
                    errors.append(f'Duplicate {kind} ID {identifier}; first seen in {seen[identifier]}')
                else:
                    seen[identifier] = path
        _emit(f'{"FAIL" if errors else "PASS"}: {path}')
        for error in errors:
            _emit(f'  {error}')
        failed |= bool(errors)
    print('Scope: structure only; passing is not factual or accessibility verification.')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
