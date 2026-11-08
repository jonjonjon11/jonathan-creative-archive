# Authoring guardrails milestone — 2026-11-08

## Starting state and choice

Started from main `de54861311695b6dd298cf137743e8dd35b43a15`. Reviewed current main, contribution guidance, workflow, module records, task templates and open PRs before editing. PRs #5/#8/#9 remain outside this change: no unresolved biomedical model, coefficients or hypothesis rankings are imported. Open #2/#4 are independent earlier proposals, not dependencies of this patch.

Compact repository map:

- `data/modules.json`, `data/modules/`, `docs/lessons/`: authored educational drafts and the corrected motion lesson.
- `tools/motion-trace-shape/`, other `tools/` and `artifacts/`: offline educational tools, archival helpers and preserved source.
- `research/als_evidence_map_2026-11-07/`: scoped, source-linked research records and deterministic views, not clinical guidance.
- `data/tasks/`, `CONTRIBUTING.md`, `docs/task-templates/`: contributor entry points.
- `tools/validate.py`, `scripts/validate_archive.py`, Archive Steward and CI: distinct structural, integrity and regression checks.

The selected bottleneck was a contributor-facing guide/template that repeated known-wrong 1:3 flower claims and asserted accessibility without evidence. The authoring validator also crashed on malformed JSON shapes and accepted empty fields, incomplete exercises and duplicate identities. Improving this path prevents future contributors from copying errors while adding a useful, completely worked mathematical specimen.

## Delivered changes

- Replace the duplicated old motion lesson in the format guide with the actual enforced contract and links to the corrected canonical lesson.
- Derive a 1:3, zero-phase retraced cubic in the example template. Its JSON includes nine stored coordinate checkpoints and polynomial coefficients, checked against the sinusoidal model. Correct the associated task suggestions and control-range assumptions.
- Mark the generic template unreviewed and accessibility unverified. Placeholders remain a scaffold, not a finished lesson.
- Harden structural validation for record/object/list/string types, duplicate JSON keys, local IDs, same-type record IDs across a batch, exercise questions/solutions, task estimates and status values.
- Handle missing files, invalid UTF-8/JSON and unprintable Unicode diagnostics without abandoning later records.
- Preserve both existing exercise field conventions and the legacy module-level example/exercise location. Prefer content-level fields; do not silently fall back from malformed canonical fields.
- Run the new authoring suite in CI and link the guide from contribution instructions.

## Review and tests

The authoring suite contains 24 regression tests, including malformed roots/nested values, missing files, duplicate keys and IDs, missing exercise solutions, legacy compatibility, batch continuation, non-finite task estimates and escaped-surrogate diagnostics. It also checks the current template status and parses the worked specimen's numerical checkpoints and cubic coefficients. A 401-sample identity check supplements the exact derivation; it is not a general proof checker.

Independent AI code review found a Unicode diagnostic crash during testing. It was repaired before publication and covered by a subprocess regression. That review also prompted tying numeric checks directly to the specimen's stored data instead of maintaining an unrelated expected-data copy. Review is not human educator acceptance.

Commands run from the repository root:

```sh
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
```

The remaining regression, build-parity, manifest and evidence-map commands are enumerated in `.github/workflows/knowledge-commons-status.yml`. All were run locally: 208 Python tests, 181 Node tests and 46 additional calculation/syntax checks. The final tracked tree is also checked from a clean export before publication. Consult the actual GitHub Actions run for remote results, rather than interpreting this local record as proof of remote success.

Only new and changed reviewed paths receive checksum entries; unrelated hashes are retained. No source license, canonical lesson data, biomedical evidence or deployment setting changes. New original work remains CC BY 4.0.

## Limits and next queue

Structural validation is not full schema enforcement, mathematical truth, source verification, clinical review, accessibility acceptance or proof of educational value. It does not reject every placeholder or validate every optional field. Duplicate record IDs are checked only among the supplied files. The generic template may structurally pass while still containing placeholders. The worked specimen has no new browser/device/learner acceptance. No restricted data, network ingestion, external code or new dependencies were introduced.

Recommended next bounded work:

1. Independently review the remaining arithmetic drafts and the earlier division proposal before integrating them.
2. Add a runnable, accessible contributor smoke-test route and perform real browser/device checks where available.
3. Keep the unsupported biomedical hypothesis engine separate until sources, coefficients and output claims have been meaningfully corrected; passing software tests cannot establish those claims.

To resume, recheck main and open PR heads, run CI commands, select one task above, and record exactly what changed and which acceptance checks remain. Do not recreate this guide or reintroduce a duplicate canonical lesson.
