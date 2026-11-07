import test from 'node:test';
import assert from 'node:assert/strict';

import {
  srgbChannelToLinear,
  linearChannelToSrgb,
  srgb8ToLinearRgb,
  linearRgbToSrgb8,
  relativeLuminance,
  linearRgbToXyzD65,
  xyzD65ToLinearRgb,
  xyzD65ToLab,
  labToXyzD65,
  linearRgbToOklab,
  oklabToLinearRgb,
  compositeStraightAlpha,
  nodeHue,
  alphaFromConfidence,
  blurFromUncertainty,
  safeDisplayRate,
  semanticColorForNode,
  visualMapNode,
  srgba8Address,
  blendSemanticColors
} from '../src/index.mjs';

function near(a, b, eps = 1e-6) {
  assert.ok(Math.abs(a - b) <= eps, `${a} !~= ${b}`);
}

function nearVec(a, b, eps = 1e-6) {
  assert.equal(a.length, b.length);
  for (let i = 0; i < a.length; i++) near(a[i], b[i], eps);
}

test('sRGB channel round-trips representative values', () => {
  for (const c of [0, 0.001, 0.04045, 0.18, 0.5, 1]) {
    near(linearChannelToSrgb(srgbChannelToLinear(c)), c, 2e-6);
  }
});

test('8-bit sRGB round-trip is exact for reference colors', () => {
  for (const rgb of [[0,0,0], [255,255,255], [255,0,0], [12,127,233]]) {
    assert.deepEqual(linearRgbToSrgb8(srgb8ToLinearRgb(rgb)), rgb);
  }
});

test('linear red relative luminance is approximately 0.2126', () => {
  near(relativeLuminance([1,0,0]), 0.2126, 1e-12);
});

test('linear white maps to D65 XYZ reference white', () => {
  const xyz = linearRgbToXyzD65([1,1,1]);
  nearVec(xyz, [0.95047, 1.0, 1.08883], 5e-5);
});

test('XYZ linear RGB round-trip', () => {
  const rgb = [0.1, 0.5, 0.9];
  nearVec(xyzD65ToLinearRgb(linearRgbToXyzD65(rgb)), rgb, 2e-6);
});

test('XYZ Lab round-trip', () => {
  const xyz = [0.25, 0.40, 0.15];
  nearVec(labToXyzD65(xyzD65ToLab(xyz)), xyz, 1e-8);
});

test('OKLab linear RGB round-trip', () => {
  const rgb = [0.18, 0.40, 0.73];
  nearVec(oklabToLinearRgb(linearRgbToOklab(rgb)), rgb, 3e-7);
});

test('straight alpha compositing returns expected opaque mix', () => {
  const out = compositeStraightAlpha([1,0,0], 0.5, [0,0,1], 1);
  nearVec(out.rgb, [0.5,0,0.5], 1e-12);
  near(out.alpha, 1, 1e-12);
});

test('node hue is deterministic and domain-bounded around anchor', () => {
  const node = { id: 'urn:universe:chemistry:element:H', domain: 'chemistry' };
  assert.equal(nodeHue(node), nodeHue(node));
  const delta = ((nodeHue(node) - 145 + 540) % 360) - 180;
  assert.ok(delta >= -18 && delta <= 18);
});

test('confidence and uncertainty visual channels are bounded', () => {
  near(alphaFromConfidence(0), 0.15);
  near(alphaFromConfidence(1), 1);
  near(blurFromUncertainty(0), 0);
  near(blurFromUncertainty(1), 12);
});

test('display rate is bounded and monotonic', () => {
  const low = safeDisplayRate(1e-6);
  const mid = safeDisplayRate(1);
  const high = safeDisplayRate(1e18);
  assert.ok(low >= 0.1);
  assert.ok(mid > low);
  assert.ok(high > mid);
  assert.ok(high <= 8);
});

test('semantic node color is deterministic and display-valid', () => {
  const node = {
    id: 'urn:universe:math:integer:7',
    domain: 'mathematics',
    type: 'integer',
    confidence: 1
  };
  const a = semanticColorForNode(node);
  const b = semanticColorForNode(node);
  assert.deepEqual(a.srgb8, b.srgb8);
  for (const c of a.srgb8) assert.ok(c >= 0 && c <= 255);
});

test('generic visual map exposes provenance legend and valid channels', () => {
  const node = {
    id: 'urn:universe:physics:particle:electron',
    domain: 'physics',
    type: 'particle',
    confidence: 0.9,
    uncertainty: 0.2
  };
  const visual = visualMapNode(node, {
    magnitudeNormalized: 0.7,
    activity: 0.5,
    physicalFrequencyHz: 1e12,
    eventRateHz: 1e3,
    historySeconds: 2
  });
  assert.equal(visual.rgba8.length, 4);
  assert.equal(visual.shape, 'point');
  assert.ok(visual.vibrationHz > 0);
  assert.ok(visual.flickerHz > 0);
  assert.equal(visual.trailLength, 2);
  assert.match(visual.legend.hue, /semantic/i);
});

test('sRGBA address generator is exact', () => {
  assert.equal(
    srgba8Address(255, 0, 127, 64),
    'urn:universe:color:srgba8:255,0,127,64'
  );
});

test('semantic color blending produces valid display values', () => {
  const mixed = blendSemanticColors([
    { encodedRgb: [1,0,0], alpha: 1, weight: 1 },
    { encodedRgb: [0,0,1], alpha: 1, weight: 1 }
  ]);
  for (const c of mixed.srgb8) assert.ok(c >= 0 && c <= 255);
  near(mixed.alpha, 1);
});
