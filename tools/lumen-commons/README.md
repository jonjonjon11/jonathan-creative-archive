# Lumen Commons 0.1

A recovered, local-first educational browser adventure prototype with a floating village, five experiments, six clearly scripted NPCs, optional synthesized music, and a local art space. It is distinct from Reality Atlas and the separate cooperation/rescue authoring kit.

**Archive status, 2026-11-06:** 24 fresh Node tests passed, and the generated build passed source/build parity, CSP-hash, size-budget and prohibited-runtime-API checks. **Fresh browser testing was blocked before page load.** Current rendering, interactions, audio, downloads and persistence have not been browser-verified in this archive review.

## Try the standalone

1. Download [Lumen-Commons-Play.html](Lumen-Commons-Play.html) from GitHub using **Download raw file**, or download and extract the repository ZIP.
2. Open the downloaded HTML in a desktop browser. GitHub’s source-file view and mobile file-preview apps do not run the application.
3. Explore Fraction Forge, Sky Ferry Lab, Harmony Garden, Star Observatory and Atlas Conservatory. The Common Table offers scripted dialogue, local artwork and optional synthesized tones.

No package installation, account, cloud AI, purchased assets, API key or runtime dependency is required. This archive publication does not enable a hosted website or multiplayer service. Some browsers or managed file viewers may restrict local HTML; file-opening behavior is not newly verified.

## Reproduce and check

From this directory:

```sh
node --test tests/core.test.cjs
python3 build_single.py
python3 tests/static_check.py
```

The preserved build script regenerates the standalone HTML from `index.html` and four local source files. The generated standalone is explicitly included in this archive even though the original `.gitignore` excludes it from a normal source checkout.

An optional development server is provided as `python3 serve.py`; it binds only to loopback by default. It is not production hosting. This review did not start a server or change firewall/network settings. The original `--lan` option exposes it to a local network and should be used only deliberately on a trusted network; never forward its port.

The preserved browser test requires Python Playwright and an installed Chromium. It is included for future testing, but no dependencies were installed for this archive integration.

## What was checked

- 24 Node tests cover bounded mathematical inputs, fraction/projectile/orbit/octave calculations, idempotent progress, approved save-state fields, bounded artwork, movement normalization, obstacles and world edges.
- Static checks confirm exact source/build parity, matching inline CSP hashes, a build under 250 KB, default-deny/no-network CSP, and absence of the selected prohibited runtime API patterns.
- Generated HTML: **81,407 bytes**.
- SHA-256: `e802f3137cf16d0ce693f28c70182a32aadaef68b8547905d000433ee477d1e2`.

Fresh browser suite did not run: Chromium exited during startup because the execution sandbox denied its process-singleton socket creation (`Operation not permitted`). **The app was not loaded.** Historical upstream documentation reported 35 browser checks; those are not current passes. That older suite used an in-memory Storage double for persistence logic, not verification of native browser persistence.

No fresh audio/listening, Safari, Firefox, phone, headset, sustained performance, accessibility certification, educational efficacy, multiplayer, public child-safety or production-security acceptance is claimed.

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

The original source and generated tool retain the complete [CC0 1.0 Universal license](LICENSE). This new archive README is covered by the surrounding archive’s [CC BY 4.0 license](../../LICENSE). Neither license clears unrelated purchased assets, other projects, trademarks, patents or unknown third-party rights. No imported art, fonts, sound recordings or runtime third-party library is bundled.
