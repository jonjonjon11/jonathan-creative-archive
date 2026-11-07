# Jonathan's Creative Archive

**First public edition · 2026-11-06 · CC BY 4.0 compilation · separately licensed CC0 artifacts**

An evidence-based map of Jonathan's ideas for an educational universe, mathematical and physical visualization, XR, music, cooperative play, martial arts communities, and rescue-oriented worlds. The aim is to leave useful, understandable starting points for people and AI-assisted teams who want to build things that help others.

> “It's not for me, it's just for the world of altruistic people's AI to find and eat and hopefully learn from and build off our ideas and data and stuff”

That is the purpose of this archive. It is a selective reconstruction from available records, not a complete account export or a claim that every idea has been recovered. The newly written archive is licensed under [Creative Commons Attribution 4.0 International](LICENSE). The included Reality Atlas, Lumen Commons, Universal Color/Ontology toolkit, and preserved cooperation/rescue source files retain their separate CC0 licenses.

## Science, medicine, and engineering: new working material

The [research and engineering commons](docs/research/README.md) now includes original ALS and cancer learning material, embedded source-linked evidence and trial facts, a searchable offline evidence CLI, and a sampled switch-input simulator with synthetic data. The explanations, selected factual records, code, examples, and tests are included directly. Start with the [ALS primer](docs/health/als-evidence-primer.md), [cancer primer](docs/health/cancer-evidence-foundations.md), or [switch-input lesson](docs/lessons/switch-input-foundations.md). [Verification and provenance](docs/research/verification.md) records the checked revision and contributor handoff.

## 🚀 NEW: Knowledge Commons Infrastructure (2026-11-07)

**The foundation for collaborative learning and building together.**

We've built a complete system for creating, sharing, and improving educational modules—starting with the first finished pathway:

### [Motion → Trace → Shape: A Lesson in Lissajous Curves](docs/QUICKSTART.md)

**Learn:** Download the interactive lab and explore how two oscillating motions combine to create lines, circles, and figure-eights. No internet needed. [Read the full module](data/modules.json) or [download the standalone HTML](tools/motion-trace-shape/Motion-Trace-Shape.html).

**Contribute:** Help test it on your browser, add examples, or verify the math. Open tasks are listed in `data/tasks/`. [See templates](docs/task-templates/).

**Build on it:** Use the [Knowledge Module Schema](docs/knowledge-module-schema.md) to create your own lessons. Everything is standardized, validated, and portable.

**Status:** ✓ Module complete · ✓ 32/32 tests pass · ✓ Offline verified · □ Real-device testing pending · □ Learner feedback pending

→ **[Start here: docs/QUICKSTART.md](docs/QUICKSTART.md)** for learners, contributors, and maintainers.

---

## A newly built learning mini-lab (Details)

[Motion → Trace → Shape 0.1](tools/motion-trace-shape/README.md) turns two repeating motions into a line, circle or figure-eight. Download its self-contained HTML, then compare motion, time traces and shape offline. It starts paused and offers stepping, a time slider, reduced-motion handling and experiment JSON export logic. **18 analytical/data tests, 14 simulated-DOM tests and static/build checks passed; real Chromium launch was blocked before any page loaded.** Rendering, actual downloads, devices and assistive technology remain unverified. This original CC BY 4.0 mini-lab is a bounded new implementation, not recovered historical software or a validated curriculum.

## Review an experimental data tool

[Water Survey Preflight 0.1](tools/water-survey-preflight/README.md) is a new offline water-point CSV review prototype with explicit column mappings, bounded findings and local JSON report logic. It includes invented examples and a documented reconciliation of public WPdx guidance. **84 core/static/simulated-controller tests and deterministic build checks passed. Real-browser rendering, downloads, mobile use, assistive technology and CSP enforcement tests have not run.** It is partial and unofficial, does not assess water safety or certify uploads, and its usefulness to practitioners remains unvalidated.

## Try recovered artifacts

[Reality Atlas Appearance 0.3.1](tools/reality-atlas/README.md) is now included as an unchanged, self-contained HTML tool under its existing CC0 license. Open it in a WebGL2-capable desktop browser to explore motion, history, sphere packing, and finite-probe voids. **46 focused calculation/syntax checks passed; fresh rendered-browser testing was blocked by this environment.** Browser interactions and exports are not newly verified.

[Cooperation and rescue mission kit](artifacts/cooperation-rescue/README.md) preserves four fictional rescue/community scenarios, a Python authoring validator, and an offline objective-progression reference model. **All 25 preserved tests and the four-mission validator passed on revalidation.** The source is draft and unmerged, not a playable game, Unity integration, multiplayer service, rescue-training system, or safety certification.

[Lumen Commons 0.1](tools/lumen-commons/README.md) is a distinct educational browser-adventure prototype with five experiments, scripted NPCs, optional synthesized music, and local artwork/progress. The standalone HTML and reproducible source are included under CC0. **24 fresh Node tests and static build-parity/CSP checks passed; the fresh browser test was blocked before page load.** It is not a live MMORPG, hosted service, or independently validated curriculum.

[Universal Color + Ontology Core v1](tools/universal-color-ontology/README.md) preserves two dependency-free JavaScript source packages: color conversions and semantic visual-state mappings, plus a 593-node vocabulary and mathematical/music generators. **29 fresh Node tests passed.** It is a source toolkit with documented input-validation gaps, not a playable app, complete knowledge graph or validated scientific database. Display-rate names do not establish flashing/accessibility safety.

