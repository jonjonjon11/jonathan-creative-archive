# Water-point preflight

An original, free, dependency-free **offline prototype** for reviewing water-point survey CSVs. Open `index.html` directly in a current browser. Nothing to install, no account, no upload, and no network connection needed for the review.

**Not water testing, WPdx certification, upload approval, or a verified improvement to field practice.** It is an independent public-benefit experiment, not affiliated with or endorsed by WPdx. Its usefulness and offline demand are unvalidated. WPdx already provides ingestion validation; this tool is not a replacement.

**85 Node checks and scoped offline Chromium/Firefox browser checks pass with invented data.** Real local downloads, file import, reload consent, narrow layouts and selected CSP enforcement are exercised. Large-paste responsiveness, physical devices, assistive technology and practitioner usefulness remain unverified. See the [dated browser report](../../docs/test-reports/water-browser-2026-11-08.md) and [verification record](docs/verification.md).

## Try it

1. Open `index.html` and select **Try a synthetic example**. All supplied records are invented.
2. Open a local UTF-8 comma-separated CSV, or paste CSV text.
3. Confirm the column mappings. Exact field names with optional `#` are suggested; custom headers require your choice.
4. Review errors and warnings with their record number and physical starting line. Resolve questions with the data collector, then review a corrected copy.
5. Optionally save a JSON report locally. Input headers and issue values are excluded by default. Review any report before sharing.

The original file is never modified. No data is automatically corrected, deleted, submitted, or categorized into a water-safety result. Browser refresh/close or **Clear this tab** removes the app's working view, not downloads, clipboard data, device traces, or browser-managed file history. Browsers/extensions can have their own retention and access behavior.

## Bounded checks

- CSV syntax and row widths; explicit column mapping and required values.
- Decimal coordinate syntax, numerical bounds, low precision, and a `(0,0)` review flag. **No country-boundary, datum, or real-location verification.**
- A documented ISO calendar-date/time profile, with leap-year checks and future-date warnings. Unsupported ISO forms are not automatically declared invalid by WPdx.
- Water-presence responses for human mapping review; unfamiliar source/technology descriptions remain open text.
- Optional installation/rehabilitation years; exact duplicate rows and repeat IDs within the same organization and date.

See [rule decisions and reconciliation](docs/rules.md), [source provenance](docs/sources.md), [verification record](docs/verification.md), and [small evaluation plan](docs/evaluation.md). All other optional fields are unvalidated, including water-quality measurements, country codes, management, URLs, and payment information. Missing non-required columns are not errors.

### Limits

The file picker permits up to **5,000,000 bytes**. The text parser permits **5,000,000 JavaScript string units**, **25,000 data records**, **256 columns**, and **65,536 string units per cell**. Physical empty lines are skipped but source record/line numbering is preserved. The first **2,000 findings** are retained; all additional findings are counted and the omission is prominently reported. Each retained value is shortened to at most 160 string units. Findings are paginated 100 at a time.

Prefer the file picker for large CSVs. A roughly one-million-character automated textarea fill timed out in Chromium; large-paste responsiveness remains unresolved. The 25,000-record synthetic file-picker path passes both tested browsers, which does not establish maximum-size paste performance.

An incomplete parse or mapping prevents full review. A width error skips that row's field checks and marks the review incomplete. “Checks finished” means this bounded checker ran, not that a dataset passed any official process.

## Privacy and security

The standalone page has no runtime dependencies, external assets, analytics, network APIs, remote fonts, cookies, local storage, or service worker. Its content security policy restricts scripts/styles to the bundled hashes and disallows connections. Optional source links navigate online only when chosen. Input appears through `textContent`, never interpreted as HTML. Reports are JSON rather than spreadsheet formulas. No real survey data is bundled.

This is not a full security audit. Use a trusted downloaded copy and a secure browser/device. It does not anonymize a dataset or decide whether sharing water-point locations or personal details is appropriate.

## Rebuild and test

Node.js 20+ is sufficient for the build and core tests; no package installation is required:

```sh
node build.cjs
node build.cjs --check
node --test tests/*.test.cjs
```

Optional browser tests use an existing Playwright installation and Chromium or Firefox, only for testing. CI pins Playwright 1.56.0. The runner does not install dependencies:

```sh
NODE_PATH=/path/to/existing/node_modules WATER_BROWSER=chromium WATER_QA_DIR=/tmp/water-chromium node tests/browser.cjs
NODE_PATH=/path/to/existing/node_modules WATER_BROWSER=firefox WATER_QA_DIR=/tmp/water-firefox node tests/browser.cjs
```

They do not add dependencies to the delivered app. The browser tests copy only `index.html` into an isolated folder and use its `file://` URL with browser networking offline. `WATER_BROWSER_EXECUTABLE` may select an existing browser binary; otherwise the matching Playwright-managed browser is used. Screenshots and a JSON summary are written to `WATER_QA_DIR`, including on browser assertion or launch failure after report initialization. Tests use invented records only. Narrow desktop viewports are not physical-phone tests. See the verification record for what actually ran and what did not.

## License and attribution

Original code, documentation, and invented fixtures use **CC BY 4.0**, following the destination archive's owner-selected license. Full text: [LICENSE](LICENSE). Suggested attribution: “Water-point preflight, Jonathan's Creative Archive (jonjonjon11), 2026”, with a link to the archive and license, and an indication of changes. No endorsement is implied. The prototype is provided without warranty.

The WPdx source documents are linked, not bundled or relicensed. Their names identify reference guidance only. No WPdx dataset, logos, or third-party code is included.
