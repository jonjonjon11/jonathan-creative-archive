// Universal Color / Pixel Engine v1
// Dependency-free ES module. All semantic mappings are explicitly representational,
// not claims that abstract concepts literally possess physical color or motion.

export const EPSILON = 1e-12;

export function clamp(value, min, max) {
  if (!Number.isFinite(value)) throw new TypeError('value must be finite');
  return Math.min(max, Math.max(min, value));
}

export function clamp01(value) {
  return clamp(value, 0, 1);
}

export function srgbChannelToLinear(encoded) {
  const c = clamp01(encoded);
  return c <= 0.04045
    ? c / 12.92
    : Math.pow((c + 0.055) / 1.055, 2.4);
}

export function linearChannelToSrgb(linear) {
  if (!Number.isFinite(linear)) throw new TypeError('linear must be finite');
  const c = Math.max(0, linear);
  return c <= 0.0031308
    ? 12.92 * c
    : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
}

export function srgb8ToLinearRgb([r, g, b]) {
  for (const c of [r, g, b]) {
    if (!Number.isInteger(c) || c < 0 || c > 255) {
      throw new RangeError('sRGB8 channels must be integers in 0..255');
    }
  }
  return [
    srgbChannelToLinear(r / 255),
    srgbChannelToLinear(g / 255),
    srgbChannelToLinear(b / 255)
  ];
}

export function linearRgbToSrgb8([r, g, b]) {
  return [r, g, b].map(c =>
    Math.round(clamp01(linearChannelToSrgb(c)) * 255)
  );
}

