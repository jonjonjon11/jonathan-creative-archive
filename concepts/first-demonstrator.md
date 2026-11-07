# Implementation brief: one inspectable learning model

## New partial starting point

[Motion → Trace → Shape](../tools/motion-trace-shape/README.md) is now included as a new original mini-lab inspired by this brief. It implements two bounded analytical sine coordinates, fixed samples, separate motion/time/shape views, paused/reduced-motion control logic and JSON export generation. It does not implement every quantity, model or acceptance gate below. Its 32 model/simulated-control checks and static build checks passed, but real-browser launch was blocked before page load. Use its README for the current limits; this brief remains a roadmap rather than a claim that the full project is complete.

**ID:** DEMO-001  
**Status:** editorial proposal  
**Related concepts:** CON-001, CON-002, CON-003, CON-004  
**Historical sources informing the proposal:** SRC-004, SRC-007, SRC-008

## Objective

Build one small learning experience that proves the useful separation between a mathematical model, its recorded history, and several representations. Do not begin with a full metaverse, account system, multiplayer service, or headset requirement.

## Candidate model

A one-dimensional harmonic oscillator is a reasonable first choice because the relation between displacement, velocity, energy, phase, and periodic motion can be inspected. The chosen implementation must cite a reliable source and explicitly state whether it uses an analytical solution or a numerical integrator.

This brief does not supply a validated implementation. Parameters and units must be specified by the builder. Any damping, driving, numerical approximation, or nonlinearity must be separately documented.

## Required experience

- Display the equation, parameter meanings, units, and model assumptions in plain language.
- Show a moving representation and a labeled time series.
- Allow pause, restart, and changing a small number of bounded parameters.
- Keep presentation speed distinct from physical/model parameters.
- Export a small reproducible experiment record.
- Provide keyboard controls and a non-motion textual summary.
- Offer optional sound only after the visual and numerical core is correct.

## Suggested record shape

A run should identify a model version, parameter values and units, initial conditions, numerical method when applicable, simulated timestamps, sampling settings, display mappings, and relevant source IDs. Do not store personal information merely to save a run.

## Acceptance evidence

1. Compare output against a known solution or reference for a documented parameter set.
2. Test conservation or expected dissipation under the selected assumptions.
3. Test that changing the view does not change the model state.
4. Test that pause and replay preserve the recorded experiment.
5. Test invalid inputs and bounded resource use.
6. Verify labels, keyboard access, reduced-motion behavior, and non-audio alternatives.
7. Record the tested browser/device, build reference, commands, results, and limitations.

## Out of scope

Clinical claims, self-defense instruction, real emergency training, novel physics claims, copied assets, student tracking, automated assessment of people, and large-scale social networking.

## Useful contribution sizes

One reliable test, one clear explanation, one accessible representation, or one independently sourced correction is a complete contribution. A contributor should not need to endorse the entire wider vision to help with a small part.
