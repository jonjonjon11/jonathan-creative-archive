# Multiplication prerequisite correction, 2026-11-08

## Defect and bounded repair

At main `2fc6542dcfa1a1a0e77c3972f711b81f85728019`, the multiplication lesson advertised a 0–10 table but stopped at row 5 and used a misleading number-filled separator in place of a labeled zero row. The worked examples directed learners to absent rows 6 and 8.

Version 1.0.1 of [the canonical multiplication module](../../data/modules/MOD-math-mult-intro-001.json) supplies all 121 products, distinct row/column labels and explicit zero-group versus zero-items-per-group explanations. Repeated-addition alternatives explain 6 × 7 = 42 and 8 × 9 = 72 without tracing a grid. The text-only path includes the same reasoning. The car example now follows the lesson's groups-first convention; the base-ten append-zero shortcut is restricted to whole numbers.

The lesson now explicitly records pending educator/learner review and unverified accessibility rather than inheriting an unsupported partial-verification label. The division lesson, its review decision and all recovered artifacts remain unchanged. No new third-party text, learner data or software dependency was added.

## Reproducible checks

From the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_*lesson.py' -v
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The six new multiplication checks validate the complete table by repeated addition, zero row/column meaning, the three worked examples, the no-grid explanations, direct written product/addition equations and the stated review limits. Five of these checks failed against the old module; its existing direct arithmetic equations passed. The seven existing division tests also pass. These are selected regressions, not a general mathematical-proof or prose-validation system.

The workflow's lesson-test pattern now includes both multiplication and division. Local aggregate validation ran all 311 Python tests, all 184 Node tests, the 46 Reality Atlas calculation/syntax checks, static standalone/source parity checks, evidence-map validation/generated-view/hash checks and archive structure checks on Python 3.12.14 and Node 24.22.1. All passed. Only the reviewed changed/new file entries may be refreshed in the archive checksum baseline.

## Review boundary

Independent AI arithmetic and code review is recorded with the integration PR. It does not substitute for educator, learner, screen-reader, browser-rendering or educational-effectiveness acceptance. This correction does not provide a new rendered lesson application or claim that the inherited book references were re-inspected. Wider prerequisite review remains future work. GitHub CI results belong to the exact commits shown in the PR and must pass before merge.
