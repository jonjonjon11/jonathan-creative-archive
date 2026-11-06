# 2. An educational universe

## Source-backed foundations

The reviewed material contains several related but distinct technical and conceptual families:

- **Reality Atlas:** scientific-model rendering and a broader educational-universe direction. The inspected default-branch material concerns version 0.1; later branches exist and must be assessed separately. [SRC-007, SRC-009]
- **AR Buddy Commons:** a self-described pre-alpha project with safety and privacy documents, a reusable Unity package, orbital-flight laboratory source, semantic lessons, and plans involving movement, music, community spaces, robotics, and emergency simulation. [SRC-008]
- **Math/Matter in Unity:** a publication receipt identifies a branch, commit, draft pull request, and a twelve-file runtime contribution. The receipt did not claim Unity acceptance or runtime verification. [SRC-005]
- **Temporal Geometry:** a design specification that separates model, state, history, representation, lens, and display. It provides a useful conceptual bridge across lessons. [SRC-004]

These are related sources, not verified interchangeable modules. No import compatibility, common API, working migration, or unified build is claimed.

## A proposed learner journey

The following is a new implementation proposal based on the sources.

1. Enter a simple lesson and choose a question, such as what changes when an orbit's starting velocity changes.
2. See the assumptions, units, and limits before or alongside the scene.
3. Manipulate a small number of meaningful variables.
4. Pause, rewind a recorded history, compare two runs, and inspect numerical values.
5. Switch representation: spatial view, plot, annotated text, or optional sound.
6. Explain what the result supports and what it does not support.
7. Save the experiment as a small reproducible record, without requiring a personal profile.

A connected world can later organize lessons by questions, skills, scale, or relationships. That navigational world should not become a prerequisite for accessing a single useful explanation.

## Architecture that keeps the idea buildable

A promising separation is:

- **Model layer:** equations or explicit rules, assumptions, parameters, integration method, and units.
- **State layer:** the values at a particular simulated time.
- **History layer:** sampled states, events, and provenance for a run.
- **Representation layer:** geometric objects, plots, text descriptions, or sonic mappings derived from that history.
- **Lens layer:** selected coordinate, scale, projection, comparison, or educational emphasis.
- **Display layer:** browser, desktop, headset, accessible text, or another device-specific interface.

This follows the documented Temporal Geometry chain. The concrete boundaries and file formats still need implementation and testing. [SRC-004]

The advantage is practical: the browser and headset can show the same model without duplicating the science; a different visual style need not alter physical behavior; an accessibility alternative can preserve the lesson's meaning.

## Content records before an enormous world

Start with a small lesson record containing an ID, question, prerequisites, source references, model validity range, parameters and units, controls, expected observations, common misconceptions, accessibility alternatives, and tests. A curriculum can grow as independently reviewable records.

Do not treat historical phrases such as “universal” or “complete” as proof of coverage. A knowledge catalog needs an explicit scope, version, date, and a way to say “unknown,” “disputed,” or “not included.”

## Build boundary

The first useful release could be one accessible desktop/browser lesson with reproducible model behavior and honest limits. VR, multiplayer, AI companions, persistence, worldbuilding, and institutional deployment should be separate milestones. This proposed sequencing does not erase the larger vision; it makes evidence of progress easier to obtain.
