# Bounded exact-number and pitch generators

An original, dependency-free validation adapter and offline CLI for four functions in the preserved [Ontology Core](../upstream/packages/universal-ontology-core/README.md). It produces inspectable JSON for exact integers, reduced fractions, equal-tempered MIDI pitches and canonical note sets. Requires **Node.js 20 or later**. No installation or account is needed.

This is a separately tested derivative, not a change to the recovered source. It does not render color, flash, move or play sound. It supplies mathematical data, not an accessibility, hearing-safety, scientific or educational certification.

## Try it offline

From the archive root:

```sh
node tools/universal-color-ontology/bounded/cli.mjs integer 9007199254740993
node tools/universal-color-ontology/bounded/cli.mjs rational 6 -8
node tools/universal-color-ontology/bounded/cli.mjs midi 69
node tools/universal-color-ontology/bounded/cli.mjs chord 67,60,64,60 432
node tools/universal-color-ontology/bounded/cli.mjs --help
```

The integer's `properties.value` is the exact string `"9007199254740993"`. The rational has numerator `"-3"` and denominator `"4"`. MIDI note 69 uses a default A4 reference of 440 Hz and returns 440 Hz. The chord sorts and deduplicates its notes to `[60, 64, 67]`, using the supplied 432 Hz reference. Chords here are note sets, not named harmonic analyses or timed performances.

Every successful command writes **one JSON record to stdout**, with exit status 0. Invalid inputs write a short error to stderr, no JSON to stdout, and exit status 1. The CLI performs no file read/write, network request, audio playback or saved-state operation. Your shell can redirect stdout to a file if you want a local copy. These examples contain mathematical values only, not measured or personal data.

## Use as a module

```js
import { integerNode, rationalNode, midiNoteNode, chordNode }
  from './tools/universal-color-ontology/bounded/generators.mjs';

integerNode('9007199254740993');  // Exact decimal string.
rationalNode(6n, -8n);           // Canonical -3/4.
midiNoteNode(69, 440);          // A4 in this tuning context.
chordNode([67, 60, 64, 60]);    // Canonical [60, 64, 67].
```

Accepted inputs deliberately have a narrower contract than the preserved originals:

- **Integers and rational operands:** safe integer JavaScript Numbers, bigint, or decimal integer strings containing an optional `+`/`-` followed by digits. At most 1,024 decimal digits per operand, including leading zeros but excluding a sign. No whitespace, radix prefixes, decimal points, exponent notation, booleans or object coercion. Zero denominators are rejected. Fractions reduce exactly and keep the denominator positive.
- **Precision:** a Number outside `Number.MIN_SAFE_INTEGER` through `Number.MAX_SAFE_INTEGER` is rejected even when its particular value is representable. Use a string or bigint before Number conversion; already-lost digits cannot be recovered. Passing an unsafe numeric literal to `BigInt(...)` first does not recover them either. Returned integer values are decimal strings, making ordinary JSON serialization exact.
- **Notes:** integer Numbers from 0 through 127. Chords require a dense array of 1–128 input notes before deduplication. Input arrays are not mutated; output arrays do not alias them. Notes are sorted, duplicates removed, and child IDs use the same tuning reference.
- **Tuning:** positive finite Numbers, default 440 Hz. Every computed frequency must also be positive and finite; combinations that overflow to infinity or underflow to zero are rejected. Positive subnormal outputs are allowed and may be imprecise. This is a numerical boundary, not a range of audible, useful or physically realizable frequencies. The formula `a4Hz × 2^((note − 69)/12)` and floating-point approximations are unchanged.
- **CLI spelling:** notes use 1–3 unsigned decimal digits. Tuning uses decimal/scientific notation, up to 64 characters. CLI tuning becomes a Number and can round; it is not exact decimal arithmetic. Integer arguments are kept as text. Extra arguments and unknown commands are errors.

Invalid types/syntax or out-of-range values throw `TypeError` or `RangeError` in the module. The digit/note bounds limit ordinary workloads; they are not a hostile-code sandbox. Custom chord iterators are ignored; in-process getters/proxies can execute caller code, and arbitrary huge bigint values already allocated by a caller are outside these resource bounds. No unvalidated generator, color mapper, pair enumerator or vocabulary registry is re-exported.

## Evidence, compatibility and remaining work

[The dated review](../../../docs/reviews/bounded-ontology-generators-2026-11-09.md) records the reproduced upstream failures, tests, source preservation and review limits. Run the preserved and new tests together:

```sh
node --test tools/universal-color-ontology/upstream/packages/*/test/*.test.mjs tools/universal-color-ontology/bounded/tests/*.test.mjs
```

The new 23-test suite covers exactness, 1,586 deterministic rational cases, all 128 MIDI notes at three ordinary tuning references, malformed/sparse/coerced inputs, limits, frequency overflow/underflow, immutable inputs and subprocess CLI behavior. Ordinary accepted records retain the original IDs and shape; negative-zero MIDI inputs normalize to zero; consumers must explicitly opt into this adapter. Existing imports continue to expose the original behavior. No ID migration or upstream baseline refresh is performed.

The original toolkit's other [known limitations](../README.md#important-limits-before-reuse) remain. The finite vocabulary still needs claim-level citations, and the color/visual APIs have not been hardened here. No browser UI, rendered color accuracy, acoustic behavior, device compatibility, learner feedback or assistive-technology assessment was performed for this addition.

## Rights and provenance

New code, tests and this explanation are original archive contributions under [CC BY 4.0](../../../LICENSE). Suggested attribution: “Bounded ontology generators, Jonathan's Creative Archive Contributors, 2026, CC BY 4.0,” with the [repository source](https://github.com/jonjonjon11/jonathan-creative-archive/tree/main/tools/universal-color-ontology/bounded), license link and notice of your changes.

The adapter imports four functions from the unchanged [CC0 1.0](../upstream/LICENSE) source revision `e17aaa014a9cf66b6a510c01c5563409780b8656`. All 12 upstream files and their [source manifest](../source-review-manifest.json) remain unchanged. This addition does not relicense those originals or establish a new color or tuning standard. No private sources, third-party prose, new dependencies or external datasets were imported.
