"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const P = require("../src/core.js");
const { makeInjectionFixture } = require("./fixtures.cjs");
const header = "#lat_deg,#lon_deg,#report_date,#status_id,#source,#water_source,#water_tech,#activity_id,#install_year,#rehab_year";
const base = ["1.2345", "32.4567", "2024-02-29", "Yes", "Synthetic Team", "Borehole", "", "SYN-1", "2020", "2021"];
const csvCell = s => /[",\r\n]/.test(s) ? '"' + s.replaceAll('"', '""') + '"' : s;
const csv = (rows = [base]) => header + "\n" + rows.map(row => row.map(csvCell).join(",")).join("\n");
const check = (text, opts = {}) => P.checkCSV(text, { referenceDate: "2026-11-07", ...opts });
const codes = result => result.issues.map(i => i.code);
function changed(index, value) { const row = [...base]; row[index] = value; return row; }

test("clean canonical input completes without findings", () => { const r = check(csv()); assert.equal(r.complete, true); assert.equal(r.counts.reviewed, 1); assert.deepEqual(r.issues, []); });
test("synthetic clean fixture is clean", () => assert.equal(check(fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-clean.csv"), "utf8")).issues.length, 0));
test("synthetic review fixture exercises errors and warnings", () => { const r = check(fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-review.csv"), "utf8")); assert.equal(r.counts.errors, 3); assert.equal(r.counts.warnings, 9); assert.equal(r.counts.records, 5); assert(codes(r).includes("EXACT_DUPLICATE")); });
test("CSV quotes, commas, doubled quotes, CRLF and multiline locations", () => { const p = P.parseCSV('a,b\r\n"x,y","said ""hi""\r\nnext"\r\nu,v\r\n'); assert.equal(p.error, null); assert.deepEqual(p.records[1], { cells: ["x,y", 'said "hi"\r\nnext'], line: 2, record: 2 }); assert.equal(p.records[2].line, 4); });
test("BOM and CR-only line endings", () => { const p = P.parseCSV("\uFEFFa,b\rx,y"); assert.equal(p.records[0].cells[0], "a"); assert.equal(p.records[1].line, 2); });
test("trailing empty cell, empty quoted cell and trailing newline preserved appropriately", () => { assert.deepEqual(P.parseCSV('a,b\n"",\n').records[1].cells, ["", ""]); assert.equal(P.parseCSV('a\n""').records.length, 2); });
test("physical blank lines are skipped without renumbering source records", () => { const p = P.parseCSV("a,b\n\nx,y\n"); assert.equal(p.skippedBlankLines, 1); assert.equal(p.records[1].record, 3); assert.equal(p.records[1].line, 3); });
for (const text of ['a,b\n"bad', 'a,b\nx"y,z', 'a,b\n"x" trailing,z', 'a,b\n"x" ,z']) test("reject malformed CSV: " + JSON.stringify(text), () => assert.equal(P.parseCSV(text).error.code, "CSV_QUOTE"));
test("NUL and nonstring input rejected", () => { assert.equal(P.parseCSV("a\0b").error.code, "CSV_ENCODING"); assert.equal(P.parseCSV(null).error.code, "CSV_INPUT"); });
test("record width errors skip field checks and mark incomplete", () => { const r = check(csv() + "\n1,2"); assert.equal(r.complete, false); assert.equal(r.counts.reviewed, 1); assert.deepEqual(codes(r), ["ROW_WIDTH"]); assert.equal(r.counts.recordsWithErrors, 1); });
test("empty and header-only files are not declared complete", () => { assert.equal(check("").complete, false); assert.equal(check(header).complete, false); assert(codes(check(header)).includes("NO_DATA")); });
test("canonical header normalization and duplicate detection", () => { assert.equal(check(csv().replace("#lat_deg", " LAT_DEG ")).issues.length, 0); const r = check(csv().replace("#lon_deg", "#LAT_DEG")); assert(codes(r).includes("HEADER_DUPLICATE")); assert.equal(r.counts.reviewed, 0); });
test("blank header detected", () => assert(codes(check(csv().replace("#lat_deg", ""))).includes("HEADER_EMPTY")));
test("custom headers require explicit mapping", () => { const renamed = csv().replace("#lat_deg", "GPS latitude"); assert(codes(check(renamed)).includes("MAPPING_REQUIRED")); const m = P.autoMapping(P.parseCSV(csv()).records[0].cells); assert.equal(check(renamed, { mapping: m }).issues.length, 0); });
test("mapping cannot reuse a column or point outside table", () => { const m = P.autoMapping(header.split(",")); assert(codes(check(csv(), { mapping: { ...m, lat_deg: 1 } })).includes("MAPPING_REUSED")); assert(codes(check(csv(), { mapping: { ...m, lat_deg: 99 } })).includes("MAPPING_INVALID")); });
test("prototype pollution names do not affect mapping", () => { const r = check(csv().replace("#lat_deg", "__proto__")); assert(codes(r).includes("MAPPING_REQUIRED")); assert.equal({}.polluted, undefined); });
test("required values checked while zero is a value", () => { assert(codes(check(csv([changed(4, " ")]))).includes("REQUIRED_VALUE")); assert(!codes(check(csv([changed(0, "0.0000")]))).includes("REQUIRED_VALUE")); });
test("source or technology required per record, either sufficient", () => { assert.equal(check(csv([changed(5, "" )])).counts.errors, 1); const row = changed(5, ""); row[6] = "Local device description"; assert.equal(check(csv([row])).counts.errors, 0); });
test("unknown technology and source text not rejected", () => { const row = changed(5, "Locally named spring type"); row[6] = "A nonstandard transport system"; assert.equal(check(csv([row])).issues.length, 0); });
for (const value of ["NaN", "Infinity", "1e2", "12,34", "12°N", "0x20", "1 2", "-"]) test("coordinate format rejected: " + value, () => assert(codes(check(csv([changed(0, value)]))).includes("COORD_FORMAT")));
test("coordinate bounds inclusive and outside rejected", () => { for (const lat of ["90.0000", "-90.0000"]) assert.equal(check(csv([changed(0, lat)])).counts.errors, 0); for (const lon of ["180.0000", "-180.0000"]) assert.equal(check(csv([changed(1, lon)])).counts.errors, 0); assert(codes(check(csv([changed(0, "90.0001")]))).includes("COORD_RANGE")); assert(codes(check(csv([changed(1, "-180.0001")]))).includes("COORD_RANGE")); });
test("exact decimal bounds reject signed tiny excesses including leading zeros", () => {
  for (const [column, bound] of [[0, "90"], [1, "180"]]) for (const sign of ["", "+", "-"]) for (const zeros of ["", "000"]) {
    const value = sign + zeros + bound + ".000000000000000001";
    assert(codes(check(csv([changed(column, value)]))).includes("COORD_RANGE"), value);
  }
});
test("exact bounds and just-inside decimals remain accepted with every sign", () => {
  for (const [column, values] of [[0, ["90.000000000000000000", "89.999999999999999999"]], [1, ["180.000000000000000000", "179.999999999999999999"]]]) {
    for (const value of values) for (const sign of ["", "+", "-"]) assert.equal(check(csv([changed(column, sign + "000" + value)])).counts.errors, 0, sign + value);
  }
});
test("huge decimals are range errors and tiny nonzero decimals do not become zero placeholders", () => {
  assert(codes(check(csv([changed(0, "9".repeat(400))]))).includes("COORD_RANGE"));
  const row = changed(0, "0." + "0".repeat(400) + "1"); row[1] = "-0.0000";
  const r = check(csv([row])); assert.equal(r.counts.errors, 0); assert(!codes(r).includes("ZERO_COORDINATES"));
});
test("decimal bounds agree with an independent exact BigInt oracle near both limits", () => {
  for (const [column, bound] of [[0, 90n], [1, 180n]]) for (let precision = 1; precision <= 50; precision++) {
    const scale = 10n ** BigInt(precision);
    for (const delta of [-1n, 0n, 1n]) {
      const absolute = bound * scale + delta;
      const value = (absolute / scale).toString() + "." + (absolute % scale).toString().padStart(precision, "0");
      const result = check(csv([changed(column, (precision % 2 ? "-" : "+") + value)]));
      assert.equal(codes(result).includes("COORD_RANGE"), absolute > bound * scale, value);
    }
  }
});
test("browser DOM-injection fixture is valid CSV and reaches mapped value review", () => {
  const clean = fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-clean.csv"), "utf8");
  const attack = makeInjectionFixture(clean), parsed = P.parseCSV(attack);
  assert.equal(parsed.error, null); assert.equal(parsed.records.length, 3);
  assert.equal(parsed.records[0].cells[0], '<img src=x onerror="window.pwned=1">');
  assert.equal(parsed.records[1].cells[2], '<script>window.pwned=1</script>');
  const mapping = P.autoMapping(parsed.records[0].cells); mapping.lat_deg = 0;
  const result = check(attack, { mapping });
  assert.equal(result.complete, true); assert.equal(result.counts.reviewed, 2);
  assert(codes(result).includes("DATE_PROFILE")); assert(!codes(result).includes("CSV_QUOTE"));
});
test("precision and zero pair are warnings, not fabricated accuracy", () => { const row = changed(0, "0"); row[1] = "-0"; const r = check(csv([row])); assert.equal(r.counts.errors, 0); assert.equal(r.counts.warnings, 3); assert(codes(r).includes("ZERO_COORDINATES")); });
for (const value of ["2024-02-29", "2000-02-29", "2024-01-31T23:59:59.123Z", "2024-01-31T13:14+03", "2024-01-31T13:14:15-0430", "2024-01-31T13:14:15+04:30", "2024-01-31T13:14:15,1", "0001-01-01"]) test("supported date accepted: " + value, () => assert.equal(P.dateParts(value).valid, true));
for (const value of ["2023-02-29", "1900-02-29", "2024-04-31", "2024-00-01", "2024-13-01", "2024-01-00", "0000-01-01", "01/02/2024", "2024-1-1", "2024-01-01junk", "2024-01-01T25:00", "2024-01-01T00:60", "2024-01-01T00:00:61", "2024-01-01T00:00+25:00", "2024-01-01T00:00+02:60", "2024-01-01T00:00Zjunk"]) test("invalid/out-of-profile date rejected: " + value, () => assert.equal(P.dateParts(value).valid, false));
test("other ISO forms clearly outside profile", () => { for (const v of ["2024-W01-1", "2024-001", "2024-01-01T24:00", "2024-12-31T23:59:60Z"]) assert.equal(P.dateParts(v).valid, false); });
test("future date is warning only, using date part not UTC conversion", () => { assert(codes(check(csv([changed(2, "2026-11-08T00:01+14:00")]))).includes("FUTURE_DATE")); assert(!codes(check(csv([changed(2, "2026-11-07T23:59-12:00")]))).includes("FUTURE_DATE")); });
test("status unknown and custom equivalents are review warnings, not errors", () => { for (const status of ["", "Functional", "Unknown", "1", "false"]) { const r = check(csv([changed(3, status)])); assert.equal(r.counts.errors, 0); assert(codes(r).includes("STATUS_REVIEW")); } for (const status of ["yes", "NO", " Yes "]) assert.equal(check(csv([changed(3, status)])).issues.length, 0); });
test("optional year format and order reviewed", () => { const r = check(csv([changed(8, "20x0")])); assert(codes(r).includes("YEAR_FORMAT")); const row = changed(9, "2010"); assert(codes(check(csv([row]))).includes("YEAR_ORDER")); assert(codes(check(csv([changed(8, "2099")]))).includes("FUTURE_YEAR")); });
test("repeated IDs differ from exact duplicate and across dates allowed", () => { const r = check(csv([base, base])); assert.equal(codes(r).filter(c => c === "EXACT_DUPLICATE").length, 1); assert(!codes(r).includes("REPEATED_VISIT_ID")); assert(codes(check(csv([base, changed(3, "No")]))).includes("REPEATED_VISIT_ID")); assert(!codes(check(csv([base, changed(2, "2024-03-01")]))).includes("REPEATED_VISIT_ID")); });
test("unknown placeholder warns without being rejected", () => { const r = check(csv([changed(5, "unknown")])); assert.equal(r.counts.errors, 0); assert(codes(r).includes("PLACEHOLDER")); });
test("unmapped optional data is not interpreted", () => { assert.equal(check(csv() + ",ignored").complete, false); assert.equal(check(header + ",extra\n" + base.join(",") + ",=1+1").issues.length, 0); });
test("issue values bounded, with complete aggregate counts and truncation disclosed", () => { const long = changed(3, "x".repeat(1000)); assert.equal(check(csv([long])).issues[0].value.length, 160); const r = check(csv(Array.from({ length: 2100 }, (_, i) => { const row = changed(0, "999"); row[7] = "SYN-" + i; return row; }))); assert.equal(r.counts.errors, 2100); assert.equal(r.issues.length, 2000); assert.equal(r.omittedIssues, 100); assert.equal(r.complete, true); });
test("resource limits explicit and maximum dimensions accepted", () => { assert.equal(P.parseCSV("x".repeat(P.LIMITS.characters + 1)).error.code, "FILE_LIMIT"); assert.equal(P.parseCSV("a\n" + "x".repeat(P.LIMITS.cell + 1)).error.code, "CELL_LIMIT"); assert.equal(P.parseCSV(Array(257).fill("x").join(",")).error.code, "COLUMN_LIMIT"); assert.equal(P.parseCSV(Array(256).fill("x").join(",")).error, null); assert.equal(P.parseCSV("a\n" + Array(25001).fill("x").join("\n")).error.code, "ROW_LIMIT"); assert.equal(P.parseCSV("a\n" + Array(25000).fill("x").join("\n")).error, null); });
test("bad reference dates cannot change review silently", () => assert.throws(() => check(csv(), { referenceDate: "2026-02-30" }), /referenceDate/));
test("input data never mutated", () => { const text = csv([changed(3, "Functional")]); check(text); assert.equal(text, csv([changed(3, "Functional")])); });
test("randomized CSV round-trips preserve cells and quoting", () => { let seed = 17; const rand = n => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed % n; }; const alphabet = ['a', ',', '"', '\n', '\r', ' ', 'é', '水']; for (let i = 0; i < 200; i++) { const rows = Array.from({ length: 1 + rand(8) }, () => Array.from({ length: 2 + rand(5) }, () => Array.from({ length: rand(20) }, () => alphabet[rand(alphabet.length)]).join(""))); const text = rows.map(row => row.map(csvCell).join(",")).join("\r\n"); const p = P.parseCSV(text); assert.equal(p.error, null); assert.deepEqual(p.records.map(r => r.cells), rows); } });
