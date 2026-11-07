"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const root = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const ui = fs.readFileSync(path.join(root, "src/ui.js"), "utf8");
const core = fs.readFileSync(path.join(root, "src/core.js"), "utf8");
test("standalone scripts and styles have matching CSP hashes", () => {
  const csp = html.match(/http-equiv="Content-Security-Policy" content="([^"]+)"/)[1];
  for (const block of html.matchAll(/<(?:script|style)>([\s\S]*?)<\/(?:script|style)>/g)) {
    const hash = crypto.createHash("sha256").update(block[1]).digest("base64");
    assert(csp.includes("'sha256-" + hash + "'"));
  }
  for (const directive of ["default-src 'none'", "connect-src 'none'", "object-src 'none'", "base-uri 'none'", "form-action 'none'"]) assert(csp.includes(directive));
  assert(!csp.includes("unsafe-inline")); assert(!csp.includes("unsafe-eval"));
});
test("no external runtime assets or remote invocation code", () => {
  assert(!/<(?:script|img|iframe|link)\b[^>]*(?:src|href)=/i.test(html));
  assert(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB|serviceWorker)\b/.test(ui + core));
  assert(!/\b(?:innerHTML|outerHTML|insertAdjacentHTML|eval)\b/.test(ui + core));
  assert(!/\son\w+=/i.test(html));
});
test("IDs are unique and explicit form labels refer to existing IDs", () => {
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
  assert.equal(ids.length, new Set(ids).size);
  for (const m of html.matchAll(/\bfor="([^"]+)"/g)) assert(ids.includes(m[1]));
  assert(html.includes('lang="en"')); assert(html.includes('class="skip"')); assert(html.includes('role="status"'));
});
test("external guidance links are explicit and no-referrer", () => {
  const links = [...html.matchAll(/<a\b[^>]*href="(https:[^"]+)"[^>]*>/g)];
  assert.equal(links.length, 3);
  for (const link of links) assert(link[0].includes('rel="noopener noreferrer"'));
  assert(html.includes('name="referrer" content="no-referrer"'));
});
test("main text palette meets WCAG AA normal-text contrast on its intended light background", () => {
  const luminance = hex => { const rgb = hex.match(/[0-9a-f]{2}/g).map(v => parseInt(v, 16) / 255).map(v => v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); return rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722; };
  for (const fg of ["203d38", "526660", "1c6952", "74500a", "9b3027"]) for (const bg of ["ffffff", "fcfdf9", "eef3ec"]) {
    const contrast = (luminance(bg) + 0.05) / (luminance(fg) + 0.05);
    assert(contrast >= 4.5, `${fg}/${bg}: ${contrast}`);
  }
});
