# ANQUR registry correction: review and verification

Review date: 2026-11-08. **Draft research only; independent AI source/software review is not ALS clinician review.**

## Scope and evidence

The [dated correction](ANQUR_REGISTRY_UPDATE.md) resolves historical ANQUR registration-access and primary-window gaps. It preserves the original November 7 `records.json` and `sources.json` bytes, sponsor result observations, regulatory assertion and efficacy limitations. A prominent correction inside the ANQUR section and above historical retrieval failures prevents the old access caveats being presented as current. Machine consumers must load `data/anqur_registry_update.json` as well as the historical snapshot. Other trials were not refreshed.

Two independent AI retrievals confirmed current ClinicalTrials.gov API fields and official-browser version comparisons. The reviewed record is version 24, submitted May 12 and posted May 15, 2026. The original version and comparisons 15–16 and 23–24 establish the selected safety-window and extended-dosing changes. The source retains Phase 1 while the sponsor's February 2026 release calls ANQUR Phase 1/2. The reason is unknown. No full protocol/SAP is posted in the reviewed registry record; its registered outcome hierarchy does not establish exploratory-analysis prespecification, multiplicity handling or clinical benefit.

The raw API response inspected was 11,962 bytes, SHA-256 `f590a9bdfd2f02fb6e4351a9daa6885e29588b1aabd427420f5a0c713b33dc20`. This identifies inspected bytes, not correctness or permanent availability. Only concise factual extracts and references are included, not the response body or screenshots. The primary-window string's unmatched bracket and the narrative planned-cohort/structured actual-enrollment difference are disclosed, not repaired by invention. Submitted, posted, verified and accessed dates remain distinct.

## Reproduction and boundaries

From repository root:

```sh
python3 research/als_evidence_map_2026-11-07/tools/validate.py
python3 -B -m unittest discover -s research/als_evidence_map_2026-11-07/tests -p 'test_*.py'
python3 research/als_evidence_map_2026-11-07/tools/render.py --check
(cd research/als_evidence_map_2026-11-07 && sha256sum -c MANIFEST.sha256)
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The separately versioned registry schema enforces bounded parent/scope, dated retrieved registry sources, required source locators, historical comparison identities and snapshot-specific endpoint/enrollment/availability values. It rejects registry-to-efficacy promotion through unsupported fields. Tests preserve historical JSON bytes, exact generated views, sponsor citations and distinction of source dates. These are structural/transcription safeguards, not automatic scientific verification; coordinated changes to metadata and tests could still be wrong. Prose and claim support require independent source review.

No browser behavior or runtime app changed. Repository browser CI is a regression gate, not clinical validation. No qualified clinician review, participant-level analysis, full protocol/SAP audit, current approval search or comprehensive safety synthesis occurred.

## Review and test outcome

Independent source and exact-patch software review found no blocking findings in the bounded registry correction. The reviewer independently reran all 81 evidence-map tests, schema validation, exact generated views, 18 manifest hashes, structural validation and whitespace checks, and verified zero Archive Steward findings on an exact-commit export.

A clean ordinary clone on Python 3.12.14 / Node 24.22.1 passed all eight offline Python suites (305 tests), 184 Node tests, Reality Atlas core checks, source/standalone parity, all evidence schemas, exact generated views, manifest checks, structural validation and Archive Steward with zero errors/warnings. The working linked checkout itself triggers an unrelated Steward finding for its `.git` pointer file; the exact clean clone/export demonstrates that this is checkout metadata, not an added archive file. No baseline exclusion was added to conceal it.

Final housekeeping corrected the README schema count and completed this review outcome. Only scoped reviewed hashes were refreshed. Exact-commit remote CI remains a separate integration gate, recorded on the pull request rather than asserted by this local report. No ALS clinician review or additional scientific validation is implied.
