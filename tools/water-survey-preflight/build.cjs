"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const root = __dirname;
const read = file => fs.readFileSync(path.join(root, file), "utf8");
const hash = text => crypto.createHash("sha256").update(text).digest("base64");
const core = read("src/core.js"), style = read("src/style.css");
const ui = read("src/ui.js").replace("'__SAMPLE__'", JSON.stringify(read("fixtures/synthetic-review.csv")));
const csp = "default-src 'none'; script-src 'sha256-" + hash(core) + "' 'sha256-" + hash(ui) + "'; style-src 'sha256-" + hash(style) + "'; connect-src 'none'; img-src 'none'; font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'";
const html = read("src/template.html").replace("__CSP__", csp).replace("__STYLE__", () => style).replace("__CORE__", () => core).replace("__UI__", () => ui);
if (/__(?:CSP|STYLE|CORE|UI|SAMPLE)__/.test(html)) throw new Error("Unfilled build placeholder");
if (process.argv.includes("--check")) {
  if (read("index.html") !== html) throw new Error("index.html is stale; run node build.cjs");
  console.log("PASS: standalone HTML exactly matches source build.");
} else {
  fs.writeFileSync(path.join(root, "index.html"), html);
  console.log("Built self-contained index.html (" + Buffer.byteLength(html) + " bytes).");
}
