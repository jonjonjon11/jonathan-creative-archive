"use strict";
// A small DOM model exercises controller state, not browser rendering, layout, CSP enforcement, or accessibility APIs.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const P = require("../src/core.js");
function harness() {
  const ids = new Map();
  const document = { activeElement: null, createElement: tag => new Element(tag), getElementById: id => ids.get(id) };
  class Element {
    constructor(tag) { this.tagName = tag; this.children = []; this.events = {}; this.hidden = false; this.value = ""; this.textContent = ""; this.checked = false; this.files = []; }
    set id(value) { this._id = value; ids.set(value, this); } get id() { return this._id; }
    append(...nodes) { this.children.push(...nodes); } replaceChildren(...nodes) { this.children = nodes; }
    addEventListener(name, handler) { this.events[name] = handler; }
    async fire(name) { if (this.events[name]) return this.events[name](); }
    focus() { document.activeElement = this; } click() { return this.fire("click"); } remove() {}
  }
  const html = fs.readFileSync(path.join(__dirname, "../src/template.html"), "utf8");
  for (const m of html.matchAll(/<([a-z]+)[^>]*\bid="([^"]+)"[^>]*>/g)) { const e = new Element(m[1]); e.id = m[2]; e.hidden = m[0].includes(" hidden"); }
  document.body = new Element("body");
  const sample = fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-review.csv"), "utf8");
  const code = fs.readFileSync(path.join(__dirname, "../src/ui.js"), "utf8").replace("'__SAMPLE__'", JSON.stringify(sample));
  const blobs = [];
  const context = { window: { WaterPreflight: P }, document, TextDecoder, Blob, Date, URL: { createObjectURL: b => { blobs.push(b); return "blob:local-test"; }, revokeObjectURL() {} }, setTimeout: fn => fn() };
  vm.runInNewContext(code, context);
  return { $: id => ids.get(id), document, blobs };
}
test("controller loads example, renders expected counts, filters, and exports privacy-default report", async () => {
  const { $, document, blobs } = harness(); await $("demo").fire("click");
  assert.equal($("count-errors").textContent, "3"); assert.equal($("count-warnings").textContent, "9");
  assert.equal($("issues").children.length, 12); assert.equal(document.activeElement, $("results"));
  $("filter").value = "error"; await $("filter").fire("change"); assert.equal($("issues").children.length, 3);
  await $("download").fire("click"); const report = JSON.parse(await blobs[0].text());
  assert.equal(report.headers, undefined); assert.equal(report.issues.length, 12); assert(report.issues.every(i => i.value === undefined));
});
test("controller explicit value export, repeated sample load, and clear behavior", async () => {
  const { $, blobs } = harness(); await $("demo").fire("click"); $("include-values").checked = true;
  await $("download").fire("click"); assert.equal(JSON.parse(await blobs[0].text()).inputValuesIncluded, true);
  await $("demo").fire("click"); assert.equal($("issues").children.length, 12); assert.equal($("include-values").checked, false);
  await $("clear").fire("click"); assert.equal($("csv").value, ""); assert.equal($("results").hidden, true); assert.equal($("mapping-panel").hidden, true); assert.equal($("issues").children.length, 0);
});
test("controller invalidates edits and mapping changes", async () => {
  const { $ } = harness(); await $("demo").fire("click"); await $("csv").fire("input"); assert.equal($("results").hidden, true);
  await $("review").fire("click"); $("map-lat_deg").value = ""; await $("map-lat_deg").fire("change"); assert.equal($("results").hidden, true);
  await $("review-mapping").fire("click"); assert.match($("review-state").textContent, /incomplete/);
  $("map-lat_deg").value = "0"; await $("map-lat_deg").fire("change"); await $("review-mapping").fire("click"); assert.equal($("count-errors").textContent, "3");
});
test("controller file reads, invalid UTF-8, and oversized file handling", async () => {
  const { $ } = harness(); const clean = fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-clean.csv"));
  $("file").files = [{ size: clean.length, arrayBuffer: async () => clean }]; await $("file").fire("change");
  assert.equal($("count-records").textContent, "2"); assert.equal($("count-errors").textContent, "0");
  $("file").files = [{ size: 2, arrayBuffer: async () => Buffer.from([255, 254]) }]; await $("file").fire("change");
  assert.match($("input-status").textContent, /Could not read/); assert.equal($("results").hidden, true);
  $("file").files = [{ size: 5000001, arrayBuffer: async () => { throw new Error("must not read"); } }]; await $("file").fire("change");
  assert.match($("input-status").textContent, /larger than 5 MB/);
});
test("clear and newer input win over a delayed earlier file read", async () => {
  const { $ } = harness(); let resolve;
  $("file").files = [{ size: 20, arrayBuffer: () => new Promise(r => resolve = r) }];
  const pending = $("file").fire("change"); await $("clear").fire("click"); resolve(Buffer.from("old,data\n1,2")); await pending;
  assert.equal($("csv").value, ""); assert.equal($("results").hidden, true);
  $("file").files = [{ size: 20, arrayBuffer: () => new Promise(r => resolve = r) }];
  const pending2 = $("file").fire("change"); await $("demo").fire("click"); const text = $("csv").value;
  resolve(Buffer.from("old,data\n1,2")); await pending2; assert.equal($("csv").value, text); assert.equal($("count-errors").textContent, "3");
});
test("controller malformed input clears mapping panel and cannot retain old findings", async () => {
  const { $ } = harness(); await $("demo").fire("click"); $("csv").value = 'a,b\n"oops'; await $("review").fire("click");
  assert.equal($("mapping-panel").hidden, true); assert.match($("review-state").textContent, /incomplete/); assert.equal($("issues").children.length, 1);
});
