# Hypothesis outcome-safety correction

Review date: 2026-11-08 (UTC). Scope: a software correction on top of PR #5 at
`f67042770e06c9fd0d12fe80003712014a2e0584`, not a scientific validation of that PR.

This is the pinned outcome-safety review record. The subsequent
[identity/export correction](hypothesis-identity-exports.md) addresses the
non-therapeutic ID collisions and export caps noted below, advances hypothesis
exports to version 1.2, and preserves the 1.1 therapeutic IDs. The earlier counts
and remaining-work statements below describe that earlier scope.

## Verified failures and correction

The old therapeutic template said every intervention "slows or reverses" its
outcome and "will reduce" it "by blocking" the mechanism. For an outcome such as
motor neuron survival, this reversed the apparent intent and asserted an
unestablished effect. The supplied population was discarded. IDs depended only
on the intervention, so a second question for another outcome or population
silently replaced the first.

The correction:

- Poses a direction-neutral question and an explicit test requirement. It does
  not infer increase, decrease, benefit, harm, or mechanism reversal.
- Preserves outcome and population in generated text and structured fields.
  Missing population is labeled unspecified. Blank and non-text context are
  rejected before registering a question.
- Uses `open_question` confidence rather than copying the registry's evidence
  label into a new outcome claim.
- Derives deterministic therapeutic IDs from the intervention/outcome/population
  tuple. Leading/trailing context whitespace is normalized; distinct questions
  remain separate. Repeating the same question remains idempotent.
- Adds interpretation limits to both hypothesis JSON exports and the generated
  Markdown report. The report no longer recommends prioritization from a score
  threshold. Its scores and timelines are explicitly labeled unvalidated.
- Regenerates the committed hypotheses/report and runs their parity regression
  in the existing CI workflow.

Hypothesis export version is `1.1`; pathway export version remains `1.0`.
Therapeutic IDs change. Rebuild and review dependent references; do not assume an
old ID still identifies the new contextual question. The generation date remains
the execution host's local date; the parity test ignores only that date field/line.

## Verification

Run from the repository root with Python 3.10 or newer:

```sh
python3 -m unittest discover -s tools/hypothesis-engine/tests -p 'test_*.py' -v
python3 tools/validate.py module data/modules.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json validate
python3 tools/evidence-library/evidence_library.py data/health/cancer-foundations.json validate
python3 -m unittest discover -s tools/evidence-library/tests -p 'test_*.py' -v
python3 -m unittest discover -s tools/switch-input-lab/tests -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_health_foundations.py' -v
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The original eight hypothesis tests passed before the correction. The fifteen
new regression tests failed against the old implementation (including subtest
failures), then all 23 passed after the correction on Python 3.12.14. These
tests cover software behavior and selected output safeguards, not source quality,
biological causal direction, treatment safety, or clinical validity.

The complete local check also passed 31 evidence-library, 14 sampled-switch,
seven health-integration, 57 Archive Steward, and 32 Idea Finder tests: 164 total
Python tests. The workflow's module/project/task validators, both evidence-pack
validators, archive structural/link checks, and diff whitespace checks passed.
Python 3.10/3.11 and other operating systems were not available locally.

An independent AI code review found no blocking defect within this scope, reran
75 hypothesis/evidence/switch/integration tests, and checked that 162 distinct
synthetic intervention/outcome/population tuples survived JSON export. It did not
provide scientific or clinical validation. Known pre-existing identity problems
in mechanistic/combination generation and the 100-record research-export limit
remain outside this correction; the non-overwrite guarantee is therapeutic only.

Archive Steward still exits 1: 38 findings already existed at the pinned base,
and this draft adds three (two new unlisted files and the changed workflow's
checksum). The shared checksum baseline is deliberately unchanged; these entries
need explicit reconciliation after review and before merge. A structural pass
does not erase this audit failure.

A clean staged-file export reproduced all 164 passing tests, the validators and
structural pass, and the same 41 checksum-audit findings without local caches.

## Remaining review boundaries

The pathway registry, enriched pathway export, raw evidence inputs, and shared
checksum baseline are unchanged. This correction does not absorb the separate
evidence auditor or evidence-map drafts (PRs #6 and #7).

The original priority formula/defaults, effect coefficients, literature counts,
timelines, mechanistic claims, and affirmative combination templates remain
unvalidated. Caller-supplied population labels such as "all ALS" are preserved
for traceability, not endorsed as valid indications. Stored evidence is not yet
connected to generated questions. Human scientific review and source-level
provenance work remain necessary before research use.

No new source articles, third-party code, restricted data, or patient records were
added. New original code, tests, and documentation follow the archive's existing
[CC BY 4.0 license](../../LICENSE). This draft is not a merge or deployment.
