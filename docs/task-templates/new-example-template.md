# Add a worked motion example

Use the [corrected module](../../data/modules.json) and [paper-first lesson](../lessons/motion-trace-shape.md), not a remembered picture of a frequency ratio. Frequency ratio **and phase** determine the trace. In this lab amplitudes are equal and the parameter names `x_frequency` and `y_frequency` denote repeat counts over the eight-second window, not hertz.

## A complete, mathematically checked specimen

This specimen is an authoring example, not a claim of browser, educator or learner acceptance. It is not yet inserted into the canonical module. Check that its ID is unused before adding it. New contributors can use its format but should choose their own useful question rather than blindly duplicate it.

```json
{
  "id": "EXE-LJ-004",
  "title": "One-to-three at zero phase: a retraced cubic",
  "difficulty": "intermediate",
  "scenario": "Over eight seconds, x repeats once and y repeats three times, with equal amplitudes and zero phase offset.",
  "parameters": {
    "x_frequency": 1,
    "y_frequency": 3,
    "phase_offset_degrees": 0,
    "time_window_seconds": 8
  },
  "prediction": "The point travels along the graph y = 3x - 4x³ for -1 ≤ x ≤ 1, retracing it. This is not a three-petal flower.",
  "step_by_step": [
    "Let u = 2πt/8. Then x = sin(u) and y = sin(3u).",
    "The triple-angle identity gives sin(3u) = 3sin(u) - 4sin³(u), so y = 3x - 4x³.",
    "At t = 0 the point is (0, 0). At t = 1 it is (√2/2, √2/2). At t = 2 it is (1, -1).",
    "At t = 3 it returns to (√2/2, √2/2), and at t = 4 it returns to (0, 0).",
    "The second half visits the negative-x portion: at t = 6 the point is (-1, 1). At t = 8 it returns to the origin."
  ],
  "explanation": "Each x value determines exactly one y value at this phase. Multiple times can have the same coordinates, so repeated motion does not imply distinct petals. Time direction and speed are separate from the geometric set of points.",
  "mathematical_form": "x(t) = sin(2πt/8); y(t) = sin(6πt/8); y = 3x - 4x³, -1 ≤ x ≤ 1.",
  "verification": "Compute the listed coordinates and compare with the cubic. If a browser is available, set x repeats to 1, y repeats to 3 and phase to 0°, then use Step or the time slider. Record actual browser observations separately from mathematical checks.",
  "verification_samples": [
    {
      "t_seconds": 0,
      "x": 0,
      "y": 0
    },
    {
      "t_seconds": 1,
      "x": 0.7071067811865476,
      "y": 0.7071067811865476
    },
    {
      "t_seconds": 2,
      "x": 1,
      "y": -1
    },
    {
      "t_seconds": 3,
      "x": 0.7071067811865476,
      "y": 0.7071067811865476
    },
    {
      "t_seconds": 4,
      "x": 0,
      "y": 0
    },
    {
      "t_seconds": 5,
      "x": -0.7071067811865476,
      "y": -0.7071067811865476
    },
    {
      "t_seconds": 6,
      "x": -1,
      "y": 1
    },
    {
      "t_seconds": 7,
      "x": -0.7071067811865476,
      "y": -0.7071067811865476
    },
    {
      "t_seconds": 8,
      "x": 0,
      "y": 0
    }
  ],
  "derived_relation": {
    "form": "y = a*x + b*x^3",
    "a": 3,
    "b": -4
  }
}
```

## Why the triple-angle identity works

Expand sin(2u + u):

sin(3u) = sin(2u)cos(u) + cos(2u)sin(u)
= 2sin(u)cos²(u) + (1 − 2sin²(u))sin(u)
= 3sin(u) − 4sin³(u).

No physical force, measured phenomenon or new theory is being inferred. This is an algebraic identity for the lab's sinusoidal model. Changing phase generally invalidates the specific cubic relation above.

## Choose another useful question

- At equal repeat counts, compare 45° and 135°: both give ellipses, with different orientation. Derive rather than guess their equations.
- Compare 1:3 at 0° and 90°. Show why the same repeat counts do not guarantee the same trace.
- For 2:3 at a stated phase, calculate a coordinate table before describing the shape. Do not infer a fixed number of points or petals from the ratio alone.
- Stay within the actual lab controls (repeat counts 1–4); do not promise that 5:2 can be selected without a separate lab change.

## Contribution steps

1. Read the [authoring guide](../knowledge-module-schema.md).
2. State repeat counts, phase, amplitude convention and time window explicitly.
3. Work through the equations; provide enough numerical checkpoints to catch a sign, phase or unit error.
4. Keep calculations separate from browser observations and learning-effectiveness claims.
5. Add an unused-ID example to `module.content.worked_examples` in `data/modules.json`.
6. Add regression tests for its actual mathematics, not only its wording.
7. Run the module validator, relevant motion tests and archive checks; update only reviewed file checksums.
8. Submit a focused pull request with scope, sources or derivation, commands, outcomes and remaining review needs.

The test suite parses this specimen's JSON and checks its stored numerical checkpoints and cubic coefficients against the sinusoidal model. Prose edits still require review. That does not establish teaching effectiveness, browser compatibility or accessibility. Original specimen and derivation: CC BY 4.0 under the repository license; linked source materials retain their own licenses.
