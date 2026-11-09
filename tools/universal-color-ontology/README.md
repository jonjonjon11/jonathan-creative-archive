# Universal Color + Ontology Core v1

A preserved, dependency-free JavaScript source toolkit connecting color representations, mathematics, music and a finite concept vocabulary. This is an experimental foundation for builders, not a playable app, renderer, complete knowledge graph or validated scientific database.

## Contents and rights

- [Universal Color](upstream/packages/universal-color/README.md): sRGB/linear RGB, CIE XYZ D65, CIELAB, OKLab/OKLCh, alpha compositing, semantic colors and visual-state metadata, with a JSON Schema and 15 tests.
- [Ontology Core](upstream/packages/universal-ontology-core/README.md): 593 finite vocabulary nodes and generators for integers, rationals, complex numbers, polygons, sRGBA8 colors, MIDI notes, chords and candidate pairs, with 14 tests.
- [Exact-source manifest](source-review-manifest.json): original paths, byte counts, Git blob hashes and SHA-256 hashes for all 12 unchanged upstream files.

The preserved `upstream/` snapshot retains its complete [CC0 1.0 Universal license](upstream/LICENSE). This archive README and publication manifest are newly written CC BY 4.0 documentation under the [compilation license](../../LICENSE). The source's credit to Björn Ottosson for OKLab conversion is retained. Standard mathematical and color-conversion formulas are not claims of new scientific invention.

Source revision: `e17aaa014a9cf66b6a510c01c5563409780b8656`, authored/committed by the repository owner. Source identity and original paths are recorded as metadata without private source links. The archive does not include the rest of that repository or its history.

## Use the new bounded adapter

The separately authored [bounded generators and offline CLI](bounded/README.md) preserve exact large integers and reduced fractions, validate note/tuning inputs, and reject computed frequency overflow or underflow. **23 new tests pass** alongside the 29 preserved tests. The adapter is opt-in, CC BY 4.0, and does not change the original CC0 files. It covers four number/pitch functions only, with no rendering or audio. See the [dated review](../../docs/reviews/bounded-ontology-generators-2026-11-09.md).

## Run the preserved tests

Requires Node.js 20 or later. From this directory:

```sh
node --test upstream/packages/universal-color/test/*.test.mjs upstream/packages/universal-ontology-core/test/*.test.mjs
```

No install, package download, build, network service or dependency is needed. Both package manifests deliberately retain `private: true`; this preservation release does not publish them to npm.

Fresh archive revalidation on 2026-11-07: **29 tests passed, zero failed or skipped**, using Node v24.22.1. The tests cover representative numerical round trips, invariants, registry counts/IDs and ordinary generator examples. No UI exists here, so no browser, rendering, audio or device acceptance is claimed.

## Important limits before reuse

1. `chordNode()` validates note values but does not validate its `a4Hz` tuning reference. Negative or non-finite tuning can produce invalid frequencies. A hardened derivative should validate it consistently with `midiNoteNode()`.
2. `integerNode()` and `rationalNode()` use `BigInt`, but a large JavaScript Number may already have rounded. Use bigint or exact integer strings for large values and reject unsafe numeric inputs in any derivative.
3. Some color/visual functions do not reject every invalid or non-finite input. For example, `visualMapNode(..., {activity: Infinity})` can emit `Infinity`, incompatible with an ordinary finite JSON representation. Existing tests are not exhaustive schema or input validation.
4. **The upstream name `safeDisplayRate()` and its legend wording do not establish photosensitivity or accessibility safety.** Its default upper rate is 8 Hz; the vibration mapping can reach 12 Hz. These are data values, not rendered flicker. A future UI should default to static presentation and separately evaluate flash area, luminance, motion and reduced-motion behavior. Do not advertise these rates as safe flashing.
5. Semantic colors are teaching/design choices, not physical properties of electrons, numbers or other concepts. Display clipping may diverge from the un-clipped linear-RGB/luminance fields. No spectral material model, chromatic adaptation, full gamut policy or calibrated display pipeline is included.
6. Registry labels such as `EVALUATED_DATA` lack authoritative citations per record. The 593 nodes form a finite vocabulary, not an exhaustive or independently validated body of knowledge. Candidate connections are not factual relationships. No patient data, diagnostic or treatment tool is supplied.
7. Pair spaces grow quadratically with the working set. Keep inputs bounded rather than materializing unbounded combinations.
8. The original Ontology Core README mentions `UNIVERSAL_ONTOLOGY_CORE_v1.zip`. That separate ZIP is not included or verified in this archive. Its mention is preserved as historical source text.

The original source is intentionally unchanged, including these limitations. Put hardening or a static visual explorer in a separate derivative and test it independently.

## Privacy and review scope

The selected files contain local pure functions and Node built-in tests. Review found no runtime dependencies, network calls, persistence, sensor APIs, imported artwork/media, private personal records or credential patterns. The JSON Schema vocabulary URL is an identifier; the modules do not fetch it. This scoped inspection and the passing tests are not a full security, legal, scientific or accessibility audit.
