# First public edition validation report

Edition: 0.1 first public edition. Review date: 2026-11-06.

## Documentation structure

Command: `python3 scripts/validate_archive.py`.

Result: PASS. JSON parseability, unique IDs, required fields, source references, status vocabularies, internal Markdown links, file types, and selected private-locator/key markers were checked.

## Included Reality Atlas artifact

Command: `node scripts/check_reality_core.cjs`.

Result: 46 focused checks passed on Node v24.22.1. The exact unchanged artifact hash and full inline-script syntax were checked, followed by calculation-layer tests. See `tools/reality-atlas/core-check-results.json` and the tool README for scope and limitations.

Fresh browser status: BLOCKED BEFORE PAGE LOAD. Chromium could not create its process-singleton socket in this environment, including the permitted escalated attempt. No fresh rendering, UI, downloads, SVG exports, accessibility, responsive layout, mobile, headset, or performance acceptance is claimed. Historical upstream browser counts are separate and were not rerun.

## Cooperation/rescue authoring kit

From `artifacts/cooperation-rescue/`, run `python3 contract.py` and `python3 -m unittest discover -s . -p 'test_*.py' -v`.

Result on 2026-11-06: four draft mission definitions validated; all 25 preserved tests passed. Exact-source hashes for the three original source/data/test files and CC0 license match the included source manifest. The suite covers bounded inputs, dependency ordering, 288 objective permutations with retries, repeated completion, isolated sessions and penalty-free exit. Tests were rerun in the integrated archive with a minimal environment and bounded resources.

This is a draft/unmerged authoring/reference artifact, not a playable game, Unity integration, authoritative multiplayer service, medical or rescue training, or accessibility/safety certification. Source review flags remain unchanged.

## Lumen Commons 0.1

From `tools/lumen-commons/`, run `node --test tests/core.test.cjs` and `python3 tests/static_check.py`.

Result on 2026-11-06: all 24 Node tests passed under Node v24.22.1. Static checks passed for exact source/build parity, CSP hashes, the 250 KB budget and selected prohibited runtime APIs. The regenerated HTML is 81,407 bytes and matches SHA-256 `e802f3137cf16d0ce693f28c70182a32aadaef68b8547905d000433ee477d1e2`. Included original files match their exact-source Git blob and SHA-256 hashes.

Fresh browser suite: BLOCKED BEFORE PAGE LOAD. Chromium exited during startup because the sandbox denied process-singleton socket creation. The app was not loaded. Historical 35-check browser evidence remains separate. No current rendering, interactions, audio, download, native-persistence, Safari/device, accessibility, educational-efficacy or child-safety acceptance is claimed.

## Archive Steward 0.1 maintenance helper

Commands from the repository root:

- `python3 -m unittest discover -s tools/archive-steward/tests -p 'test_*.py' -v`
- `python3 tools/archive-steward/archive_steward.py .`
- `python3 tools/archive-steward/archive_steward.py . --format json`

Result on 2026-11-06: all 33 synthetic tests passed under Python 3.12.14. Both text and JSON reports completed with zero configured errors or warnings against the reviewed 58-file archive (57 baseline hashes, 16 preserved-source hashes, one generated-build hash and one pinned-artifact hash). The existing structural and artifact checks also passed; browser limitations remain unchanged.

The helper is newly written editorial software under the existing compilation license. Its synthetic tests cover checksum drift, preserved-source disagreement after baseline updates, missing/unlisted files, source/status metadata, both preserved-manifest formats, symlinks/traversal, malformed JSON, size limits, nonregular files, deterministic reports, CLI exit codes and unchanged archive bytes. See the helper README for the exact scope and limitations. It does not run the artifact suites or establish new browser verification.

## Archive Steward 0.2 comparison improvement

The 0.2 helper adds optional `--compare PREVIOUS_JSON`. Its report retains actual file hashes and selected source metadata; comparison output identifies changed records/bytes and introduced/no-longer-reported findings without silently hiding current persistent findings.

Commands remain those above, plus `python3 tools/archive-steward/archive_steward.py . --compare /path/to/previous-report.json`. Save both previous and current reports outside the repository. JSON output can be reused for another comparison. Version 0.1 inputs have explicit missing file/source comparison coverage rather than invented history.

