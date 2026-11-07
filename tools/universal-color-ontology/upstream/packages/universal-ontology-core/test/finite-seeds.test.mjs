import test from 'node:test';
import assert from 'node:assert/strict';
import {
  ELEMENTS,
  FUNDAMENTAL_PARTICLES,
  SI_BASE,
  SI_DERIVED,
  GEOMETRY_CONCEPTS,
  MATHEMATICS_CONCEPTS,
  MUSIC_CONCEPTS,
  COLOR_CONCEPTS,
  VISUAL_CHANNELS,
  RELATION_TYPES,
  EPISTEMIC_STATUSES,
  buildCoreFiniteNodes,
  CORE_COUNTS
} from '../src/finite-seeds.mjs';

test('periodic table seed has 118 elements in atomic-number order', () => {
  assert.equal(ELEMENTS.length, 118);
  assert.deepEqual(ELEMENTS[0], ['H','Hydrogen']);
  assert.deepEqual(ELEMENTS.at(-1), ['Og','Oganesson']);
});

test('bounded seed family counts remain intentional', () => {
  assert.equal(FUNDAMENTAL_PARTICLES.length, 30);
  assert.equal(SI_BASE.length, 7);
  assert.equal(SI_DERIVED.length, 19);
  assert.equal(GEOMETRY_CONCEPTS.length, 52);
  assert.equal(MATHEMATICS_CONCEPTS.length, 105);
  assert.equal(MUSIC_CONCEPTS.length, 71);
  assert.equal(COLOR_CONCEPTS.length, 61);
  assert.equal(VISUAL_CHANNELS.length, 38);
  assert.equal(RELATION_TYPES.length, 52);
  assert.equal(EPISTEMIC_STATUSES.length, 14);
});

test('core finite registry builds 593 unique node IDs', () => {
  const nodes = buildCoreFiniteNodes();
  assert.equal(nodes.length, 593);
  assert.equal(new Set(nodes.map(n => n.id)).size, 593);
});

test('element nodes carry atomic number and evaluated-data status', () => {
  const nodes = buildCoreFiniteNodes();
  const iron = nodes.find(n => n.id === 'urn:universe:chemistry:element:Fe');
  assert.equal(iron.properties.atomicNumber, 26);
  assert.equal(iron.epistemicStatus, 'EVALUATED_DATA');
});

test('CORE_COUNTS mirrors the source vocabularies', () => {
  assert.equal(CORE_COUNTS.elements, ELEMENTS.length);
  assert.equal(CORE_COUNTS.musicConcepts, MUSIC_CONCEPTS.length);
  assert.equal(CORE_COUNTS.relationTypes, RELATION_TYPES.length);
});
