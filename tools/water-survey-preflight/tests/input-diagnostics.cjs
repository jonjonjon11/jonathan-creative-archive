"use strict";
// Optional synthetic diagnostic, not a performance acceptance test or native-paste test.
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");
const { spawn } = require("node:child_process");
const { pathToFileURL } = require("node:url");
const sha256 = value => crypto.createHash("sha256").update(value).digest("hex");
const METHODS = ["file-closed", "reopen-after-file", "assign-open", "fill-open"];
const TARGET_PHASES = new Set(["file-import-closed", "toggle-populated-textarea", "observe-details-open", "paint-after-open", "playwright-fill", "programmatic-value-assignment", "synthetic-input-dispatch", "paint-after-input", "review-after-input", "verify-result", "scroll-results"]);
function isDiagnosticTimeout(stage) { return TARGET_PHASES.has(stage); }
function makeFixture(rows) {
  if (![2050, 25000].includes(rows)) throw new Error("Only bounded fixture sizes are supported");
  return "lat_deg,lon_deg,report_date,status_id,source,water_source\n" + Array.from({ length: rows }, (_, i) => `999,999,2024-02-30,Unknown,,Unknown ${i}`).join("\n");
}
function caseMatrix() {
  return [2050, 25000].flatMap(rows => METHODS.map(method => ({ method, rows, width: 320, repeat: 1 })));
}
function validateCases(cases) {
  if (!Array.isArray(cases) || !cases.length || cases.length > 16) throw new Error("Expected 1–16 diagnostic cases");
  for (const c of cases) if (!METHODS.includes(c.method) || ![2050, 25000].includes(c.rows) || ![320, 1280].includes(c.width) || !Number.isInteger(c.repeat) || c.repeat < 1 || c.repeat > 3) throw new Error("Invalid bounded diagnostic case");
  return cases;
}
// Linux watchdog tracks process ancestry plus start times, including detached browser
// descendants. It never signals a process merely because its numeric PID was reused.
function processStat(pid) {
  try {
    const raw = fs.readFileSync(`/proc/${pid}/stat`, "utf8");
    const fields = raw.slice(raw.lastIndexOf(")") + 2).split(" ");
    return { pid: Number(pid), parent: Number(fields[1]), state: fields[0], start: fields[19] };
  } catch (e) { if (["ENOENT", "ESRCH"].includes(e.code)) return null; throw e; }
}
function runProcess(command, args, options = {}) {
  if (process.platform !== "linux") throw new Error("Descendant watchdog requires Linux /proc");
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { detached: true, stdio: ["ignore", "pipe", "pipe"], env: options.env || process.env });
    const start = Date.now(), tracked = new Map(); let output = "", timedOut = false, killTimer, trackingError;
    const retain = data => { output = (output + data.toString()).slice(-16000); };
    child.stdout.on("data", retain); child.stderr.on("data", retain);
    const collect = () => {
      try {
        const all = fs.readdirSync("/proc").filter(name => /^\d+$/.test(name)).map(processStat).filter(Boolean);
        const roots = new Set([...tracked.values()].filter(p => all.some(now => now.pid === p.pid && now.start === p.start)).map(p => p.pid));
        if (!tracked.size && all.some(p => p.pid === child.pid)) roots.add(child.pid);
        let changed = true;
        while (changed) { changed = false; for (const p of all) if (roots.has(p.pid) || roots.has(p.parent)) {
          if (!roots.has(p.pid)) { roots.add(p.pid); changed = true; }
          tracked.set(p.pid, p);
        } }
      } catch (e) { trackingError = String(e).slice(0,300); }
    };
    const alive = () => [...tracked.values()].filter(p => { const now = processStat(p.pid); return now && now.start === p.start && now.state !== "Z"; });
    const signal = sig => { collect(); for (const p of alive()) {
      try { process.kill(p.pid, sig); } catch (e) { if (e.code !== "ESRCH") trackingError = String(e).slice(0,300); }
    } };
    collect(); const poll = setInterval(collect, 50);
    const timer = setTimeout(() => {
      timedOut = true; signal("SIGTERM");
      killTimer = setTimeout(() => { signal("SIGSTOP"); signal("SIGKILL"); }, 1000);
    }, options.timeoutMs || 40000);
    child.on("error", error => { clearTimeout(timer); clearTimeout(killTimer); clearInterval(poll); reject(error); });
    child.on("close", async (code, exitSignal) => {
      clearTimeout(timer); clearTimeout(killTimer);
      // Detached descendants may survive the direct child and close its pipe handles.
      signal("SIGSTOP"); signal("SIGKILL");
      await new Promise(r => setTimeout(r,100)); collect(); signal("SIGKILL");
      await new Promise(r => setTimeout(r,100)); clearInterval(poll);
      resolve({ code, signal: exitSignal, timedOut, elapsedMs: Date.now()-start, output,
        trackedProcesses: tracked.size, cleanupIncomplete: alive().length > 0, trackingError });
    });
  });
}
async function childCase(config) {
  const playwright = require("playwright"), text = makeFixture(config.rows);
  const dir = config.dir, html = fs.readFileSync(path.join(__dirname, "../index.html"));
  const standalone = path.join(dir, "standalone"); fs.mkdirSync(standalone, { recursive: true });
  fs.writeFileSync(path.join(standalone, "index.html"), html);
  const report = { ...config, dir: undefined, status: "running", startedAt: new Date().toISOString(),
    commit: process.env.GITHUB_SHA || null, browserVersion: null, playwright: require("playwright/package.json").version,
    node: process.version, platform: process.platform, architecture: process.arch,
    standaloneSha256: sha256(html), runnerSha256: sha256(fs.readFileSync(__filename)),
    fixture: { rows: config.rows, bytes: Buffer.byteLength(text), stringUnits: text.length, sha256: sha256(text), syntheticOnly: true },
    nativePasteTested: false, offline: true, phases: [], pageErrors: [], requests: [] };
  const write = () => fs.writeFileSync(path.join(dir, "case.json"), JSON.stringify(report, null, 2) + "\n");
  let browser, page, stage = "launch";
  async function phase(name, action) {
    stage = name; const p = { name, startedAt: new Date().toISOString(), state: "running" }; report.phases.push(p); write();
    const t = performance.now(); const result = await action(); p.elapsedMs = Math.round((performance.now() - t) * 100) / 100; p.state = "completed"; write(); return result;
  }
  try {
    browser = await phase("launch", () => playwright[config.browser].launch({ headless: true })); report.browserVersion = browser.version();
    const context = await browser.newContext({ offline: true, viewport: { width: config.width, height: 700 }, locale: "en-US" });
    page = await context.newPage(); page.setDefaultTimeout(30000); page.setDefaultNavigationTimeout(15000);
    page.on("pageerror", e => { if (report.pageErrors.length < 20) report.pageErrors.push(e.message.slice(0,500)); write(); });
    page.on("request", r => { if (/^https?:/.test(r.url()) && report.requests.length < 20) { report.requests.push(r.url().slice(0,300)); write(); } });
    report.streamedEvents = []; report.streamedHeartbeats = [];
    await page.exposeFunction("recordInputDiagnostic", entry => {
      const target = entry.kind === "event" ? report.streamedEvents : report.streamedHeartbeats;
      if (target.length < (entry.kind === "event" ? 20 : 80)) { target.push(entry); write(); }
    });
    await phase("load-and-sample", async () => {
      await page.goto(pathToFileURL(path.join(standalone, "index.html")).href);
      await page.locator("#demo").click();
      await page.evaluate(() => {
        window.inputDiagnostic = { events: [], maxTimerGapMs: 0, ticks: 0, last: performance.now() };
        const d = window.inputDiagnostic;
        for (const type of ["paste", "beforeinput", "input"]) document.querySelector("#csv").addEventListener(type, e => {
          if (d.events.length < 20) {
            const entry = { kind: "event", type, inputType: e.inputType || null, isTrusted: e.isTrusted, valueLength: e.target.value.length, atMs: performance.now() };
            d.events.push(entry); window.recordInputDiagnostic(entry).catch(() => {});
          }
        });
        setInterval(() => { const now = performance.now(); d.maxTimerGapMs = Math.max(d.maxTimerGapMs, now - d.last); d.last = now; d.ticks++;
          if (d.ticks % 10 === 0) window.recordInputDiagnostic({ kind: "heartbeat", atMs: now, maxTimerGapMs: d.maxTimerGapMs, ticks: d.ticks }).catch(() => {});
        }, 50);
      });
    });
    const paint = () => page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    if (config.method === "file-closed" || config.method === "reopen-after-file") {
      await phase("file-import-closed", async () => {
        await page.locator("#file").setInputFiles({ name: "synthetic.csv", mimeType: "text/csv", buffer: Buffer.from(text) });
        await page.waitForFunction(n => document.querySelector("#count-records").textContent === n.toLocaleString("en-US") && !document.querySelector("#results").hidden, config.rows);
        await paint();
      });
      if (config.method === "reopen-after-file") {
        await phase("toggle-populated-textarea", () => page.locator("#paste-details summary").click());
        report.detailsOpen = await phase("observe-details-open", () => page.locator("#paste-details").evaluate(e => e.open));
        if (report.detailsOpen !== true) throw new Error("Details did not open");
        await phase("paint-after-open", paint);
      }
    } else {
      await phase("open-small-textarea", async () => { await page.locator("#paste-details summary").click(); await paint(); });
      if (config.method === "fill-open") await phase("playwright-fill", () => page.locator("#csv").fill(text));
      else {
        await phase("programmatic-value-assignment", () => page.locator("#csv").evaluate((element, value) => { element.value = value; }, text));
        await phase("synthetic-input-dispatch", () => page.locator("#csv").evaluate(element => { element.dispatchEvent(new Event("input", { bubbles: true })); }));
      }
      await phase("paint-after-input", paint);
      await phase("review-after-input", async () => { await page.locator("#review").click(); await paint(); });
    }
    await phase("verify-result", async () => {
      report.observed = await page.evaluate(() => ({ length: document.querySelector("#csv").value.length,
        records: document.querySelector("#count-records").textContent, errors: document.querySelector("#count-errors").textContent,
        warnings: document.querySelector("#count-warnings").textContent, resultsVisible: !document.querySelector("#results").hidden,
        inputDiagnostic: window.inputDiagnostic, documentWidth: document.documentElement.scrollWidth, viewport: innerWidth }));
      report.valueMatches = await page.locator("#csv").evaluate((e, expected) => e.value === expected, text);
      const o = report.observed; report.resultMatches = report.valueMatches && o.length === text.length && o.records === config.rows.toLocaleString("en-US") && o.errors === (config.rows * 4).toLocaleString("en-US") && o.warnings === config.rows.toLocaleString("en-US") && o.resultsVisible;
      if (!report.resultMatches || report.requests.length || report.pageErrors.length) throw new Error("Unexpected result, request or page error");
      });
    await phase("scroll-results", () => page.locator(".stats").scrollIntoViewIfNeeded());
    await phase("optional-screenshot", async () => {
      try { await page.screenshot({ path: path.join(dir,"result.png"), timeout: 1000 }); report.screenshotCaptured = true; }
      catch (e) { report.captureFailure = String(e.message).slice(0,200); report.screenshotCaptured = false; }
    });
    report.status = "completed";
  } catch (error) {
    report.status = error.name === "TimeoutError" ? "automation_timeout" : "error";
    report.failure = { stage, name: error.name, message: String(error.message).slice(0,500) }; write();
    // Do not echo giant locator arguments or let screenshots hide the original phase.
    if (page) await phase("failure-screenshot", async () => {
      try { await page.screenshot({ path: path.join(dir,"failure.png"), timeout: 1000 }); }
      catch (e) { report.captureFailure = String(e.message).slice(0,200); }
    });
  } finally { write(); if (browser) await phase("close-browser", () => browser.close()); report.finishedAt = new Date().toISOString(); write(); }
}
async function main() {
  const browser = process.env.WATER_BROWSER || "chromium";
  if (!["chromium", "firefox"].includes(browser)) throw new Error("Unsupported browser");
  const cases = validateCases(process.env.WATER_INPUT_CASES ? JSON.parse(process.env.WATER_INPUT_CASES) : caseMatrix());
  const dir = process.env.WATER_INPUT_QA_DIR || fs.mkdtempSync(path.join(os.tmpdir(), "water-input-diagnostics-")); fs.mkdirSync(dir, { recursive: true });
  const summary = { kind: "bounded synthetic diagnostics, not performance acceptance", browser, nativePasteTested: false,
    commit: process.env.GITHUB_SHA || null, startedAt: new Date().toISOString(), caseBudgetMs: 40000, totalBudgetMs: 420000, cases: [] };
  const start = Date.now(); let invalid = false;
  for (let i=0; i<cases.length; i++) {
    const config = { ...cases[i], browser, dir: path.join(dir, String(i+1).padStart(2,"0")+"-"+cases[i].method+"-"+cases[i].rows+"-"+cases[i].width+"-r"+cases[i].repeat) };
    if (Date.now()-start > 380000) { summary.cases.push({ ...config, dir: undefined, status: "budget_skipped" }); invalid = true; continue; }
    fs.mkdirSync(config.dir, { recursive: true });
    const execution = await runProcess(process.execPath, [__filename,"--child"], { env: { ...process.env, WATER_INPUT_CASE: JSON.stringify(config) } });
    const reportPath = path.join(config.dir,"case.json");
    const report = fs.existsSync(reportPath) ? JSON.parse(fs.readFileSync(reportPath,"utf8")) : { ...config, dir: undefined, status: "missing_report" };
    report.process = { ...execution, output: undefined };
    if (execution.timedOut) {
      if (report.status !== "error") report.status = "watchdog_timeout";
      report.timeoutStage = report.phases && report.phases.findLast(p => p.state === "running")?.name || "unknown";
    } else if (report.status === "automation_timeout") report.timeoutStage = report.failure.stage;
    if (report.timeoutStage) {
      report.timeoutClassification = isDiagnosticTimeout(report.timeoutStage) ? "measured-path finding" : "setup-or-cleanup failure";
      if (!isDiagnosticTimeout(report.timeoutStage)) invalid = true;
    }
    if (execution.cleanupIncomplete || execution.trackingError || ["error","missing_report"].includes(report.status) || execution.code !== 0 && !execution.timedOut) { invalid = true; report.process.output = execution.output.slice(0,1000); }
    summary.cases.push(report);
    fs.writeFileSync(path.join(dir,"summary.json"), JSON.stringify(summary,null,2)+"\n");
    console.log(JSON.stringify({ method:config.method, rows:config.rows, width:config.width, repeat:config.repeat, status:report.status, elapsedMs:execution.elapsedMs, failure:report.failure && { stage:report.failure.stage, name:report.failure.name } }));
  }
  summary.finishedAt = new Date().toISOString(); summary.observationComplete = !invalid;
  summary.meaning = "Recorded timeouts are diagnostic findings, not passing performance claims. No native clipboard paste was tested.";
  fs.writeFileSync(path.join(dir,"summary.json"), JSON.stringify(summary,null,2)+"\n");
  if (invalid) process.exitCode = 1;
}
module.exports = { makeFixture, caseMatrix, validateCases, runProcess, isDiagnosticTimeout, processStat };
if (require.main === module) (process.argv.includes("--child") ? childCase(JSON.parse(process.env.WATER_INPUT_CASE)) : main()).catch(e => { console.error(String(e).slice(0,1000)); process.exitCode=1; });
