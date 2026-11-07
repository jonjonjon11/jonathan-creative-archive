# Archive Steward 0.2

An inspectable offline mini-helper for maintaining this creative archive. It reports byte drift, missing provenance files and dangling source references, then turns the archive's existing next steps into a review queue. Version 0.2 adds comparison between saved local reports, so repeated reviews can focus on what changed. It is a deterministic Python command-line tool, not a language model or an autonomous publisher.

## Run

Requires Python 3.10 or later and no third-party packages. From the repository root:

```sh
python3 tools/archive-steward/archive_steward.py .
python3 tools/archive-steward/archive_steward.py . --format json
python3 -m unittest discover -s tools/archive-steward/tests -p 'test_*.py' -v
```

The root directory is required explicitly. Output goes only to the terminal. To save a report, redirect it to a location **outside** the archive so it does not become an unlisted file. The helper never refreshes checksums: an editor must first review each changed or new file, then deliberately update the baseline.

Exit codes: **0** means no configured integrity/metadata errors, **1** means findings need review, and **2** means invalid/missing input or an invalid command. Warnings do not change a zero exit code. Zero is not permission to publish or a claim of legal clearance.

## Compare two local reviews

Save a JSON report **outside** the repository before making a change. After reviewing your edits, compare the current archive with that report. For example, these Unix-like shell commands use a temporary directory:

```sh
python3 tools/archive-steward/archive_steward.py . --format json > /tmp/steward-before.json
# Make and review an archive change, then run:
python3 tools/archive-steward/archive_steward.py . --compare /tmp/steward-before.json
python3 tools/archive-steward/archive_steward.py . --compare /tmp/steward-before.json --format json > /tmp/steward-after.json
```

Choose your own filenames. Shell redirection overwrites its destination; do not use the same file for `--compare` input and redirected output. The helper itself does not create or overwrite reports.

The focused text comparison shows:

- Added, removed and changed concept records in the review queue, including exact before/after next steps, status and limitations.
- Changes to artifact license declarations, scope, review paths and scoped verification claims.
- Added/removed source records and changes to their titles, access labels or evidence classes.
- Added, removed and changed file bytes from actual local SHA-256 snapshots, including unlisted files. This can reveal changed bytes after the ordinary archive checksum baseline has been refreshed.
- Newly introduced and no-longer-reported findings, plus **all current findings**, so persistent errors remain visible.

Comparison uses stable record IDs. It does not compare every metadata field semantically; file-byte changes provide a broader pointer to review. File paths in an old report are inert labels and are never opened. Unhashable common files are marked `uncompared`, not silently treated as unchanged. Added/removed files mean inventory presence changed; a failed or incomplete scan can also change the inventory. If either directory inventory is incomplete, added/removed claims are withheld and unmatched paths are marked `uncompared_presence`.

JSON comparison output includes a full current report with `report_schema_version: "1"`, `file_snapshot`, `file_inventory_complete`, `source_inventory` and an added `comparison` section. You can use that JSON as the next comparison input. Reports from version 0.1 are accepted for their existing concept/artifact/finding/count fields, but lack file snapshots and per-source metadata; unavailable comparisons are explicitly identified.

Compare reports from the **same archive**. A saved report is editable and unauthenticated, not a signed history or proof of progress, rights, safety or a successful repair. Changes alone do not make the exit code nonzero; the current archive's integrity errors still determine exit code 1. Malformed, oversized or unsupported comparison inputs produce exit code 2. Comparison reports must fit the 4 MiB JSON input limit.

## What it does

- Compares included files with the SHA-256 baseline in `data/checksums.json` and flags missing, changed and unlisted files.
- Separately checks preserved-source hashes in the two existing source manifest formats, Lumen's generated-build hash and Reality Atlas's pinned HTML hash. Updating only the archive baseline cannot hide a change to a preserved original.
- Warns when a registered artifact has no independent preserved-source or pinned-file hash checks.
- Reads the recovered-artifact registry in `data/artifacts.json`, checks the artifact directory, source references and declared license/provenance/test-record file presence, and reports license scope and verification limits. Declared licenses are metadata, not the output of a legal review.
- Counts concept statuses and source-access declarations, checks concept/artifact source IDs and concept artifact paths, and lists sources without a concept/artifact reference. A source may still be cited in prose; that list is not a deletion recommendation.
- Copies every concept's existing next step into a stable review queue. Evidence gaps, delivery receipts and historical-only test reports come first; other records follow by ID. This ordering is a simple rule, not a quality, urgency or scientific confidence score.
- Produces deterministic text or JSON with no clock-dependent timestamps; optional comparison reports retain actual hashes and selected source metadata.

## Boundaries

It makes no network calls, requests no credentials, runs no source files or shell commands, writes no files, and never publishes, messages people or makes decisions about sharing. Running the **tests** creates temporary fixture directories, then removes them. The helper itself only reads the explicitly selected archive and optional saved comparison report.

It ignores `.git` and `__pycache__` directories, `.pyc` files and `.DS_Store`. The checksum file is excluded from its own baseline. Other unlisted files, including local reports, are flagged. Input-controlled exclusions are not accepted. Symbolic links and traversal paths are rejected; JSON inputs are limited to 4 MiB and hashed files to 64 MiB. Unsupported files require human review, not silent omission.

The tool is intended for a trusted, stationary local checkout, not a hostile or concurrently changing filesystem. Its path checks are not an operating-system security sandbox. It does not prove who created the baseline or detect coordinated changes to both files and hash records. It does not parse license obligations or validate the truth of a verification record. It does not execute tests, check URLs, search private accounts, recover missing files, detect all secrets, review science, or certify privacy, accessibility, medical safety or educational efficacy. Metadata shown in a report may itself contain private information; review it before sharing.

`data/artifacts.json` lists selected included learning artifacts, distinguishing recovered sources from new implementations; it does not enumerate every support script. Its `rights` fields name the declaration, applicable file scope, local license file and human review record. Its `verification` fields preserve the scoped test status and limitations. New recoveries require a human-authored entry and source/rights review. The supported upstream manifest layouts are intentionally limited to the two formats already in this archive.

## Verification

All 57 synthetic tests passed on Python 3.12.14 on 2026-11-06. The reviewed archive produced zero configured errors or warnings. Comparison tests cover byte drift after a refreshed baseline, concept/license/source changes, malformed and legacy reports, persistent findings, unhashable files, path handling and reusable JSON output. These checks cover the helper's local logic, not artifact runtime correctness or legal rights.

## A small improvement loop

1. Run the helper before a proposed archive change, save its JSON report outside the repository, and read the review queue.
2. Choose one bounded task, verify its evidence and rights, and do the work.
3. Run the existing structural validator and relevant artifact tests. This helper does not replace them.
4. Review the diff, update the metadata and checksums deliberately, then rerun the helper with `--compare` against the saved report.
5. Keep publication a separate authorized step.

Detecting stale verification claims against explicitly recorded dates remains a possible later improvement and is not implemented. No daily scheduler or background agent is installed by this tool.

## License

This newly written helper, its tests and registry use the archive's existing [CC BY 4.0 license](../../LICENSE). It does not relicense the separately licensed recovered artifacts. The choice follows the current compilation license rather than silently assigning a new software license.
