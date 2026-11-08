"use strict";
// Optional test-only dependency. Uses an installed Playwright browser; never installs anything.
// Only synthetic fixtures and an isolated copy of the standalone HTML are exercised.
const playwright = require("playwright");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const { pathToFileURL } = require("node:url");
const P = require("../src/core.js");
const { makeInjectionFixture } = require("./fixtures.cjs");

(async () => {
  const browserName = process.env.WATER_BROWSER || "chromium";
  if (!["chromium", "firefox"].includes(browserName)) throw new Error("WATER_BROWSER must be chromium or firefox");
  const dir = process.env.WATER_QA_DIR ? path.resolve(process.env.WATER_QA_DIR) : fs.mkdtempSync(path.join(os.tmpdir(), "water-preflight-qa-"));
  fs.mkdirSync(dir, { recursive: true });
  const standalone = fs.mkdtempSync(path.join(dir, "standalone-"));
  const html = fs.readFileSync(path.join(__dirname, "../index.html"));
  const isolatedFile = path.join(standalone, "index.html");
  fs.writeFileSync(isolatedFile, html);
  assert.deepEqual(fs.readdirSync(standalone), ["index.html"]);
  const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
  const checks = [], errors = [], network = [], cspErrors = [], screenshots = [];
  const summary = {
    startedAt: new Date().toISOString(), status: "running", browser: browserName,
    playwright: require("playwright/package.json").version, node: process.version,
    platform: process.platform, architecture: process.arch, commit: process.env.GITHUB_SHA || null,
    standaloneSha256: sha256(html), runnerSha256: sha256(fs.readFileSync(__filename)),
    networking: "offline", syntheticDataOnly: true, standaloneFiles: ["index.html"],
    limitations: "Scoped desktop-browser automation only; not physical-device, comprehensive accessibility, practitioner-effectiveness, WPdx-certification or water-safety acceptance."
  };
  let browser, page;
  const pass = message => { checks.push(message); console.log("PASS: " + message); };
  try {
    const executablePath = process.env.WATER_BROWSER_EXECUTABLE || (browserName === "chromium" ? process.env.CHROMIUM : undefined);
    browser = await playwright[browserName].launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
    summary.browserVersion = browser.version();
    const context = await browser.newContext({ offline: true, acceptDownloads: true, locale: "en-US", viewport: { width: 1280, height: 900 } });
    page = await context.newPage();
    page.on("pageerror", e => errors.push(e.message));
    page.on("request", r => { if (/^https?:/.test(r.url())) network.push(r.url()); });
    page.on("console", msg => { if (msg.type() === "error" && /Content Security Policy|Refused to/.test(msg.text())) cspErrors.push(msg.text()); });
    await page.goto(pathToFileURL(isolatedFile).href);
    await page.getByRole("button", { name: "Try a synthetic example" }).click();
    assert.equal(await page.locator("#count-errors").textContent(), "3");
    assert.equal(await page.locator("#count-warnings").textContent(), "9");
    assert.equal(await page.locator("#results").evaluate(e => e === document.activeElement), true);
    assert.equal(await page.locator(".issue").count(), 12);
    pass("file:// standalone loads with browser networking offline and synthetic fixture produces expected findings");
    await page.screenshot({ path: path.join(dir, "desktop-findings.png"), fullPage: true }); screenshots.push("desktop-findings.png");
    await page.locator("#filter").selectOption("error");
    assert.equal(await page.locator(".issue").count(), 3);
    await page.locator("#filter").selectOption("warning");
    assert.equal(await page.locator(".issue").count(), 9);
    pass("severity filters use text labels and correct counts");
    const report = page.waitForEvent("download");
    await page.locator("#download").click();
    const downloaded = await report;
    const reportPath = path.join(dir, "default-report.json"); await downloaded.saveAs(reportPath);
    const json = JSON.parse(fs.readFileSync(reportPath, "utf8"));
    assert.equal(json.inputValuesIncluded, false); assert.equal(json.headers, undefined);
    assert(json.issues.every(issue => issue.value === undefined));
    assert.equal(json.issues.length, 12);
    pass("default local JSON report omits input values and headers and exports all severities");
    await page.locator("#include-values").check();
    const fullReport = page.waitForEvent("download"); await page.locator("#download").click();
    const fullPath = path.join(dir, "opt-in-report.json"); await (await fullReport).saveAs(fullPath);
    const full = JSON.parse(fs.readFileSync(fullPath, "utf8"));
    assert.equal(full.inputValuesIncluded, true); assert(full.headers.length > 0);
    assert(full.issues.every(issue => typeof issue.value === "string"));
    assert(full.issues.some(issue => issue.code === "STATUS_REVIEW" && issue.value === "Functional"));
    pass("values enter the exported report only after explicit local checkbox choice");
    await page.locator("#file").setInputFiles(path.join(__dirname, "../fixtures/synthetic-clean.csv"));
    await page.waitForFunction(() => document.querySelector("#count-records").textContent === "2" && !document.querySelector("#results").hidden);
    assert.equal(await page.locator("#count-errors").textContent(), "0"); assert.equal(await page.locator("#count-warnings").textContent(), "0");
    assert.match(await page.locator("#result-summary").textContent(), /Human verification/);
    assert.equal(await page.locator("#include-values").isChecked(), false);
    pass("real UTF-8 file-picker read works offline, resets export consent, and avoids an official pass claim");
    const clean = fs.readFileSync(path.join(__dirname, "../fixtures/synthetic-clean.csv"), "utf8");
    await page.locator("#paste-details").evaluate(e => e.open = true);
    await page.locator("#csv").fill(clean.replace("#lat_deg", "My GPS latitude"));
    assert.equal(await page.locator("#results").isVisible(), false);
    await page.locator("#review").click(); assert.match(await page.locator("#issues").textContent(), /MAPPING_REQUIRED/);
    await page.locator("#map-lat_deg").selectOption("0");
    assert.equal(await page.locator("#results").isVisible(), false);
    await page.locator("#review-mapping").click(); assert.equal(await page.locator("#count-errors").textContent(), "0");
    pass("edits and mapping changes invalidate old results; explicit custom-header mapping restores review");
    const attack = makeInjectionFixture(clean);
    const parsedAttack = P.parseCSV(attack);
    assert.equal(parsedAttack.error, null, "DOM-injection fixture must be valid CSV before browser interaction");
    assert.equal(parsedAttack.records[0].cells[0], '<img src=x onerror="window.pwned=1">');
    await page.locator("#csv").fill(attack); await page.locator("#review").click();
    await page.locator("#map-lat_deg").selectOption("0"); await page.locator("#review-mapping").click();
    assert.equal(await page.evaluate(() => window.pwned), undefined);
    assert.equal(await page.locator("#mapping img, #issues script, #issues img").count(), 0);
    assert.match(await page.locator("#issues").textContent(), /<script>/);
    pass("HTML-like headers and values render as inert text without DOM injection");
    const many = "lat_deg,lon_deg,report_date,status_id,source,water_source\n" + Array.from({ length: 2050 }, (_, i) => `999,32.4567,2024-01-01,Yes,Synthetic ${i},Borehole`).join("\n");
    await page.locator("#csv").fill(many); await page.locator("#review").click();
    assert.equal(await page.locator(".issue").count(), 100);
    assert.match(await page.locator("#result-summary").textContent(), /50 further findings/);
    await page.locator("#next").click(); assert.match(await page.locator("#page-summary").textContent(), /101–200/);
    await page.locator("#previous").click(); assert.match(await page.locator("#page-summary").textContent(), /1–100/);
    pass("large finding sets paginate and disclose the retained-issue cap without losing aggregate error counts");
    await page.locator("#csv").fill('a,b\n"unclosed'); await page.locator("#review").click();
    assert.match(await page.locator("#review-state").textContent(), /incomplete/);
    assert.match(await page.locator("#issues").textContent(), /CSV_QUOTE/);
    assert.equal(await page.locator("#mapping-panel").isVisible(), false);
    pass("malformed CSV explicitly aborts review and hides stale mappings");
    await page.locator("#file").setInputFiles({ name: "invalid.csv", mimeType: "text/csv", buffer: Buffer.from([0xFF, 0xFE, 0x41, 0x00]) });
    await page.waitForFunction(() => document.querySelector("#input-status").textContent.includes("Could not read"));
    assert.equal(await page.locator("#results").isVisible(), false);
    pass("non-UTF-8 file fails explicitly without stale findings");
    await page.locator("#file").setInputFiles({ name: "too-big.csv", mimeType: "text/csv", buffer: Buffer.alloc(5000001, 65) });
    await page.waitForFunction(() => document.querySelector("#input-status").textContent.includes("larger than 5 MB"));
    pass("file byte limit enforced before reading");
    await page.getByRole("button", { name: "Try a synthetic example" }).click();
    await page.getByRole("button", { name: "Try a synthetic example" }).click();
    assert.equal(await page.locator(".issue").count(), 12);
    await page.locator("#clear").click();
    assert.equal(await page.locator("#csv").inputValue(), ""); assert.equal(await page.locator("#results").isVisible(), false);
    assert.equal(await page.locator("#mapping-panel").isVisible(), false); assert.equal(await page.locator("#file").inputValue(), "");
    pass("repeated sample loads do not duplicate findings; Clear removes visible input, mappings, and results");
    await page.getByRole("button", { name: "Try a synthetic example" }).click();
    await page.locator("#include-values").check();
    assert.equal(await page.locator("#include-values").isChecked(), true);
    await page.reload();
    assert.equal(await page.locator("#results").isVisible(), false);
    assert.equal(await page.locator("#include-values").isChecked(), false);
    pass("native reload does not restore a completed review or opt-in export choice");
    await page.keyboard.press("Tab");
    assert.equal(await page.evaluate(() => document.activeElement.className), "skip");
    await page.keyboard.press("Enter");
    await page.getByRole("button", { name: "Try a synthetic example" }).focus(); await page.keyboard.press("Enter");
    assert.equal(await page.locator("#results").isVisible(), true);
    const labels = await page.locator("input,select,textarea").evaluateAll(nodes => nodes.every(n => (n.labels && n.labels.length) || n.hasAttribute("aria-label")));
    assert.equal(labels, true); assert.equal(await page.locator("main").count(), 1);
    pass("keyboard skip link, keyboard sample action, result focus, and form labels checked");
    const storage = await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length, cookie: document.cookie }));
    assert.deepEqual(storage, { local: 0, session: 0, cookie: "" });
    assert.equal(network.length, 0); assert.deepEqual(errors, []); assert.deepEqual(cspErrors, []);
    pass("no HTTP(S) requests, page errors, CSP violations, cookies, or web-storage entries observed");
    for (const viewport of [{ width: 390, height: 844 }, { width: 320, height: 700 }]) {
      await page.setViewportSize(viewport);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
      const filename = `narrow-${viewport.width}-findings.png`;
      await page.screenshot({ path: path.join(dir, filename), fullPage: true }); screenshots.push(filename);
      await page.locator("#filter").selectOption("error");
      assert.equal(await page.locator(".issue").count(), 3);
      const narrowDownload = page.waitForEvent("download"); await page.locator("#download").click();
      const narrowPath = path.join(dir, `narrow-${viewport.width}-report.json`);
      await (await narrowDownload).saveAs(narrowPath);
      const narrowReport = JSON.parse(fs.readFileSync(narrowPath, "utf8"));
      assert.equal(narrowReport.inputValuesIncluded, false); assert.equal(narrowReport.issues.length, 12);
      await page.locator("#clear").click();
      assert.equal(await page.locator("#results").isVisible(), false);
      await page.getByRole("button", { name: "Try a synthetic example" }).click();
      assert.equal(await page.locator(".issue").count(), 12);
      pass(`${viewport.width}-pixel viewport has no horizontal overflow and supports filtering, a real download, Clear and repeat review`);
    }
    // The large result cap must remain usable at the narrowest viewport too.
    await page.locator("#paste-details").evaluate(e => e.open = true);
    const large = "lat_deg,lon_deg,report_date,status_id,source,water_source\n" + Array.from({ length: 25000 }, (_, i) =>
      `999,999,2024-02-30,Unknown,,Unknown ${i}`).join("\n");
    await page.locator("#csv").fill(large); await page.locator("#review").click();
    assert.equal(await page.locator("#count-records").textContent(), "25,000");
    assert.equal(await page.locator("#count-errors").textContent(), "100,000");
    await page.locator(".stats").scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(dir, "maximum-counts.png") }); screenshots.push("maximum-counts.png");
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    assert.equal(await page.locator(".stats strong").evaluateAll(nodes => nodes.every(node => node.scrollWidth <= node.clientWidth)), true);
    pass("maximum record count and six-digit error total fit the 320-pixel viewport");
    // Separate positive-control CSP probe: no remote target, data, or policy relaxation.
    const probe = await context.newPage();
    await probe.goto(pathToFileURL(isolatedFile).href);
    await probe.evaluate(() => {
      window.policyViolations = [];
      document.addEventListener("securitypolicyviolation", event => window.policyViolations.push(event.effectiveDirective));
      const script = document.createElement("script"); script.textContent = "window.unapprovedScriptRan = true";
      document.body.append(script);
      fetch("data:text/plain,synthetic-csp-probe").catch(() => {});
    });
    await probe.waitForFunction(() => window.policyViolations.some(x => x.startsWith("script-src")) && window.policyViolations.includes("connect-src"));
    assert.equal(await probe.evaluate(() => window.unapprovedScriptRan), undefined);
    summary.cspProbeViolations = await probe.evaluate(() => window.policyViolations);
    await probe.close();
    pass("separate CSP probe blocks an unapproved inline script and a data-URL fetch without contacting a remote service");
    assert.equal(network.length, 0); assert.deepEqual(errors, []); assert.deepEqual(cspErrors, []);
    summary.status = "passed";
  } catch (error) {
    summary.status = "failed";
    summary.failure = { name: error.name, message: error.message, stack: error.stack };
    if (page && !page.isClosed()) {
      try { await page.screenshot({ path: path.join(dir, "failure.png"), fullPage: true }); screenshots.push("failure.png"); }
      catch (captureError) { summary.screenshotFailure = captureError.message; }
    }
    throw error;
  } finally {
    Object.assign(summary, { checkedAt: new Date().toISOString(), passed: checks.length, checks,
      httpRequests: network.length, requestUrls: network, pageErrors: errors, cspErrors, screenshots });
    fs.writeFileSync(path.join(dir, "summary.json"), JSON.stringify(summary, null, 2) + "\n");
    console.log("QA output: " + dir);
    if (browser) await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
