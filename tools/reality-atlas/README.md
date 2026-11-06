# Reality Atlas Appearance 0.3.1

A recovered, self-contained browser teaching tool for motion, observation, sphere packing, and void exploration. The HTML is preserved **unchanged** and has its own **CC0 1.0 Universal** license. That license applies to this upstream artifact, not automatically to the rest of the archive.

## Open the tool

1. Extract the archive to a normal folder.
2. Open [Reality_Atlas_Appearance_0.3.1.html](Reality_Atlas_Appearance_0.3.1.html) in a desktop browser with WebGL2 support.
3. If a file-preview app shows text or a blank preview, use an actual browser. No server, account, paid API, or runtime download is required by the file.
4. Start with Motion composer. Compare Snapshot, Trail, Exposure, and Occupancy. Then try Matter & void, change the radius family, and vary the probe radius.

The interface includes Save state (JSON) and Export vector view (SVG). These are existing source features, **not freshly browser-verified exports** in this archive review.

## Fresh testing: limited pass; browser test blocked

**46 focused calculation-layer and syntax checks passed** on Node v24.22.1. The test extracts the original calculation code, leaves the HTML unchanged, and supplies no filesystem, network, process, or browser objects to that code. It checks finite geometry, circle closure, rotation, declared speed bounds, history budgets/weights, occupancy weight conservation, deterministic non-overlapping packing, finite-probe voxel behavior, invalid inputs, the exact original hash, and whole-script syntax.

Run `node scripts/check_reality_core.cjs` from the repository root. [Machine-readable results](core-check-results.json) list the checks.

**A fresh rendered-browser test did not run.** Chromium aborted before loading the file because this environment denied creation of its process-singleton socket, including the permitted escalated attempt. Therefore no new claim is made about WebGL rendering, interaction, downloads, SVG export, narrow-screen layout, accessibility, or device performance.

Historical source records report 40 numerical/build checks and 41 Chromium/SwiftShader browser/pixel checks. Those historical suites were not rerun here. iPhone/Safari, native GPU, Unity, VR/headsets, and full inherited-regression acceptance remain unestablished by this edition.

## Scientific limits

- This is prescribed classical geometry and visualization, not a first-principles physics or atomic-orbital solver.
- An accumulated path is not an electron path or intrinsic spin. Occupancy is a sampled time histogram, not a quantum probability law.
- Sphere placement is bounded and non-overlapping, not proven optimal packing.
- Void connectivity is a six-neighbor voxel-center estimate. Narrow passages and small cavities can be missed or falsely disconnected; finite-probe and grid choices matter.
- Colors and glyph sizes are explanatory mappings. Physical and display time are kept distinct.
- The SVG feature produces an orthographic vector-glyph schematic, not a volumetric or optical photograph.

## Provenance and rights

- Source family: Jonathan's Ultimate Educational Universe / Reality Atlas.
- Source commit: `0ffa9ee282e48c8e1dbe9edd77523f8237ec2cb7`.
- Source review: exact-commit root CC0 license verified; complete tree reported no narrower module license; the local bundler uses original local modules and CSS, with no runtime dependency/CDN.
- Recovered HTML matched the original standalone linked by the source pull request byte for byte.
- HTML size: 57,046 bytes.
- HTML SHA-256: `fdb0f246ddcf45e3b6b90fae356c95dfce86cfab122fab33a1143659f87bce0d`.
- License: [CC0 1.0 Universal legal text](LICENSE.CC0-1.0.txt).
- Archive sources: SRC-019 and SRC-033.

The preserved HTML contains its original GitHub pull-request link, which may require access to the source repository. It contains no private Drive or conversation locator. Static inspection found no network-request APIs, remote runtime dependencies, persistent storage, device-permission APIs, forms, or identified credentials. This is a focused review, not a comprehensive security or legal audit.

CC0 does not clear trademark, patent, privacy, publicity, or unknown third-party rights. Do not apply this artifact's license to unrelated datasets, other projects, purchased assets, or the compilation by association.
