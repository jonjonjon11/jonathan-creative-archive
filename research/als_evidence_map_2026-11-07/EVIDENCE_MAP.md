# ALS evidence map

Snapshot: 2026-11-07. Six purposively selected records. Not comprehensive.

**Draft research candidate. Not independently reviewed by an ALS clinician. No patient predictions or treatment recommendations.**

Read README.md for selection, interpretation, reproducibility, and limitations. Source dates and access caveats are in SOURCE_ACCESS.md. A separately dated [VALOR/OLE follow-up](VALOR_OLE_FOLLOWUP.md) adds later evidence without changing the historical primary result.

## Tofersen / SOD1: VALOR and original US accelerated approval

- Record: `tofersen_sod1`
- Stage: randomized trial and regulatory decision
- Target: SOD1 mRNA
- Population: Adults with SOD1-ALS; VALOR randomized 108: 72 tofersen and 36 placebo. Faster-progression primary analysis: 60.
- Design: Phase 3 VALOR, randomized, double-blind, placebo-controlled; week-28 assessment.
- Trial identifiers: NCT02623699
- Context sources: [valor_2022](https://www.nejm.org/doi/full/10.1056/NEJMoa2204705); [qalsody_label_2023](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/215887s000lbl.pdf); [qalsody_snapshot](https://www.fda.gov/drugs/drug-trials-snapshots/drug-trials-snapshots-qalsody); [qalsody_fda_action](https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-treatment-amyotrophic-lateral-sclerosis-associated-mutation-sod1-gene); [qalsody_fda_statistics_2023](https://www.fda.gov/media/166392/download)

### Clinical primary

ALSFRS-R change from baseline, faster-progression subgroup. Timepoint: 28 weeks.

The prespecified primary joint-rank test with multiple imputation did not meet the endpoint.

Measure: joint_rank_test. Analysis: Joint-rank test with multiple imputation. Reported p-value: 0.97 (Joint-rank test with multiple imputation).

Sources: [valor_2022](https://www.nejm.org/doi/full/10.1056/NEJMoa2204705); [qalsody_fda_statistics_2023](https://www.fda.gov/media/166392/download)

### Clinical supportive

ALSFRS-R change from baseline, faster-progression subgroup; supportive analysis. Timepoint: 28 weeks.

The adjusted mean difference and confidence interval describe the supportive ANCOVA analysis, not the joint-rank test.

Measure: adjusted_mean_difference. Analysis: ANCOVA with multiple imputation. Estimate: 1.2 ALSFRS-R points. 95% confidence interval: -3.2 to 5.5. Reported p-value: 0.6 (ANCOVA with multiple imputation).

Sources: [qalsody_fda_statistics_2023](https://www.fda.gov/media/166392/download); [qalsody_label_2023](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/215887s000lbl.pdf)

### Biomarker

Plasma NfL and CSF SOD1. Timepoint: 28 weeks.

Both decreased relative to placebo; these are biomarker outcomes, not direct functional recovery.

Sources: [qalsody_label_2023](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/215887s000lbl.pdf)

### Regulatory

Original US accelerated approval. Timepoint: 2023-04-25.

FDA approval for adults with SOD1-ALS was based on plasma NfL reduction, with clinical-benefit confirmation required.

Sources: [qalsody_snapshot](https://www.fda.gov/drugs/drug-trials-snapshots/drug-trials-snapshots-qalsody); [qalsody_fda_action](https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-treatment-amyotrophic-lateral-sclerosis-associated-mutation-sod1-gene); [qalsody_label_2023](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/215887s000lbl.pdf)

**Negative or absent evidence**
- VALOR's prespecified primary clinical result was nonsignificant.

**Unknowns**
- This historical record does not synthesize all later evidence. See the separately dated VALOR_OLE_FOLLOWUP.md for the bounded final VALOR/OLE extraction.

**Caveats**
- Do not generalize SOD1-specific evidence to all ALS.
- Original 2023 label lists serious neurologic risks; this is not a current prescribing guide.
- Open-label follow-up does not replace the randomized primary analysis.

Regulatory field: original accelerated approval; jurisdiction: US; event date: 2023-04-25.

Regulatory sources: [qalsody_snapshot](https://www.fda.gov/drugs/drug-trials-snapshots/drug-trials-snapshots-qalsody); [qalsody_fda_action](https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-treatment-amyotrophic-lateral-sclerosis-associated-mutation-sod1-gene)

**Named scope exclusions**

- [valor_ole_final_2025](https://jamanetwork.com/journals/jamaneurology/fullarticle/2843130): Excluded from this original-trial/approval record. Selected final VALOR/OLE outcomes and limitations are now extracted separately in VALOR_OLE_FOLLOWUP.md, dated 2026-11-08; the historical primary result is unchanged.

## Ulefnersen / FUS: sponsor-reported FUSION topline result

- Record: `ulefnersen_fus`
- Stage: sponsor reported randomized trial
- Target: FUS RNA/protein reduction
- Population: FUS-ALS; primary analysis population 73.
- Design: FUSION: randomized, double-blind, placebo-controlled Phase 1-3 trial; 72-week controlled period, then open-label extension.
- Trial identifiers: NCT04768972
- Context sources: [fusion_ionis_2026](https://ir.ionis.com/news-releases/news-release-details/ionis-announces-positive-topline-results-phase-3-fusion-study)

### Clinical primary

Joint rank: death/permanent ventilation, rescue, and ALSFRS-R change. Timepoint: Day 505 / 72 weeks.

Sponsor reported a favorable primary comparison with placebo on 2026-09-22.

Measure: joint_rank_test. Analysis: Prespecified joint-rank analysis as described by sponsor. Reported p-value: 0.0005 (Joint-rank analysis).

Sources: [fusion_ionis_2026](https://ir.ionis.com/news-releases/news-release-details/ionis-announces-positive-topline-results-phase-3-fusion-study)

### Biomarker

Serum NfL secondary endpoint. Timepoint: Not detailed in the selected topline report.

Sponsor reported a significant favorable change; no numerical effect extracted.

Sources: [fusion_ionis_2026](https://ir.ionis.com/news-releases/news-release-details/ionis-announces-positive-topline-results-phase-3-fusion-study)

**Negative or absent evidence**
- No negative controlled efficacy finding was reported in this selected topline source; this is not evidence of absence.

**Unknowns**
- Detailed effect size, uncertainty, subgroup results, and full safety analysis were not supplied in this topline summary.

**Caveats**
- Sponsor report, not a peer-reviewed full trial report in this map.
- Rescue permits early open-label treatment after prespecified progression.
- A composite p-value does not quantify survival gain.
- Do not extrapolate to non-FUS ALS.

Regulatory field: investigational in cited source; jurisdiction: Not a jurisdiction-wide approval search; event date: 2026-09-22.

Regulatory sources: [fusion_ionis_2026](https://ir.ionis.com/news-releases/news-release-details/ionis-announces-positive-topline-results-phase-3-fusion-study)

## QRL-201 / STMN2: early ANQUR interim signals

**Registry correction checked 2026-11-08:** The registration posted 2026-05-15 lists Phase 1, 69 actual participants, a primary safety endpoint through Day 421 and three plasma-PK secondary endpoints. This resolves the registry-access/window gap below, not the unexplained sponsor Phase 1/2 terminology. [Dated extraction, amendment comparisons and limits](ANQUR_REGISTRY_UPDATE.md). No efficacy inference or posted registry results.

The following fields preserve the original November 7 snapshot; their registry-access/window caveats are superseded by the dated correction above.

- Record: `qrl201_stmn2`
- Stage: sponsor reported early trial
- Target: Restoration of STMN2 expression
- Population: Sporadic and C9orf72-related ALS; 69 dosed, including 17 dose-escalation and 52 dose-range-finding participants.
- Design: Double-blind, placebo-controlled ANQUR. Sponsor called it Phase 1 in 2024 and Phase 1/2 in 2026; current registry protocol not verified.
- Trial identifiers: NCT05633459
- Context sources: [anqur_design_2024](https://www.quralis.com/news/quralis-anqur-clinical-trial-of-qrl-201-in-als-advances-to-dose-range-finding-drf-phase-with-first-participant-dosed/); [anqur_interim_2026](https://www.quralis.com/news/quralis-demonstrates-effects-on-disease-progression-and-target-engagement-in-anqur-clinical-trial-of-qrl-201-a-first-in-class-precision-medicine-in-development-for-sporadic-als/)

### Safety primary

Safety and tolerability of repeated doses, per 2024 sponsor design description. Timepoint: Current protocol assessment window not verified.

2026 sponsor report described generally acceptable tolerability; it did not provide a complete adverse-event table.

Sources: [anqur_design_2024](https://www.quralis.com/news/quralis-anqur-clinical-trial-of-qrl-201-in-als-advances-to-dose-range-finding-drf-phase-with-first-participant-dosed/); [anqur_interim_2026](https://www.quralis.com/news/quralis-demonstrates-effects-on-disease-progression-and-target-engagement-in-anqur-clinical-trial-of-qrl-201-a-first-in-class-precision-medicine-in-development-for-sporadic-als/)

### Biomarker

Tissue STMN2 expression/mis-splicing and low-dose pNfH. Timepoint: Interim report, 2026-02-23.

Sponsor reported target engagement versus natural-history tissue and reduced low-dose pNfH.

Sources: [anqur_interim_2026](https://www.quralis.com/news/quralis-demonstrates-effects-on-disease-progression-and-target-engagement-in-anqur-clinical-trial-of-qrl-201-a-first-in-class-precision-medicine-in-development-for-sporadic-als/)

### Clinical exploratory

ALSFRS-R decline in sporadic ALS. Timepoint: 24 weeks for the reported post-hoc subset.

Overall trend; significant result reported only after post-hoc exclusion of highest-baseline-NfL participants.

Sources: [anqur_interim_2026](https://www.quralis.com/news/quralis-demonstrates-effects-on-disease-progression-and-target-engagement-in-anqur-clinical-trial-of-qrl-201-a-first-in-class-precision-medicine-in-development-for-sporadic-als/); [anqur_design_2024](https://www.quralis.com/news/quralis-anqur-clinical-trial-of-qrl-201-in-als-advances-to-dose-range-finding-drf-phase-with-first-participant-dosed/)

**Negative or absent evidence**
- No confirmatory primary clinical efficacy success is established by these selected interim data.

**Unknowns**
- Numerical effect sizes, confidence intervals, multiplicity handling, and subgroup denominators were not supplied in the selected release.

**Caveats**
- Sponsor-only interim analysis; post-hoc exclusions can create optimistic results.
- Target engagement and neurofilament changes do not establish clinical benefit.
- 2024 endpoint hierarchy may have changed; verify registry amendments.

Regulatory field: investigational in cited source; jurisdiction: Not a jurisdiction-wide approval search; event date: 2026-02-23.

Regulatory sources: [anqur_interim_2026](https://www.quralis.com/news/quralis-demonstrates-effects-on-disease-progression-and-target-engagement-in-anqur-clinical-trial-of-qrl-201-a-first-in-class-precision-medicine-in-development-for-sporadic-als/)

## DNL343: negative HEALEY Regimen G randomized result

- Record: `dnl343`
- Stage: peer reviewed randomized trial
- Target: eIF2B activation / integrated stress response
- Population: ALS; 249 randomized within Regimen G: 186 active, 63 placebo; 76 concurrent shared controls, yielding 139 pooled placebo and 325 analyzed participants.
- Design: Double-blind HEALEY platform trial at 74 US centers; 200 mg/day tested for 24 weeks.
- Trial identifiers: NCT05842941
- Context sources: [dnl343_jama_2026](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2854318)

### Clinical primary

Bayesian joint function/survival disease rate ratio (DRR). Timepoint: 24 weeks.

Primary endpoint was not met; posterior probability DRR < 1 was 0.37.

Measure: median_disease_rate_ratio. Analysis: Bayesian shared-parameter model of function and survival. Estimate: 1.04 ratio. 95% credible interval: 0.83 to 1.32.

Sources: [dnl343_jama_2026](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2854318)

**Negative or absent evidence**
- No demonstrated slowing at the tested formulation, dose, duration, and population; secondary clinical outcomes did not show benefit.

**Unknowns**
- A null trial does not resolve every alternative dose, formulation, exposure, or biological subgroup.

**Caveats**
- Credible interval and posterior probability are not a frequentist confidence interval or p-value.
- Shared controls are not additional active-arm randomizations.
- Prior target-engagement evidence did not establish clinical efficacy.

Regulatory field: not assessed; jurisdiction: Not assessed; event date: not asserted.

## Relyvrio / AMX0035: PHOENIX failure and distinct withdrawal events

- Record: `relyvrio_withdrawal`
- Stage: negative trial report and regulatory withdrawal
- Target: Sodium phenylbutyrate plus taurursodiol
- Population: PHOENIX: 664 adults with ALS, randomized 3:2 active versus placebo, alongside standard care.
- Design: Global, 48-week, placebo-controlled Phase 3 trial.
- Trial identifiers: None asserted in this record
- Context sources: [phoenix_topline_2024](https://investors.amylyx.com/news-releases/news-release-details/amylyx-pharmaceuticals-announces-topline-results-global-phase-3); [relyvrio_announcement_2024](https://investors.amylyx.com/news-releases/news-release-details/amylyx-pharmaceuticals-announces-formal-intention-remove); [relyvrio_fda_withdrawal_2025](https://www.govinfo.gov/content/pkg/FR-2025-08-29/pdf/2025-16646.pdf)

### Clinical primary

Change in ALSFRS-R total score from baseline. Timepoint: 48 weeks.

Sponsor reported primary and secondary endpoints were not met on 2024-03-08.

Measure: primary_endpoint_test. Analysis: Primary endpoint analysis; exact test not specified in selected sponsor release. Reported p-value: 0.667 (Not specified in selected sponsor release).

Sources: [phoenix_topline_2024](https://investors.amylyx.com/news-releases/news-release-details/amylyx-pharmaceuticals-announces-topline-results-global-phase-3)

### Commercial action

Market-removal announcement and end of new-patient access. Timepoint: 2024-04-04.

Amylyx announced a voluntary withdrawal process in the US and Canada; this was not FDA's effective approval-withdrawal date.

Sources: [relyvrio_announcement_2024](https://investors.amylyx.com/news-releases/news-release-details/amylyx-pharmaceuticals-announces-formal-intention-remove)

### Regulatory

FDA withdrawal of NDA 216660 approval. Timepoint: 2025-08-29.

US approval withdrawal took effect, following the sponsor's voluntary request based on PHOENIX.

Sources: [relyvrio_fda_withdrawal_2025](https://www.govinfo.gov/content/pkg/FR-2025-08-29/pdf/2025-16646.pdf)

**Negative or absent evidence**
- The larger confirmatory PHOENIX trial failed to establish its prespecified clinical benefit.

**Unknowns**
- This record does not reproduce all earlier CENTAUR analyses, PHOENIX methods, or evidence in other diseases.

**Caveats**
- Sponsor topline efficacy data and an official regulatory action are different source types.
- Canada's exact legal cancellation date is not established here.
- Regulatory withdrawal is not a biological endpoint.

Regulatory field: approval withdrawn; jurisdiction: US; event date: 2025-08-29.

Regulatory sources: [relyvrio_fda_withdrawal_2025](https://www.govinfo.gov/content/pkg/FR-2025-08-29/pdf/2025-16646.pdf)

## UNC13A: TDP-43-associated cryptic-splicing mechanism

- Record: `unc13a_mechanism`
- Stage: peer reviewed mechanistic research
- Target: UNC13A cryptic exon regulation
- Population: Human brain tissue, neuronal cell lines, and induced-pluripotent-stem-cell-derived motor neurons; not a treatment trial population.
- Design: Ma and colleagues, published online 2022-02-23: laboratory perturbation and human tissue analyses.
- Trial identifiers: None asserted in this record
- Context sources: [unc13a_ma_2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8891019/)

### Mechanistic

UNC13A cryptic exon inclusion and protein abundance. Timepoint: Experiment-specific; no clinical follow-up interval.

Nuclear TDP-43 loss promoted UNC13A cryptic splicing and reduced protein expression; risk variants increased mis-splicing under TDP-43 dysfunction.

Sources: [unc13a_ma_2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8891019/)

### Hypothesis

Potential therapeutic relevance of correcting mis-splicing. Timepoint: Not a clinical outcome.

Mechanistic evidence motivates testing restoration; it does not demonstrate benefit in people with ALS.

Sources: [unc13a_ma_2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8891019/)

**Negative or absent evidence**
- This mechanistic study contains no randomized patient efficacy test.

**Unknowns**
- Whether, when, and how much restoring UNC13A changes clinical outcomes is not answered by this record.

**Caveats**
- The cryptic exon event is not conserved in mouse; model choice matters.
- Genetic risk association is not deterministic patient prognosis.
- No individual-level datasets or predictive model were accessed or created.

Regulatory field: not applicable; jurisdiction: Not applicable; event date: not asserted.
