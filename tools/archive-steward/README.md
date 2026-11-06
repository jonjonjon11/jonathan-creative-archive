# Archive Steward 0.1

An inspectable offline mini-helper for maintaining this creative archive. It reports byte drift, missing provenance files and dangling source references, then turns the archive's existing next steps into a review queue. It is a deterministic Python command-line tool, not a language model or an autonomous publisher.

## Run

Requires Python 3.10 or later and no third-party packages. From the repository root:

```sh
python3 tools/archive-steward/archive_steward.py .
python3 tools/archive-steward/archive_steward.py . --format json
python3 -m unittest discover -s tools/archive-steward/tests -p 'test_*.py' -v
```

The root directory is required explicitly. Output goes only to the terminal. To save a report, redirect it to a location **outside** the archive so it does not become an unlisted file. The helper never refreshes checksums: an editor must first review each changed or new file, then deliberately update the baseline.

Exit codes: **0** means no configured integrity/metadata errors, **1** means findings need review, and **2** means invalid/missing input or an invalid command. Warnings do not change a zero exit code. Zero is not permission to publish or a claim of legal clearance.

## What it does

- Compares included files with the SHA-256 baseline in `data/checksums.json` and flags missing, changed and unlisted files.
- Separately checks preserved-source hashes in the two existing source manifest formats, Lumen's generated-build hash and Reality Atlas's pinned HTML hash. Updating only the archive baseline cannot hide a change to a preserved original.
- Warns when a registered artifact has no independent preserved-source or pinned-file hash checks.
- Reads the recovered-artifact registry in `data/artifacts.json`, checks the artifact directory, source references and declared license/provenance/test-record file presence, and reports license scope and verification limits. Declared licenses are metadata, not the output of a legal review.
- Counts concept statuses and source-access declarations, checks concept/artifact source IDs and concept artifact paths, and lists sources without a concept/artifact reference. A source may still be cited in prose; that list is not a deletion recommendation.
- Copies every concept's existing next step into a stable review queue. Evidence gaps, delivery receipts and historical-only test reports come first; other records follow by ID. This ordering is a simple rule, not a quality, urgency or scientific confidence score.
- Produces deterministic text or JSON with no clock-dependent timestamps.

## Boundaries

It makes no network calls, requests no credentials, runs no source files or shell commands, writes no files, and never publishes, messages people or makes decisions about sharing. Running the **tests** creates temporary fixture directories, then removes them. The helper itself only reads the explicitly selected archive.

It ignores `.git` and `__pycache__` directories, `.pyc` files and `.DS_Store`. The checksum file is excluded from its own baseline. Other unlisted files, including local reports, are flagged. Input-controlled exclusions are not accepted. Symbolic links and traversal paths are rejected; JSON inputs are limited to 4 MiB and hashed files to 64 MiB. Unsupported files require human review, not silent omission.

The tool is intended for a trusted, stationary local checkout, not a hostile or concurrently changing filesystem. Its path checks are not an operating-system security sandbox. It does not prove who created the baseline or detect coordinated changes to both files and hash records. It does not parse license obligations or validate the truth of a verification record. It does not execute tests, check URLs, search private accounts, recover missing files, detect all secrets, review science, or certify privacy, accessibility, medical safety or educational efficacy. Metadata shown in a report may itself contain private information; review it before sharing.

`data/artifacts.json` currently lists the three recovered artifact families, not every support script. Its `rights` fields name the declaration, applicable file scope, local license file and human review record. Its `verification` fields preserve the scoped test status and limitations. New recoveries require a human-authored entry and source/rights review. The supported upstream manifest layouts are intentionally limited to the two formats already in this archive.

## Verification

All 33 synthetic tests passed on Python 3.12.14 on 2026-11-06. The reviewed archive produced zero configured errors or warnings. These checks cover the helper's local logic, not artifact runtime correctness or legal rights.

## A small improvement loop

1. Run the helper before a proposed archive change and read the review queue.
2. Choose one bounded task, verify its evidence and rights, and do the work.
3. Run the existing structural validator and relevant artifact tests. This helper does not replace them.
4. Review the diff, update the metadata and checksums deliberately, then rerun the helper.
5. Keep publication a separate authorized step.

Possible later improvements include comparing two reports and detecting stale verification claims against explicitly recorded dates. Those features are not implemented. No daily scheduler or background agent is installed by this tool.

## License

This newly written helper, its tests and registry use the archive's existing [CC BY 4.0 license](../../LICENSE). It does not relicense the separately licensed recovered artifacts. The choice follows the current compilation license rather than silently assigning a new software license.
