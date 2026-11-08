# Water Survey Preflight browser validation

Follow-up: the [controlled input investigation](water-input-diagnostics-2026-11-08.md) narrows the automated-fill timeout without changing delivered runtime files or establishing native clipboard-paste behavior. This report retains its historical verification checkpoint.

Date: 2026-11-08. Assessment: **scoped automated desktop-browser checks pass using invented records only**. This is a partial unofficial data preflight, not water testing, WPdx certification, upload approval or demonstrated practitioner benefit.

## Exact build and evidence

Base main: `924e20021989b8a34838156a9f4b6830bda07283`. Successful implementation/test head: `75228137240771344ccc60401007ebd91e38d7c8`, tree `7dae64cc0a50c588f65339c5e73ea5258b2b5c2d`.

Both the [exact-head push run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42474100869) and [PR run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42474104300) passed all seven jobs: archive validation and Motion, Lumen and Water Chromium/Firefox jobs. The push run checked the exact published head; the PR run checked GitHub's generated merge revision. Subsequent documentation-only changes must also pass CI before merge.

The [Chromium JSON report](water-chromium-2026-11-08.json) and [Firefox JSON report](water-firefox-2026-11-08.json) are unchanged summaries from the exact-head push artifacts, with 19 passing check groups per browser. Environment: GitHub-hosted Ubuntu 24.04 x86-64, Node v22.23.4, Playwright 1.56.0, Chromium 141.0.7390.37 and Firefox 142.0.1. These are pinned automation builds, not the newest consumer-browser claim.

The standalone is 40,581 bytes, SHA-256 `709f1db0bb210c5bf02762302da635ecdae5304841d40cb36e1c4abf54189cb7`. Browser runner SHA-256: `b21e6b288e0f979ceb7e45cd7d1c6cd9abace10729a12e3cd01e7f57519b7e3f`. Only the report-value checkbox's browser-restoration setting and narrow summary layout changed at runtime. Core rules, CSV parsing, UI-controller logic, synthetic fixtures, WPdx reference sources and CC BY 4.0 licensing remain unchanged.

## What was exercised

The runner copies **only** `index.html` to an isolated directory and opens its actual `file://` URL in a fresh browser context with networking offline. It does not bypass or relax the CSP. No real survey, personal or location data was used.

- Synthetic sample counts, severity filters, explicit custom-column mappings and invalidation of stale findings after edits/mapping changes.
- Four real JSON downloads per browser: default export omits input headers and values, explicit opt-in includes the expected synthetic values, and exports at 390 and 320 CSS pixels work. A filtered display does not silently filter the exported findings.
- Native UTF-8 file-picker import; fresh failure handling for malformed CSV, invalid UTF-8 and a file above the five-million-byte limit. A clean invented file produces a human-verification reminder, not official approval.
- CSV-escaped HTML-like headers and values remain inert text. Pagination and the 2,000-retained-finding cap are disclosed while aggregate findings continue to be counted.
- Repeated sample loads, Clear and native page reload. Reload does not restore completed findings or the previous value-export opt-in. File history, clipboard contents, downloads, browser profiles and extensions are outside this claim.
- Keyboard skip-link activation, keyboard sample activation, result focus and form labels. This is not full keyboard-only or assistive-technology acceptance.
- No observed HTTP(S) requests, page exceptions or CSP error messages in the main test flow; no cookies or web-storage entries at the stated checkpoint. Optional online reference links are not opened by the test.
- Desktop 1280×900 and narrow 390×844 / 320×700 layouts, real filter/download/Clear/repeat actions at both narrow sizes. Maximum native-file import uses 25,000 invented records, producing 100,000 errors and 25,000 warnings. All three totals fit their own boxes without page horizontal overflow at 320, 401, 660 and 661 pixels, including both sides of the narrow-layout breakpoint.
- A separate positive-control CSP probe tries an unapproved inline script and a `data:` URL fetch. Both browsers report `script-src-elem` and `connect-src` violations; the script does not run. No remote destination is used. These deliberate probe violations are separate from the clean main-flow report.

