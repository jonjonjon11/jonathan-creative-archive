# Open Tasks (High Impact)

## 1) Source trace hardening [data]
- Add page-level references under a `sources/` folder.
- Connect financing rows to exact source references.
- Acceptance: every displayed fixture row has source metadata nearby.

## 2) Courtyard asset upgrade [ui]
- Replace schematic SVG with supplied real floor plan assets where available.
- Keep Option A/B and Floor 1/2 switching.
- Acceptance: switching option/floor updates plan image, caption, and areas correctly.

## 3) Hydrogen replay determinism [sim]
- Add explicit baseline lock indicator and deterministic step index.
- Preserve save/restore behavior across resets.
- Acceptance: reset + restore reproduces the saved comparison state exactly.

## 4) Mobile accessibility pass [ui]
- Improve tap targets, contrast, and reduced-motion handling.
- Acceptance: key journey is fully usable at ~390px width.

## 5) Validation scripts [docs/data]
- Add a lightweight checker for broken local links and JSON parse sanity.
- Acceptance: one command reports pass/fail for core routes and datasets.
