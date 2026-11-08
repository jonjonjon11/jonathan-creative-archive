# Addition and subtraction prerequisite correction, 2026-11-08

## Defect and bounded correction

At main `0c946960e27d07233cf6719cd364710d515e903d`, the [canonical addition and subtraction module](../../data/modules/MOD-math-add-001.json) introduced equality as "the same as" but also described the equals sign as telling the total or result. Its text-only route sent learners to physical objects at home; worked steps required looking at and moving objects without equivalent instructions in those steps. Its `partially_verified` accessibility label supplied no supporting checks. Readable numerical stories and correct arithmetic were already present. This finding does not establish that the whole lesson was inaccessible to every learner.

Version 1.0.1 consistently explains equal value on both sides, including `5 = 3 + 2` and `3 + 2 = 4 + 1`. Named-item descriptions provide addition, take-away and comparison without a picture or physical objects. Comparison matches pairs without removing items. Three worked examples include explicit item traces and recounts. The car description now distinguishes rearranging five existing cars from adding items to a selected group. Zero cases and the whole-number take-away boundary are explicit. Looking, moving objects, handwriting and spoken answers are optional.

The three worked answers remain 5, 4 and 4. The five exercise answers remain 5, 5, 9, 6 and 4. Stable module identity, prerequisites, original attribution, CC BY 4.0 license and inherited source records are preserved. The counting, multiplication and division lessons, curriculum outline, review decisions, workflow and recovered artifacts are unchanged. No third-party text, private records, dependency or rendered lesson application was added.

## Reproducible checks

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

Nine new tests check selected numeric equalities, relational-equality examples, zero and whole-number boundaries, item conservation and recounts, pair comparison, the worked text route, original exercise answers, optional methods and review metadata. Seven test methods reject the old record because corrected content or item-trace/review metadata is absent; the existing written numeric equations and exercise answers already passed. These checks are selected regressions, not a general proof of prose, accessibility or educational effectiveness.

The existing workflow discovers the new test through `test_*lesson.py`, so it needs no edit. Local aggregate validation ran 329 Python tests, 184 Node tests, the 46 Reality Atlas calculation/syntax checks, static source/standalone parity checks, evidence-map validation/generated-view/hash checks and archive structure checks on Python 3.12.14 and Node 24.22.1. All passed. Checksum updates are restricted to the corrected module, its new test and this note after inspection. The checksum file excludes itself.

## Review boundary

Independent AI content and code review was performed; its findings will accompany the integration PR. This review is separate from human acceptance. Educator, learner, screen-reader, other assistive-technology, browser-rendering and educational-effectiveness acceptance have not been performed for this correction. The lesson remains `draft_pending_review`, with accessibility explicitly `unverified`. The inherited book references were not re-inspected; no source-page verification is claimed. A handful of examples does not establish arithmetic fluency or numeral-form recognition, and these text alternatives may not suit every learner.

GitHub CI must pass against the exact published changes before integration. Merging the correction does not upgrade its human educational or accessibility acceptance status.
