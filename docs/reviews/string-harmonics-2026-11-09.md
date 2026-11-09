# String harmonics companion review, 2026-11-09

## Scope and prior work

Based on archive main `ab0c1a6d9ca501b0bc0b06f2875691ecf9c482e8`, with content tree `f3c818bba3e2d082fa318128e9cb33f593b338a9`. Main and open pull requests were rechecked before authoring. The four open pull requests at that check were the disease-evidence and hypothesis work, #4, #5, #8 and #9. No overlapping harmonics contribution was identified; uncommitted work and other repositories were not exhaustively inspected.

The archive's [Cloud City v7 section](../project-map.md#cloud-city-v7) already records a standing-wave lab. Its exact source locator and current runtime were unavailable in this bounded review. The new [companion](../lessons/string-harmonics.md) therefore makes no first-implementation, recovery or feature-parity claim. It supplies a directly readable offline path next to the current motion, arithmetic and switch-input lessons.

The addition consists of original teaching text, three worked examples, five questions with hints and solutions, two checked tables, 14 regression tests and navigation. It is a standalone companion, not a new structured Knowledge Module or evidence of completed physics-curriculum coverage. Existing modules, tools, artifacts, licenses and workflow are unchanged. The existing `test_*lesson.py` discovery includes the new test file.

## Scientific and rights scope

The model is a uniform flexible string with two fixed endpoints, constant tension, small transverse slopes/displacements and no bending stiffness or damping. Examples use chosen numbers, not measurements. The lesson distinguishes wavelength from string length, internal from endpoint nodes, displacement from a time trace, and model frequency from playback speed. It explicitly avoids applying its formula to atomic orbitals, a real instrument's complete sound, or an arbitrary wave system.

Four linked public teaching references were opened on 2026-11-09; the lesson records their relevant sections and claim scope. Two University Physics sections and the Chemistry section share OpenStax authorship and are not three independent confirmations. Daniel Russell's Penn State page independently supports the single-mode/mixture distinction. Its reserved text/image rights are noted. No external text, diagrams, animation, recordings or code are imported; new work follows the archive's CC BY 4.0 license. No private source, conversation or personal record was added.

## Verification record

The 14 focused tests pass locally. They parse the actual learner-facing tables, compare exact rational mode quantities and node lists, check all 25 temporal displacement cells against the analytical sine/cosine mode, verify milliseconds and quarter-period conversion, and check worked/exercise answers and selected scope/provenance statements. Phrase checks protect explicit boundaries but cannot assess every sentence's meaning. Passing tests do not prove source validity, pedagogy or accessibility.

An independent AI reviewer opened all four reference pages and recalculated all three examples, both tables and all five solutions. It independently reconstructed the 25 snapshot cells by adding two oppositely travelling waves of amplitude 0.5 mm, matching the lesson within 1e-12 mm. Maximum mode-2 slopes at amplitudes 1 mm and 2 mm were approximately 0.01047 and 0.02094, consistent with the small-slope assumption. It found no blocking content or numerical defect and independently ran the 14 focused tests, all 45 lesson tests, 31 authoring tests and module validation. This is AI review, not educator, learner, accessibility or legal acceptance.

Local aggregate checks also passed on Linux with Python 3.12.14 and Node v24.22.1:

- **343 Python tests:** 31 authoring, 45 lesson (including 14 new), 29 switch-input, 25 cooperation/rescue, 57 Archive Steward, 32 Idea Finder, 43 evidence integrity and 81 evidence-map/follow-up tests.
- **212 Node tests**, plus **46 Reality Atlas calculation/syntax checks**.
- All module/project/task validators; Lumen and motion static/build checks; cooperation mission validation; exact water standalone parity; evidence-map validation, generated-view parity and all manifest hashes; clean synthetic evidence audit.
- Archive structural/local-link validation and whitespace checks. The independent review's earlier missing review-link finding was resolved by adding this report. Its unlisted-file findings are addressed only after reviewing the new lesson and test, not by refreshing unrelated baselines.

No browser application was changed, so local browser suites were not repeated. Existing browser CI checks remain required for this contribution's integration; passing them does not assess this Markdown lesson's screen-reader or print behavior.

Reproduce the focused check from the repository root with Python 3:

```sh
python3 -B -m unittest discover -s tests -p 'test_string_harmonics_lesson.py' -v
```

Use the full commands in [.github/workflows/knowledge-commons-status.yml](../../.github/workflows/knowledge-commons-status.yml), followed by archive structure, reviewed checksums and whitespace checks, for integration. Do not infer remote CI success from this local report; the Actions record identifies the actual tested revision.

## Remaining limits and bounded next review

No human educator/learner study, screen-reader or physical-device check, print-layout assessment, listening test or physical-string experiment has been performed. All tasks are optional and untimed, drawing is optional, and a verbal path accompanies each table, but these design choices do not certify accessibility or comprehension. The sources are available through external links; their full pages are not bundled for offline reading.

An archive maintainer can review a voluntary independent calculation or text alternative before accepting it. A useful next human check is to work through one example using only the written description, report any ambiguous term, and preserve units and model assumptions in a proposed revision. No participant-identifying information or external recruitment is required. Integration of a reviewed draft must not be recorded as educator acceptance or validation of learning outcomes.
