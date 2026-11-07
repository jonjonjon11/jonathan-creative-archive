(function () {
  "use strict";
  const P = window.WaterPreflight;
  const $ = id => document.getElementById(id);
  const sample = '__SAMPLE__';
  let result = null, mapping = null, headerKey = null, page = 0, generation = 0;
  const perPage = 100;
  function el(tag, text, className) { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; }
  function status(text) { $("input-status").textContent = text; }
  function invalidate(message) {
    result = null; $("results").hidden = true; $("include-values").checked = false;
    $("issues").replaceChildren(); $("result-summary").textContent = ""; $("page-summary").textContent = "";
    $("review-state").textContent = ""; $("pagination").hidden = true;
    for (const id of ["count-records", "count-errors", "count-warnings"]) $(id).textContent = "0";
    status(message || "Input changed. Review again to refresh findings.");
  }
  function buildMapping(headers) {
    const key = JSON.stringify(headers);
    if (headerKey === key && mapping) return;
    headerKey = key; mapping = P.autoMapping(headers);
    const container = $("mapping"); container.replaceChildren();
    for (const field of P.FIELDS) {
      const wrapper = el("div", undefined, "map-field"), label = el("label", field.label + " ");
      const id = "map-" + field.key; label.htmlFor = id;
      label.append(el("small", field.need === "required" ? "required" : field.need === "either" ? "one of these two" : "optional"));
      const select = el("select"); select.id = id;
      const none = el("option", "Not mapped"); none.value = ""; select.append(none);
      headers.forEach((header, index) => { const option = el("option", (index + 1) + ". " + (header.length > 100 ? header.slice(0, 97) + "…" : header)); option.value = String(index); select.append(option); });
      select.value = mapping[field.key] === null ? "" : String(mapping[field.key]);
      select.addEventListener("change", () => { mapping[field.key] = select.value === "" ? null : Number(select.value); invalidate("Column mapping changed. Review again to apply it."); });
      wrapper.append(label, select); container.append(wrapper);
    }
  }
  function review() {
    const text = $("csv").value;
    const parsed = P.parseCSV(text);
    if (!parsed.error && parsed.records.length) { buildMapping(parsed.records[0].cells); $("mapping-panel").hidden = false; }
    else { $("mapping-panel").hidden = true; mapping = null; headerKey = null; }
    result = P.checkCSV(text, mapping ? { mapping } : {});
    page = 0; $("filter").value = "all"; $("include-values").checked = false;
    const c = result.counts;
    $("count-records").textContent = c.records.toLocaleString();
    $("count-errors").textContent = c.errors.toLocaleString();
    $("count-warnings").textContent = c.warnings.toLocaleString();
    $("review-state").textContent = result.complete ? "Checks finished" : "Review incomplete";
    $("result-summary").textContent = (result.complete ? "Reviewed " + c.reviewed + " data records. " : "Could not complete all field checks. Reviewed " + c.reviewed + " of " + c.records + " data records. ") +
      (c.errors + c.warnings ? "Inspect the findings below before deciding what to change." : "No issues found by these limited checks. Human verification is still needed.") +
      (c.skippedBlankLines ? " Skipped " + c.skippedBlankLines + " empty physical line(s)." : "") +
      (result.omittedIssues ? " Only the first " + P.LIMITS.issues + " findings are shown and exported; " + result.omittedIssues + " further findings were counted but omitted. Fix these issues and review again." : "");
    $("results").hidden = false;
    renderIssues();
    status("Review finished in this tab. Reference date: " + result.referenceDate + " (UTC). Original file unchanged.");
    $("results").focus();
  }
  function renderIssues() {
    if (!result) return;
    const filter = $("filter").value;
    const all = result.issues.filter(issue => filter === "all" || issue.severity === filter);
    const pages = Math.max(1, Math.ceil(all.length / perPage)); page = Math.min(page, pages - 1);
    const start = page * perPage, selected = all.slice(start, start + perPage);
    $("page-summary").textContent = all.length ? (start + 1) + "–" + (start + selected.length) + " of " + all.length + " retained findings" : "No findings in this view";
    const target = $("issues"); target.replaceChildren();
    if (!selected.length) target.append(el("p", "No findings in this view. This does not establish data quality or water safety.", "empty"));
    for (const issue of selected) {
      const article = el("article", undefined, "issue"), aside = el("div"), body = el("div");
      aside.append(el("span", issue.severity, "severity " + issue.severity), el("span", issue.record === null ? "File / mapping" : "Record " + issue.record + " · line " + issue.line, "location"));
      body.append(el("h3", issue.field + " · " + issue.code), el("p", issue.message));
      if (issue.value !== "") body.append(el("code", issue.value));
      body.append(el("span", "Rule basis: " + issue.basis, "basis")); article.append(aside, body); target.append(article);
    }
    $("pagination").hidden = pages <= 1; $("previous").disabled = page === 0; $("next").disabled = page >= pages - 1;
  }
  function download() {
    if (!result) return;
    const include = $("include-values").checked;
    const exported = { ...result, generatedAt: new Date().toISOString(), inputValuesIncluded: include, headers: include ? result.headers : undefined,
      issues: result.issues.map(issue => ({ ...issue, value: include ? issue.value : undefined })) };
    const blob = new Blob([JSON.stringify(exported, null, 2) + "\n"], { type: "application/json" });
    const url = URL.createObjectURL(blob), a = el("a"); a.href = url; a.download = "water-point-preflight-report.json";
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status("A local report download was requested. It omits " + (include ? "no issue values; review carefully before sharing." : "input headers and values; review before sharing."));
  }
  $("review").addEventListener("click", review); $("review-mapping").addEventListener("click", review);
  $("csv").addEventListener("input", () => { generation++; invalidate(); });
  $("demo").addEventListener("click", () => { generation++; $("file").value = ""; $("csv").value = sample; headerKey = null; mapping = null; invalidate(); review(); status("Synthetic example loaded and reviewed. Every observation is invented; the deliberate issues are for practice."); });
  $("clear").addEventListener("click", () => { generation++; $("file").value = ""; $("csv").value = ""; mapping = null; headerKey = null; $("mapping").replaceChildren(); $("mapping-panel").hidden = true; $("paste-details").open = false; invalidate("Cleared this tab’s visible data and findings. Previously downloaded files, clipboard contents, and browser history are not erased."); $("file").focus(); });
  $("file").addEventListener("change", async () => {
    const token = ++generation, file = $("file").files[0];
    if (!file) return;
    $("csv").value = ""; mapping = null; headerKey = null; $("mapping-panel").hidden = true; invalidate("Reading the local file…");
    if (file.size > 5000000) { status("File is larger than 5 MB. Export a smaller UTF-8 CSV. Nothing was reviewed."); return; }
    try {
      const bytes = await file.arrayBuffer();
      if (token !== generation) return;
      $("csv").value = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
      review();
    } catch (error) {
      if (token !== generation) return;
      status("Could not read this file as UTF-8 text. Export a UTF-8 CSV and try again. Nothing was reviewed.");
    }
  });
  $("filter").addEventListener("change", () => { page = 0; renderIssues(); });
  $("previous").addEventListener("click", () => { page--; renderIssues(); $("filter").focus(); });
  $("next").addEventListener("click", () => { page++; renderIssues(); $("filter").focus(); });
  $("download").addEventListener("click", download);
})();
