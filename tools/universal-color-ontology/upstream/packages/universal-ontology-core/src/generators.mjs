// Universal Ontology Core v1 generators for infinite/large address spaces.

export function integerNode(n) {
  const v = BigInt(n);
  return {
    id: `urn:universe:mathematics:integer:${v}`,
    domain: 'mathematics',
    subdomain: 'number',
    type: 'integer',
    label: v.toString(),
    properties: {
      value: v.toString(),
      parity: v % 2n === 0n ? 'even' : 'odd'
    },
    state: {},
    epistemicStatus: 'DERIVED'
  };
}

function absBigInt(n) {
  return n < 0n ? -n : n;
}

function gcd(a, b) {
  a = absBigInt(a);
  b = absBigInt(b);
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

export function rationalNode(numerator, denominator) {
  let p = BigInt(numerator);
  let q = BigInt(denominator);
  if (q === 0n) throw new RangeError('denominator cannot be zero');
  const g = gcd(p, q);
  p /= g;
  q /= g;
  if (q < 0n) {
    p = -p;
    q = -q;
  }
  return {
    id: `urn:universe:mathematics:rational:${p}/${q}`,
    domain: 'mathematics',
    subdomain: 'number',
    type: 'rational',
    label: `${p}/${q}`,
    properties: { numerator: p.toString(), denominator: q.toString() },
    state: {},
    epistemicStatus: 'DERIVED'
  };
}

export function complexNode(real, imaginary) {
  if (!Number.isFinite(real) || !Number.isFinite(imaginary)) {
    throw new TypeError('complex coordinates must be finite');
  }
  return {
    id: `urn:universe:mathematics:complex:${real},${imaginary}`,
    domain: 'mathematics',
    subdomain: 'number',
    type: 'complex',
    label: `${real}${imaginary < 0 ? '' : '+'}${imaginary}i`,
    properties: { real, imaginary },
    state: {},
    epistemicStatus: 'DERIVED'
  };
}

export function regularPolygonNode(n) {
  if (!Number.isInteger(n) || n < 3) throw new RangeError('n must be an integer >= 3');
  return {
    id: `urn:universe:geometry:regular-polygon:${n}`,
    domain: 'geometry',
    subdomain: 'polygon',
    type: 'geometry',
    label: `Regular ${n}-gon`,
    properties: {
      sides: n,
      interiorAngleDegrees: ((n - 2) * 180) / n
    },
    state: {},
    epistemicStatus: 'DERIVED'
  };
}

export function srgba8Node(r, g, b, a = 255) {
  for (const c of [r,g,b,a]) {
    if (!Number.isInteger(c) || c < 0 || c > 255) throw new RangeError('RGBA must be integers 0..255');
  }
  return {
    id: `urn:universe:color:srgba8:${r},${g},${b},${a}`,
    domain: 'color',
    subdomain: 'srgba8',
    type: 'color',
    label: `sRGBA(${r}, ${g}, ${b}, ${a})`,
    properties: { r, g, b, a, colorSpace: 'sRGB', transferFunction: 'sRGB' },
    state: {},
    epistemicStatus: 'CONVENTIONAL'
  };
}

export function midiNoteNode(note, a4Hz = 440) {
  if (!Number.isInteger(note) || note < 0 || note > 127) throw new RangeError('MIDI note must be 0..127');
  if (!(a4Hz > 0) || !Number.isFinite(a4Hz)) throw new RangeError('A4 reference must be positive finite Hz');
  const frequencyHz = a4Hz * Math.pow(2, (note - 69) / 12);
  return {
    id: `urn:universe:music:midi:${note}:a4=${a4Hz}`,
    domain: 'music',
    subdomain: 'pitch',
    type: 'note',
    label: `MIDI ${note}`,
    properties: { midi: note, frequencyHz, tuningReferenceHz: a4Hz },
    state: {},
    epistemicStatus: 'CONVENTIONAL'
  };
}

export function chordNode(midiNotes, a4Hz = 440) {
  if (!Array.isArray(midiNotes) || midiNotes.length === 0) throw new RangeError('midiNotes must be non-empty');
  const notes = [...new Set(midiNotes.map(n => {
    if (!Number.isInteger(n) || n < 0 || n > 127) throw new RangeError('MIDI note must be 0..127');
    return n;
  }))].sort((a,b) => a-b);

  return {
    id: `urn:universe:music:chord:${notes.join(',')}:a4=${a4Hz}`,
    domain: 'music',
    subdomain: 'harmony',
    type: 'system',
    label: `Chord(${notes.join(',')})`,
    properties: {
      midiNotes: notes,
      frequenciesHz: notes.map(n => a4Hz * Math.pow(2, (n - 69) / 12)),
      tuningReferenceHz: a4Hz
    },
    children: notes.map(n => `urn:universe:music:midi:${n}:a4=${a4Hz}`),
    state: {},
    epistemicStatus: 'CONVENTIONAL'
  };
}

export function* unorderedSelfInclusivePairs(items) {
  for (let i = 0; i < items.length; i++) {
    for (let j = i; j < items.length; j++) {
      yield [items[i], items[j]];
    }
  }
}

export function* orderedPairs(items) {
  for (const a of items) {
    for (const b of items) yield [a, b];
  }
}
