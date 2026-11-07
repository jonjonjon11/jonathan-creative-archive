# Universal Color / Pixel Engine v1

Dependency-free reference implementation for the Universal Node Graph's first executable representation layer.

## What is implemented

- sRGB encoded channel ↔ linear-light conversion
- sRGB8 ↔ linear RGB
- linear sRGB ↔ CIE XYZ D65
- XYZ D65 ↔ CIELAB
- linear sRGB ↔ OKLab
- OKLab ↔ OKLCh
- relative luminance
- straight-alpha compositing
- deterministic domain/node hue generation
- semantic node color generation in OKLCh
- confidence → alpha
- uncertainty → blur
- source rate → bounded display animation rate
- ontological node type → conventional shape
- node/state → visual-state mapping
- procedural sRGBA8 node addresses
- weighted semantic color-contribution blending
- numerical tests for round trips and invariants

## Scientific honesty

The package distinguishes display/semantic mappings from physical color.

`semanticColorForNode()` is a semantic identity mapping. It is **not** a claim that an electron, integer, element, historical event or other abstract/scientific entity literally has that color.

Physical material/light color should override the semantic fallback when measured/evaluated spectral/colorimetric information is available.

Similarly:
- confidence → alpha is a representation rule
- uncertainty → blur is a representation rule
- source frequency → vibration/flicker is a bounded display mapping
- quantum spin must not be fed into classical `rotationHz`

## Run

```bash
npm test
```

Requires Node.js 20+ and no third-party dependencies.

## Next

1. Add spectral distribution → XYZ integration using versioned observer/color-matching data.
2. Add chromatic adaptation and explicit display profiles.
3. Add gamut mapping/tone mapping policies.
4. Add mapping provenance records tying every final channel to source nodes and transformation IDs.
5. Add Canvas/WebGL reference renderer.
6. Add Unity and Unreal adapters only after the pure math layer remains invariant under tests.
