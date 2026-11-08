# Reality Atlas Appearance browser validation

Date: 2026-11-08. Assessment: **scoped offline Chromium/Firefox checks pass with software WebGL2 rendering**. The preserved 0.3.1 runtime remains unchanged. This is classical geometry visualization, not a quantum simulation or a validated learning intervention.

## Exact artifact and evidence

Base main: `6a98641e71e6c7b853e53b4b8d5938ec4c953a4c`. Passing implementation/test head: `30405d4ed988b8c45c37c092eeac661c0b2733ba`, tree `9c23362e3091d370e46bb276424252eaf9364430`.

The [exact-head push run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42482772533) and [PR run](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42482775452) passed all nine jobs: aggregate validation plus Motion, Lumen, Water and Reality Atlas in Chromium/Firefox. The PR job checks GitHub's generated merge revision. Later documentation changes must also pass CI before integration.

The preserved HTML is 57,046 bytes, SHA-256 `fdb0f246ddcf45e3b6b90fae356c95dfce86cfab122fab33a1143659f87bce0d`. Browser runner SHA-256: `3e5dae7ce9ed8b68fb75d9ec9a938cf9146ae6297245587bf07f3484611e1926`. Neither runtime nor its CC0 license changed. The new archive harness and documentation are CC BY 4.0.

The unchanged [Chromium JSON report](reality-atlas-chromium-2026-11-08.json) and [Firefox JSON report](reality-atlas-firefox-2026-11-08.json) each record **18 passing check groups**, not 18 independent scientific acceptance criteria. Environment: GitHub-hosted Ubuntu 24.04 x86-64, Python 3.11.18, Playwright 1.56.0, Xvfb; Chromium 141.0.7390.37 and Firefox 142.0.1. These are pinned automation builds, not a claim to test the latest consumer releases.

Chromium reported `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`. Firefox reported `llvmpipe, or similar`. Software rendering was requested explicitly; this is actual WebGL2 execution on software backends, not hardware-GPU performance evidence.

## What was exercised

The runner copies **only** the unchanged HTML into a temporary folder and opens its actual `file://` URL in a fresh browser context with networking offline. No server, HTML injection, imported app source or network service supplies the main flow. Source/reference hyperlinks are not opened.

- Nonblank framebuffer pixels, actual instanced draw batches and no WebGL error at the recorded checkpoints.
- Snapshot, Trail, Exposure and Occupancy produce distinct frames while retaining the same underlying motion settings. All four presets and native keyboard range actions change the displayed geometry.
- Orbit, precession, vertical vibration, radial breathing, observation window, palette and physical reference frequency controls. Palette changes retain model settings; physical time and display playback time remain separate.
- Reduced-motion startup pauses. Scrubbing pauses and freezes the frame; Play advances model time and pixels. Keyboard camera, zoom button, Fit and mouse drag update the camera. Motion Reset restores the selected preset, cycle and observation window.
- Matter and Void switch actual rendered data. Cutaway changes pixels; the tetrahedral reference distinguishes point-probe and finite-probe accessibility. The 25³, 33³ and 49³ grids render. Fibonacci, seeded unequal placement, spherical container and packing Reset are exercised. These tests do not establish exact physical topology or optimal packing.
- **Ten real downloads per browser:** five JSON/SVG pairs, covering motion exposure, packing void and three narrow/landscape layouts. Saved JSON equals current recorded state with finite numbers. Saved SVG parses as XML, contains calculated glyphs and matching metadata, and discloses schematic limits. Each pair is retained in its own artifact folder with hashes. SVG rendering in third-party editors, packing-cap geometry fidelity and round-trip editing are not established.
- Repeated Motion/Packing switches at 390×844, 320×844 and 844×390 CSS pixels. The framebuffer has the resized backing dimensions and nonblank pixels; page scroll width fits the visible client width, both export controls stay within that width, the SVG control is reachable and exports work. This is desktop viewport testing, not phone/touch acceptance or complete per-control accessibility testing.
- Native page reload restores the initial paused motion scene, rather than stale packing state.
- A separately labeled centered-sphere renderer fixture checks a filled cutaway-cap pixel. It does not claim that every arbitrary cutaway is visually correct.
- The native `WEBGL_lose_context` testing extension triggers real context loss/restoration. The app explicitly requires Reload; a reload recreates the working scene. It does not automatically rebuild lost resources.
- A separate synthetic test makes the WebGL2 context request return null and verifies the explicit requirement message, rather than reporting a rendered scene. This is fault injection, not a separate physical device test.
- Main-flow page exceptions, console errors and attempted external HTTP(S)/WebSocket requests were empty in both recorded reports. The deliberate unavailable-WebGL error belongs to its separate fault scenario; it is not included in those clean main-flow arrays.

