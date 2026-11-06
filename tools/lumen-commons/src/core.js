/* Lumen Commons: deterministic, renderer-independent simulation. Original CC0 code. */
(function (root) {
  'use strict';
  const VERSION = 1;
  const QUESTS = ['fractions', 'trajectory', 'harmony', 'orbit', 'coordinates'];
  const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));
  function finite(n, name) { if (!Number.isFinite(n)) throw new TypeError(name + ' must be finite'); return n; }
  function fractionOf(n, d, total) {
    [n,d,total].forEach(v => finite(v, 'fraction input'));
    if (d <= 0 || total < 0 || n < 0) throw new RangeError('Use nonnegative values and a positive denominator');
    return n * total / d;
  }
  function trajectory(speed, angle, gravity = 9.81) {
    [speed,angle,gravity].forEach(v => finite(v, 'trajectory input'));
    if (speed < 0 || angle < 0 || angle > 90 || gravity <= 0) throw new RangeError('Invalid trajectory');
    const a = angle * Math.PI / 180, vx = speed * Math.cos(a), vy = speed * Math.sin(a);
    return {range: speed * speed * Math.sin(2*a) / gravity, time: 2*vy/gravity, height: vy*vy/(2*gravity), vx, vy};
  }
  function orbitalPeriod(a) { finite(a, 'semimajor axis'); if (a <= 0) throw new RangeError('Positive AU required'); return Math.pow(a, 1.5); }
  function frequency(base, semitones) { finite(base, 'base'); finite(semitones, 'semitones'); if (base <= 0 || Math.abs(semitones) > 120) throw new RangeError('Invalid frequency'); return base * Math.pow(2, semitones/12); }
  function fresh() { return {version:VERSION, complete:[], motes:[], lang:'en', quality:'balanced', skin:2, reduced:false, art:[]}; }
  function sanitize(input) {
    const s = fresh();
    if (!input || typeof input !== 'object' || input.version !== VERSION) return s;
    s.complete = [...new Set(Array.isArray(input.complete) ? input.complete.filter(v => QUESTS.includes(v)) : [])];
    s.motes = [...new Set(Array.isArray(input.motes) ? input.motes.filter(v => Number.isInteger(v) && v >= 0 && v < 12) : [])];
    if (['en','es','ja'].includes(input.lang)) s.lang = input.lang;
    if (['low','balanced','high'].includes(input.quality)) s.quality = input.quality;
    if (Number.isInteger(input.skin)) s.skin = clamp(input.skin,0,5);
    s.reduced = input.reduced === true;
    s.art = Array.isArray(input.art) ? input.art.slice(-100).filter(p => p && [p.x,p.y,p.hue].every(Number.isFinite)).map(p => ({x:clamp(p.x,0,1),y:clamp(p.y,0,1),hue:clamp(p.hue,0,360)})) : [];
    return s;
  }
  function complete(state, id) { if (!QUESTS.includes(id)) throw new RangeError('Unknown quest'); if (state.complete.includes(id)) return false; state.complete.push(id); return true; }
  function inside(x,y) { return Number.isFinite(x) && Number.isFinite(y) && ((x-800)/680)**2 + ((y-560)/395)**2 < 1; }
  // Fixed-step movement: wall sliding, normalized diagonal input, no tab-resume leaps.
  function move(p, dx, dy, dt, speed, blocked = () => false) {
    [p.x,p.y,dx,dy,dt,speed].forEach(v => finite(v, 'movement'));
    const length = Math.hypot(dx,dy), d = Math.min(Math.max(dt,0),0.05)*clamp(speed,0,360);
    if (!length) return {...p};
    const x = p.x + dx/length*d, y = p.y + dy/length*d;
    const out = {...p};
    if (inside(x,p.y) && !blocked(x,p.y)) out.x = x;
    if (inside(out.x,y) && !blocked(out.x,y)) out.y = y;
    return out;
  }
  const api = Object.freeze({VERSION,QUESTS,clamp,fractionOf,trajectory,orbitalPeriod,frequency,fresh,sanitize,complete,inside,move});
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.LumenCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
