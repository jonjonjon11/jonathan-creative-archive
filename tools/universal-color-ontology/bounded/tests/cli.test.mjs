import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const cli = fileURLToPath(new URL('../cli.mjs', import.meta.url));
const run = (...args) => spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8', timeout: 5000 });
const read = (...args) => {
  const result = run(...args);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, '');
  return JSON.parse(result.stdout);
};

test('CLI emits exact integer and canonical rational JSON', () => {
  assert.equal(read('integer', '9007199254740993').properties.value, '9007199254740993');
  assert.deepEqual(read('rational', '6', '-8').properties, { numerator: '-3', denominator: '4' });
});

test('CLI note and chord output retain optional tuning and canonical notes', () => {
  assert.equal(read('midi', '69').properties.frequencyHz, 440);
  assert.equal(read('midi', '69', '4.32e2').properties.frequencyHz, 432);
  const chord = read('chord', '67,60,64,60', '432');
  assert.deepEqual(chord.properties.midiNotes, [60, 64, 67]);
  assert.equal(chord.properties.tuningReferenceHz, 432);
});

test('CLI reports invalid commands and values with nonzero exit and no partial JSON', () => {
  for (const args of [[], ['bad'], ['integer'], ['integer', '1', '2'], ['integer', '1e3'], ['rational', '1', '0'],
    ['midi', '69', '-440'], ['midi', '69.0'], ['midi', '128'], ['midi', '69', '0x10'], ['midi', '69', 'Infinity'],
    ['midi', '69', '1e309'], ['midi', '0', '5e-324'], ['midi', '127', '1.7976931348623157e308'],
    ['chord', ''], ['chord', '60,'], ['chord', '60,,64'], ['chord', '60, 64'], ['--help', 'extra']]) {
    const result = run(...args);
    assert.equal(result.status, 1, JSON.stringify(args));
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /^Error: /);
    assert.ok(result.stderr.length < 300);
  }
});

test('CLI bounds integers, chord text and numeric text without echoing the payload', () => {
  for (const args of [['integer', '9'.repeat(1025)], ['chord', Array(129).fill('127').join(',')], ['chord', Array(129).fill('0').join(',')], ['midi', '69', '1'.repeat(65)]]) {
    const result = run(...args);
    assert.equal(result.status, 1);
    assert.equal(result.stdout, '');
    assert.ok(result.stderr.length < 300);
  }
  assert.equal(read('integer', '9'.repeat(1024)).properties.value.length, 1024);
  assert.equal(read('chord', Array.from({ length: 128 }, (_, i) => i).join(',')).properties.midiNotes.length, 128);
});

test('CLI help explains offline use and limits without attempting generation', () => {
  const result = run('--help');
  assert.equal(result.status, 0);
  assert.equal(result.stderr, '');
  assert.match(result.stdout, /Offline JSON/);
  assert.match(result.stdout, /not a claim/);
});