Result on 2026-11-06: all 57 synthetic tests passed under Python 3.12.14. The original 33 checks remain included. The new tests cover record/rights/source changes, byte changes after a refreshed baseline, added/removed/unhashable files, finding differences, legacy and malformed reports, path safety, persistent errors, terminal control-character escaping, incomplete-inventory handling and reusable output. Directory read failures cannot be silently relabeled as file removals. The real-archive comparison identified the seven changed content files after checksum refresh, with zero current errors/warnings and no metadata changes. A report emitted by published 0.1 also compared successfully with explicit missing file/source coverage. Existing artifact bytes and browser-verification limits remain unchanged.

The comparator does not authenticate report history or establish that a removed finding is truly fixed. It compares selected metadata fields and local bytes; changes alone are not a quality score, new runtime verification or permission to publish.

## Universal Color and Ontology Core v1 preservation

From `tools/universal-color-ontology/`, run `node --test upstream/packages/universal-color/test/*.test.mjs upstream/packages/universal-ontology-core/test/*.test.mjs`.

Result on 2026-11-07: 29 tests passed, zero failed or skipped, under Node v24.22.1. All 12 preserved upstream files, including the complete CC0 license, match their source Git blob and SHA-256 hashes. No installation or runtime dependencies are needed. The source toolkit has no UI, so no browser or rendering acceptance is asserted.

Known limits are recorded in the toolkit README: tuning validation differs between note/chord generators; unsafe Number integers can round; some visual inputs allow non-finite values; semantic colors and vocabulary labels are not physical or authoritative scientific evidence; pair growth is quadratic; and the separately mentioned ZIP is unverified. In particular, `safeDisplayRate` does not establish safe flashing or accessibility. The source snapshot remains unchanged.

The integrated archive's structural check, all 57 Archive Steward tests, its four-family manifest/hash report and existing focused artifact suites passed. The archive now contains 22 concepts and 35 source records; earlier counts above describe their historical checkpoints. Existing browser limits are unchanged.

## Idea Finder 0.1

Command from the repository root: `python3 -m unittest discover -s tools/idea-finder/tests -p 'test_*.py' -v`.

Result on 2026-11-07: all 32 synthetic tests passed under Python 3.12.14. Coverage includes literal all-terms matching, Unicode normalization, exact tag/status filters, deterministic ranking and ties, duplicate-term handling, bounded/omitted results, source attribution, artifact relationship limits, unknown fields, malformed/oversized inputs, nonregular files, symlinks including a root loop, inert metadata paths, controlled errors, terminal escaping and unchanged archive bytes.

The tool reads only the three specified metadata files. It does not run artifact code, check URLs, certify rights, evaluate science or claim semantic retrieval. A shared source ID is not proof of implementation. The existing browser-verification limits remain unchanged.

Integrated after the Universal Color/Ontology preservation release: real queries for music, rescue, inspected physics, Lumen and ontology resolve against the expanded 22-concept/35-source archive. The ontology result preserves its known input-validation and display-safety limits. All prior artifact files, registry/source/concept records and licenses are unchanged by this helper addition.

## Rights and privacy boundary

Exact-commit CC0 provenance was reviewed separately for Reality Atlas, Lumen Commons, Universal Color/Ontology and the preserved cooperation/rescue files; their complete source licenses are included. The new compilation is CC BY 4.0, with the owner’s existing root license preserved; other upstream rights remain separate. Private conversation/Drive/file locators and editorial review records remain outside this repository. The unchanged tool retains its original GitHub source link, which may require repository access.

These are pre-publication content checks. The initial public repository’s owner, public visibility, README, and CC BY 4.0 license were verified before adding this edition. The placeholder README is replaced by the archive index, and its existing license is preserved unchanged. No source-project history or application deployment is included. SHA-256 values in `data/checksums.json` provide file-integrity comparison, not proof of scientific truth or rights. These checks do not certify license compatibility, clinical or educational efficacy, exhaustive absence of secrets, account completeness, or full source-project correctness.
