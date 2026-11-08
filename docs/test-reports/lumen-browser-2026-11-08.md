# Lumen Commons standalone browser validation

Date: 2026-11-08. Assessment: **scoped automated desktop-browser checks pass; broader device, accessibility and educational acceptance remains open**.

## Exact build and evidence

Base main: `4ec2de69023b42550fb0838ea641cf2411b13dfc`. Test contribution: `ba995cbcf328d80027102250d5bd3543b95cc062`, tree `e37ac2700de04c12e9b580c977d4240c99402a5d`.

Both the [exact-head push run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42465334878) and [PR run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42465340120) passed all five jobs: archive validation, Motion Chromium/Firefox and the new Lumen Chromium/Firefox jobs. The PR run used GitHub's generated merge revision; the separate push run checked the exact published head. Subsequent documentation-only changes must also pass CI before merge.

The [Chromium JSON report](lumen-chromium-2026-11-08.json) and [Firefox JSON report](lumen-firefox-2026-11-08.json) preserve the actual reports from the successful PR-job artifacts, including runtime and test-runner SHA-256 hashes. They record GitHub-hosted Ubuntu 24.04 x86-64, Python 3.11.18, Playwright 1.56.0, Chromium 141.0.7390.37 and Firefox 142.0.1. These are pinned automation builds, not claims about the newest consumer browsers.

No runtime fix was needed for the tested flows. The recovered source, original tests, generated standalone, CSP and source-review manifest remain byte-for-byte unchanged. The standalone remains 81,407 bytes, SHA-256 `e802f3137cf16d0ce693f28c70182a32aadaef68b8547905d000433ee477d1e2`. The new archive test and report use CC BY 4.0; preserved Lumen code and generated HTML retain CC0.

## What was exercised

The new `tools/lumen-commons/tests/standalone_browser.py` copies **only** the portable HTML into an isolated temporary folder. It opens the actual file URL in a fresh browser context with networking disabled. The main flow uses native file-origin localStorage, not a Storage substitute. CSP is not bypassed or relaxed.

- All five quests: supportive wrong-answer feedback and a hint, native keyboard ranges for the known answers, completion indicators and repeated fraction completion without a duplicate reward.
- Dialogs: keyboard activation of Begin, explicit Close and Escape dismissal, and focus return to the world canvas. This is not comprehensive keyboard-only traversal.
- Settings: English/Spanish/Japanese language switching, low graphics quality and reduced-motion setting. These check UI state, not translation quality, animation smoothness or absence of all motion.
- Scripted café: a new reply is appended by Say hello, and adding one star produces the expected bounded artwork in saved state. No audio is played.
- Native storage: the five quest flags, artwork and settings survive a page reload and closing/reopening a tab in the same browser context. Browser restart/profile persistence and moving the file were not tested; file-origin storage behavior can vary across browsers and settings.
- Four real JSON downloads per browser: two repeated exports, an export after the erase/restore roundtrip and an export under injected storage denial. The first three exactly match the captured synthetic state; the fourth retains the completed fraction quest despite unavailable storage.
- Erase/restore: Cancel preserves synthetic state, Accept clears progress and artwork, and restoring the actual exported JSON restores both. Malformed JSON, a future version and an oversized file produce fresh error responses without overwriting existing progress.
- Layout: correctly sized, nonblank world pixels after resizing, no page horizontal overflow, six destinations reachable through Explore, and horizontal/vertical dialog bounds at 1280×1000, 390×844, 320×844 and 844×390 CSS pixels. The fraction controls are also operated to completion at every size, including the scrolled short-landscape dialog. Narrow viewports are **not physical phone or touch tests**.
- Separate fault injection: a localStorage getter deliberately throws SecurityError before startup. The app explains unavailable storage, remains playable and exports the current quest state. Reload correctly starts without saved progress. This tests a controlled denial, not every browser storage-failure mode.
- No page exceptions, console errors or external network requests occurred during these tested flows. Reference links were not opened.

## Reproduce

The application itself needs no installation. These are optional development dependencies for an appropriate test environment, matching the Ubuntu 24.04 CI job:

```sh
python -m pip install playwright==1.56.0
python -m playwright install --with-deps chromium firefox
python tools/lumen-commons/tests/standalone_browser.py --browser chromium --screenshots /tmp/lumen-chromium --report /tmp/lumen-chromium.json
python tools/lumen-commons/tests/standalone_browser.py --browser firefox --screenshots /tmp/lumen-firefox --report /tmp/lumen-firefox.json
node --test tools/lumen-commons/tests/core.test.cjs
python tools/lumen-commons/tests/static_check.py
```

The runner only uses an already installed browser. Its optional `--chromium` argument selects an existing executable. All erase/import actions target isolated synthetic test state, not a person's browser profile or progress. Reports are emitted only after all assertions pass. Failure screenshots are attempted before preserving the original exception. CI keeps screenshots and reports for seven days; the checked-in JSON reports remain after temporary artifact expiry.

The local execution environment still prevents Chromium startup before page load with a process-singleton socket error. GitHub-hosted CI supplies the browser evidence. Local aggregate checks include 244 Python tests, 183 Node tests, 46 Reality Atlas calculation/syntax checks, record/structure/link checks, exact generated views and reviewed archive checksums. Counts are software checks, not educational or accessibility acceptance.

## Independent review and limits

Independent AI review identified three false-positive risks before the first published browser run. The test now checks the new café reply rather than existing welcome text, checks vertical as well as horizontal dialog bounds, and requires a fresh error toast for each invalid import. Follow-up review confirmed all seven report hashes match the current files, the reported scope matches assertions and the runtime is unchanged. The historical `tests/browser_smoke.py` is preserved, not counted as newly passing evidence.

The first passing CI run at `b45a360ca07e817eb5dc740d810b53ec48aa8b20` exposed a test weakness during screenshot inspection: Firefox captures at 320×844 and 844×390 showed a cleared black world canvas immediately after resizing, while subsequent dialog captures showed rendered scenery. Source review confirmed that resizing clears the canvas before the next scheduled render. A persistent app failure was not established.

The test now waits up to five seconds for correctly resized, varied nonblack pixels on two successive reads before capturing the world. Both browser jobs passed again at the revision above, and fresh screenshots show the world rendered at all four sizes. The runtime itself remains unchanged. The pixel check establishes paint readiness, not graphical accuracy.

AI visual review inspected the 12 current screenshots per browser (world and fraction views at four sizes plus the four other completed quest views). The updated world captures are nonblank, diagrams and controls are present, and the landscape dialog scrolls to its controls in the automated interaction. Tiny canvas labels, differing font wrapping and browser-default range styling remain usability considerations, not certified accessibility. No human visual acceptance is established.

Artifact ZIP SHA-256 values were verified before inspection: Chromium `d46007e30a389f482b783504c7bd366b3adf09f8a0feb8a2bbb9889d14abff13`, Firefox `4fc28cc2880a7d349153bc57fcbe69a8bdd26c023ca96b2619558ef8be6f9f73`. All seven report hashes match the source, standalone and runner used here.

Still unverified: direct browser navigation to the source edition; browser-restart/profile persistence and file moves; actual iPhone/Android/touch; Safari/Edge; audio/listening; canvas walking and joystick input; zoom, screen readers and full keyboard traversal; full accessibility conformance; native-speaker translation review; educator/learner acceptance; sustained performance; public child-safety or production-security acceptance. No hosting, multiplayer, clinical or learning-effectiveness claim is made.

Rollback: revert this focused contribution's merge commit. The original recovered runtime is unchanged; no unrelated proposal branch is needed.
