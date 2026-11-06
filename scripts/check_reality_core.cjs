#!/usr/bin/env node
'use strict';
// Focused tests of the unchanged HTML's calculation layer. No browser/GPU/UI is exercised.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const artifact = path.join(__dirname, '../tools/reality-atlas/Reality_Atlas_Appearance_0.3.1.html');
const bytes = fs.readFileSync(artifact);
const hash = crypto.createHash('sha256').update(bytes).digest('hex');
assert.equal(hash, 'fdb0f246ddcf45e3b6b90fae356c95dfce86cfab122fab33a1143659f87bce0d', 'Artifact must match reviewed original');
const html = bytes.toString('utf8');
const inline = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(inline); // Syntax check the full script without invoking browser code.
const end = inline.indexOf('const AVERT =');
assert.ok(end > 0, 'Expected original module boundary');
const coreSource = inline.slice(0, end).replace(/^\(\(\)=>\{/, '') + '\nglobalThis.core = {APRESETS,axisQuaternion,rotateVector,validateMotion,motionPoint,motionSpeed,speedUpperBound,sampleHistory,occupancy,phaseRGB,makePacking,isValidPacking,packingFraction,analyzeVoid};';
const context = vm.createContext({}); // No process, filesystem, network, DOM or browser objects are supplied to the original core.
new vm.Script(coreSource).runInContext(context, {timeout:5000});
const c = context.core;
const results = [];
function check(name, fn) { fn(); results.push({name, result:'pass'}); }
const close = (a,b,eps=1e-8) => assert.ok(Math.abs(a-b)<=eps, `${a} differs from ${b}`);
check('original bytes and complete inline-script syntax', ()=>assert.equal(bytes.length,57046));
check('quarter-turn rotation', ()=>{const v=c.rotateVector(c.axisQuaternion([0,0,1],Math.PI/2),[1,0,0]);close(v[0],0);close(v[1],1);close(v[2],0);});
check('zero rotation axis rejected', ()=>assert.throws(()=>c.axisQuaternion([0,0,0],1),/nonzero/));
for (const [name,s] of Object.entries(c.APRESETS)) {
 check(`${name}: accepted finite parameters`, ()=>c.validateMotion(s));
 check(`${name}: finite sampled positions`, ()=>{for(const t of [0,.125,.5,1,7.9])assert.ok(c.motionPoint(s,t).every(Number.isFinite));});
 check(`${name}: numerical speed within declared upper bound`, ()=>{for(const t of [0,.125,.5,1])assert.ok(c.motionSpeed(s,t)<=c.speedUpperBound(s)*1.00001);});
 check(`${name}: history budget and equal-time mass`, ()=>{const h=c.sampleHistory(s,1,1,512);assert.ok(h.samples.length<=512);close(h.samples.reduce((a,x)=>a+x.weight,0),1);});
 check(`${name}: occupancy conserves sample weight`, ()=>{const h=c.sampleHistory(s,1,1,512);const cells=c.occupancy(h.samples,24,1.8);close(cells.reduce((a,x)=>a+x.mass,0),1);});
}
check('circle closes after one cycle', ()=>{const a=c.motionPoint(c.APRESETS.Circle,0),b=c.motionPoint(c.APRESETS.Circle,1);a.forEach((v,i)=>close(v,b[i]));});
check('zero exposure yields one snapshot', ()=>assert.equal(c.sampleHistory(c.APRESETS.Circle,1,0).samples.length,1));
check('negative exposure rejected', ()=>assert.throws(()=>c.sampleHistory(c.APRESETS.Circle,1,-1),/exposure/));
check('nonfinite parameter rejected', ()=>assert.throws(()=>c.validateMotion({...c.APRESETS.Circle,radius:NaN}),/finite/));
check('phase color repeats after one cycle', ()=>{const a=c.phaseRGB(.25),b=c.phaseRGB(1.25);a.forEach((v,i)=>close(v,b[i]));});
for (const family of ['Equal','Unequal','Fibonacci','Tetrahedral throat']) {
 for (const kind of ['box','sphere']) {
  check(`${family}/${kind}: bounded nonoverlapping placement`, ()=>{const p=c.makePacking(family,16,17,kind);assert.ok(c.isValidPacking(p));assert.ok(p.balls.length<=p.requested);assert.ok(c.packingFraction(p)>0 && c.packingFraction(p)<1);});
 }
 check(`${family}: seeded placement reproducible`, ()=>assert.equal(JSON.stringify(c.makePacking(family,16,17)),JSON.stringify(c.makePacking(family,16,17))));
 check(`${family}: larger probe cannot increase accessible voxel count`, ()=>{const p=c.makePacking(family,16,17);const a=c.analyzeVoid(p,17,0),b=c.analyzeVoid(p,17,.08);assert.ok(b.cells.length<=a.cells.length);assert.equal(a.componentCounts.reduce((x,y)=>x+y,0),a.cells.length);assert.ok(a.accessibleFraction>=0 && a.accessibleFraction<=1);});
}
check('invalid requested sphere count rejected', ()=>assert.throws(()=>c.makePacking('Equal',65),/count/));
check('invalid probe rejected', ()=>assert.throws(()=>c.analyzeVoid(c.makePacking('Equal',4),17,-1),/probe/));
const report={test_suite:'archive-reality-core-smoke/1',artifact_sha256:hash,runtime:process.version,passed:results.length,failed:0,scope:'Exact-original calculation layer plus full-script syntax only. No browser, WebGL, UI, download, SVG-export, accessibility, mobile, or headset acceptance.',checks:results};
console.log(JSON.stringify(report,null,2));
