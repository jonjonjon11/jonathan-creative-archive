# Bounded ontology generator review — 2026-11-09

## Scope and source boundary

Based on main `7b7962f1b2e64c5cc122bba09fb458bfe97ab172`. The archive already documented unsafe numeric input and invalid tuning in the preserved Ontology Core and named a separate derivative as its next experiment (`CON-022`). This contribution adds `tools/universal-color-ontology/bounded/`: four opt-in validation adapters, an offline command-line entry point, instructions and regression tests.

No preserved file is modified. All 12 CC0 originals, the exact-source manifest and existing tests remain unchanged. New files and explanatory updates use the archive's CC BY 4.0 license. Public source is the included revision `e17aaa014a9cf66b6a510c01c5563409780b8656`; no private material or external dataset was needed. The original source is evidence of the behavior below, not independent validation of all ontology claims.

## Reproduced original behavior

Before implementing the adapter, Node v24.22.1 reproduced:

- `integerNode(9007199254740993)` emitted identity `urn:universe:mathematics:integer:9007199254740992`, because the Number literal had already rounded. Original rational operands have the same conversion boundary.
- `chordNode([69], -440)` emitted a negative 440 Hz frequency and negative reference.
- `midiNoteNode(127, Number.MAX_VALUE)` accepted a finite reference but computed infinity; ordinary JSON serialized the frequency as `null`.
- `midiNoteNode(0, Number.MIN_VALUE)` emitted a zero frequency through underflow.

The adapter rejects unsafe Numbers and invalid output frequencies, accepts exact bounded strings/bigints, and retains the original canonicalization and tuning formula. It makes no claim to reconstruct digits already lost before a call. Existing consumers are unchanged unless they choose the adapter's import path.

## Independent review and corrections

Independent AI code review reproduced a candidate bound defect: a one-element array's custom iterator could yield 129 notes despite the pre-deduplication limit. The candidate now snapshots the array length, requires own indexed entries and performs bounded indexed reads; custom iterators are ignored. A regression covers this and inherited sparse entries. The review also found that negative-zero MIDI input did not retain strict JSON roundtrip identity; it now normalizes to zero with a regression.

The independent reviewer ran the original 29 tests and an additional 5,090 deterministic checks across integer representations, 1,024-digit consecutive-Fibonacci rational operands and all 128 MIDI notes over 12 tuning magnitudes. The tuning sweep accepted 1,412 finite cases and rejected 124 overflow/underflow cases. All 12 upstream byte counts, SHA-256 and Git blob hashes matched their unchanged manifest. This is software review by another AI, not human scientific, accessibility or educational acceptance.

## Local verification

Environment: Linux, Node v24.22.1, Python 3.12.14. All executed checks below passed on the final candidate:

- **23 new Node tests**, including subprocess CLI checks, exact values over the safe-Number limit, 1,024-digit operands, invalid/coerced/sparse inputs, bounded indexed chord reads, negative zero, frequency overflow/underflow and output compatibility.
- **329 Python tests** across authoring (31), arithmetic lessons (31), switch input (29), cooperation/rescue (25), Archive Steward (57), Idea Finder (32), evidence integrity (43) and the ALS evidence map/follow-ups (81).
- **212 combined Node tests**, including the 23 new tests, plus **46 Reality Atlas calculation/syntax checks**.
- Module/project/task validation; Lumen and motion static/build checks; cooperation mission validation; exact water standalone build parity; evidence-map validation, generated-view parity and all manifest hashes; clean synthetic evidence audit.
- Archive structural/local-link validation, whitespace checks and Archive Steward after deliberate review of this contribution's checksums. The prior main baseline was clean; no unrelated baseline was refreshed.

Representative reproducible commands, from the repository root:

```sh
node --test tools/universal-color-ontology/upstream/packages/*/test/*.test.mjs tools/universal-color-ontology/bounded/tests/*.test.mjs
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The complete aggregate commands are in [.github/workflows/knowledge-commons-status.yml](../../.github/workflows/knowledge-commons-status.yml). This contribution adds its tests to the existing Node step and explicitly allows its four reviewed `.mjs` paths in the archive file-type policy. Other new `.mjs` paths remain rejected; no test/check is removed. Local browser suites were not repeated because no browser app changed. Existing browser jobs must still pass on the published candidate before integration. The repository's Actions record is the authority for remote run status; this local report does not predict it.

## Limits and next step

This is not a generic sanitizer or a sandbox for arbitrary executable JavaScript objects. Bounds cover ordinary inputs; caller-supplied proxies/getters may execute code, and a huge bigint can already exist before this adapter sees it. Only four functions are exported. Color mapping, display rates, vocabulary evidence and pair enumeration remain outside this scope.

MIDI frequencies remain binary floating-point approximations in a conventional equal-tempered reference model. Positive subnormal outputs may be imprecise, and arbitrary accepted frequencies need not be audible or physically realizable. No renderer or audio path is added. There was no human/device, assistive-technology, learning-effectiveness, acoustical or clinical testing. No health claims or biomedical proposal changes were made.

Use the [offline CLI and API](../../tools/universal-color-ontology/bounded/README.md) for inspectable number/pitch records. Expand the derivative only for a concrete consumer with equally explicit input/output contracts. Claim-level vocabulary citations and static-by-default visual design remain separate future work.
