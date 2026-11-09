// Original archive validation adapter, CC BY 4.0; preserved imports remain CC0.
// No general re-export: only these four bounded generator entry points are covered.
import {
  integerNode as upstreamInteger,
  rationalNode as upstreamRational,
  midiNoteNode as upstreamNote,
  chordNode as upstreamChord,
} from '../upstream/packages/universal-ontology-core/src/generators.mjs';

export const MAX_INTEGER_DIGITS = 1024;
export const MAX_CHORD_INPUTS = 128;

function exactInteger(value, name) {
  if (typeof value === 'number') {
    if (!Number.isSafeInteger(value)) {
      throw new RangeError(`${name} must be a safe integer Number; use a decimal string or bigint for larger values`);
    }
    return BigInt(value);
  }
  if (typeof value !== 'bigint' && typeof value !== 'string') {
    throw new TypeError(`${name} must be a safe integer Number, bigint or decimal integer string`);
  }
  const text = typeof value === 'bigint' ? value.toString() : value;
  const sign = text[0] === '+' || text[0] === '-' ? 1 : 0;
  if (text.length - sign > MAX_INTEGER_DIGITS) {
    throw new RangeError(`${name} is limited to ${MAX_INTEGER_DIGITS} decimal digits, including leading zeros`);
  }
  if (!/^[+-]?[0-9]+$/.test(text)) {
    throw new TypeError(`${name} must contain only an optional sign and decimal digits`);
  }
  return BigInt(text);
}

function midiValue(note) {
  if (typeof note !== 'number' || !Number.isInteger(note) || note < 0 || note > 127) {
    throw new RangeError('MIDI note must be an integer Number from 0 through 127');
  }
  return note === 0 ? 0 : note;
}

function tuningValue(a4Hz) {
  if (typeof a4Hz !== 'number' || !Number.isFinite(a4Hz) || a4Hz <= 0) {
    throw new RangeError('A4 reference must be a positive finite Number in Hz');
  }
  return a4Hz;
}

function checkedFrequency(frequencyHz) {
  if (!Number.isFinite(frequencyHz) || frequencyHz <= 0) {
    throw new RangeError('Computed frequency must be positive and finite; this note and tuning overflow or underflow Number');
  }
}

export function integerNode(value) {
  return upstreamInteger(exactInteger(value, 'value'));
}

export function rationalNode(numerator, denominator) {
  return upstreamRational(exactInteger(numerator, 'numerator'), exactInteger(denominator, 'denominator'));
}

export function midiNoteNode(note, a4Hz = 440) {
  const result = upstreamNote(midiValue(note), tuningValue(a4Hz));
  checkedFrequency(result.properties.frequencyHz);
  return result;
}

export function chordNode(midiNotes, a4Hz = 440) {
  if (!Array.isArray(midiNotes)) {
    throw new RangeError('midiNotes must be an array');
  }
  const count = midiNotes.length;
  if (!Number.isInteger(count) || count === 0 || count > MAX_CHORD_INPUTS || count < 0) {
    throw new RangeError(`midiNotes must be an array of 1 through ${MAX_CHORD_INPUTS} notes before deduplication`);
  }
  // Bound indexed reads, ignore custom iterators, and reject missing entries.
  const notes = [];
  for (let i = 0; i < count; i++) {
    if (!Object.hasOwn(midiNotes, i)) throw new RangeError('midiNotes must not contain sparse entries');
    notes.push(midiValue(midiNotes[i]));
  }
  const result = upstreamChord(notes, tuningValue(a4Hz));
  for (const frequency of result.properties.frequenciesHz) checkedFrequency(frequency);
  return result;
}
