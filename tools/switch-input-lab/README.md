# Switch Input Lab

A dependency-free Python learning tool for turning invented, timestamped switch observations into debounced press/release events. It is a small inspectable foundation for learning about accessible-input software, embedded state machines, sampling, and latency. It does not connect to hardware, control an appliance, collect patient data, or establish clinical suitability.

Start with the new [One press, one star programming exercise](../../docs/lessons/one-press-one-star.md): trace a score variable, loop over confirmed events, and change the reward without counting held inputs repeatedly. This is a text-only rule, not a live keyboard interface or graphical game.

The [complete lesson](../../docs/lessons/switch-input-foundations.md) includes three worked examples and five exercises with answers. The code, fixture, explanations, and tests are all present locally; nothing has to be downloaded to run them after obtaining the repository.

## Run offline

From the repository root, using Python 3.8 or later:

```sh
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json
python3 tools/switch-input-lab/switch_input.py tools/switch-input-lab/fixtures/synthetic-bounce.json
python3 tools/switch-input-lab/switch_input.py tools/switch-input-lab/fixtures/synthetic-bounce.json --json
python3 -m unittest discover -s tools/switch-input-lab/tests -p 'test_*.py' -v
```

The original switch fixture produces exactly:

```text
Synthetic trace: 14 samples; stability interval 20 ms
45 ms: press
90 ms: release
Only sample-time observations are modeled; unobserved intervals remain unknown.
Educational simulation; no hardware or clinical validation.
```

`--json` includes the initial and final accepted states, the event list, and limits. Output is deterministic. The program writes only to stdout/stderr and makes no network calls. It exits 0 on a valid simulation, 1 on invalid trace input, and 2 on invalid command syntax.

## Model

The initial accepted state is supplied explicitly: `initial_pressed`. It is a modeling assumption, not an observation inferred from the first sample. Each sample has a strictly increasing integer `timestamp_ms` and a boolean `pressed`.

A reading that differs from the accepted state starts a candidate and stores its timestamp. A reading equal to the accepted state cancels any candidate. A later opposite-state reading accepts the candidate only when the elapsed time from its first observation is at least `stability_ms`. An accepted change emits one event at the confirming sample's time. Holding a state does not emit repeated events. No event is invented after the last sample.

This rule describes stability of the **observed sequence**. The simulator cannot establish that a physical contact remained in one state between samples. A long sampling gap can hide bounce or a short intentional action. There is no maximum-gap rejection rule in this teaching model; the JSON result explicitly preserves that limitation. A future hardware design must address sampling gaps and faults based on actual requirements.

The 20 ms fixture setting is invented for teaching. It is not a recommended setting for a particular switch or person. Physical switch characteristics, electronics, sampling, response requirements, and the intended user's preferences affect a real design.

## Input format and limits

The included [fixture](fixtures/synthetic-bounce.json) is the complete example format. `schema_version` must be `1.0`; `metadata.synthetic` must be true and `title` and `provenance` must be nonempty text. This educational lab accepts only examples declared synthetic. A declaration does not independently prove provenance or screen for private information; do not feed it personal or patient traces.

`stability_ms` is an integer from 1 to 60000. The input must contain 1–10000 observations. Timestamps are nonnegative integers no greater than 2^53−1 ms; booleans are not accepted as integers. Repeated or decreasing timestamps, non-boolean states, duplicate JSON keys, non-finite JSON numbers, malformed UTF-8, JSON integers longer than 32 digits, excessively nested JSON, and files larger than 2 MiB are rejected. The entire trace is validated before events are calculated.

Use a trusted local input path. The tool is an ordinary file reader, not a hostile-filesystem sandbox. It does not execute metadata, follow instructions embedded in a trace, or interpret data fields as file paths. No claims are made about detecting all sensitive information or malicious filesystem behavior.

## Evidence and rights

[Source notes](sources.json) record two inspected technical references. Texas Instruments explains the physical problem of contact bounce; Arduino's official example illustrates elapsed-time software debouncing. This simulator and lesson are original implementations and explanations. Their timing boundary and output behavior are specified here; they are not a copy or exact emulation of Arduino's example.

New code, text, tests, and invented fixture follow this archive's existing [CC BY 4.0 license](../../LICENSE). The cited sources retain their own rights. No diagrams, source prose, or external source code are reproduced.

## Verification and next contribution

The synthetic test suite covers bouncing press and release, held states, threshold equality, cancellation, elapsed time versus sample count, sparse samples, initial state, repeated cycles, input errors, byte/sample/numeric limits, deep nesting, inert metadata, deterministic JSON output, and readable CLI errors. Passing these tests establishes these local behaviors only. No hardware, person, medical device, assistive technology, screen reader, or real-world usability has been tested.

The star counter composes this simulator and awards points only for confirmed press events. Its original two-press fixture yields scores of 1 at 45 ms and 2 at 150 ms. `--stars-per-press 2` changes those totals to 2 and 4 without changing event times; `--json` preserves all input events and limits. Invalid input or rewards exit 1 and invalid command syntax exits 2. No results are written to files. The new tests also cover initial held states, unfinished releases, score limits, maximum sample count, deterministic CLI output and escaped Unicode diagnostics.

A useful next task is an independent state-machine review: recalculate the fixture, add a counterexample involving a sampling gap, and explain what the software can and cannot conclude. Changes intended for an actual access device require an agreed user need, qualified engineering review, hardware testing, fault analysis, and appropriate authorization; this lab does not supply those approvals.

## Extraction provenance

The foundation lesson, implementation, original fixture, source notes and original tests were extracted from [PR #4](https://github.com/jonjonjon11/jonathan-creative-archive/pull/4) at `81d395382ea18b8116ba96ddd1c202c8ab361948`. The unrelated biomedical files and evidence CLI were not imported. This version adds the game-rule exercise and makes input-derived error messages printable even for escaped surrogate characters. The original algorithm and 20 ms fixture behavior are preserved. See the [integration review](../../docs/reviews/switch-learning-integration-2026-11-08.md) for exact checks and limits.