Screenshots and all ten downloaded files per browser are retained in the [Chromium artifact](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42482772533/artifacts/13617289401) and [Firefox artifact](https://github.com/jonjonjon11/jonathan-creative-archive/actions/runs/42482772533/artifacts/13618410869). Artifacts expire after seven days and may require GitHub sign-in. Checked-in JSON summaries remain available afterward. Downloaded ZIP hashes matched GitHub's digests: Chromium `bedffac8abec800e8ff36e286673c83c998a93956c9e65eb5eb86455ee8cd222`; Firefox `14495b1e0411aa72a022308eddda7a0fc74c91a5fba23231b942448e0f44954a`.

## Review and prior limitations

Independent AI source review identified an evidence-retention mistake before publication: repeated downloads would have overwritten earlier scenario files. Each scenario now has its own directory and report paths. Browser assertions passed on their first published run; no failing browser assertion was removed or skipped. No runtime defect requiring an artifact edit was found in this scope.

Independent AI visual review inspected all 20 initial full-page screenshots and found that Chromium captures trim a scrollbar-width strip at the right edge. The suite was strengthened rather than declaring those images clipping-free: it now checks `scrollWidth <= documentElement.clientWidth`, checks both export buttons against that width, and retains normal viewport captures. In the final run, Chromium measured matching scroll/client widths of 375, 305 and 829 px for the requested 390, 320 and 844 px viewports; Firefox measured 390, 320 and 844 px. Both export buttons were inside these bounds. Independent AI review inspected all six new normal-viewport screenshots and verified intact right margins and complete controls beside the Chromium scrollbar. The apparent trimming is specific to full-page captures. Full-page capture cropping remains a screenshot-evidence limitation; these measurements do not establish comprehensive responsive or accessibility acceptance.

The first archive edition's Chromium process-singleton socket failure remains an accurate historical account. The local environment has not been reclassified as browser-capable; GitHub-hosted execution supplies the fresh browser evidence. The source's historical 40 numerical/build and 41 browser checks were not simply relabeled as this new suite. The upstream six-scene suite and source-project draft acceptance gate remain separate.

## Reproduce

From the archive root, with test dependencies installed on an appropriate Linux runner:

```sh
python -m pip install playwright==1.56.0
python -m playwright install --with-deps chromium firefox
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a python tools/reality-atlas/tests/browser_smoke.py --browser chromium --output /tmp/atlas-chromium
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a python tools/reality-atlas/tests/browser_smoke.py --browser firefox --output /tmp/atlas-firefox
node scripts/check_reality_core.cjs
```

The harness installs nothing and requires already installed browsers and an X display. It writes a partial JSON report if a browser launch or assertion fails after report initialization. Test-dependency import or output-directory failures can happen earlier. The runtime remains dependency-free.

Local aggregate checks pass: **251 Python tests, 184 Node tests, 46 Atlas calculation/syntax checks**, record validation, source/standalone parity, generated evidence views, structural/internal-link checks and Archive Steward integrity checks. The new browser jobs join the seven existing CI jobs. Check counts are software evidence, not quality, safety or effectiveness scores.

## Remaining limits

- No iPhone/Safari, Edge, physical touch/pinch, native GPU/Metal, WebGPU, Unity, Unreal or VR testing.
- No browser Back/Forward or back-forward-cache acceptance, browser restart/profile/extension coverage, external-link navigation, or arbitrary operating-system download permissions.
- No complete keyboard traversal, screen-reader assessment, zoom/reflow audit, accessibility conformance, human usability review or learner/educator acceptance.
- No performance benchmark, exhaustive parameter/state coverage, hostile-input security certification or scientific validation of all visual encodings.
- The model prescribes classical motion, not forces, relativity, atomic orbitals or intrinsic spin. Occupancy is a sampled time histogram. Packing is bounded rather than optimal; finite-probe connectivity is an approximate six-neighbor voxel calculation. Colors are declared explanatory mappings.