export function relativeLuminance([r, g, b]) {
  for (const c of [r, g, b]) {
    if (!Number.isFinite(c)) throw new TypeError('RGB channels must be finite');
  }
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// D65, sRGB linear RGB <-> CIE XYZ.
// XYZ values are normalized to Y=1 for reference white.
export function linearRgbToXyzD65([r, g, b]) {
  return [
    0.4124564 * r + 0.3575761 * g + 0.1804375 * b,
    0.2126729 * r + 0.7151522 * g + 0.0721750 * b,
    0.0193339 * r + 0.1191920 * g + 0.9503041 * b
  ];
}

export function xyzD65ToLinearRgb([x, y, z]) {
  return [
     3.2404542 * x - 1.5371385 * y - 0.4985314 * z,
    -0.9692660 * x + 1.8760108 * y + 0.0415560 * z,
     0.0556434 * x - 0.2040259 * y + 1.0572252 * z
  ];
}

const D65 = [0.95047, 1.0, 1.08883];
const LAB_DELTA = 6 / 29;

function labF(t) {
  const d3 = LAB_DELTA ** 3;
  return t > d3
    ? Math.cbrt(t)
    : t / (3 * LAB_DELTA ** 2) + 4 / 29;
}

function labFInv(t) {
  return t > LAB_DELTA
    ? t ** 3
    : 3 * LAB_DELTA ** 2 * (t - 4 / 29);
}

export function xyzD65ToLab([x, y, z]) {
  const fx = labF(x / D65[0]);
  const fy = labF(y / D65[1]);
  const fz = labF(z / D65[2]);
  return [
    116 * fy - 16,
    500 * (fx - fy),
    200 * (fy - fz)
  ];
}

export function labToXyzD65([L, a, b]) {
  const fy = (L + 16) / 116;
  const fx = fy + a / 500;
  const fz = fy - b / 200;
  return [
    D65[0] * labFInv(fx),
    D65[1] * labFInv(fy),
    D65[2] * labFInv(fz)
  ];
}

// Björn Ottosson OKLab conversion.
export function linearRgbToOklab([r, g, b]) {
  const l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b;
  const m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b;
  const s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b;

  const l_ = Math.cbrt(l);
  const m_ = Math.cbrt(m);
  const s_ = Math.cbrt(s);

  return [
    0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
    1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
    0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
  ];
}

export function oklabToLinearRgb([L, a, b]) {
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.2914855480 * b;

  const l = l_ ** 3;
  const m = m_ ** 3;
  const s = s_ ** 3;

  return [
     4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
  ];
}

export function oklabToOklch([L, a, b]) {
  const C = Math.hypot(a, b);
  let h = Math.atan2(b, a) * 180 / Math.PI;
  if (h < 0) h += 360;
  return [L, C, h];
}

export function oklchToOklab([L, C, h]) {
  const radians = h * Math.PI / 180;
  return [L, C * Math.cos(radians), C * Math.sin(radians)];
}

export function compositeStraightAlpha(srcRgb, srcA, dstRgb, dstA = 1) {
  srcA = clamp01(srcA);
  dstA = clamp01(dstA);
  const outA = srcA + dstA * (1 - srcA);
  if (outA <= EPSILON) return { rgb: [0, 0, 0], alpha: 0 };
  const rgb = [0, 1, 2].map(i =>
    (srcRgb[i] * srcA + dstRgb[i] * dstA * (1 - srcA)) / outA
  );
  return { rgb, alpha: outA };
}

export function hash32(text) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export const DOMAIN_HUE = Object.freeze({
  mathematics: 255,
  geometry: 190,
  physics: 42,
  chemistry: 145,
  biology: 118,
  medicine: 350,
  mind: 295,
  earth: 75,
  astronomy: 265,
  engineering: 210,
  computation: 165,
  information: 175,
  language: 20,
  history: 30,
  philosophy: 280,
  music: 325,
  sports: 90,
  art: 5,
  color: 0,
  measurement: 180,
  education: 205
});

export function nodeHue(node) {
  const base = DOMAIN_HUE[node.domain] ?? 0;
  const offset = (hash32(node.id) / 0xffffffff) * 36 - 18;
  return (base + offset + 360) % 360;
}

export function alphaFromConfidence(confidence = 1) {
  return 0.15 + 0.85 * clamp01(confidence);
}

export function blurFromUncertainty(uncertainty = 0, maxPx = 12) {
  return clamp01(uncertainty) * maxPx;
}

export function logMapPositive(value, inputMin, inputMax, outputMin, outputMax) {
  if (!(inputMin > 0) || !(inputMax > inputMin)) {
    throw new RangeError('input range must be positive and increasing');
  }
  if (!(outputMax >= outputMin)) {
    throw new RangeError('output range must be increasing');
  }
  const v = Math.max(value, inputMin);
  const lo = Math.log10(inputMin);
  const hi = Math.log10(inputMax);
  const t = clamp01((Math.log10(v) - lo) / (hi - lo));
  return outputMin + t * (outputMax - outputMin);
}

export function safeDisplayRate(sourceHz, {
  sourceMin = 1e-9,
  sourceMax = 1e20,
  displayMin = 0.1,
  displayMax = 8
} = {}) {
  if (!(sourceHz > 0)) return 0;
  return logMapPositive(sourceHz, sourceMin, sourceMax, displayMin, displayMax);
}

export const SHAPE_BY_TYPE = Object.freeze({
  entity: 'sphere',
  object: 'sphere',
  particle: 'point',
  element: 'sphere',
  state: 'cube',
  transformation: 'tetrahedron',
  event: 'octahedron',
  system: 'shell',
  process: 'torus',
  relationship: 'line',
  edge: 'line',
  field: 'field',
  dataset: 'grid',
  number: 'glyph',
  integer: 'glyph',
  rational: 'glyph',
  color: 'point',
  note: 'glyph'
});

export function semanticColorForNode(node, {
  magnitude = 0.5,
  confidence = node.confidence ?? 1
} = {}) {
  magnitude = clamp01(magnitude);
  confidence = clamp01(confidence);

  const hue = nodeHue(node);
  const L = clamp(0.42 + 0.40 * magnitude, 0.20, 0.90);
  const C = 0.08 + 0.12 * confidence;

  const oklab = oklchToOklab([L, C, hue]);
  const linearRgb = oklabToLinearRgb(oklab);
  const encodedRgb = linearRgb.map(c => clamp01(linearChannelToSrgb(c)));
  const srgb8 = encodedRgb.map(c => Math.round(c * 255));

  return {
    colorSpace: 'sRGB',
    encodedRgb,
    linearRgb,
    srgb8,
    alpha: alphaFromConfidence(confidence),
    oklch: [L, C, hue],
    mappingStatus: 'SEMANTIC'
  };
}

export function visualMapNode(node, state = {}) {
  const magnitude = clamp01(state.magnitudeNormalized ?? 0.5);
  const confidence = clamp01(state.confidence ?? node.confidence ?? 1);
  const uncertainty = clamp01(state.uncertainty ?? node.uncertainty ?? 0);
  const activity = Math.max(0, state.activity ?? 0);
  const probability = clamp01(state.probability ?? 1);

  const color = semanticColorForNode(node, { magnitude, confidence });

  const physicalFrequencyHz = state.physicalFrequencyHz;
  const eventRateHz = state.eventRateHz;
  const angularVelocityRadS = state.angularVelocityRadS;

  const rotationHz = Number.isFinite(angularVelocityRadS)
    ? angularVelocityRadS / (2 * Math.PI)
    : 0;

  return {
    rgba8: [...color.srgb8, Math.round(color.alpha * 255)],
    linearRgb: color.linearRgb,
    oklch: color.oklch,
    luminance: relativeLuminance(color.linearRgb),
    shape: SHAPE_BY_TYPE[node.type] ?? 'sphere',
    size: 0.5 + 1.5 * magnitude,
    emission: activity,
    sharpness: 1 - uncertainty,
    blurPx: blurFromUncertainty(uncertainty),
    roughness: uncertainty,
    metallic: 0,
    transmission: 0,
    symmetry: 0.5,
    complexity: 0.5,
    rotationHz,
    vibrationHz: Number.isFinite(physicalFrequencyHz)
      ? safeDisplayRate(physicalFrequencyHz, { displayMax: 12 })
      : 0,
    vibrationAmplitude: Number.isFinite(physicalFrequencyHz) ? 0.05 : 0,
    pulseHz: activity > 0 ? 0.25 + Math.min(activity, 4) * 0.5 : 0,
    pulseAmplitude: Math.min(activity * 0.1, 0.4),
    flickerHz: Number.isFinite(eventRateHz)
      ? safeDisplayRate(eventRateHz)
      : 0,
    flickerAmplitude: Number.isFinite(eventRateHz) ? 0.15 : 0,
    jitter: uncertainty * 0.25,
    turbulence: Math.max(0, state.turbulence ?? 0),
    fieldRadius: Math.max(0, state.fieldRadius ?? 1),
    fieldStrength: Math.max(0, state.fieldStrength ?? probability),
    trailLength: Math.max(0, state.historySeconds ?? 0),
    probability,
    confidence,
    uncertainty,
    mappingStatus: 'PEDAGOGICAL',
    legend: {
      hue: 'semantic domain/identity mapping unless overridden by a physical color model',
      lightness: 'normalized magnitude',
      alpha: 'epistemic confidence',
      blur: 'uncertainty',
      emission: 'activity',
      vibration: Number.isFinite(physicalFrequencyHz)
        ? 'source frequency mapped to safe display frequency'
        : 'unused',
      flicker: Number.isFinite(eventRateHz)
        ? 'event rate mapped to safe display frequency'
        : 'unused',
      rotation: Number.isFinite(angularVelocityRadS)
        ? 'classical angular velocity / 2π'
        : 'unused'
    }
  };
}

export function srgba8Address(r, g, b, a = 255) {
  for (const c of [r, g, b, a]) {
    if (!Number.isInteger(c) || c < 0 || c > 255) {
      throw new RangeError('RGBA channels must be integers in 0..255');
    }
  }
  return `urn:universe:color:srgba8:${r},${g},${b},${a}`;
}

export function colorContribution({
  sourceNodeId,
  channel,
  value,
  weight = 1,
  mappingStatus = 'SEMANTIC',
  explanation = ''
}) {
  return {
    sourceNodeId,
    channel,
    value,
    weight,
    mappingStatus,
    explanation
  };
}

// Weighted OKLab blend for semantic/pedagogical color contributions.
// Physical spectral mixing must use a physical spectral model instead.
export function blendSemanticColors(colors) {
  if (!Array.isArray(colors) || colors.length === 0) {
    throw new RangeError('colors must be a non-empty array');
  }

  let total = 0;
  let L = 0, a = 0, b = 0, alpha = 0;

  for (const item of colors) {
    const weight = Math.max(0, item.weight ?? 1);
    if (weight === 0) continue;
    const encoded = item.encodedRgb;
    const linear = encoded.map(srgbChannelToLinear);
    const lab = linearRgbToOklab(linear);

    total += weight;
    L += lab[0] * weight;
    a += lab[1] * weight;
    b += lab[2] * weight;
    alpha += clamp01(item.alpha ?? 1) * weight;
  }

  if (total <= EPSILON) {
    return { encodedRgb: [0, 0, 0], alpha: 0, mappingStatus: 'SEMANTIC' };
  }

  const linear = oklabToLinearRgb([L / total, a / total, b / total]);
  const encodedRgb = linear.map(c => clamp01(linearChannelToSrgb(c)));

  return {
    encodedRgb,
    srgb8: encodedRgb.map(c => Math.round(c * 255)),
    alpha: alpha / total,
    mappingStatus: 'SEMANTIC'
  };
}
