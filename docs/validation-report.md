# First public edition validation report

Edition: 0.1 first public edition. Review date: 2026-11-06.

## Documentation structure

Command: `python3 scripts/validate_archive.py`.

Result: PASS. JSON parseability, unique IDs, required fields, source references, status vocabularies, internal Markdown links, file types, and selected private-locator/key markers were checked.

## Included Reality Atlas artifact

Command: `node scripts/check_reality_core.cjs`.

Result: 46 focused checks passed on Node v24.22.1. The exact unchanged artifact hash and full inline-script syntax were checked, followed by calculation-layer tests. See `tools/reality-atlas/core-check-results.json` and the tool README for scope and limitations.

Fresh browser status: BLOCKED BEFORE PAGE LOAD. Chromium could not create its process-singleton socket in this environment, including the permitted escalated attempt. No fresh rendering, UI, downloads, SVG exports, accessibility, responsive layout, mobile, headset, or performance acceptance is claimed. Historical upstream browser counts are separate and were not rerun.

## Rights and privacy boundary

Exact-commit CC0 provenance was reviewed for the single standalone tool; its complete license is included. The new compilation is CC BY 4.0, with the owner’s existing root license preserved; other upstream rights remain separate. Private conversation/Drive/file locators and editorial review records remain outside this repository. The unchanged tool retains its original GitHub source link, which may require repository access.

These are pre-publication content checks. The initial public repository’s owner, public visibility, README, and CC BY 4.0 license were verified before adding this edition. The placeholder README is replaced by the archive index, and its existing license is preserved unchanged. No source-project history or application deployment is included. SHA-256 values in `data/checksums.json` provide file-integrity comparison, not proof of scientific truth or rights. These checks do not certify license compatibility, clinical or educational efficacy, exhaustive absence of secrets, account completeness, or full source-project correctness.
