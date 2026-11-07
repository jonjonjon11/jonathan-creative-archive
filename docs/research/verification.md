# Science and engineering contribution: verification and provenance

Edition: 2026-11-07. This contribution builds on the repository's established text, JSON, and local-tool approach. It contains original ALS and cancer lessons, source-linked factual records, a read-only evidence tool, and an original sampled-switch simulator. The previous division contribution remains a separate draft PR; this branch is based on main at `f3168d5`.

## Included content

- ALS: 19 source-linked claims, 14 cited sources, and three reported confidence intervals in the [evidence pack](../../data/health/als-evidence.json), plus an original [primer](../health/als-evidence-primer.md) with three worked examples and five exercises with answers.
- Trial facts: four dated records for VALOR, CENTAUR, PHOENIX, and ATLAS in [als-trial-facts.json](../../data/health/als-trial-facts.json). Actual numerical results, group counts where reported, endpoint units, provenance locations, and inspected-response hashes are embedded. PHOENIX sponsor results and the ATLAS design paper have their own explicit categories.
- Cancer: ten source-linked claims and six inspected references in a second [evidence pack](../../data/health/cancer-foundations.json), and an original [primer](../health/cancer-evidence-foundations.md) with three worked examples and five exercises with answers.
- Software: an [evidence library](../../tools/evidence-library/README.md) that validates, searches, and reports committed records offline, and a [switch-input lab](../../tools/switch-input-lab/README.md) that produces events from synthetic observations.
- Engineering: a [switch-input lesson](../lessons/switch-input-foundations.md) with three worked examples and five exercises, plus a complete invented input trace. The sample produces one press at 45 ms and one release at 90 ms.

## Source inspection and original authorship

Source pages, returned publication abstracts, regulatory notices, and technical references were inspected on 2026-11-07. Scientific sources include NIH/NLM, NCI, FDA, and the cited primary publications. The final tofersen extension report is included alongside the 2022 primary trial, rather than counted as another independent trial. An independent AI source review checked primary DOI/abstract records and confirmed numerical values and source dates. The FDA RELYVRIO withdrawal notice was read as an official full-body record.

ClinicalTrials.gov extraction was not used: the provided retrieval wrapper's shared dependency was unavailable, and study HTML returned an application shell. The useful replacement is a table of facts extracted from inspected publications and the sponsor's PHOENIX release. Consequently, these files do not assert current registry status. This acquisition distinction is retained in the data rather than substituting invented metadata.

The repository includes original explanations, original code, selected factual measurements and identifiers, bibliographic titles, and invented teaching examples. It does not redistribute full abstracts, journal articles, official PDFs, source diagrams, external implementation code, or participant-level data. Original material follows the archive's CC BY 4.0 license. Source publications, agency materials, manufacturer guidance, and referenced upstream code retain their own rights. Source hashes identify response bytes inspected during drafting; they are not signatures or evidence that a later response will match.

## Repeat the checks

From the repository root with Python 3.10 or newer:

```sh
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json validate
python3 tools/evidence-library/evidence_library.py data/health/cancer-foundations.json validate
python3 -m unittest discover -s tools/evidence-library/tests -p 'test_*.py' -v
python3 -m unittest discover -s tools/switch-input-lab/tests -p 'test_*.py' -v
python3 -m unittest discover -s tests -p 'test_health_foundations.py' -v
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The CI workflow runs the new evidence and code checks alongside the original record checks. The archive checker now permits the exact existing workflow YAML path; unrelated YAML remains outside its file-type list.

Results on 2026-11-07:

| Check | Result |
| --- | --- |
| Evidence tool synthetic tests | 31 passed |
| Switch-input synthetic tests | 14 passed |
| Real-pack/data/CLI integration tests | 7 passed |
| Both committed medical evidence packs | Valid record structures |
| Existing motion and arithmetic module validation | All four passed |
| Project and task records | Both projects and all three tasks passed |
| Archive structure, local links, source IDs, selected private-marker checks | Passed |
| Whitespace check | Passed |
| Unrelated YAML negative probe | Rejected as intended, then removed |
| Clean staged-file export | All documented evidence, tool, integration, record, and structural checks passed |
| Archive Steward after scoped checksum update | Exit 1: 27 inherited unlisted files; no new checksum or provenance finding |

An independent AI reviewer checked the code and scientific records and independently ran all 52 tests. It identified malformed-input tracebacks in the switch loader, which were corrected and covered by a regression test. It also corrected author initials and a trial-identifier citation chain. Scientific observations in the data retain their source-specific scope and review status.

The 27 remaining checksum findings are inherited files outside this contribution, including earlier master/status instructions, curriculum/motion records, the three earlier arithmetic files, collaboration/schema/task templates, and the older template/generator/validator. The baseline had 29 findings; this contribution reviewed the changed README and workflow and registered all newly added files. Unrelated files were not silently added to clear the report.

## What the checks establish

The evidence suite exercises malformed shapes, duplicate IDs and JSON keys, dangling references, source-type relationships, dates, nonfinite numbers, reversed confidence intervals, byte bounds, deterministic output, and inert instruction-like content. It validates structural consistency, not the truth or completeness of a scientific assertion. The source review addresses the numerical and interpretation claims in this edition separately.

The switch suite checks elapsed-time boundaries, bounce, cancellation, holds, repeated cycles, sparse observations, explicit initial state, parser errors, numeric bounds, and deterministic output. It models sampled observations. No physical switch, access device, person, or clinical intervention was tested. No browser application was changed; browser testing is outside this CLI contribution.

The integration suite checks both real evidence packs, the trial table's sources and group-count arithmetic, matching transcribed estimates, preserved missing values, design classifications, documented CLI examples, expected switch events, and pending review links.

At the start, Archive Steward reported 29 inherited findings: a README checksum mismatch and 28 unlisted files. Only deliberately reviewed contribution files receive new or updated checksums. Unrelated inherited findings remain visible and are reported separately. No checksum update changes any preserved upstream license or source history.

## Handoff

The [project record](../../data/projects/proj-health-and-assistive-foundations.json), [source review task](../../data/tasks/task-als-source-review.json), and [pending review record](../../data/reviews/review-als-foundations-001.json) describe the manual contribution workflow. No human reviewer or acceptance decision has been fabricated. Qualified source review, user-directed evaluation of future access technology, and another independently authored disease pack are concrete continuation paths.
