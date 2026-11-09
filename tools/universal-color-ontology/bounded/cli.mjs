#!/usr/bin/env node
// Original archive CLI, CC BY 4.0. Writes one JSON record or a bounded error.
import { integerNode, rationalNode, midiNoteNode, chordNode, MAX_CHORD_INPUTS } from './generators.mjs';

const USAGE = `Usage (Node.js 20+):
  node cli.mjs integer DECIMAL_INTEGER
  node cli.mjs rational NUMERATOR DENOMINATOR
  node cli.mjs midi NOTE [A4_HZ]
  node cli.mjs chord NOTE,NOTE,... [A4_HZ]
  node cli.mjs --help

Offline JSON output only. No audio, files, network or saved state.
Integer strings: at most 1024 digits each. Chords: at most 128 input notes.
NOTE: integer 0..127. A4_HZ: positive finite decimal/scientific notation.
Frequencies must remain positive and finite. These are mathematical data,
not a claim that a frequency is audible, playable or safe to render.\n`;

function decimalNumber(text, label) {
  if (text.length > 64 || !/^[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$/.test(text)) {
    throw new TypeError(`${label} must be a decimal number (up to 64 characters)`);
  }
  return Number(text);
}

function noteNumber(text) {
  if (text.length > 3 || !/^[0-9]+$/.test(text)) throw new TypeError('NOTE must be 0..127 written as decimal digits');
  return Number(text);
}

function generate(args) {
  const [command, ...values] = args;
  if (command === 'integer' && values.length === 1) return integerNode(values[0]);
  if (command === 'rational' && values.length === 2) return rationalNode(...values);
  if ((command === 'midi' || command === 'chord') && (values.length === 1 || values.length === 2)) {
    const tuning = values.length === 2 ? decimalNumber(values[1], 'A4_HZ') : 440;
    if (command === 'midi') return midiNoteNode(noteNumber(values[0]), tuning);
    if (values[0].length > MAX_CHORD_INPUTS * 4 - 1) throw new RangeError('Chord input exceeds the 128-note text bound');
    return chordNode(values[0].split(',').map(noteNumber), tuning);
  }
  throw new TypeError('Unknown command or wrong argument count; run with --help');
}

const args = process.argv.slice(2);
if (args.length === 1 && args[0] === '--help') {
  process.stdout.write(USAGE);
} else {
  try {
    process.stdout.write(`${JSON.stringify(generate(args), null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`Error: ${error.message}\n`);
    process.exitCode = 1;
  }
}
