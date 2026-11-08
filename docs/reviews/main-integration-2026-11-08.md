# Verified integration into main: 2026-11-08

## Scope and provenance

This integration combines the following independent contributions while retaining their original commits and licenses:

- PR #3: `660acb6afb824eb24a21afe1221088cce62c6cfa`, corrected Motion → Trace → Shape teaching text, paper-first worksheet and numerical regressions.
- PR #6: `12166e488731bef10050dba36cabad29d6933f23`, standalone offline structure/provenance auditor, invented fixtures and tests.
- PR #7: `85e143c5a4c96aaea91a973583ecbc23feb19eb2`, six-record ALS evidence-map snapshot with 14 public sources and 15 observations, structured JSON, generated views and validation tools.

The main base was `f3168d5cd6460a8e82d02afcf7c3c84a6c17707f`. The original three branches merge without file conflicts. A separate integration commit makes only the shared repairs and current navigation/status corrections described here. New original work retains the archive's CC BY 4.0 license; preserved third-party artifacts retain their existing licenses. The evidence map includes original concise summaries and public aggregate facts, not publication copies, restricted datasets or patient-level data.

No human educator or ALS-clinician acceptance is claimed. Evidence-map source-access statements describe the earlier source review; this integration reruns software checks but does not re-extract or independently reverify every publication. The map's named exclusions and source-access limits remain intact.

## What remains outside main

PR #5 (`f67042770e06c9fd0d12fe80003712014a2e0584`) and stacked PRs #8 (`4b032958d88074af1f1cfd2e0d364a70f5819203`) and #9 (`c1c1ce410736776ccacaaaeb143d74ed7b7b4a00`) are not dependencies of these additions and are not integrated.

PR #5's therapeutic template asserts a reduction even when the requested outcome is motor-neuron survival, transfers registry evidence labels into confidence in a new claim, and uses incomplete question identity. Its pathways, literature-count declarations, numerical relevance coefficients and ranking scores are not adequately grounded by linked source evidence. The stacked corrections repair demonstrated wording, identity and export bugs, but do not validate the underlying mechanistic claims, counts, coefficients or ranking. Taking those branches wholesale would also bring in the unresolved engine and data. No treatment recommendation or validated research-priority claim is introduced here.

The standalone auditor supports the documented version-1.0 research-plan format. It must not be assumed compatible with the unmerged version-1.1/1.2 exports. Its 158-warning report is historical and pertains only to the pinned PR #5 snapshot, not current main.

## Shared integration repairs

- Allow exactly three reviewed paths in the structural checker: the existing Knowledge Commons workflow YAML, the auditor's extensionless license and the evidence map's local SHA-256 manifest. No global YAML, LICENSE or SHA256 exemption is added.
- Add explicit checksum entries for reviewed new contribution files; refresh only reviewed changed files. Preserve every unrelated existing checksum entry.
- Reconcile inherited checksum gaps as historical byte provenance, as detailed below. This does not endorse their prose or pedagogical claims.
- Expand GitHub Actions to run all local Python/Node suites, targeted calculation checks, record validators, source/build parity, evidence-map render/manifest checks, the clean synthetic auditor example, structural validation and Archive Steward. The workflow uses read-only repository permission. Browser/device tests are not silently implied.
- Put direct links to integrated code and data at the top of README and replace its blanket completed/validated claims with scoped draft status. Mark earlier review records as historical snapshots rather than silently rewriting their original results.

## Inherited checksum reconciliation

At the base, Archive Steward reported 29 findings: one README byte mismatch and 28 unlisted files. PR #3 already adds a reviewed canonical `data/modules.json` checksum. The other historical files below were inspected in their exact base snapshot. Their checksum entries establish which bytes are included, not that their statements are correct, licensed by an independent authority, medically safe, accessible or educationally effective.

In particular, older status documents contain optimistic “complete”, “ready”, “proven” and accessibility statements that are not current acceptance evidence. The corrected canonical motion lesson is the teaching source. Older schema/template motion examples are not canonical and still need review; the 1:3 zero-phase example is a retraced cubic, not a three-petal flower. Other curriculum scaffolds are draft records whose structural checks do not establish content quality. Do not use a zero-error integrity report to upgrade any of these claims.

The exact reviewed base paths were:

- `README.md`
- `.github/workflows/knowledge-commons-status.yml`
- `FOR_OTHER_AIS.md`
- `HANDOFF.md`
- `IMPLEMENTATION_COMPLETE.md`
- `MASTER_BUILD_INSTRUCTIONS.md`
- `MASTER_PROMPT_FOR_CODEX.md`
- `PR_DESCRIPTION.md`
- `README_PROGRESS.md`
- `START_HERE.md`
- `SYSTEM_STATUS.md`
- `TASK_COMPLETE_MARKERS.txt`
- `data/TODO-modules.json`
- `data/modules-math-curriculum.json`
- `data/modules.json`
- `data/modules/MOD-math-add-001.json`
- `data/modules/MOD-math-count-001.json`
- `data/modules/MOD-math-mult-intro-001.json`
- `data/projects/proj-motion-trace-shape.json`
- `data/tasks/task-motion-add-example.json`
- `data/tasks/task-motion-browser-test.json`
- `docs/QUICKSTART.md`
- `docs/collaboration-workflow.md`
- `docs/knowledge-module-schema.md`
- `docs/task-templates/browser-test-template.md`
- `docs/task-templates/new-example-template.md`
- `tools/generate-math-modules.py`
- `tools/module-template.json`
- `tools/validate.py`

README, the workflow and canonical modules have deliberately reviewed changes in this integration or PR #3; the other historical paths remain byte-for-byte identical to the pinned main base. No entire checksum map was replaced from another branch, and no unchanged existing hash was silently refreshed. The integration record itself and its changed documentation also receive explicit hashes. Hashes are integrity records, not an immutable or independently signed audit log.

## Verification on the integrated tree

- Python 3.12.14: 184 tests pass (25 cooperation/rescue, 57 Archive Steward, 32 Idea Finder, 43 evidence auditor, 27 evidence map).
- Node: 181 tests pass (24 Lumen, 44 motion, 84 water survey, 29 color/ontology), plus 46 focused Reality Atlas calculation/syntax checks.
- Four module records, one project and two tasks pass their structural validators.
- Lumen and motion source/standalone parity pass; four preserved cooperation/rescue mission definitions pass structural checks.
- Evidence-map validation, deterministic generated-view comparison and all eight package manifest hashes pass. The research observations and source registry are unchanged from PR #7.
- Clean synthetic auditor fixture returns exit 0. Its review fixture and malformed-input paths are exercised by the 43-test suite. No real PR #5 input is needed or imported.
- Archive structural checks, all reviewed archive checksums and whitespace checks pass after explicit reconciliation.

The same commands are listed in `.github/workflows/knowledge-commons-status.yml` and can be run from the repository root; use its declared working directory for the evidence-map manifest check. Outputs should be saved outside the repository. The expanded workflow is intended to run on the published integration head and again on main; consult GitHub Actions for those actual run results rather than treating this local record as proof of remote CI success.

Not tested: rendered browser use, native controls/downloads, mobile devices, assistive technology, learner outcomes, qualified educator acceptance, biological truth, clinical efficacy or treatment safety. The evidence map remains an incomplete research-organizing draft.
