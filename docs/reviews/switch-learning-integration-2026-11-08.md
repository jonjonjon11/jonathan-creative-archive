# Switch learning integration review — 2026-11-08

## Scope and provenance

Base: main `1cef31b22532ff5f8814af302685f0f1faf40f02`. The open branch heads and current repository tree were checked before work. No overlapping active engineering worker was found at that checkpoint.

This isolated change extracts only `tools/switch-input-lab/` and `docs/lessons/switch-input-foundations.md` from [PR #4](https://github.com/jonjonjon11/jonathan-creative-archive/pull/4), source revision `81d395382ea18b8116ba96ddd1c202c8ab361948`. The entire parent branch was not merged. Its biomedical evidence, health lessons, evidence CLI, hypothesis engine and claims are not dependencies and are not imported. The source revision remains available for history and comparison.

Original foundation files retain the existing CC BY 4.0 archive license. New lesson, code, invented fixture and tests use the same license. The two technical references are linked and inspected; their prose, diagrams and code are not copied. No private conversation, patient record, credentials or third-party assets are included.

## What changed

- Preserve the existing timestamped-observation state machine, original bounce fixture, foundation lesson and tests.
- Add [One press, one star](../lessons/one-press-one-star.md), a paper-first trace and beginner programming exercise. It explains variables, lists, a loop and a condition; the runnable score logic composes the existing simulator rather than duplicating it.
- Add a synthetic two-press fixture with accepted presses at 45 and 150 ms and releases at 90 and 210 ms. Holds and releases award no points; the initial accepted state is not itself an event.
- Expose a bounded `--stars-per-press` option and deterministic JSON output. The program is a text-only rule, not a game engine or live input driver.
- Escape input-derived Unicode and control characters so invalid JSON duplicate keys produce predictable, single-line diagnostics. Standard Python stderr already escapes lone surrogates; the change also escapes embedded newlines and other controls.
- Add integration links, source/artifact records, reviewed checksum entries and the new tests to CI. Only changed/new reviewed files receive new hashes.

## Verification

The local workflow commands passed with Python 3.12.14 and Node 24.22.1: 244 Python tests, 181 Node tests and 46 Reality Atlas calculation/syntax checks, plus record validation, source/build parity, evidence-map generated-view/hash verification and the clean evidence-auditor fixture. Local versions are recorded here; other operating systems and Python versions were not tested locally.

The 29 switch-lab tests cover original state rules and new score behavior, initial-held states, release cancellation, unfinished candidates, threshold equality, sparse observations, invalid input/rewards, maximum timestamps and sample counts, interval endpoints, printable Unicode diagnostics, deterministic CLI output, the lesson's complete observation table and its actual code excerpt. Tests remain synthetic. The sparse-trace counterexample deliberately demonstrates information that the algorithm cannot know.

Reproduce the focused checks from the repository root:

```sh
python3 -B -m unittest discover -s tools/switch-input-lab/tests -p 'test_*.py' -v
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json --stars-per-press 2 --json
python3 tools/switch-input-lab/switch_input.py tools/switch-input-lab/fixtures/synthetic-bounce.json
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
```

The full aggregate commands live in `.github/workflows/knowledge-commons-status.yml`. Consult the exact published commit's GitHub Actions result for remote verification; a local pass alone is not a remote pass.

Independent AI review approved all 18 changed paths after re-reading the state machine, retrieving both technical sources, replaying all 22 table rows (including candidate timestamps), running 1,020 additional state-sequence comparisons and passing the aggregate checks above. Review found implicit text encodings in the new tests; all three reads now explicitly use UTF-8 and were retested. A clean staged-file export reproduces the aggregate checks and all 180 checksums with zero warnings. Whitespace checks run in the Git checkout. This is software/source review, not educator acceptance.

## Limits and next contribution

No physical switches, keyboard/controller events, sensors, person, medical device, assistive technology, screen reader or mobile device have been tested. The example cannot infer continuity or intention between samples. The 20 ms interval is a teaching choice, not a recommendation for an input device or person. No hardware control, restored mobility, safety, clinical suitability or learning-effectiveness claim is made.

A useful next contribution is learner/educator feedback on whether the prediction table and code explanation make the distinction between an observation and an event clear. Do not present this release as completing a C# platformer, resuming a historical game request, or validating the unrelated biomedical proposals.
