# VALOR/OLE companion: extraction and review record

Date: 2026-11-08. Base archive commit: `410831e`.

**Draft public-aggregate research organization only. Independent AI source extraction and software review are not independent ALS clinician review, clinical endorsement, reanalysis of participant data, or proof of scientific validity.**

## Scope and preservation

The [companion](VALOR_OLE_FOLLOWUP.md) addresses a named omission in the historical six-record map. It adds selected function, survival, biomarker and neurological-safety observations from the final VALOR/OLE report, each with analysis identity and exact source locations. Seven observations use two source entries, referring to the article and its supplement. The original 15 observations, historical dates and original regulatory assertion remain unchanged; navigation and scope notes now point to the companion.

The companion has a separate schema and retrieval date. It does not imply that all historical sources were re-read on November 8. It does not update approval status, infer completed confirmatory obligations, rank treatments, forecast patients, or extrapolate SOD1 findings to all ALS. Quality-of-life, natural-history comparisons, EMPOWER simulations, and detailed subgroup estimates are not extracted in this bounded addition. The original statistical-analysis-plan files and amendment history remain unverified.

## Primary-source review

Source: [Miller et al., Long-Term Tofersen in SOD1 Amyotrophic Lateral Sclerosis](https://jamanetwork.com/journals/jamaneurology/fullarticle/2843130), DOI `10.1001/jamaneurol.2025.4946`, online December 22, 2025, February 2026 issue. The supplement cover prints December 15, 2025; that discrepancy is recorded rather than silently harmonized.

Two separate AI review passes independently retrieved the publisher text and Supplement 1, extracted results, and reconciled the selected estimates, denominators and methods. The implementing reviewer also inspected the independently rendered eFigure 4, publisher Table 2 and Figure 2. No original article, supplemental PDF, figure or screenshot is redistributed in this archive.

The important correction during review was precision in the alternative joint-rank result: eFigure 4, PDF page 20, gives **0.0541** and labels that analysis **post hoc**. Main Table 2 rounds it to .05. The companion preserves this separately from ordinary post hoc JRT (0.1064) and ANCOVA/MI (0.1432), and does not turn rounding into a threshold-success claim. The original week-28 primary failure is retained separately.

Source entries bind model, endpoint, timepoint and estimate to the same observation. Within-arm modeled biomarker reductions remain separate from clinical outcomes. OLE completion counts are not relabeled as week-148 observed-case counts. Safety uses the 104-person exposed population rather than the 108 randomized population. Reported event resolution does not imply that the drug is risk-free.

### Source-level inconsistencies not repaired

Visual review confirmed an impossible negative upper confidence limit for slower-subgroup death in publisher Table 2, and nonmonotone delayed-group ITT risk counts in Figure 2. Those entries are excluded from the extraction, not guessed or recalculated. The selected ITT HRs agree between main text and Table 2, but underlying participant-level data were not available for re-estimation. These discrepancies remain reasons for caution and further source clarification, not proof that all reported results are invalid.

The supplement itself cautions against late survival estimates after week 192 because numbers at risk decrease. No precise causal survival extension is asserted. Attrition, crossover, nominal testing, analysis revisions, small samples and sponsor involvement remain visible.

### Retrieval fingerprints

These fingerprints identify bytes inspected during review; they do not prove correctness, authenticity, rights or permanent availability. The publisher page is the durable navigation link; its supplemental download was signed and temporary.

- Supplement 1 PDF: 1,180,704 bytes; SHA-256 `7dab464be44c78bc17f2c3b815a3fb5cc8bf50840617fa7063f53712e8967ab2`.
- Publisher Table 2 image: SHA-256 `44abdf5fa2dd6d3289633ab2515409e82ad53c3ff89798e9f7a921d6ba22d9ec`.
- Publisher Figure 2 image: SHA-256 `7c764f2a95abd08c5e0bc156d2f73bcfaf01aef097e3b065a904b9afa612544f`.

Only concise original factual summaries, bibliographic references, code and hashes are included. Root CC BY 4.0 applies to the original archive work, not the cited article or supplement, which retain their publisher-declared CC BY-NC-ND terms.

## Validation scope

The companion validator rejects unsupported analysis categories, primary-efficacy promotion, invented regulatory fields, missing primary/supplement references and locators, inconsistent denominators, impossible hazard ratios, invalid intervals, nonfinite values and lost nominal-inference labels. Tests separately pin the selected transcription values, original primary failure and exact generated views. These checks do not verify that a cited passage truly supports a claim; that requires source review.

The existing evidence-integrity auditor uses a different input format. Its clean synthetic fixture run is a regression check of that tool, **not** an audit of this companion. This companion is covered by its dedicated validator and tests.

## Test and independent review outcome

Initial local checks passed on Python 3.12.14 / Node 24.22.1:

- 65 evidence-map tests: 27 historical plus 38 companion tests.
- All eight offline Python suites and the numerical/simulated-control Node suites from the archive's `validate` CI job.
- Source/standalone parity checks, both evidence validators, exact generated views and the auditor's clean synthetic fixture.

Independent software review found and prompted fixes for analysis-identity relabeling, zero/empty denominators, malformed type handling and function units. Seven new mutation tests cover these fixes. Independent source and software reviewers subsequently approved the corrected candidate as draft research only. Neither approval is clinician review. Both schemas, all 65 ALS tests, the 13-entry manifest, root archive validation and Archive Steward (zero errors/warnings) were independently rerun. Reviewed hashes were refreshed only for this scoped change. No new browser behavior is introduced by this change. Browser suites remain repository regression checks, not medical validation.

The source reviewer verified the selected estimates against independently retrieved text and rendered primary figures, including source inconsistencies and retrieval fingerprints. The software reviewer independently checked analysis identity, zero/empty denominators, malformed labels, units, exact generated output and file coverage. No unresolved blocking finding remained in those scopes.

Exact-commit remote CI is a separate integration gate, verified on the pull request rather than asserted by this local report. Other outstanding limits remain: no ALS clinician review, no original SAP/amendment audit, no participant-level reanalysis, no complete current safety/regulatory synthesis, and no resolution from the publisher of the disclosed source anomalies.
