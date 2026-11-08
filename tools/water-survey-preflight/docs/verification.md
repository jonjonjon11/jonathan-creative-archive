# Verification record

## Controlled input follow-up — 2026-11-08

The [bounded input investigation](../../../docs/test-reports/water-input-diagnostics-2026-11-08.md) records 40 synthetic observations: 27 complete and 13 Chromium automated-fill timeouts. The repeated timeout persists at both widths after removing only the original input callback in the test page. It does not demonstrate a native clipboard-paste defect. Delivered app/source/fixture bytes are unchanged; native paste remains untested and large files should use file import. The existing 85 app/core tests plus five new diagnostic-harness tests pass. The historical browser review below remains intact.

## Current browser update — 2026-11-08

85 Node tests pass (73 core, 6 static, 6 simulated controller), with exact standalone build parity. Scoped offline Chromium and Firefox runs pass 19 browser check groups each using invented records only. Browser verification fixed native Firefox restoration of the export-value opt-in and maximum-count overflow at narrow widths. See the [dated browser report](../../../docs/test-reports/water-browser-2026-11-08.md) and its unchanged JSON summaries for exact revisions, hashes, versions, screenshots and failures.

The roughly one-million-character paste path remains unresolved after a Chromium timeout; large CSVs should use the verified file-picker route. Physical devices, Safari/Edge, assistive technology, real data and practitioner benefit remain unvalidated. This is not water-safety assessment or official upload certification.

## Historical initial review — 2026-11-07

Candidate **0.1.0**, reviewed **2026-11-07 UTC**. No real field data was used. This record distinguishes code tests from browser or field verification.

### Passed on the initial candidate

- Node.js v24.22.1: **84 tests passed**, zero failed/skipped: 73 core tests, 5 static tests, and 6 UI-controller tests using a small DOM model. Command: `node --test tests/*.test.cjs`.
- Reproducible standalone build: `node build.cjs --check` confirmed `index.html` exactly matches its source/fixture inputs.
- JavaScript syntax checks for core, controller, build, and browser-test code.
- Core coverage includes malformed CSV, embedded newlines/commas/quotes, BOM/CRLF/CR, source line numbers, mapping conflicts, required fields, exact decimal bounds, zero coordinates, dates and leap years, optional-year questions, duplicate distinctions, resource/output caps, and 200 deterministic randomized CSV round-trips. Decimal edge cases include signed/leading-zero limits, tiny excesses beyond floating-point precision, underflow-resistant zero checks, and 300 comparisons with an independent BigInt oracle. A regression confirms the HTML-like browser fixture parses as CSV and reaches the intended field-review path.
- Controller-model coverage includes example load, filters, privacy-default and explicit-value exports, repeated loads, clear/invalidation, mapping changes, real UTF-8 decoding, invalid encoding, file-size limits, and delayed file reads losing to newer input or Clear.
- Static checks confirm bundled CSP hashes, no external runtime assets or network/storage API references, no HTML-insertion sinks, unique IDs, label targets, and no-referrer source links. Main text-palette contrast pairs meet 4.5:1 on their intended light backgrounds. These are not a full accessibility or security audit.

### Browser verification did not run in the initial environment

Chromium could not start before page load because local socket creation was restricted. Another available browser route did not support opening the local file. No browser tests, screenshots, mobile layout checks, or live network observations completed.

`tests/browser.cjs` is supplied for a permitted environment with Playwright and Chromium. It is syntactically checked but **its assertions are unrun**. It exercises offline file loading, local downloads, filters, mappings, inert malicious text, paging, invalid files, repeated/clear flows, keyboard/labels, storage/network observation, and narrow viewports. A reviewer should run it and inspect screenshots before describing this as browser-tested.

### Not assessed in the initial review

- Real-browser rendering and content-security-policy enforcement; Safari, Firefox, mobile operating systems, and assistive-technology use.
- Real survey exports, practitioner comprehension, workflow fit, demand for offline review, error-reduction benefits, or field impact.
- Geographic boundaries, WGS 84 correctness, field truth, water quality, upload acceptance, or the entire WPdx standard.
- Production security audit, formal WCAG conformance, legal clearance for anyone's future datasets, or all browser-extension/device behaviors.

This verification was performed before the experimental archive release. The included manifest records file hashes for comparison, not proof of safety, impact, or external certification.

### Initial independent-review corrections

Two initial-candidate defects were reproduced and corrected before release review: (1) a browser-test header contained unescaped quotes, preventing the intended DOM test from reaching the page; it now uses a shared CSV-escaped fixture with a successful-parse assertion and a runnable core regression; (2) numeric conversion rounded decimal coordinates such as `90.000000000000000001` to the boundary. Bounds now compare the original decimal strings exactly. These corrections do not turn the still-blocked browser suite into a passed test.
