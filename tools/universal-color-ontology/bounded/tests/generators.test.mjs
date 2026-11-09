import test from 'node:test';
import assert from 'node:assert/strict';
import * as bounded from '../generators.mjs';
import * as original from '../../upstream/packages/universal-ontology-core/src/generators.mjs';

const { integerNode, rationalNode, midiNoteNode, chordNode } = bounded;

function finiteJson(record) {
  function visit(value) {
    if (typeof value === 'number') assert.ok(Number.isFinite(value));
    if (value && typeof value === 'object') for (const child of Object.values(value)) visit(child);
  }
  visit(record);
  assert.deepEqual(JSON.parse(JSON.stringify(record)), record);
}

test('exports only four validated generators and explicit bounds', () => {
  assert.deepEqual(Object.keys(bounded).sort(), ['MAX_CHORD_INPUTS', 'MAX_INTEGER_DIGITS', 'chordNode', 'integerNode', 'midiNoteNode', 'rationalNode']);
});

test('ordinary integer output preserves upstream identity and shape', () => {
  for (const value of [0, 1, -1, 7, Number.MAX_SAFE_INTEGER, Number.MIN_SAFE_INTEGER]) {
    assert.deepEqual(integerNode(value), original.integerNode(value));
  }
});

test('exact decimal strings and bigints retain digits above Number precision', () => {
  for (const value of ['9007199254740993', '-9007199254740993', '123456789012345678901234567890']) {
    assert.equal(integerNode(value).properties.value, value);
    assert.deepEqual(integerNode(value), integerNode(BigInt(value)));
    finiteJson(integerNode(value));
  }
});

test('unsafe or non-integral Numbers are rejected rather than rounded', () => {
  for (const value of [9007199254740993, -9007199254740993, Number.MAX_VALUE, 0.1, NaN, Infinity, -Infinity]) {
    assert.throws(() => integerNode(value), RangeError);
    assert.throws(() => rationalNode(value, 1), RangeError);
    assert.throws(() => rationalNode(1, value), RangeError);
  }
});

test('integer coercions, whitespace, radix and exponential text are rejected', () => {
  for (const value of [null, true, false, undefined, {}, [], new Number(1), new String('1'), '', ' ', ' 1', '1 ', '1\n', '0x10', '0b10', '1e2', '1.0', '+', '--1', '١']) {
    assert.throws(() => integerNode(value));
    assert.throws(() => rationalNode(value, 1));
    assert.throws(() => rationalNode(1, value));
  }
});

test('integer syntax normalizes signs, leading zeros and negative zero', () => {
  for (const value of ['+0007', '007', 7n]) assert.equal(integerNode(value).properties.value, '7');
  for (const value of ['-0', '+000', 0n, -0]) assert.equal(integerNode(value).properties.value, '0');
});

test('digit bounds apply to signed text, leading zeros and bigint', () => {
  const maximum = '9'.repeat(1024);
  assert.equal(integerNode(maximum).properties.value, maximum);
  assert.equal(integerNode(`-${maximum}`).properties.value, `-${maximum}`);
  assert.equal(integerNode(BigInt(maximum)).properties.value, maximum);
  for (const value of [`${maximum}9`, `-${maximum}9`, '0'.repeat(1025), 10n ** 1024n]) {
    assert.throws(() => integerNode(value), RangeError);
    assert.throws(() => rationalNode(value, 1), RangeError);
    assert.throws(() => rationalNode(1, value), RangeError);
  }
});

test('rational canonicalization preserves exact sign and gcd', () => {
  for (const [p, q, numerator, denominator] of [
    [6, -8, '-3', '4'], [-6, -8, '3', '4'], [0, -9, '0', '1'],
    ['9007199254740993', '3', '3002399751580331', '1'],
    ['123456789012345678901234567890', '10', '12345678901234567890123456789', '1'],
  ]) {
    assert.deepEqual(rationalNode(p, q).properties, { numerator, denominator });
    finiteJson(rationalNode(p, q));
  }
});

test('zero denominator is rejected in every accepted representation', () => {
  for (const zero of [0, -0, 0n, '0', '-00', '+000']) assert.throws(() => rationalNode(1, zero), RangeError);
});

