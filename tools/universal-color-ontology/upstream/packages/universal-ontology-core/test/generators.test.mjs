import test from 'node:test';
import assert from 'node:assert/strict';
import {
  integerNode, rationalNode, complexNode, regularPolygonNode,
  srgba8Node, midiNoteNode, chordNode,
  unorderedSelfInclusivePairs, orderedPairs
} from '../src/generators.mjs';

test('integer generator is stable', () => {
  assert.equal(integerNode(7).id, 'urn:universe:mathematics:integer:7');
  assert.equal(integerNode(7).properties.parity, 'odd');
});

test('rational generator canonicalizes sign and gcd', () => {
  assert.equal(rationalNode(6, -8).id, 'urn:universe:mathematics:rational:-3/4');
});

test('complex generator records coordinates', () => {
  const n = complexNode(3, -4);
  assert.equal(n.properties.real, 3);
  assert.equal(n.properties.imaginary, -4);
});

test('regular polygon generator derives angle', () => {
  assert.equal(regularPolygonNode(3).properties.interiorAngleDegrees, 60);
  assert.equal(regularPolygonNode(4).properties.interiorAngleDegrees, 90);
});

test('sRGBA generator addresses all 8-bit tuples procedurally', () => {
  assert.equal(srgba8Node(1,2,3,4).id, 'urn:universe:color:srgba8:1,2,3,4');
});

test('MIDI A4 at 440 Hz is exact by definition of this tuning context', () => {
  assert.equal(midiNoteNode(69, 440).properties.frequencyHz, 440);
});

test('chord generator canonicalizes note ordering and duplicates', () => {
  const chord = chordNode([67,60,64,60]);
  assert.deepEqual(chord.properties.midiNotes, [60,64,67]);
});

test('self-inclusive pair generator includes N(N+1)/2 pairs', () => {
  const values = [1,2,3,4];
  const pairs = [...unorderedSelfInclusivePairs(values)];
  assert.equal(pairs.length, 10);
  assert.deepEqual(pairs[0], [1,1]);
  assert.deepEqual(pairs.at(-1), [4,4]);
});

test('ordered pair generator includes N^2 pairs', () => {
  const values = ['a','b','c'];
  assert.equal([...orderedPairs(values)].length, 9);
});
