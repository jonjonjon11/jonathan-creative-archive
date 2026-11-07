/* Water-point preflight 0.1.0. Original implementation. See LICENSE and docs/rules.md. */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.WaterPreflight = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const VERSION = "0.1.0";
  const LIMITS = Object.freeze({ characters: 5000000, rows: 25000, columns: 256, cell: 65536, issues: 2000 });
  const FIELDS = Object.freeze([
    ["lat_deg", "Latitude", "required"], ["lon_deg", "Longitude", "required"],
    ["report_date", "Visit date", "required"], ["status_id", "Water present at visit", "required"],
    ["source", "Collecting organization", "required"],
    ["water_source", "Water source", "either"], ["water_tech", "Water technology", "either"],
    ["activity_id", "Water-point ID", "optional"], ["install_year", "Installation year", "optional"],
    ["rehab_year", "Rehabilitation year", "optional"]
  ].map(([key, label, need]) => Object.freeze({ key, label, need })));
  function normalHeader(value) { return value.trim().replace(/^#/, "").toLowerCase(); }
  function exceedsDecimalBound(value, bound) {
    // Called only for syntactically valid plain decimals. Compare the supplied decimal
    // exactly, so binary floating-point rounding cannot hide a tiny out-of-range value.
    const [integerPart, fraction = ""] = value.replace(/^[+-]/, "").split(".");
    const integer = integerPart.replace(/^0+/, "") || "0", limit = String(bound);
    return integer.length > limit.length ||
      (integer.length === limit.length && (integer > limit || (integer === limit && /[1-9]/.test(fraction))));
  }
  function excerpt(value) { return String(value).length > 160 ? String(value).slice(0, 159) + "…" : String(value); }
  function parseCSV(input) {
    const fail = (code, message, line, record) => ({ records: [], skippedBlankLines: 0, error: { code, message, line, record } });
    if (typeof input !== "string") return fail("CSV_INPUT", "Input must be text.", 1, 1);
    if (input.length > LIMITS.characters) return fail("FILE_LIMIT", "This prototype supports at most 5,000,000 text characters.", 1, 1);
    let text = input.charCodeAt(0) === 0xFEFF ? input.slice(1) : input;
    if (text.includes("\u0000")) return fail("CSV_ENCODING", "NUL characters found. Export a UTF-8 CSV, not UTF-16 or a spreadsheet workbook.", 1, 1);
    let cells = [], field = "", state = "start", line = 1, startLine = 1, record = 1, touched = false, skipped = 0;
    const records = [];
    const pushField = () => { cells.push(field); field = ""; state = "start"; };
    const pushRecord = () => {
      pushField();
      if (!touched && cells.length === 1 && cells[0] === "") skipped++;
      else records.push({ cells, line: startLine, record });
      cells = []; touched = false; record++;
    };
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      const newline = c === "\r" || c === "\n";
      if (state === "quoted") {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; }
          else state = "closed";
        } else if (newline) {
          if (c === "\r" && text[i + 1] === "\n") { field += "\r\n"; i++; }
          else field += c;
          line++;
        } else field += c;
      } else if (newline) {
        pushRecord();
        if (c === "\r" && text[i + 1] === "\n") i++;
        line++; startLine = line;
      } else if (c === ",") {
        touched = true; pushField();
      } else if (state === "closed") {
        return fail("CSV_QUOTE", "Only a comma or a line break may follow a closing quote. Remove extra characters or spaces outside the quotes.", line, record);
      } else if (c === '"') {
        if (state !== "start") return fail("CSV_QUOTE", "Quote inside an unquoted field. Quote the whole field and double embedded quotes.", line, record);
        touched = true; state = "quoted";
      } else {
        touched = true; state = "plain"; field += c;
      }
      if (field.length > LIMITS.cell) return fail("CELL_LIMIT", "A cell exceeds 65,536 characters. Split or shorten it in a copy of the CSV.", line, record);
      if (cells.length >= LIMITS.columns) return fail("COLUMN_LIMIT", "This prototype supports at most 256 columns.", line, record);
      if (records.length > LIMITS.rows + 1) return fail("ROW_LIMIT", "This prototype supports at most 25,000 data records.", line, record);
    }
    if (state === "quoted") return fail("CSV_QUOTE", "Unclosed quoted field. Check the record beginning on this line.", startLine, record);
    if (touched || field !== "" || cells.length > 0) pushRecord();
    if (records.length > LIMITS.rows + 1) return fail("ROW_LIMIT", "This prototype supports at most 25,000 data records.", line, record);
    return { records, skippedBlankLines: skipped, error: null };
  }
  function autoMapping(headers) {
    const mapping = Object.create(null);
    for (const { key } of FIELDS) {
      const candidates = headers.map((header, index) => normalHeader(header) === key ? index : -1).filter(index => index >= 0);
      mapping[key] = candidates.length === 1 ? candidates[0] : null;
    }
    return mapping;
  }
  function dateParts(value) {
    // Deliberately bounded ISO calendar profile. Never use Date.parse on local or ambiguous input.
    const m = /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2})(?:[.,](\d+))?)?(Z|[+-]\d{2}(?::?\d{2})?)?)?$/.exec(value);
    if (!m) return { valid: false, reason: "Use YYYY-MM-DD, optionally followed by T and HH:mm[:ss[.fraction]], then optional Z or ±HH[:mm]. Other ISO forms are outside this checker’s profile." };
    const year = +m[1], month = +m[2], day = +m[3];
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (year < 1 || month < 1 || month > 12 || day < 1 || day > days[month - 1]) return { valid: false, reason: "This is not a valid calendar date in years 0001–9999. Check the month, day, and leap year." };
    if (m[4] !== undefined) {
      const hour = +m[4], minute = +m[5], second = +(m[6] || 0);
      if (hour > 23 || minute > 59 || second > 59) return { valid: false, reason: "This checker accepts hours 00–23 and minutes/seconds 00–59. End-of-day 24:00 and leap-second forms require manual review and are outside its profile." };
      if (m[8] && m[8] !== "Z") {
        const z = /^[+-](\d{2})(?::?(\d{2}))?$/.exec(m[8]);
        if (+z[1] > 23 || +(z[2] || 0) > 59) return { valid: false, reason: "The timezone offset has an out-of-range hour or minute." };
      }
    }
    return { valid: true, year, date: value.slice(0, 10), hasTime: m[4] !== undefined };
  }
  function checkCSV(input, options = {}) {
    const parsed = parseCSV(input);
    const referenceDate = options.referenceDate || new Date().toISOString().slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(referenceDate) || !dateParts(referenceDate).valid) throw new Error("referenceDate must be a valid YYYY-MM-DD date.");
    const result = {
      version: VERSION, referenceDate, complete: false, headers: [], mapping: {},
      counts: { records: 0, reviewed: 0, errors: 0, warnings: 0, recordsWithErrors: 0, recordsWithWarnings: 0, skippedBlankLines: parsed.skippedBlankLines },
      issues: [], omittedIssues: 0,
      scope: "Local preflight only; not WPdx certification, upload acceptance, field verification, or water-safety assessment. No geographic boundary or full optional-field checks. Values in issues are shortened to 160 characters."
    };
    const errorRows = new Set(), warningRows = new Set();
    const add = (severity, code, row, field, value, message, basis = "local-review") => {
      result.counts[severity === "error" ? "errors" : "warnings"]++;
      if (row && row.record) (severity === "error" ? errorRows : warningRows).add(row.record);
      if (result.issues.length < LIMITS.issues) result.issues.push({ severity, code, record: row ? row.record : null, line: row ? row.line : null, field, value: excerpt(value), message, basis });
      else result.omittedIssues++;
    };
    if (parsed.error) {
      add("error", parsed.error.code, parsed.error, "CSV", "", parsed.error.message, "parser-profile");
      return result;
    }
    if (!parsed.records.length) { add("error", "EMPTY_FILE", null, "CSV", "", "No header or data records found.", "parser-profile"); return result; }
    const header = parsed.records[0];
    result.headers = header.cells;
    const rows = parsed.records.slice(1);
    result.counts.records = rows.length;
    if (!rows.length) add("error", "NO_DATA", null, "CSV", "", "A header alone is not a survey. Add data records.", "parser-profile");
    let headerBad = false;
    const seenHeaders = new Set();
    header.cells.forEach((value, index) => {
      const name = normalHeader(value);
      if (!name) { add("error", "HEADER_EMPTY", null, "column " + (index + 1), value, "Give every column a non-empty, unique header.", "parser-profile"); headerBad = true; }
      else if (seenHeaders.has(name)) { add("error", "HEADER_DUPLICATE", null, "column " + (index + 1), value, "Duplicate header after ignoring #, case, and surrounding spaces. Rename it to avoid ambiguous mapping.", "parser-profile"); headerBad = true; }
      seenHeaders.add(name);
    });
    const mapping = options.mapping === undefined ? autoMapping(header.cells) : options.mapping;
    const used = new Map();
    for (const { key, need } of FIELDS) {
      const index = mapping && Object.hasOwn(mapping, key) ? mapping[key] : null;
      result.mapping[key] = index;
      if (index !== null && (!Number.isInteger(index) || index < 0 || index >= header.cells.length)) {
        add("error", "MAPPING_INVALID", null, key, index, "Choose an existing column or leave this field unmapped.", "parser-profile"); headerBad = true;
      } else if (index !== null) {
        if (used.has(index)) { add("error", "MAPPING_REUSED", null, key, header.cells[index], "This column is already mapped to " + used.get(index) + ". Use a separate column for each meaning.", "parser-profile"); headerBad = true; }
        used.set(index, key);
      } else if (need === "required") { add("error", "MAPPING_REQUIRED", null, key, "", "Map a column for this required parameter. No values are guessed or supplied as constants.", "wpdx-required"); headerBad = true; }
    }
    if (result.mapping.water_source === null && result.mapping.water_tech === null) {
      add("error", "MAPPING_TYPE", null, "water_source / water_tech", "", "Map at least one water-source or water-technology column.", "wpdx-required"); headerBad = true;
    }
    if (headerBad) return result;
    const exactRows = new Map(), visits = new Map();
    for (const row of rows) {
      if (row.cells.length !== header.cells.length) {
        add("error", "ROW_WIDTH", row, "CSV", row.cells.length, "This record has " + row.cells.length + " cells; the header has " + header.cells.length + ". Check commas and quoting. Field checks were skipped for this record.", "parser-profile");
        continue;
      }
      result.counts.reviewed++;
      const raw = key => result.mapping[key] === null ? "" : row.cells[result.mapping[key]];
      const value = key => raw(key).trim();
      for (const key of ["lat_deg", "lon_deg", "report_date", "source"]) {
        if (!value(key)) add("error", "REQUIRED_VALUE", row, key, raw(key), "This required value is blank. Check the survey record; do not invent a value.", "wpdx-required");
      }
      if (!value("water_source") && !value("water_tech")) add("error", "WATER_TYPE_MISSING", row, "water_source / water_tech", "", "Provide at least one observed water-source or technology value.", "wpdx-required");
      let coordinatesValid = true;
      for (const [key, bound] of [["lat_deg", 90], ["lon_deg", 180]]) {
        const v = value(key);
        if (!v) { coordinatesValid = false; continue; }
        if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(v)) {
          add("error", "COORD_FORMAT", row, key, raw(key), "Use a plain decimal-degree number with a dot. DMS, comma decimals, exponents, NaN, and infinity are not supported.", "parser-profile"); coordinatesValid = false;
        } else if (exceedsDecimalBound(v, bound)) {
          add("error", "COORD_RANGE", row, key, raw(key), "Must be between −" + bound + " and +" + bound + ". Verify latitude/longitude order and the coordinate system; no swap was made.", "coordinate-bounds"); coordinatesValid = false;
        } else if ((v.split(".")[1] || "").length < 4) {
          add("warning", "COORD_PRECISION", row, key, raw(key), "Fewer than four decimal places were supplied. WPdx recommends at least four. Verify the original GPS precision; adding zeros does not improve accuracy.", "wpdx-guidance");
        }
      }
      if (coordinatesValid && !/[1-9]/.test(value("lat_deg")) && !/[1-9]/.test(value("lon_deg"))) add("warning", "ZERO_COORDINATES", row, "lat_deg / lon_deg", "0, 0", "Both coordinates are zero. This can be a default placeholder. Verify the original location; no boundary check was performed.");
      const status = value("status_id");
      if (!/^(yes|no)$/i.test(status)) add("warning", "STATUS_REVIEW", row, "status_id", raw("status_id"), status ? "Not Yes/No. WPdx permits mapped binary equivalents and represents unknowns as blank. A person must confirm the intended mapping; this tool does not infer water presence from functionality wording." : "Water-presence value is blank. WPdx describes blank/unknown responses as empty cells. Confirm that this reflects the survey rather than a missing observation.", "wpdx-guidance");
      let date = null;
      if (value("report_date")) {
        date = dateParts(value("report_date"));
        if (!date.valid) add("error", "DATE_PROFILE", row, "report_date", raw("report_date"), date.reason, "parser-profile");
        else if (date.date > referenceDate) add("warning", "FUTURE_DATE", row, "report_date", raw("report_date"), "Visit calendar date is after the review date (" + referenceDate + ", UTC). Check timezone, device clock, or transcription. Timestamp offsets are not converted for this warning.");
      }
      const years = {};
      for (const key of ["install_year", "rehab_year"]) {
        const v = value(key);
        if (!v) continue;
        if (!/^\d{4}$/.test(v) || Number(v) < 1) add("warning", "YEAR_FORMAT", row, key, raw(key), "Use a four-digit calendar year when known; this optional value could not be checked.", "wpdx-guidance");
        else {
          years[key] = Number(v);
          if (years[key] > Number(referenceDate.slice(0, 4))) add("warning", "FUTURE_YEAR", row, key, v, "Year is after the review year. Confirm the original record.");
          if (date && date.valid && years[key] > date.year) add("warning", "YEAR_AFTER_VISIT", row, key, v, "Year is after the visit year. This may combine information from different visits; review the provenance.");
        }
      }
      if (years.install_year && years.rehab_year && years.rehab_year < years.install_year) add("warning", "YEAR_ORDER", row, "rehab_year", value("rehab_year"), "Rehabilitation year precedes installation year. Confirm whether the fields describe the same infrastructure.");
      for (const key of ["source", "water_source", "water_tech"]) {
        if (/^(unknown|n\/?a|null|none|-|not known)$/i.test(value(key))) add("warning", "PLACEHOLDER", row, key, raw(key), "This may be an unknown-value placeholder. Confirm its meaning. Open-text categories are not restricted to a fixed vocabulary.");
      }
      const exactKey = JSON.stringify(row.cells);
      const isExactDuplicate = exactRows.has(exactKey);
      if (isExactDuplicate) add("warning", "EXACT_DUPLICATE", row, "record", "", "All cells exactly match record " + exactRows.get(exactKey) + ". Confirm whether both observations belong. Nothing was deleted.");
      else exactRows.set(exactKey, row.record);
      if (value("activity_id") && value("source") && date && date.valid) {
        const visitKey = JSON.stringify([value("source"), value("activity_id"), date.date]);
        if (visits.has(visitKey) && !isExactDuplicate) add("warning", "REPEATED_VISIT_ID", row, "activity_id", raw("activity_id"), "Same organization, water-point ID, and calendar visit date as record " + visits.get(visitKey) + ". Multiple visits can be legitimate; review rather than delete automatically.");
        else if (!visits.has(visitKey)) visits.set(visitKey, row.record);
      }
    }
    result.counts.recordsWithErrors = errorRows.size;
    result.counts.recordsWithWarnings = warningRows.size;
    result.complete = rows.length > 0 && result.counts.reviewed === rows.length;
    return result;
  }
  return Object.freeze({ VERSION, LIMITS, FIELDS, normalHeader, parseCSV, autoMapping, dateParts, checkCSV });
});