test('rational results obey exact cross multiplication and lowest terms across deterministic inputs', () => {
  const gcd = (a, b) => { a = a < 0n ? -a : a; while (b !== 0n) [a, b] = [b, a % b]; return a < 0n ? -a : a; };
  for (let p = -30; p <= 30; p++) for (let q = -13; q <= 13; q++) {
    if (!q) continue;
    const props = rationalNode(p, q).properties;
    const a = BigInt(props.numerator), b = BigInt(props.denominator);
    assert.equal(a * BigInt(q), b * BigInt(p));
    assert.ok(b > 0n);
    assert.equal(gcd(a, b), 1n);
  }
});

test('all 128 ordinary MIDI outputs preserve original records and survive JSON roundtrip', () => {
  for (let note = 0; note <= 127; note++) for (const tuning of [432, 440, 442]) {
    const result = midiNoteNode(note, tuning);
    assert.deepEqual(result, original.midiNoteNode(note, tuning));
    assert.ok(result.properties.frequencyHz > 0);
    finiteJson(result);
  }
  assert.equal(midiNoteNode(69).properties.frequencyHz, 440);
  assert.equal(midiNoteNode(81).properties.frequencyHz, 880);
});

test('MIDI input rejects coercions, fractional, sparse and out-of-range notes', () => {
  for (const value of [-1, 128, 1.5, NaN, Infinity, '69', 69n, null, false, {}, undefined]) {
    assert.throws(() => midiNoteNode(value), RangeError);
    assert.throws(() => chordNode([value]), RangeError);
  }
  assert.throws(() => chordNode(Array(3)), RangeError);
});

test('MIDI and chords reject nonpositive, non-finite and coerced tuning', () => {
  for (const value of [-440, 0, -0, NaN, Infinity, -Infinity, '440', 440n, null, false, {}]) {
    assert.throws(() => midiNoteNode(69, value), RangeError);
    assert.throws(() => chordNode([60, 69], value), RangeError);
  }
});

test('positive finite tuning is insufficient if computed frequencies overflow or underflow', () => {
  for (const [note, tuning] of [[127, Number.MAX_VALUE], [0, Number.MIN_VALUE]]) {
    assert.throws(() => midiNoteNode(note, tuning), RangeError);
    assert.throws(() => chordNode([69, note], tuning), RangeError);
  }
  finiteJson(midiNoteNode(69, Number.MAX_VALUE));
  finiteJson(midiNoteNode(69, Number.MIN_VALUE));
});

test('chords preserve canonical output without mutating or aliasing caller input', () => {
  const input = Object.freeze([67, 60, 64, 60]);
  const chord = chordNode(input, 432);
  assert.deepEqual(chord, original.chordNode(input, 432));
  assert.deepEqual(chord.properties.midiNotes, [60, 64, 67]);
  const mutable = [69];
  const result = chordNode(mutable);
  mutable[0] = 70;
  assert.deepEqual(result.properties.midiNotes, [69]);
  for (const id of chord.children) assert.match(id, /:a4=432$/);
  finiteJson(chord);
});

test('chords enforce nonempty dense bounded arrays before deduplication', () => {
  for (const input of [[], null, {}, '60,64,67', new Set([60]), Array(129).fill(60)]) assert.throws(() => chordNode(input), RangeError);
  assert.equal(chordNode(Array.from({ length: 128 }, (_, i) => i)).properties.midiNotes.length, 128);
  assert.deepEqual(chordNode(Array(128).fill(60)).properties.midiNotes, [60]);
});


test('chords use bounded own indexed values rather than caller iterators or inherited entries', () => {
  const notes = [60];
  notes[Symbol.iterator] = function* () { throw new Error('Custom iterator must not run'); };
  assert.deepEqual(chordNode(notes).properties.midiNotes, [60]);
  const inherited = Array(1);
  Object.setPrototypeOf(inherited, { 0: 60 });
  assert.throws(() => chordNode(inherited), RangeError);
});

test('negative-zero MIDI values are canonicalized for exact JSON roundtrips', () => {
  assert.deepEqual(midiNoteNode(-0), midiNoteNode(0));
  assert.deepEqual(chordNode([-0]), chordNode([0]));
  finiteJson(midiNoteNode(-0));
});
