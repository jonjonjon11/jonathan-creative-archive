"use strict";
const { test } = require("node:test"), assert = require("node:assert/strict");
const { makeFixture, caseMatrix, validateCases, runProcess, isDiagnosticTimeout, processStat } = require("./input-diagnostics.cjs");
const P = require("../src/core.js");
test("diagnostic matrix is small, explicit and excludes native paste claims", () => {
 const cases=validateCases(caseMatrix()); assert.equal(cases.length,8); assert(cases.every(c=>c.width===320));
 for(const bad of [[],Array(17).fill(cases[0]),[{...cases[0],rows:1000000}],[{...cases[0],width:100000}],[{...cases[0],method:"native-paste"}]]) assert.throws(()=>validateCases(bad));
});
test("diagnostic maximum fixture has exact known synthetic length and counts",()=>{
 const text=makeFixture(25000); assert.equal(text.length,1038947);assert.equal(Buffer.byteLength(text),1038947);
 const result=P.checkCSV(text);assert.equal(result.counts.records,25000);assert.equal(result.counts.errors,100000);assert.equal(result.counts.warnings,25000);assert.throws(()=>makeFixture(1));
});
test("external watchdog permits completion and bounds a stalled child",{skip:process.platform!=="linux"},async()=>{
 const success=await runProcess(process.execPath,["-e","process.stdout.write('ok')"],{timeoutMs:2000});assert.equal(success.code,0);assert.equal(success.timedOut,false);assert.equal(success.output,"ok");
 const stopped=await runProcess(process.execPath,["-e","setInterval(()=>{},1000)"],{timeoutMs:100});assert.equal(stopped.timedOut,true);assert(stopped.elapsedMs<2500);assert.notEqual(stopped.code,0);
});

test("setup and cleanup timeouts cannot be reported as completed diagnostics",()=>{
 for(const stage of ["launch","load-and-sample","open-small-textarea","close-browser","unknown",undefined]) assert.equal(isDiagnosticTimeout(stage),false);
 for(const stage of ["playwright-fill","paint-after-open","programmatic-value-assignment","file-import-closed"]) assert.equal(isDiagnosticTimeout(stage),true);
});

test("watchdog also terminates detached browser-like descendants",{skip:process.platform!=="linux"},async()=>{
 const script = "const {spawn}=require('node:child_process');const p=spawn(process.execPath,['-e',\"process.on('SIGTERM',()=>{});setInterval(()=>{},1000)\"],{detached:true,stdio:'ignore'});console.log(p.pid);setInterval(()=>{},1000)";
 const result=await runProcess(process.execPath,["-e",script],{timeoutMs:500});
 assert.equal(result.timedOut,true);assert.equal(result.cleanupIncomplete,false);assert.equal(result.trackingError,undefined);assert(result.trackedProcesses>=2);
 const grandchild=processStat(Number(result.output.trim()));assert(!grandchild || grandchild.state==="Z");
});
