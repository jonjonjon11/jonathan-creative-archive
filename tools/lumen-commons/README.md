# Lumen Commons 0.1

A recovered, local-first educational browser adventure prototype with a floating village, five experiments, six clearly scripted NPCs, optional synthesized music, and a local art space. It is distinct from Reality Atlas and the separate cooperation/rescue authoring kit.

**Archive status, 2026-11-08:** 24 Node tests and static source/build, CSP-hash, size-budget and selected prohibited-API checks pass. **The unchanged standalone now passes scoped offline Chromium and Firefox checks**, including all five quests, native save/reload and same-context tab reopen, actual JSON export/restore and narrow layouts. See the [dated browser report](../../docs/test-reports/lumen-browser-2026-11-08.md) for exact builds, coverage and remaining limits. Physical devices, audio/listening, accessibility and educational acceptance remain unverified.

## Try the standalone

1. Download [Lumen-Commons-Play.html](Lumen-Commons-Play.html) from GitHub using **Download raw file**, or download and extract the repository ZIP.
2. Open the downloaded HTML in a desktop browser. GitHub’s source-file view and mobile file-preview apps do not run the application.
3. Explore Fraction Forge, Sky Ferry Lab, Harmony Garden, Star Observatory and Atlas Conservatory. The Common Table offers scripted dialogue, local artwork and optional synthesized tones.
4. To keep a backup, open Settings and choose **Export local progress**. **Restore progress (.json)** reads that downloaded file. Browser storage can be cleared; moving the HTML or changing browsers may use different storage.

No package installation, account, cloud AI, purchased assets, API key or runtime dependency is required. This archive publication does not enable a hosted website or multiplayer service. The standalone was opened as a local file in the two pinned desktop automation browsers. Other browsers and managed file-preview apps may restrict local HTML; their file-opening behavior is not verified.

## Reproduce and check

From this directory:

```sh
node --test tests/core.test.cjs
python3 build_single.py
python3 tests/static_check.py
```

The preserved build script regenerates the standalone HTML from `index.html` and four local source files. The generated standalone is explicitly included in this archive even though the original `.gitignore` excludes it from a normal source checkout.

An optional development server is provided as `python3 serve.py`; it binds only to loopback by default. It is not production hosting. This review did not start a server or change firewall/network settings. The original `--lan` option exposes it to a local network and should be used only deliberately on a trusted network; never forward its port.

The new archive test `tests/standalone_browser.py` requires Python Playwright 1.56.0 and its installed Chromium or Firefox. The [browser report](../../docs/test-reports/lumen-browser-2026-11-08.md) gives exact setup and run commands. It copies only the standalone into an isolated temporary folder and opens it with networking disabled. This is an optional development dependency, not a runtime requirement. The original `tests/browser_smoke.py` remains unchanged for provenance; its `set_content` and memory-Storage approach is not the source of the new browser evidence.

## What was checked

- 24 Node tests cover bounded mathematical inputs, fraction/projectile/orbit/octave calculations, idempotent progress, approved save-state fields, bounded artwork, movement normalization, obstacles and world edges.
- Static checks confirm exact source/build parity, matching inline CSP hashes, a build under 250 KB, default-deny/no-network CSP, and absence of the selected prohibited runtime API patterns.
- Generated HTML: **81,407 bytes**.
- SHA-256: `e802f3137cf16d0ce693f28c70182a32aadaef68b8547905d000433ee477d1e2`.

The November 6 archive attempt failed before page load because local Chromium could not create its process-singleton socket. That remains a local-environment limitation, not the result of the later successful GitHub-hosted browser runs. Historical upstream documentation reported 35 checks from an older memory-Storage test; those are not counted as current passes. The new suite uses native file-origin storage in its main flow and a separately labeled injected-denial scenario for unavailable storage. Reload and reopening a tab in the same browser context pass; persistence across browser restarts, profile changes, file moves or browser clearing is not established.

No audio/listening, Safari/Edge, physical phone/touch, headset, sustained-performance, accessibility certification, educational efficacy, multiplayer, public child-safety or production-security acceptance is claimed. Browser testing covers the standalone, not direct navigation to the separate source edition. Source/build parity is checked separately.

## Privacy, access and model limits

- The runtime contains no account, analytics, payment, public chat, camera, microphone, device-location or cloud-AI integration. Companions are scripted NPCs, not other players or a live AI.
- Quest flags, discoveries, local artwork, language, appearance and graphics settings are stored only in the browser. Export/restore uses a bounded approved JSON shape; no cross-device sync is implemented. Storage may be unavailable or cleared by the browser.
- Educational source links are ordinary click-only external references with no referrer; those external sites have their own policies. No private source links are included.
- Sound is optional. Direct destination controls offer an alternative to walking. These are implemented source features, not a certification that every device or assistive technology works.
- English, Spanish and Japanese text is present; non-English translations are drafts pending native-speaker review. Some diagnostic/accessibility strings remain English.
- The mathematical lessons use explicitly limited models. Finishing a quest is not proof of academic mastery, scientific validity beyond the stated model, or real-world training qualification.

## Provenance and licenses

Source revision: `6ab40aa56ce9b5fd94908bda3b0e55cdb3e1f33b`, from Jonathan’s Ultimate Educational Universe. The original repository was private at review; its identity is recorded in the [source manifest](source-review-manifest.json), not offered as a public download link.

All 12 included source/license/test files preserve their upstream bytes. The standalone was generated from that source and matches the reviewed build exactly. The manifest records original Git blob hashes and SHA-256 values, distinguishing included files from historical documentation that was inspected but not bundled.

The original source and generated tool retain the complete [CC0 1.0 Universal license](LICENSE). This archive README, the new `tests/standalone_browser.py` and the new validation reports are covered by the surrounding archive’s [CC BY 4.0 license](../../LICENSE). The new test is not one of the 12 preserved upstream files. Neither license clears unrelated purchased assets, other projects, trademarks, patents or unknown third-party rights. No imported art, fonts, sound recordings or runtime third-party library is bundled.
