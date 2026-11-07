# Motion lesson: correction and portable review handoff

**Module MOD-lissajous-motion-001, version 1.0.1. Corrected draft, pending human acceptance.**

Start with the [paper-first lesson](../lessons/motion-trace-shape.md). It contains the full teaching text, three examples, five exercises and solutions, and coordinate tables that can be read without animation. The [canonical JSON](../../data/modules.json) preserves the existing module structure and parameter names. The [numerical lab](../../tools/motion-trace-shape/README.md) is unchanged.

## Why this contribution exists

At base commit `f3168d5cd6460a8e82d02afcf7c3c84a6c17707f`, the lab's tests already passed, but the separate lesson prose disagreed with its equations. A passing software test suite did not establish that the teaching material was correct.

| Existing claim | Correct result in this model |
| --- | --- |
| Line minimum at t≈4 | At t=4 both coordinates are 0; the minimum is at t=6. |
| Circle at t≈4 has x=−1 and y=−1 | At t=4 the point is (0, −1); the leftmost point occurs at t=6. |
| Circle may trace back and forth | With equal unit amplitudes and +90° phase, increasing time traverses it clockwise in positive-y-up coordinates. |
| Figure-eight reaches x=1 and completes two y cycles by t≈4 | At t=2 the point is (1, 0). At t=4 it is (0, 0), after one y cycle and half an x cycle. |
| Figure-eight loops are vertical | For x:y=1:2 and 0° phase, the loops are side by side. |
| Zero-phase line may have either diagonal orientation | With equal amplitudes and repeat counts, 0° gives y=x. A 180° offset gives y=−x. |
| Phase pattern repeats every 180° | 180° reflects y and need not preserve the path; 360° restores every time-position value. |
| Ratio alone fixes a shape or a simple petal count | At 1:2, 0° gives a figure-eight, while 90° gives y=1−2x², a retraced parabola segment. |
| Try five repeats in the current lab | Controls allow integer repeats from 1 to 4 only. |
| A repeat count of 1 is a frequency of 1 cycle per second | Controls count repeats in 8 model seconds; frequency is n/8 cycles per model second. |

The correction also narrows keyboard and offline verification language, fixes the intended x/y number-line description, removes unsupported planetary/sound equivalence, and replaces an unverified historical title with an inspected MacTutor reference. The earlier content remains in Git history. No recovered source or separate artifact license changed.

## Evidence and rights

The lesson cites inspected OpenStax, MathWorld, MacTutor, and OpenStax-via-LibreTexts pages. The first supplies oscillation terminology, the second the Lissajous family and its special cases, the third historical context, and the fourth angle-sum identities. Source pages were read on 2026-11-07. The two OpenStax-derived references share authorship, not independent confirmation. The parabola counterexample follows by applying the cosine-sum and Pythagorean identities to the actual lab equations.

All added prose, tests, and coordinate tables are original and follow the archive's CC BY 4.0 license. Citations do not relicense their sources. No source diagrams or prose, private conversations, personal learner data, account information, network service, or analytics were added.

## Repeatable checks

From the repository root, with Node and Python 3 already available:

```sh
node --check tools/motion-trace-shape/src/core.js
node --check tools/motion-trace-shape/src/app.js
node --test tools/motion-trace-shape/tests/*.test.cjs
python3 tools/motion-trace-shape/tests/static_check.py
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py . --format json
git diff --check
```

The new lesson suite checks 27 coordinate rows against independent special-angle fixtures and the numerical core, critical corrected prose claims, full teaching-text parity, all readable table rows and text equivalents, exercise results, the parabola identity, phase behavior, units, control limits, and honest review status. These are focused regression checks, not a general mathematical proof checker. Source relevance is reviewed separately from URL structure.

The existing workflow runs only the basic Python record validators. A green result from that workflow does not mean the Node lesson suite or browser checks ran. Run the commands above explicitly.

### Verification record

Checks run on 2026-11-07:

| Check | Result |
| --- | --- |
| Node syntax checks | Passed for the unchanged numerical core and app. |
| Node test suite | Passed: 44 tests, comprising 32 original model/simulated-UI tests and 12 new lesson regressions. |
| Static app checks | Passed: exact standalone/source build parity and targeted source checks. |
| Basic record validators | Passed: four modules, one project, and two tasks on this branch. |
| Archive structural checker | Failed: only the existing `.github/workflows/knowledge-commons-status.yml` file-type exclusion. The same failure occurs at the base commit. |
| Archive Steward | Exit 1: 28 inherited findings remain, down from 29 at baseline because the reviewed canonical module now has a checksum entry. The inherited README checksum mismatch and 27 other unlisted files remain visible. |
| Whitespace check | Passed. |
| Negative regression probes | Passed: isolated corruptions of figure-eight table data, line-minimum prose, and a readable circle table were all rejected. |

The documented syntax, Node, static, and record checks also passed from a clean staged-file export. In that clean export, the structural checker and Archive Steward reproduced exactly the inherited failures stated above.

Only the five reviewed contribution files receive checksum entries or refreshes. No unrelated file is added simply to clear the report. The archive-wide checksum baseline is not certified. The separate division draft includes an unmerged fix for the inherited workflow file-type exclusion; it is not included or assumed here.

A separate AI reviewer recalculated the candidate's mathematics and reran the Node, static, and record checks. This is not qualified educator approval. The module remains a draft pending human acceptance.

## Portable review task

A willing educator, mathematician, or AI-assisted reviewer can copy this file, the lesson, canonical JSON, the numerical core, and the lesson tests into a local checkout together with the license. All inputs are public; no connection to a new service or permission to publish elsewhere is needed to inspect them. This is a manual handoff, not automatic federation or an outreach action.

- **Goal:** independently verify the timed positions, ratio convention, phase counterexample, and whether the seven-step text path can be followed without the lab.
- **Allowed scope:** read public inputs, recalculate results, run local checks, and propose corrections for maintainer review. Return the exact revision inspected, commands and outcomes, unresolved questions, and a suggested accept/revise decision.
- **Acceptance criteria:** every table row and exercise solution agrees with the stated equations; the text path supplies its own inputs; claims distinguish model, rendering, accessibility, and learning evidence; attribution and source licenses remain clear.
- **Restrictions:** do not infer permission to contact others, collect learner information, change access, deploy, merge, or publish on another site. Do not claim human educator endorsement or learner outcomes from automated checks.
- **Stop conditions:** missing files, contradictory results that cannot be resolved from the equations, unavailable required tools, or a proposed step needing additional permission. Record the exact blocker and any completed checks.
- **Decision owner:** Jonathan or a maintainer-designated reviewer. No reviewer is assigned without agreement. Independent AI review is not human acceptance.

No browser, mobile, touch, screen-reader, printed-layout, learner study, or qualified educator review was performed for this correction. The numerical application did not change. UI acceptance remains a separate open task.

## Remaining inherited work

The illustrative examples in `docs/knowledge-module-schema.md` and `docs/task-templates/new-example-template.md` still need their own review. They are not the canonical teaching lesson. In particular, the template's 1:3, 0° “three-lobed flower” description is misleading: x=sin(θ), y=sin(3θ) gives the retraced cubic y=3x−4x³, not enclosed petals. The template also suggests repeat counts outside the lab's range. Do not copy those examples without independently checking them.

The separate division draft PR changes contributor instructions and its own lesson. This motion correction avoids those files. The shared checksum baseline must be reconciled entry by entry if both contributions are integrated; do not replace either whole map blindly.
