#!/usr/bin/env python3
"""Offline structural checks. This does not certify truth, safety, rights or secrecy."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
sources = json.loads((root / "sources/manifest.json").read_text())['sources']
concepts = json.loads((root / "data/concepts.json").read_text())['concepts']
source_ids = [s['id'] for s in sources]
concept_ids = [c['id'] for c in concepts]
if len(source_ids) != len(set(source_ids)): errors.append("Duplicate source IDs")
if len(concept_ids) != len(set(concept_ids)): errors.append("Duplicate concept IDs")
allowed_status = {'idea', 'documented_design', 'artifact_delivery_record', 'source_inspected', 'historical_test_report', 'runtime_verified', 'review_gap', 'editorial_proposal'}
allowed_science = {'established_model_scoped', 'design_mapping', 'speculative_unvalidated', 'not_a_scientific_claim', 'insufficient_evidence'}
for c in concepts:
    for k in ('id', 'title', 'tags', 'summary', 'source_ids', 'artifact_status', 'scientific_standing', 'limitations', 'next_step'):
        if k not in c or not c[k]: errors.append(f"{c.get('id')}: missing {k}")
    if c['artifact_status'] not in allowed_status: errors.append(f"{c['id']}: bad status")
    if c['scientific_standing'] not in allowed_science: errors.append(f"{c['id']}: bad science label")
    for s in c['source_ids']:
        if s not in source_ids: errors.append(f"{c['id']}: missing source {s}")
private_patterns = [r'https://chatgpt\.com/c/', r'https://(?:docs|drive)\.google\.com/', r'libfile_[A-Za-z0-9]+', r'Sentinel_[A-Za-z0-9]+', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
# This reviewed adapter does not broaden the repository-wide extension policy.
bounded_module_files = {
    root / 'tools/universal-color-ontology/bounded' / relative
    for relative in ('cli.mjs', 'generators.mjs', 'tests/cli.test.mjs', 'tests/generators.test.mjs')
}
for p in files:
    if p.suffix in {'.pem', '.key', '.p12', '.pfx', '.jks', '.keystore'}: errors.append(f"Disallowed file: {p.relative_to(root)}")
    if p.suffix not in {'.md', '.json', '.txt', '.py', '.cjs', '.html'} and p.name != '.gitignore' and p not in {root / 'LICENSE', root / 'artifacts/cooperation-rescue/LICENSE', root / 'tools/lumen-commons/LICENSE', root / 'tools/universal-color-ontology/upstream/LICENSE', root / 'tools/water-survey-preflight/LICENSE', root / '.github/workflows/knowledge-commons-status.yml', root / 'tools/evidence-integrity-audit/LICENSE', root / 'research/als_evidence_map_2026-11-07/MANIFEST.sha256'} and p not in bounded_module_files and not (p.suffix == '.mjs' and p.is_relative_to(root / 'tools/universal-color-ontology/upstream/packages')) and not (p.suffix in {'.js', '.css'} and any(p.is_relative_to(root / path) for path in ('tools/lumen-commons/src', 'tools/motion-trace-shape/src', 'tools/water-survey-preflight/src'))) and p not in {root / "tools/water-survey-preflight/fixtures/synthetic-clean.csv", root / "tools/water-survey-preflight/fixtures/synthetic-review.csv"}: errors.append(f"Unexpected file type: {p.relative_to(root)}")
    text = p.read_text(encoding='utf-8')
    if p.suffix != '.py':
        for pat in private_patterns:
            if re.search(pat, text): errors.append(f"Private locator/credential marker in {p.relative_to(root)}")
    if p.suffix in {'.md', '.txt'}:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'): continue
            local = (p.parent / target.split('#')[0]).resolve()
            if not local.is_relative_to(root): errors.append(f"Link escapes root: {p.relative_to(root)} -> {target}")
            elif not local.exists(): errors.append(f"Broken link: {p.relative_to(root)} -> {target}")
        for sid in re.findall(r'SRC-\d{3}', text):
            if sid not in source_ids: errors.append(f"Unknown source in {p.relative_to(root)}: {sid}")
if errors:
    print('FAIL\n' + '\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(files)} files, {len(concepts)} concept records, {len(sources)} source records; internal links, source references, required fields, label vocabularies, file types, and selected private-locator/key markers checked.')
print('Not checked: scientific correctness, legal rights, exhaustive secrets, private source access, source-project runtime, or current hosting.')
