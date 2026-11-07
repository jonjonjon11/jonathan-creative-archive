# Motion → Trace → Shape 0.1.0

**A newly built, offline learning mini-lab for Jonathan’s Creative Archive.** Combine a left-right rhythm with an up-down rhythm, inspect their time traces, and discover a line, circle or figure-eight. No prior mathematics is needed to try the three short experiments.

This is a new implementation inspired by the archive’s [one-model demonstrator brief](../../concepts/first-demonstrator.md) and [model/history/representation design](../../chapters/03-math-physics-and-xr.md). It is not recovered historical software. It implements a deliberately small two-coordinate analytical model, rather than all requirements or physical quantities proposed in the brief.

**Verification:** 32 Node tests and targeted static checks passed. Real Chromium could not start in the build environment, before loading any page, because its process-singleton socket was not permitted. Rendered-browser, actual touch-device, download and assistive-technology behavior remain unverified. The included browser suite is a future acceptance test, not a passed test.

## Try it

1. Download [Motion-Trace-Shape.html](Motion-Trace-Shape.html), using GitHub’s file download control. A GitHub source preview does not run an HTML app.
2. Open the downloaded file in a modern browser. It needs no server, packages, account or connection. On mobile, open it in a full browser if the file viewer will not run HTML.
3. Choose **Line**, **Circle** or **Figure-eight**. Press **Play one cycle**, use **Step +⅛ s**, or move the time slider.
4. Compare the two separate motions, their position-versus-time traces and the combined shape.
5. Change a repeat count or the up-down head start. That begins a new drawing at time zero. Make a prediction first.
6. Choose **Save experiment JSON** to request a local download of the full model sample set and display settings. Check the browser’s downloads to confirm it saved.

You can instead open `index.html` while keeping the `src` directory beside it. Reference links are optional and require a connection when opened. No background network requests, storage, analytics, account, audio, external libraries, fonts or image assets are used. The lab does not remember your experiment after closing the page; save the JSON first if you want its record. There is no JSON import interface in this version.

## A five-minute learning path

- **Motion:** a circle marks the left-right coordinate; a diamond marks the up-down coordinate. Both travel on single lines. The combined point takes one coordinate from each.
- **Trace:** the two stacked graphs put model time on the horizontal axis. The vertical coordinate is position, from −1 to +1 model unit.
- **Shape:** the square graph puts left-right position on its horizontal axis and up-down position on its vertical axis. Solid gold marks sampled history. The optional dashed line is the full-window preview, not visited history.

Try the line first, then give one rhythm a quarter-cycle head start to make a circle. Finally double the up-down repeat count while both rhythms start together. A 1:2 ratio alone is not sufficient to guarantee a figure-eight; phase matters too.

The built-in question cards include explanations, but there is no grading, student tracking or evidence of educational effectiveness.

## Exact model and honest limits

The two coordinates are analytical sinusoidal functions:

- `x(t) = sin(2π × xCycles × t / 8)`
- `y(t) = sin(2π × yCycles × t / 8 + phase × π / 180)`

`t` is model time in seconds, restricted to 0–8. Each amplitude is one **model unit**, not a claim about metres or any measured object. Repeat counts are integers 1–4 per 8-second window. Phase is the up-down rhythm’s own angular offset, 0–360 degrees in steps of 15 degrees. The square plot has equal spatial scale on both axes, with positive y up.

The family is known as **Lissajous curves**. The sine functions have the mathematical form of simple harmonic motion. This lab specifies positions directly: it does not simulate forces, masses, friction, energy exchange, quantum behavior or a real mechanism. It solves no numerical differential equation. Colors and plotting choices are representations, not discoveries or physical attributes.

The trace contains exactly 481 analytic samples at 1/60-second intervals, including both endpoints. SVG straight-line segments approximate the continuous curve between samples. The live cursor is calculated at the current time and may be ahead of the last fixed sample. On slow devices, frames may skip, but the sample set does not change. The integer repeat counts make both motions repeat by 8 seconds, sometimes earlier.

Playback speed is presentation-only: half, normal or double. It changes model-time advancement per elapsed display second; it does not change equations, sample spacing or exported model data. Animation stops at the end of the window and pauses when the document is hidden. There is no unbounded trail buffer.