Screenshots include desktop/narrow full-page findings and all four maximum-count views. Screenshot evidence is retained in the [Chromium artifact](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42474100869/artifacts/13614099710) and [Firefox artifact](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42474100869/artifacts/13614543308). CI retention is seven days and downloads may require GitHub sign-in. The checked-in JSON summaries remain after those artifacts expire. The downloaded artifact ZIP SHA-256 values matched GitHub's reported digests. Independent AI visual review inspected all 14 screenshots across both engines: controls and findings were readable, all maximum counts fit and remained separately labeled, and the earlier misplaced skip-link capture was absent. This is scoped inspection, not a human usability study.

## Failures found and corrected

1. The [first Firefox run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42473368007/job/128709130859) restored an opted-in checkbox on native reload. `autocomplete="off"` now prevents that restoration in both tested browsers, with a static regression. There was no automatic export or upload; the existing review action also resets the choice.
2. The [next two-browser run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42473660927) exposed six-digit summary totals overflowing a 320-pixel page. The summary now stacks at the existing 660-pixel breakpoint. Independent review caught a proposed narrower cutoff that could have left a gap; maximum-count checks now include 401, 660 and 661 pixels rather than weakening the original 320-pixel regression.
3. The [first Chromium run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42473368007/job/128709130676) timed out while filling a roughly one-million-character textarea, and the subsequent failure screenshot also timed out. This remains an **unresolved large-paste responsiveness gap**, not a proven test-runner-only problem. The maximum-record test now imports the same synthetic CSV through the actual file picker with the paste panel closed. That route passes; it does not validate maximum-size pasting. Prefer file import for large CSVs until the paste path is separately investigated.

Independent AI review also strengthened opt-in reload setup, required actual expected values in the opt-in export, and added per-count layout checks so a clipped number cannot pass a page-width-only assertion. Browser failures were not bypassed; subsequent successful runs include these regressions.

## Reproduce and current CI

The runtime still has no dependencies. Optional test-only dependencies are installed outside the repository by CI:

```sh
npm install --prefix /tmp/water-playwright --no-audit --no-fund playwright@1.56.0
/tmp/water-playwright/node_modules/.bin/playwright install --with-deps chromium firefox
NODE_PATH=/tmp/water-playwright/node_modules WATER_BROWSER=chromium WATER_QA_DIR=/tmp/water-chromium node tools/water-survey-preflight/tests/browser.cjs
NODE_PATH=/tmp/water-playwright/node_modules WATER_BROWSER=firefox WATER_QA_DIR=/tmp/water-firefox node tools/water-survey-preflight/tests/browser.cjs
node --test tools/water-survey-preflight/tests/*.test.cjs
node tools/water-survey-preflight/build.cjs --check
```

The runner uses already installed browsers and attempts a failure screenshot and summary on browser-launch/assertion failures. Missing test dependencies or output-directory preparation failures can occur before report initialization. The local review environment still blocks Chromium startup before page load; GitHub-hosted CI supplies the actual browser evidence.

Water now has **85 passing Node tests**: 73 core, 6 static and 6 simulated-controller tests. Local aggregate checks passed: 251 Python tests, 184 Node tests, 46 Reality Atlas calculation/syntax checks, record validation, exact generated views, source/standalone parity, archive structure/internal links and reviewed checksums. CI now explicitly checks Water standalone parity and runs Water Chromium and Firefox on every push and pull request alongside the existing five jobs. Test counts are not safety or effectiveness scores.

## Remaining limits

- Large-paste responsiveness, Safari/Edge, physical phones/touch, browser-restart/history restoration, assistive technology, comprehensive accessibility and performance under other input shapes remain unverified.
- No real survey exports, practitioner comprehension, workflow demand, adoption, error reduction or field impact have been evaluated. Any next practitioner exercise should use consenting participants and invented examples first.
- This does not validate every WPdx rule, geographic boundaries, WGS 84 truth, actual water presence, water quality/safety, submission acceptance, dataset-sharing rights or external reference freshness indefinitely.
- No production security certification, exhaustive browser/extension behavior review or claim of anonymization. A downloaded report is a separate file the user must review before sharing.
