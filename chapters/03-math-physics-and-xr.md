# 3. Math, physics, temporal geometry and XR

## The strongest reusable idea: separate reality, model, and view

A simulation is a model operating under assumptions. A rendered scene is a representation of that model. The user may change scale, perspective, color, history display, or audio mapping without changing the underlying equations. The Temporal Geometry specification makes this distinction explicit through:

**Model → State → History → Representation → Lens → Display**. [SRC-004]

This separation should be visible to learners. “Compressed distance,” “slowed playback,” “probability density,” and “illustrative sound mapping” should be labels in the experience, not only footnotes in source code.

## Time and recorded history

A useful learning tool needs to distinguish physical/model time, integration and sampling choices, replay, presentation, and device behavior. The source specification names six clocks: `t_physical`, `t_solver`, `t_sample`, `t_exposure`, `t_display`, and `t_navigation`. Future implementations should not collapse them into a single vague time variable. [SRC-004]

A history trail is a record or visualization of sampled model states. It should not be described as a measured trajectory when no such measurement occurred. In quantum contexts especially, a display of amplitudes, probability densities, samples, or an educational analogy must not be mislabeled as a literal path taken by a particle.

Implementation proposal:

- Store simulated timestamps and sampling metadata with the history.
- Keep replay speed separate from the integration method.
- Make interpolation visible in the technical description.
- Provide bounded history buffers and deterministic export where feasible.
- Test coordinate conversions independently from rendering.

## Existing scientific-model work and its limits

Reality Atlas default-branch records describe six scientific-model renderers. A historical status document reports 25 numerical, catalog, and source tests and a WebGL2 browser check. Those are reports from the source, not tests rerun during this archive's creation. The same source explicitly does not establish GPU-executed WebGPU, headset sessions, sonification, multiplayer, or engine adapters. [SRC-007]

More ambitious names and branches exist. Their existence is evidence of additional work to review, not evidence that each named feature is finished. [SRC-009]

The Math/Matter receipt is evidence of a concrete code contribution and handoff state. A commit and draft pull request are not acceptance tests. The contribution still needs its own runtime, engine, scene, and platform review. [SRC-005]

## Scientific catalog quality

A recovered Master Scientific Unification Catalog is a historical draft input, not a reliable scientific dataset ready for redistribution. The review found reason to question broad completeness language, particle taxonomy/counting, and some mass interpretations. This archive does not copy its claims into a factual knowledge base. [SRC-006]

A salvage process should work claim by claim:

1. Identify exactly what a record asserts and whether it is mathematical, empirical, conventional terminology, or conjecture.
2. Find an appropriate authoritative or peer-reviewed source.
3. Record units, uncertainty, source date, edition, and scope.
4. Reconcile conflicting conventions explicitly.
5. Keep speculative connections in a separate namespace.
6. Remove the claim from teaching content if verification remains inadequate.

## What counts as speculation

Any proposed universal ontology, unification framework, novel field interpretation, or biological/physical synthesis requires its own evidence. Naming a concept after familiar science does not validate the connection. Attractive geometry and meaningful personal intuition can motivate a hypothesis but cannot serve as measurements or proof.

This archive preserves interest in these ideas without asserting discoveries, clinical effects, or a new theory of physics. A future hypothesis record should include a precise claim, relation to established work, testable predictions, possible falsification, evidence quality, and unresolved objections.

## XR-specific obligations

Moving a lesson to VR or AR adds device, comfort, privacy, accessibility, and physical-space requirements. A headset build should declare tested devices and versions, session conditions, locomotion options, scale cues, performance, and known limitations. Prefer stationary and seated alternatives, an immediate exit, non-flashing modes, and controls that do not encourage unsafe motion.

Do not infer headset readiness from a desktop rendering test. Do not infer educational effectiveness from technical performance. Evaluate comprehension and comfort with appropriately consented, privacy-preserving studies before making efficacy claims.
