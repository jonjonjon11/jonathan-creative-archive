# ALS evidence map: six-record research candidate

**Snapshot: 2026-11-07. Draft research candidate. Not comprehensive and not independently reviewed by an ALS clinician.**

This small, hand-curated map separates molecular mechanisms, biomarkers, clinical outcomes, sponsor announcements, and regulatory decisions. It is a starting point for public computational evidence organization, not a systematic review, efficacy ranking, patient prediction, treatment recommendation, or clinical decision tool.

## Bounded follow-up added 2026-11-08

[VALOR/OLE follow-up](VALOR_OLE_FOLLOWUP.md) separately extracts selected final-report outcomes, supplemental methods and limits. The six historical records and their 2026-11-07 access dates are preserved; this is not a whole-map refresh. The companion uses its own schema 1.0.0 in `data/valor_ole_followup.json`, claim-level source locations and 2026-11-08 access dates. See [review scope and tests](REVIEW_VALOR_OLE.md). Independent AI extraction/software review is distinct from ALS clinician review, which has not occurred.

## Read and reproduce

- `EVIDENCE_MAP.md`: generated human-readable records.
- `data/records.json`: structured observations and their supporting source identifiers.
- `data/sources.json`: exact public URLs, publication-date precision, source class, access observations, and reuse notes.
- `SOURCE_ACCESS.md`: generated source/access register, including unsuccessful retrievals.
- `tools/validate.py`: offline structural and curation safeguards.
- `tests/test_validation.py`: deterministic validation and mutation tests.
- `MANIFEST.sha256`: hashes of the candidate's files, excluding the manifest itself and interpreter caches.

Run with Python 3.10 or later, using only its standard library:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/render.py
python3 tools/render.py --check
sha256sum -c MANIFEST.sha256
```

`render.py` deterministically regenerates the two historical Markdown views and the follow-up companion. The validator checks both schemas, including separate analysis identity, source locators, denominators and nominal inference. It cannot establish the truth of source claims or the adequacy of an analysis. Hashes and passing tests prove local file integrity and consistency, not scientific correctness. No test contacts the internet or re-estimates trial statistics. A reviewer must revisit cited sources and examine methods, protocols, amendments, and supplements before reuse.

## Selection and interpretation

The six topics were selected in advance: tofersen/SOD1; ulefnersen/FUS; QRL-201/STMN2; DNL343; Relyvrio withdrawal; UNC13A mechanism. Selection is purposive and omits many important ALS treatments and studies. Searches were targeted by intervention, trial identifier, primary publisher, sponsor, regulator, and mechanism. They are not an exhaustive search strategy. Access date is not the date of the experiment or proof that the page is current.

Numeric values are transcriptions of public aggregate reports, not calculations from participant data. No PRO-ACT, restricted consortium data, genomic files, individual patient records, or uncontrolled patient anecdotes were used. No remote repository, trial registry, clinical system, or public website was changed.

An observation's `source_ids` bind the entire observation, including its statistic, to its evidence. Record-level source identifiers support population/design context. Null statistics mean unavailable or inapplicable, never zero. A reported primary failure is retained even if a biomarker improves. A favorable sponsor report is not relabeled peer-reviewed. Investigational status is a dated source description, not a search of every jurisdiction's current approvals.

Schema 1.1.0 separates statistical methods: tofersen's primary joint-rank test with multiple imputation (p = .97) is a different observation from its supportive ANCOVA/MI adjusted mean difference and confidence interval (p = .60). Statistics explicitly identify the analysis and p-value method, including when a sponsor release does not specify the test.

Regulatory fields are typed and must match a dated, record-specific assertion in an in-record cited source. Approvals and withdrawals require a retrieved regulator source type. These assertions are curated extractions, not an independent truth oracle: metadata and matching assertions could both be wrong. Positive synthetic tests demonstrate that a newly sourced status can be accepted rather than permanently fixing a drug's current status. Snapshot-specific clinical guardrails protect selected historical extractions, not all future evidence.

Dates distinguish original publication, source-described events, retrieval, and archive cutoff. The April 2024 Relyvrio announcement is deliberately separate from FDA's August 2025 approval withdrawal. Registry links whose pages did not render are navigation aids only; their contents were not treated as verified. QRL-201's phase and endpoint descriptions are explicitly attributed to sponsor reports from different dates.

## Limitations and review before publication

1. Recheck every claim against full methods and statistical-analysis plans. Selected source sections, not all supplements, were read. VALOR's publisher page was unavailable; its numerical findings were cross-checked against the accessible original FDA label.
2. Resolve trial-registry access gaps and inspect amendment histories, especially ANQUR's phase terminology and endpoint hierarchy. Do not silently treat a 2024 sponsor description as a verified 2026 protocol.
3. Review later publications, regulator updates, and safety evidence. This is not a complete current safety/benefit assessment. The historical tofersen label is intentionally identified as historical.
   - Significant named omission: [Long-Term Tofersen in SOD1 Amyotrophic Lateral Sclerosis](https://jamanetwork.com/journals/jamaneurology/fullarticle/2843130), published online December 22, 2025 (February 2026 issue), reports final integrated VALOR/OLE results. Its longer-term efficacy and safety results remain outside this historical tofersen record. Selected findings are now in the separately dated [follow-up companion](VALOR_OLE_FOLLOWUP.md); broader later evidence and original SAP versions remain unverified.
4. Obtain independent ALS clinical and research-methods review. No such review has occurred here. Absence of a reported result is not evidence that no result exists.
5. Keep third-party articles and figures out of this package unless their reuse rights are checked. This package contains original concise summaries and references, not copies of source articles or underlying datasets. Original code and original concise summaries follow the repository's root [Creative Commons Attribution 4.0 International (CC BY 4.0) license](../../LICENSE). Cited articles, figures, datasets, and sponsor materials retain their own rights and licenses; citations do not relicense them.

## Computational research next steps

Useful follow-on work is evidence maintenance: compare protocol versions, pre-specify extraction fields, independently double-extract effect sizes and denominators, and audit how conclusions change when sponsor-only or post-hoc findings are excluded. Do not pool these six heterogeneous records into a treatment score or meta-analysis: endpoints, populations, designs, stages, and comparators differ substantially.
