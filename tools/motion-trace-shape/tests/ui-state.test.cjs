/* Minimal DOM/RAF stand-ins exercise the real application control logic.
 * These tests do NOT test a browser, rendering, native input behavior or accessibility. */
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const root=path.join(__dirname,'..');
function setup(reduced=false) {
  const elements={},raf=new Map(), downloads=[],mediaEvents={};let serial=0;
  const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
  const element=()=>({ value:'', checked:false, disabled:false, textContent:'', attrs:{}, listeners:{}, setAttribute(k,v){this.attrs[k]=v;}, addEventListener(k,f){this.listeners[k]=f;}, click(){if(this.href)downloads.push(this);else if(!this.disabled)this.listeners.click?.();}, remove(){} });
  for(const match of html.matchAll(/<[^>]+\bid="([^"]+)"[^>]*>/g)) {
    const e=element();e.value=/\bvalue="([^"]*)"/.exec(match[0])?.[1]||'';e.checked=/\bchecked\b/.test(match[0]);elements[match[1]]=e;
  }
  elements.speed.value='1';
  const document={hidden:false,events:{},getElementById:id=>{if(!elements[id])throw Error(id);return elements[id];},addEventListener(k,f){this.events[k]=f;},createElement:()=>element(),body:{appendChild(){}}};
  const media={matches:reduced,addEventListener(k,f){mediaEvents[k]=f;}};
  const blobs=[];
  const context=vm.createContext({ document, Blob, URL:{createObjectURL(blob){blobs.push(blob);return 'blob:test';},revokeObjectURL(){}}, window:{matchMedia:()=>media,requestAnimationFrame(fn){raf.set(++serial,fn);return serial;},cancelAnimationFrame(id){raf.delete(id);},setTimeout(){}}, console });
  vm.runInContext(fs.readFileSync(path.join(root,'src/core.js'),'utf8'),context);context.window.MotionModel=context.MotionModel;
  vm.runInContext(fs.readFileSync(path.join(root,'src/app.js'),'utf8'),context);
  return {e:elements,document,raf,blobs,downloads,context,emit(id,event,value){if(value!==undefined)elements[id].value=String(value);elements[id].listeners[event]?.();},frame(now){const pending=[...raf.values()];raf.clear();pending.forEach(f=>f(now));},reduced(value){media.matches=value;mediaEvents.change({matches:value});},time(){return Number(elements.time.value);}};
}
test('starts still with one fixed sample and three rendered SVG paths',()=>{const s=setup();assert.equal(s.raf.size,0);assert.equal(s.time(),0);assert.equal(s.e.shapeName.textContent,'Circle');assert.ok(s.e.shapeGuide.attrs.d.startsWith('M'));assert.equal(s.e.shapeTrace.attrs.d.split('L').length,1);});
test('reduced-motion preference enables still mode and disables play',()=>{const s=setup(true);assert.equal(s.e.still.checked,true);assert.equal(s.e.play.disabled,true);s.e.play.click();assert.equal(s.raf.size,0);s.e.step.click();assert.equal(s.time(),.125);});
test('play, pause and repeated play do not create duplicate frame loops',()=>{const s=setup();s.e.play.click();s.frame(100);s.frame(1100);assert.equal(s.time(),1);s.e.play.click();assert.equal(s.raf.size,0);s.e.play.click();assert.equal(s.raf.size,1);s.e.play.click();assert.equal(s.raf.size,0);});
test('restart clears visited history but preserves model and guide',()=>{const s=setup();s.emit('time','input',4);const guide=s.e.shapeGuide.attrs.d;s.e.restart.click();assert.equal(s.time(),0);assert.equal(s.e.shapeGuide.attrs.d,guide);assert.equal(s.e.shapeTrace.attrs.d.split('L').length,1);});
test('preset changes pause and reset while updating repeat counts',()=>{const s=setup();s.e.play.click();s.e['preset-eight'].click();assert.equal(s.raf.size,0);assert.equal(s.time(),0);assert.equal(Number(s.e.yCycles.value),2);assert.equal(s.e.shapeName.textContent,'Figure-eight');assert.equal(s.e['preset-eight'].attrs['aria-pressed'],'true');});
test('parameter edits preserve validation and reset history',()=>{const s=setup();s.emit('time','input',5);s.emit('xCycles','input',3);assert.equal(s.time(),0);assert.equal(Number(s.e.xValue.textContent),3);assert.equal(s.e['preset-circle'].attrs['aria-pressed'],'false');});
test('scrubbing is reversible and pauses playback',()=>{const s=setup();s.emit('time','input',2);const d=s.e.shapeTrace.attrs.d;s.emit('time','input',7);s.e.play.click();s.emit('time','input',2);assert.equal(s.raf.size,0);assert.equal(s.e.shapeTrace.attrs.d,d);});
test('guide toggle leaves trajectory and selected time unchanged',()=>{const s=setup();s.emit('time','input',3);const d=s.e.shapeTrace.attrs.d;s.e.guide.checked=false;s.emit('guide','change');assert.equal(s.time(),3);assert.equal(s.e.shapeTrace.attrs.d,d);assert.equal(s.e.shapeGuide.attrs.visibility,'hidden');});
test('speed changes leave history unchanged and affect only subsequent display time',()=>{const s=setup();s.e.play.click();s.frame(0);s.frame(1000);const d=s.e.shapeTrace.attrs.d;s.emit('speed','change',2);assert.equal(s.e.shapeTrace.attrs.d,d);s.frame(1100);s.frame(2100);assert.equal(s.time(),3);});
test('one cycle stops at 8 seconds; replay returns to beginning',()=>{const s=setup();s.e.play.click();s.frame(0);s.frame(9000);assert.equal(s.time(),8);assert.equal(s.raf.size,0);assert.equal(s.e.step.disabled,true);s.e.play.click();assert.equal(s.time(),0);assert.equal(s.raf.size,1);});
test('hidden page pauses without secretly resuming',()=>{const s=setup();s.e.play.click();s.frame(0);s.frame(1000);s.document.hidden=true;s.document.events.visibilitychange();assert.equal(s.raf.size,0);s.document.hidden=false;s.document.events.visibilitychange();assert.equal(s.raf.size,0);assert.equal(s.time(),1);});
test('enabling still mode during playback cancels motion',()=>{const s=setup();s.e.play.click();s.e.still.checked=true;s.emit('still','change');assert.equal(s.raf.size,0);assert.equal(s.e.play.disabled,true);s.e.still.checked=false;s.emit('still','change');assert.equal(s.raf.size,0);});
test('new system reduced-motion request stops motion and enables still mode',()=>{const s=setup();s.e.play.click();s.reduced(true);assert.equal(s.raf.size,0);assert.equal(s.e.still.checked,true);s.reduced(false);assert.equal(s.e.still.checked,true);});
test('export pauses, creates deterministic JSON and does not include user data',async()=>{const s=setup();s.emit('time','input',2);s.e.play.click();s.e.export.click();assert.equal(s.raf.size,0);assert.equal(s.downloads.length,1);assert.equal(s.downloads[0].download,'motion-trace-shape-experiment.json');const record=JSON.parse(await s.blobs[0].text());assert.equal(record.model.samples.length,481);assert.equal(record.presentation.time,2);assert.equal(record.model.parameters.phase_degrees,90);});
