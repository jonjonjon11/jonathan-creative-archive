# Learner-entry repair, 2026-11-08

## Scope

Based on main commit `86b9b03f8d654f589e5aea061fcee131c2a229b4`. The existing quick start directed learners through schema/JSON files and developer-only submission commands, referred to a missing verification template, and suggested disabled GitHub Discussions. The browser task excluded volunteers with one browser. No open PR covered this repair at the initial check.

The revised [quick start](../QUICKSTART.md) and [start page](../../START_HERE.md) lead directly to existing readable lessons. They explain ZIP/raw downloads, a paper-first arithmetic adaptation, attribution, private local work and optional account-based issue or fork submission. The missing verification template is now included. The browser task and template accept partial single-setup observations while leaving full acceptance open. The collaboration guide identifies its JSON examples as illustrative, not actual completed reviews.

No runtime, canonical lesson data, preserved third-party source, license, dependency, deployment or biomedical branch changes are included. New original text and tests use the archive's existing CC BY 4.0 license.

## Verification

The seven new `tools/tests/test_learner_entry.py` checks cover local guide links and used heading fragments, readable entry points, the two arithmetic equalities and source version, report provenance/uncertainty fields, partial browser evidence, and voluntary licensed sharing. All seven fail on the base tree (four assertion failures and three missing-field/file errors) and pass on the changed tree. These are selected structural/textual regression contracts, not a reading study or complete Markdown parser.

The arithmetic adaptation is author-written: 12 pencils / 3 tables = 4 pencils per table becomes 15 / 3 = 5, checked with multiplication. It is explicitly not a real learner observation. The canonical division record and existing lesson remain unchanged.

Local validation passed 251 Python tests, 183 Node tests and 46 additional calculation/syntax checks, plus module/project/task validation, both standalone build-parity checks, four rescue mission definitions, evidence-map validation/generated views/eight manifest hashes, the synthetic evidence audit, archive structure/internal links and whitespace checks. Commands follow [.github/workflows/knowledge-commons-status.yml](../../.github/workflows/knowledge-commons-status.yml). The existing workflow discovers the new seven tests without a workflow edit. Local runtime: Python 3.12.14 and Node 24.22.1.

Independent AI review approved the ten-file content/test diff after independently running 31 tools tests, 7 division tests, 29 switch-input tests, 46 motion Node tests, motion static/build parity, all record validators, archive structural checks and whitespace checks. Its review found no blocking defect; it did not perform human learner or accessibility validation.

Before publication, the final staged tree is exported and checked separately, without Git metadata or untracked local work. Exact commit-level remote results belong to the corresponding GitHub Actions run. Do not interpret this record as a substitute for reading that run.

Only reviewed changed/new files receive checksum updates. Unrelated entries and preserved-source hashes remain unchanged.

## Remaining limits

Independent AI review and software checks cannot establish human learner comprehension, educator acceptance, accessibility, real-device/touch behavior or suitability for any particular person. This change performs no new physical-device, assistive-technology, translation or learner testing. The inherited motion/Lumen browser suites provide scoped CI checks, not full device acceptance. GitHub's download interface can differ by client; no universal client behavior is promised. Plain Markdown remains readable as text but is not a newly rendered or user-tested learning interface.

The browser task remains open for its recorded physical-device, Safari/Edge, human visual and assistive-technology gaps. One partial report does not close it. Posting on GitHub requires an account and connection, and no anonymous intake or automatic submission service was added. No real learner data or private conversations were collected.
