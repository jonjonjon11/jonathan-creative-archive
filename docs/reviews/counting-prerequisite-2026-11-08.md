# Counting prerequisite correction, 2026-11-08

## Defect and bounded correction

At main `3420d85f6bb419da6247a5bd57500cbc894bb130`, the [canonical counting module](../../data/modules/MOD-math-count-001.json) directed its text-only route to numeral recognition "by seeing them." All three worked examples used looking, pointing or touching without equivalent instructions in those steps. Its `partially_verified` accessibility label cited no supporting checks. The wider lesson already mentioned counting sounds and actions; this finding does not establish that the entire lesson was inaccessible to every learner.

Version 1.0.1 provides sequential named-item examples and a worked text-only route. Physical objects, touching, pointing, handwriting and spoken answers are optional. The lesson distinguishes an unchanged collection's item order from the stable number sequence, states the count of an empty collection, and explains the last-count rule. It supplies numeral-name pairs through twenty and keeps quantity matching separate from recognizing printed or tactile numeral forms. It does not teach Braille notation or assert that a list verifies a real collection that has not been observed.

The three worked totals remain 4, 7 and 12. The five exercise answers remain 6, 8 objects, 5 in either item order, 0 and 15. Stable module identity, original attribution, CC BY 4.0 license and inherited source records are preserved. The curriculum outline, addition, multiplication and division lessons, review decisions and recovered artifacts are unchanged. No new third-party text, private data, software dependency or rendered lesson application was added.

## Checks and scope

From the repository root:

```sh
python3 -B -m unittest discover -s tests -p 'test_*lesson.py' -v
python3 -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

Nine new counting regressions cover the complete numeral-name sequence, the three named-item counting traces, exercise totals, item identity during a recount, empty/nonempty counting, the worked text route, notation distinctions and review metadata. The 22 counting, multiplication and division lesson tests pass. The new tests reject the previous record because the required corrected content and metadata are absent; this is not a claim that its original numerical answers were incorrect. These are selected written-content checks, not a general proof or an accessibility test.

The existing workflow automatically includes `test_counting_lesson.py` through its `test_*lesson.py` pattern; no workflow change is needed. Local aggregate validation ran all 320 Python tests, all 184 Node tests, the 46 Reality Atlas calculation/syntax checks, static standalone/source parity checks, evidence-map validation/generated-view/hash checks and archive structure checks on Python 3.12.14 and Node 24.22.1. All passed. Archive checksum changes are restricted to the corrected module, its new test and this review note after inspecting those files. The checksum file excludes itself.

## Review boundary

Independent AI review is recorded with the integration PR and is distinct from human acceptance. Educator, learner, screen-reader, other assistive-technology, browser-rendering and educational-effectiveness acceptance have not been performed for this correction. Accessibility is explicitly `unverified` and the lesson remains `draft_pending_review`. The inherited book references were not re-inspected; no source-page verification is claimed. The alternatives need evaluation with people using their chosen communication and reading methods, without assuming that any one method works for everyone.

GitHub CI results belong to the exact commits shown in the PR and must pass before integration. Merging a bounded correction does not upgrade the lesson's educational or accessibility acceptance status.