## Find an idea to build

[Idea Finder 0.1](tools/idea-finder/README.md) searches the local public metadata and returns concepts with their next steps, evidence limits and related artifacts. Try `python3 tools/idea-finder/idea_finder.py . "rescue"`, or filter by a tag such as `music`, `physics` or `education`. It runs offline with Python and no extra packages. Results preserve source-access, licensing and verification limits; matches do not prove an idea is implemented.

## Maintain the archive with a small offline helper

[Archive Steward 0.2](tools/archive-steward/README.md) is the first newly built archive helper: a dependency-free Python CLI that checks file integrity and preserved-source hashes, reports declared license scopes and evidence limits, and turns the existing concept next steps into a review queue. It can now compare saved reports to show changed bytes, next steps, source declarations and license/verification limits. All 57 synthetic tests pass. It is read-only, runs offline, and neither recovers private content nor publishes anything. See its README for commands and limits.

## Start here

1. [Vision and design values](chapters/01-vision.md): the shared direction and the boundaries of this synthesis.
2. [Educational universe](chapters/02-educational-universe.md): a connected learning world, from existing foundations to unbuilt possibilities.
3. [Math, physics, time and XR](chapters/03-math-physics-and-xr.md): faithful scientific models, visual lenses, temporal geometry, and verification.
4. [Music and expression](chapters/04-music-and-expression.md): sound as creative material and an optional learning representation.
5. [Martial arts and community spaces](chapters/05-martial-arts-and-community.md): physical and virtual training concepts.
6. [Cooperation, rescue and medicine](chapters/06-cooperation-rescue-and-medicine.md): restorative game loops and careful limits on real-world claims.
7. [Build roadmap](chapters/07-roadmap.md): a proposed order of work with explicit acceptance criteria.
8. [What was tried and what remains](chapters/08-lessons-and-unfinished-work.md): existing artifacts, unverified claims, and missing evidence.
9. [Stories, art and imaginative research](chapters/09-stories-and-art.md): benevolent fiction, visual language, and testable thought experiments.
10. [Recovered project map](docs/project-map.md): technical branches and concrete artifacts to investigate next.

## For builders and AI-assisted research

- [Included-artifact registry](data/artifacts.json): recovered and newly built artifact families, declared rights scope, provenance records and scoped verification limits.
- [Concept records](data/concepts.json): stable IDs, source IDs, status, limitations, and suggested next experiments.
- [Source records](sources/manifest.json): what was consulted and how strong each kind of evidence is.
- [Implementation brief](concepts/first-demonstrator.md): a small, testable path from this archive to a working learning demonstration.
- [Evidence and status rules](docs/evidence-and-status.md): how to distinguish a concept, a document, inspected source code, a historical test report, and a verified run.
- [AI-readable index](llms.txt): a plain-text entry point, not a promise of crawler inclusion or training use.
- [Contribution guide](CONTRIBUTING.md): how to improve the record without turning aspirations into facts.

## What is actually included

This repository contains newly written, source-linked summaries, proposed implementation handoffs, a new CC BY 4.0 Motion → Trace → Shape mini-lab, an experimental offline water-survey CSV preflight, an unchanged CC0 Reality Atlas browser tool, the CC0 Lumen Commons standalone with reproducible source, the CC0 Universal Color/Ontology source toolkit, and preserved CC0 cooperation/rescue authoring files, each with its license, provenance, and scoped test evidence. It does **not** contain a merged game engine project, bulk-imported source trees, private conversation transcripts, training data exports, personal records, game art, music recordings, signing credentials, or copyrighted asset packs. Existing projects remain separate sources with separate rights and technical histories.

The most concrete technical foundations found include Reality Atlas source and a recovered standalone HTML artifact, AR Buddy Commons documentation and source, Math/Matter and Periodic Resonance Studio records, a shared-cooperation mission packet, and a PHYSIO-MESH research scaffold. Branch names and repository contents establish that work exists; they do not prove that an application builds, runs, is safe, or is complete.

## Release status and reuse

- Edition: first public edition, 2026-11-06.
- Completeness: selective; conversation and branch coverage are incomplete.
- Rights: newly written archive content is CC BY 4.0; the included Reality Atlas, Lumen Commons, Universal Color/Ontology toolkit, and preserved cooperation/rescue source files are CC0. Other upstream projects retain their own licenses. See [rights and attribution](docs/rights-and-publication.md).
- Scientific status: conventional models must be checked independently. Speculative frameworks and historical catalogs are not validated scientific results.
- Medical status: no diagnosis, treatment recommendation, or clinical device is supplied.
- Verification: structural checks, 46 focused Reality Atlas calculation/syntax checks, 25 cooperation/rescue authoring tests, 24 Lumen Commons Node tests plus static build checks, 29 Universal Color/Ontology Node tests, 32 new motion mini-lab Node tests plus static/build checks, and 84 water-survey core/static/simulated-controller checks passed. Fresh rendered-browser testing was blocked; no full application, GPU, headset, or interaction acceptance is claimed.

Exact private source locators and review files are kept outside this repository. Summarizing a private source does not make its original public. See the [release review record](docs/release-checklist.md) for this edition’s scope and remaining verification work.