### References consulted

- [OpenStax, University Physics Volume 1, §15.1: Simple Harmonic Motion](https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion), for sinusoidal position, amplitude, period and phase.
- [Wolfram MathWorld: Lissajous Curve](https://mathworld.wolfram.com/LissajousCurve.html), for paired sinusoidal coordinates and the line/circle/ellipse family.

Consulted 2026-11-07. Explanations and implementation here are original; no reference text, diagrams or third-party assets are bundled. These references support the mathematical model, not the lab’s instructional effectiveness.

## Access and comfort

The lab always starts paused. A reduced-motion system preference enables **Still mode**, disabling continuous play while leaving step and time-scrubbing controls available. A new request for reduced motion also pauses an active run. Turning that system preference off does not automatically resume animation or turn off Still mode.

Controls use native buttons, ranges and a select, visible keyboard focus, explicit labels, position numbers and a readable summary. Colors are supplemented by labels and circle/diamond markers. Tab moves focus, Enter/Space activates buttons, and arrow keys adjust sliders. The time slider’s Home/End keys go to the beginning/end. Controls are designed with at least 44-pixel interactive height, and the layout has a narrow-screen breakpoint.

Selected text-color pairs pass a source-level 4.5:1 contrast calculation. This is **not** a full accessibility audit. Native slider behavior, focus order in responsive layout, zoom, screen readers, touch precision and motion comfort require real-device evaluation. No flashing, autoplay or sound is added.

## Inspect, build and test

Runtime has no dependencies. Development checks use Node’s built-in test runner and Python’s standard library:

```sh
cd tools/motion-trace-shape
python3 build_single.py
node --check src/core.js
node --check src/app.js
node --test tests/*.test.cjs
python3 tests/static_check.py
```

The build embeds the source CSS and scripts into the standalone HTML deterministically. Static checks verify exact build parity, valid ID/label/ARIA targets, no standalone runtime asset references, chosen CSP restrictions, absence of selected network/storage APIs, relevant accessibility hooks and seven text-color pairs. They do not execute a browser.

The 18 model/data tests cover known line, circle and figure-eight values, closure and bounds across all 400 allowed parameter combinations, sampling, reproducibility, replay order, display/model independence and invalid inputs. The 14 UI-state tests run the real application code against minimal DOM and animation-frame stand-ins. They cover pause/replay/reset/scrub, repeated actions, parameter changes, hidden-page pausing, reduced-motion changes and JSON generation. They do **not** test rendering, native controls or real downloads.

A separate real-browser smoke suite requires a separately available Playwright installation and Chromium. Nothing in this project installs them:

```sh
python3 tests/browser_smoke.py --chromium /path/to/chromium --screenshots /tmp/motion-lab-screenshots
```

It is intended to test both source and standalone forms offline, reduced-motion startup, keyboard ranges, presets, guide, play/pause/restart, a real JSON download and overflow at 320/390 CSS-pixel widths. Review resulting screenshots yourself. It has not passed in this build environment. See [validation record](validation.json) for exact scope and remaining checks.

## Files and reuse

- `Motion-Trace-Shape.html`: portable generated app.
- `index.html` and `src/`: original HTML, CSS, numerical core and control logic.
- `build_single.py`: deterministic standard-library builder.
- `tests/`: numerical, simulated-control, static and optional browser checks.
- `validation.json`: scoped verification record; not a certificate.
- [CC BY 4.0 license](LICENSE.CC-BY-4.0.txt): complete terms, matching the archive’s license for new material.

All newly authored code and explanations in this directory are provided under **CC BY 4.0**, consistent with the archive’s chosen license. You can copy, adapt and share them, including commercially, with attribution, a license link and an indication of changes. Suggested attribution: “Motion → Trace → Shape, Jonathan’s Creative Archive, 2026,” linked to [the public archive](https://github.com/jonjonjon11/jonathan-creative-archive). Do not imply endorsement. This license statement is not a legal audit, warranty or certification.

A useful next contribution is one documented physical-device or assistive-technology test, a clearer learner explanation, or a small, independently checked improvement. Keep scientific and accessibility claims tied to evidence.
