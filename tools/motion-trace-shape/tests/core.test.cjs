const test = require('node:test');
const assert = require('node:assert/strict');
const M = require('../src/core.js');
const close = (a, b, tolerance = 1e-12) => assert.ok(Math.abs(a - b) <= tolerance, `${a} != ${b}`);
const view = { time: 2, playbackSpeed: 1, showGuide: true, stillMode: true };

test('line has equal coordinates at reference times', () => {
  for (const [t, value] of [[0,0],[2,1],[4,0],[6,-1],[8,0]]) {
    const s = M.stateAt(M.PRESETS.line, t); close(s.x, value); close(s.y, value);
  }
});
test('quarter-cycle offset gives unit circle at all samples', () => {
  for (const s of M.sample(M.PRESETS.circle)) close(s.x*s.x + s.y*s.y, 1);
});
test('circle cardinal positions have positive y upwards', () => {
  const expected = [[0,0,1],[2,1,0],[4,0,-1],[6,-1,0],[8,0,1]];
  for (const [t,x,y] of expected) { const s=M.stateAt(M.PRESETS.circle,t); close(s.x,x);close(s.y,y); }
});
test('figure-eight has correct distinct lobes and crossings', () => {
  const p = M.PRESETS.eight;
  close(M.stateAt(p,1).y,1); close(M.stateAt(p,3).y,-1);
  close(M.stateAt(p,4).x,0); close(M.stateAt(p,4).y,0);
  close(M.stateAt(p,5).y,1); close(M.stateAt(p,7).y,-1);
  assert.ok(M.stateAt(p,1).x>0 && M.stateAt(p,5).x<0);
});
test('481 uniformly spaced samples include both endpoints', () => {
  const list=M.sample(M.PRESETS.circle); assert.equal(list.length,481);
  assert.equal(list[0].t,0); assert.equal(list.at(-1).t,8);
  for(let i=1;i<list.length;i++) close(list[i].t-list[i-1].t,1/60);
});
test('all allowed parameter combinations are finite, bounded and closed', () => {
  for(let x=1;x<=4;x++) for(let y=1;y<=4;y++) for(let phase=0;phase<=360;phase+=15) {
    const p={xCycles:x,yCycles:y,phase}; const list=M.sample(p);
    for(const s of list) { assert.ok(Number.isFinite(s.x)&&Number.isFinite(s.y));assert.ok(Math.abs(s.x)<=1&&Math.abs(s.y)<=1); }
    close(list[0].x,list.at(-1).x); close(list[0].y,list.at(-1).y);
  }
});
test('changing phase preserves the horizontal trace', () => {
  const a=M.sample(M.PRESETS.line), b=M.sample({...M.PRESETS.line,phase:165});
  assert.deepEqual(a.map(s=>s.x),b.map(s=>s.x));
});
test('full phase turn is equivalent to zero within floating-point tolerance', () => {
  const a=M.sample(M.PRESETS.line),b=M.sample({...M.PRESETS.line,phase:360});
  a.forEach((s,i)=>close(s.y,b[i].y));
});
test('samples are freshly allocated and do not mutate parameters', () => {
  const p={...M.PRESETS.line};const a=M.sample(p);a[0].x=123;
  assert.equal(M.sample(p)[0].x,0);assert.deepEqual(p,M.PRESETS.line);
});
test('history contains fixed samples only, with correct edge behavior', () => {
  const list=M.sample(M.PRESETS.circle);
  assert.equal(M.historyUntil(list,0).length,1);assert.equal(M.historyUntil(list,0.125).length,8);
  assert.equal(M.historyUntil(list,8).length,481);assert.equal(list.length,481);
  const h=M.historyUntil(list,2);assert.equal(h.at(-1).t,2);assert.equal(h.length,121);
});
test('replay is independent of scrubbing order', () => {
  const list=M.sample(M.PRESETS.eight), a=M.historyUntil(list,2);
  M.historyUntil(list,7);M.historyUntil(list,0);assert.deepEqual(M.historyUntil(list,2),a);
});
test('playback speed controls time only and clamps at end', () => {
  assert.equal(M.advance(1,2,.5),2);assert.equal(M.advance(1,2,1),3);
  assert.equal(M.advance(1,2,2),5);assert.equal(M.advance(7,100,2),8);
});
test('elapsed time composes regardless of frame subdivision', () => {
  for(const speed of [.5,1,2]) { let t=0;for(let i=0;i<120;i++)t=M.advance(t,1/60,speed);close(t,M.advance(0,2,speed)); }
});
test('export is deterministic and faithfully includes analytical samples', () => {
  const a=M.record(M.PRESETS.eight,view),b=M.record(M.PRESETS.eight,view);
  assert.deepEqual(a,b);assert.equal(a.model.samples.length,481);
  assert.deepEqual(a.model.samples,M.sample(M.PRESETS.eight));
  assert.equal(a.model.sampling.sample_count,a.model.samples.length);
  assert.deepEqual(JSON.parse(JSON.stringify(a)),a);
});
test('changing all presentation controls leaves model export identical', () => {
  const a=M.record(M.PRESETS.line,view);
  const b=M.record(M.PRESETS.line,{time:7,playbackSpeed:2,showGuide:false,stillMode:false});
  assert.deepEqual(a.model,b.model);assert.notDeepEqual(a.presentation,b.presentation);
});
test('rejects malformed and out-of-range model parameters', () => {
  for(const p of [null,{}, {xCycles:0,yCycles:1,phase:0},{xCycles:5,yCycles:1,phase:0},{xCycles:1.5,yCycles:1,phase:0},{xCycles:'1',yCycles:1,phase:0},{xCycles:1,yCycles:NaN,phase:0},{xCycles:1,yCycles:1,phase:16},{xCycles:1,yCycles:1,phase:Infinity},{xCycles:1,yCycles:1,phase:-15},{xCycles:1,yCycles:1,phase:375}]) assert.throws(()=>M.sample(p));
});
test('rejects invalid time and playback values', () => {
  for(const t of [-1,8.1,NaN,Infinity,'1']) {assert.throws(()=>M.stateAt(M.PRESETS.line,t));assert.throws(()=>M.historyUntil([],t));assert.throws(()=>M.advance(t,1,1));}
  for(const n of [-1,NaN,Infinity])assert.throws(()=>M.advance(0,n,1));
  for(const n of [0,3,NaN,'1'])assert.throws(()=>M.advance(0,1,n));
});
test('export rejects invalid presentation and excludes unknown data', () => {
  for(const v of [null,{}, {...view,showGuide:1},{...view,stillMode:'yes'},{...view,playbackSpeed:4}]) assert.throws(()=>M.record(M.PRESETS.line,v));
  const r=M.record({...M.PRESETS.line,private:'not copied'},{...view,private:'not copied'});
  assert.ok(!JSON.stringify(r).includes('not copied'));
});
