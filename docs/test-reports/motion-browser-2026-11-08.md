# Motion lab browser validation and SVG correction

Date: 2026-11-08. Overall assessment: **automated desktop-browser checks pass; broader device/accessibility acceptance remains partial**.

## Exact scope

Base main was `7959373d07ab0fdeb9e94b322502998e2b9ba972`. This contribution adds reproducible browser checks, fixes one confirmed SVG rendering defect, and records evidence. It does not merge biomedical proposals, change the numerical model, deploy a site or add runtime packages. Original contributions retain CC BY 4.0.

The corrected app and test runner were tested at commit `01ef1e2283bdc182a61123c80fa06f14a7d1e5e0` in [push CI](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42460445954) and [PR CI](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42460449818). Both run the existing archive validation job plus Chromium and Firefox jobs. The committed JSON reports preserve browser versions and tested file hashes; subsequent documentation-only commits must also pass CI before merge.

Environment: GitHub-hosted Ubuntu 24.04 x86-64; Python 3.11.18; Playwright 1.56.0; headless Chromium 141.0.7390.37 and Firefox 142.0.1. These are pinned automation-browser builds, not assertions about latest consumer releases. Both `index.html` and the portable HTML are opened as local file URLs with networking disabled. The app makes no HTTP(S) requests during the tested flows. The desktop viewport is 1280 × 1000; 390 × 844 and 320 × 844 are narrow CSS viewports, **not mobile devices or touch tests**.

## Defect found and corrected

Screenshot inspection of the initially passing browser run at `6276bf8d8669a0c6377cd254e90752034329986f` showed a solid black triangle covering the time plots in both browsers. The open SVG axes path had no fill declaration. SVG implicitly closes open subpaths when filling; `M58 25V175H570` therefore formed an opaque triangle.

The fix adds `fill="none"` only to that path in `index.html`, then deterministically rebuilds `Motion-Trace-Shape.html`. The JavaScript, CSS, equations, model version and exported data format are unchanged. Two new source/standalone regressions failed before the correction and pass afterward. A browser assertion now checks the actual computed fill. Fresh screenshots from both browsers were inspected after the fix: the opaque triangle is gone and both time traces remain visible. This is AI visual review, not human acceptance or a full graphical audit.

Independent AI review confirmed the original defect and the minimal correction, checked other open SVG paths and reviewed the browser runner. Remaining default-filled open paths are isolated straight segments with no enclosed area; diamond markers deliberately retain their fills.

## Controls and observed behavior

- Startup: no autoplay with either normal or reduced-motion preferences; Still mode and disabled Play under reduced motion.
- Step: advances by 0.125 model seconds; disabled at the endpoint. Restart returns to zero.
- Time range: keyboard Home/End reaches 0/8; changing it pauses playback.
- Parameters: one native ArrowRight increment for each of left-right repeats, up-down repeats and phase; all three presets and their labels/pressed states. This is not exhaustive keyboard traversal or every slider value.
- Guide and disclosures: hide/show all three guide paths and open/close every disclosure.
- Playback: repeated Play/Pause/Restart, automatic end, Replay, preset interruption and a live reduced-motion change. Removing reduced motion does not auto-resume.
- Speed: all three choices are saved correctly; downloaded model samples are identical across presentation speeds. Exact wall-clock playback-rate accuracy is not measured.
- Downloads: four actual JSON downloads per edition per browser, preserving time, settings and all 481 samples checked against independently evaluated sine equations.
- Rendering: visible SVGs, equal coordinate scale despite desktop SVG letterboxing, unfilled time axes, no whole-page horizontal overflow at the three widths.
- No page/console errors or HTTP(S) requests observed during the tested startup and interaction flows.

Screenshots show the line preset at 0.125 seconds with Still mode on. They do not establish animation smoothness, every preset's visual correctness, focus order, zoom usability or screen-reader output. The narrow time-graph labels are small; readable text and numeric outputs remain available, but mobile legibility requires user testing.

## Reproduce

The runtime needs no installation. These are optional development dependencies, installed only in a supported testing environment:

```sh
python -m pip install playwright==1.56.0
python -m playwright install --with-deps chromium firefox
python tools/motion-trace-shape/tests/browser_smoke.py --browser chromium --screenshots /tmp/motion-chromium --report /tmp/motion-chromium.json
python tools/motion-trace-shape/tests/browser_smoke.py --browser firefox --screenshots /tmp/motion-firefox --report /tmp/motion-firefox.json
node --test tools/motion-trace-shape/tests/*.test.cjs
python tools/motion-trace-shape/tests/static_check.py
```

Use Ubuntu 24.04 for the pinned CI configuration. The initial `ubuntu-latest` attempt failed installation after that label moved to 26.04. A first test-harness attempt used function polling blocked by the app's CSP; it was replaced by native value assertions without relaxing CSP. Another assertion incorrectly equated the SVG viewport with its square coordinate plot; it now checks equal coordinate-transform scale, allowing correct letterboxing. These failed attempts are retained in PR history, not presented as app passes.

Local browser launch still fails before page load because the execution environment does not permit Chromium's process socket, including a permitted elevated attempt. CI is the source of browser evidence. Offline aggregate checks pass locally: 244 Python tests, 183 Node tests (including 46 motion tests), 46 Reality Atlas calculation/syntax checks, record/schema, generated-view, evidence and archive integrity checks. These counts are software checks, not a count of browser scenarios or scientific acceptance.

The workflow keeps reports and screenshots for seven days. The checked-in JSON reports preserve the result and runtime hashes after those temporary artifacts expire. Failure before screenshot/report creation leaves only CI logs. Reviewed baseline hashes were updated only for this contribution's changed/new files, including the corrected pinned HTML.

## Still open

`TASK-motion-browser-test` remains open: Safari, Edge, actual desktop/device workflows, physical mobile/touch interaction, keyboard-only traversal, zoom, screen readers, background-tab pausing on a real desktop, human visual review, educator review and learner acceptance remain unverified. No accessibility certification, educational-effectiveness or physical-safety claim is made.

Rollback: revert this focused PR's merge commit. Earlier runtime bytes remain available in main's history; do not merge an unrelated parent branch to retrieve this fix.
