/* Motion → Trace → Shape 0.1.0. Original code, CC BY 4.0; see README.md. */
(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MotionModel = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = '0.1.0';
  const DURATION = 8;
  const INTERVALS = 480;
  const STEP = DURATION / INTERVALS;
  const PRESETS = Object.freeze({
    line: Object.freeze({ xCycles: 1, yCycles: 1, phase: 0 }),
    circle: Object.freeze({ xCycles: 1, yCycles: 1, phase: 90 }),
    eight: Object.freeze({ xCycles: 1, yCycles: 2, phase: 0 })
  });
  function validate(params) {
    if (!params || typeof params !== 'object') throw new TypeError('Parameters must be an object.');
    for (const key of ['xCycles', 'yCycles']) {
      if (!Number.isInteger(params[key]) || params[key] < 1 || params[key] > 4) {
        throw new RangeError(key + ' must be an integer from 1 to 4.');
      }
    }
    if (!Number.isFinite(params.phase) || params.phase < 0 || params.phase > 360 || params.phase % 15 !== 0) {
      throw new RangeError('Phase must be a multiple of 15 degrees from 0 to 360.');
    }
    return { xCycles: params.xCycles, yCycles: params.yCycles, phase: params.phase };
  }
  function stateAt(params, t) {
    const p = validate(params);
    if (!Number.isFinite(t) || t < 0 || t > DURATION) throw new RangeError('Time must be from 0 to 8 seconds.');
    return {
      t,
      x: Math.sin(2 * Math.PI * p.xCycles * t / DURATION),
      y: Math.sin(2 * Math.PI * p.yCycles * t / DURATION + p.phase * Math.PI / 180)
    };
  }
  function sample(params) {
    const p = validate(params);
    return Array.from({ length: INTERVALS + 1 }, (_, i) => stateAt(p, i * STEP));
  }
  function historyUntil(samples, time) {
    if (!Number.isFinite(time) || time < 0 || time > DURATION) throw new RangeError('Time must be from 0 to 8 seconds.');
    // Fixed samples only. The live cursor is analytical and may fall between them.
    return samples.slice(0, Math.floor(time / STEP + 1e-10) + 1);
  }
  function advance(time, elapsedSeconds, playbackSpeed) {
    if (!Number.isFinite(time) || time < 0 || time > DURATION) throw new RangeError('Invalid time.');
    if (!Number.isFinite(elapsedSeconds) || elapsedSeconds < 0) throw new RangeError('Invalid elapsed time.');
    if (![0.5, 1, 2].includes(playbackSpeed)) throw new RangeError('Invalid playback speed.');
    return Math.min(DURATION, time + elapsedSeconds * playbackSpeed);
  }
  function record(params, presentation) {
    const p = validate(params);
    if (!presentation || typeof presentation !== 'object') throw new TypeError('Presentation is required.');
    const t = presentation.time;
    stateAt(p, t);
    advance(t, 0, presentation.playbackSpeed);
    if (typeof presentation.showGuide !== 'boolean' || typeof presentation.stillMode !== 'boolean') throw new TypeError('Display switches must be boolean.');
    return {
      format: 'motion-trace-shape-experiment', schema_version: 1, model_version: VERSION,
      model: {
        method: 'Analytical sine functions; no numerical integration or measured data.',
        equations: ['x(t) = sin(2*pi*x_cycles*t/8)', 'y(t) = sin(2*pi*y_cycles*t/8 + phase_degrees*pi/180)'],
        parameters: { x_cycles: p.xCycles, y_cycles: p.yCycles, phase_degrees: p.phase, duration_seconds: DURATION, amplitude_model_units: 1 },
        units: { t: 'model seconds', x: 'model units', y: 'model units' },
        initial_state: stateAt(p, 0),
        sampling: { interval_seconds: STEP, intervals: INTERVALS, sample_count: INTERVALS + 1, endpoints_included: true },
        samples: sample(p)
      },
      presentation: { time: t, playback_speed: presentation.playbackSpeed, show_complete_guide: presentation.showGuide, still_mode: presentation.stillMode, positive_y: 'up', plot_aspect_ratio: 'equal units on both axes', trace: 'fixed samples joined by straight segments; analytical live cursor' }
    };
  }
  return Object.freeze({ VERSION, DURATION, INTERVALS, STEP, PRESETS, validate, stateAt, sample, historyUntil, advance, record });
}));
