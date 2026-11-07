# ALS: an evidence notebook for learners and contributors

**Original educational synthesis · 2026-11-07 · CC BY 4.0 · AI-assisted draft awaiting qualified review**

This notebook explains selected ALS biology and trial results, then shows how to check them. The content is embedded here for offline reading. Its purpose is to make scientific work easier to understand, reproduce, and improve. It is a starting collection, not a complete clinical guideline or a treatment plan.

After working through it, you should be able to distinguish a disease mechanism from a therapeutic hypothesis, a biomarker from a clinical outcome, and a promising result from replicated evidence. You should also be able to check a reported difference, keep units and populations attached to it, and propose a useful next research task.

## Start with the person and the biology

Amyotrophic lateral sclerosis (ALS) damages motor neurons: nerve cells in the brain and spinal cord that control voluntary muscles. When those connections fail, muscle weakness affects activities such as moving, speaking, swallowing, and breathing. People have different starting symptoms and rates of progression. Some also experience changes in thinking, language, or behavior. An inability to speak or move does not by itself tell us what someone understands or wants.[1]

Useful work includes preserving communication, access, comfort, and choice while developing better disease treatments. The NIH MedlinePlus overview describes medicines that may slow functional loss, relieve symptoms, or sometimes extend life, alongside physical, occupational, and speech therapy, communication aids, nutritional support, and breathing support. A multidisciplinary team can help people make decisions that fit their needs. These are meaningful goals alongside the search for treatments that reverse or prevent disease.[1]

A research library should therefore contain two connected kinds of work: evidence about disease mechanisms and treatment effects, and knowledge that supports living well and participating now. People with ALS and their caregivers should help define which outcomes matter; a laboratory measurement alone cannot decide that for them.

## One diagnosis, several biological routes

A gene supplies instructions for making functional products such as proteins. A pathogenic variant can alter those instructions. ALS can occur with or without an apparent family history, and multiple genes contribute to inherited forms; no single mutation explains all cases. The distinction matters when selecting a model or interpreting a targeted therapy.[2]

| Gene or product | Established starting point | Question that remains useful for research |
| --- | --- | --- |
| **SOD1** | Normally encodes an enzyme involved in handling superoxide radicals. ALS-associated variants can alter the protein; misfolding and toxic effects are investigated.[3] | Which harmful processes matter for a particular variant, and when can a targeted intervention change the person's disease course? |
| **C9orf72** | A repeat expansion in this gene is associated with ALS and frontotemporal dementia. Its biology involves RNA and protein processes.[4] | How do altered gene function and abnormal products contribute across cell types and stages? Association with a repeat does not specify one universally effective treatment. |
| **TARDBP / TDP-43** | TARDBP encodes TDP-43, involved in RNA processing, including splicing. Altered protein behavior and aggregates are observed in ALS-related biology.[5] | Which changes drive injury, which follow injury, and which can be altered without disrupting essential normal functions? |
| **FUS** | Encodes a DNA/RNA-binding protein involved in gene expression and RNA processing. ALS-associated changes can disrupt protein localization and function.[6] | Which model reproduces the relevant human defect, and can it distinguish rescue of a useful function from a general change in cell behavior? |

These are entry points, not four complete explanations. Finding a protein clump does not, on its own, prove that removing the clump restores a neuron. Likewise, an effect in a SOD1 model does not establish efficacy in every form of ALS. A useful evidence chain keeps its steps separate: **biological observation → proposed mechanism → testable intervention → target engagement → clinical outcome → independent confirmation**. Each step can succeed or fail for different reasons.

## Decide what a result actually measures

A **clinical outcome** describes something directly relevant to a person's health or function. A **biomarker** is a measured biological characteristic. A biomarker may help identify a disease process, prognosis, or response to an intervention; those are different uses.

The ALS Functional Rating Scale–Revised (**ALSFRS-R**) summarizes aspects of function on a scale from 0 to 48, with higher scores indicating better function. A negative change indicates decline. A group average can contain decimals even though an individual's scale score is recorded in discrete points. Plasma **neurofilament light (NfL)** is a biomarker related to nerve-cell injury. A reduction can be important evidence about biology without independently proving improved function or longer survival.[7], [8]

A study's **primary endpoint** is the main outcome specified for its central analysis. Secondary and exploratory outcomes can be informative, but their interpretation depends on the plan, the number of comparisons, missing data, and the actual analysis. Read the population, time point, and units beside every number.

### Worked example 1: read VALOR without changing its question

Miller and colleagues' 2022 VALOR report randomized 108 adults with SOD1-associated ALS: 72 to tofersen and 36 to placebo. The primary analysis concerned the predicted faster-progressing subgroup, with 39 and 21 participants respectively. It assessed ALSFRS-R change from baseline to week 28.[7]

The reported changes were **−6.98 points** with tofersen and **−8.14 points** with placebo. Simple subtraction gives:

`−6.98 − (−8.14) = +1.16 points`

The paper reports a difference of **1.2 points**, with a **95% confidence interval from −3.2 to +5.5**, and a reported **P value of 0.97**. Preserve those as the study's reported estimates; rounded arm summaries do not reconstruct every feature of its analysis. Do not calculate a replacement P value from this interval.[7]

The prespecified primary clinical endpoint was not met. The study also found reductions in SOD1 and NfL, demonstrating biological effects. The confidence interval includes zero and values in both directions, so the primary result does not establish a functional benefit at that time point. It also does not prove that the true effect is exactly zero. A confidence interval is not a 95% probability assignment to the fixed true effect; its coverage interpretation concerns the statistical procedure over repeated studies.

In April 2023, the US FDA granted tofersen accelerated approval for a genetically defined SOD1-associated ALS indication, based on reduced plasma NfL considered reasonably likely to predict clinical benefit. The regulatory decision and the 28-week primary clinical result answer different questions. Neither supports extrapolation to every form of ALS.[8]

The same publication reports common lumbar-puncture-related adverse events and neurologic serious adverse events in 7% of tofersen recipients.[7] The inspected abstract does not give the exact safety denominator or phase-specific window for that percentage. Keep the reported safety finding alongside the endpoint results; it does not supply a derived event count or placebo risk comparison.

### Keep the later follow-up in view

The original report also described a 52-week early-start versus delayed-start comparison, after the placebo group began treatment at week 28: ALSFRS-R changes of −6.0 and −9.5, a reported difference of 3.5 points, with a 95% interval of 0.4 to 6.7. These follow-up findings must stay distinct from the original primary endpoint and its analysis.[7]

The final VALOR/open-label-extension report, published in the 2026 print issue of *JAMA Neurology*, reports numerically less decline over 148 weeks with earlier treatment: **−9.9 versus −13.5 ALSFRS-R points**. Its authors conclude that the long-term evidence supports benefit in SOD1-ALS. Of the original 108 participants, 95 entered the extension and 46 completed it. All extension participants received tofersen.[9]

This later evidence adds information; it should neither be omitted nor relabeled as a continuously placebo-controlled 148-week trial. Timing of treatment, attrition, analysis assumptions, and comparisons with expected natural history matter. These publications also describe overlapping participants, so they are not three independent trials to count separately in a pooled analysis.

### Worked example 2: a biomarker and function can tell different stories

**Invented teaching data, not a real study:** suppose both groups start with a biomarker average of 100 arbitrary units. At follow-up, the intervention group averages 60 and the comparator 100. Both groups' mean function scores change from 40 to 38.

The intervention group's biomarker change is `(60 − 100) / 100 × 100 = −40%`. Its functional change is `38 − 40 = −2 points`; the comparator also changes by −2. The between-group functional-change difference is therefore `−2 − (−2) = 0 points`.

The descriptive numbers support a biomarker difference and no observed difference in these mean functional changes. They do not provide uncertainty, adverse-event information, or a design sufficient to establish a treatment effect. Reporting “40% better function” would mix different measurements and would be wrong.

### Worked example 3: promising early evidence needs confirmation

In the 2020 CENTAUR trial, Paganoni and colleagues randomized 137 participants to sodium phenylbutyrate–taurursodiol or placebo. The modified intention-to-treat analysis reported ALSFRS-R rates of change of **−1.24 versus −1.66 points per month** through 24 weeks: a difference of **0.42 points per month**, 95% confidence interval **0.03 to 0.81**, P = **0.03**. Secondary outcomes were not significantly different.[10]

The subtraction is `−1.24 − (−1.66) = +0.42 points/month`. This is a rate, so it cannot be ranked directly against VALOR's difference in points at one time. Do not project an unchanging benefit indefinitely or treat one positive endpoint as a cure.

The US FDA's later withdrawal notice states that the 48-week randomized, placebo-controlled PHOENIX trial did not meet its prespecified primary and secondary endpoints. The notice distinguishes planned marketing discontinuation on **October 31, 2024**, the sponsor's withdrawal request in **February 2025**, and formal US approval withdrawal effective **August 29, 2025**.[11] These dates refer to different actions. The notice does not provide a numerical effect estimate, confidence interval, or P value to extract. This is a concrete example of why a useful library preserves later negative evidence alongside earlier positive findings.

## Make model results easier to trust

Cell systems, organoids, computational models, and animal models can isolate questions that cannot be studied the same way in people. Each represents only part of human disease. Record the model, relevant genotype, measured outcome, comparison, and limits before claiming a result translates to patients.

Study conduct and reporting also matter. A systematic review of 569 SOD1-mouse papers published in 2005–2015 found major reporting gaps, including information about randomization and blinding. That historical finding identifies a reproducibility concern; absence of reporting is not proof that a procedure was never performed, and the review is not a census of current practice.[12]

For computational work, preserve code versions, units, exclusions, and expected outputs. Use genuinely synthetic examples to test analysis logic. Keep failed replications and null results findable. Before running new biological experiments, use existing evidence to refine the question and involve the appropriate scientific, ethical, and animal-welfare expertise.

## Five exercises, with answers

1. **Which population?** A headline says tofersen proved effective for everyone with ALS because it changes NfL. Identify two missing distinctions. **Answer:** the indication and trial population are SOD1-associated ALS, and a biomarker change differs from demonstrated clinical benefit in a specified endpoint and time frame.
2. **Check the arithmetic.** Why is +1.16 not a reason to “correct” VALOR's reported 1.2? **Answer:** +1.16 is subtraction of rounded arm summaries. The publication's reported estimate, interval, and analysis must be preserved with provenance; summaries do not recover the full statistical model.
3. **Read uncertainty.** Does an interval from −3.2 to +5.5 prove harm or prove no effect? **Answer:** neither. It includes zero and estimates on either side. State what the endpoint analysis did and did not establish rather than choosing the most favorable endpoint of the interval.
4. **Avoid double counting.** Can the 28-, 52-, and 148-week tofersen reports be treated as three independent groups of 108 people? **Answer:** no. They report overlapping trial and follow-up participants, with different designs and follow-up completeness.
5. **Choose the next useful task.** You find a promising cell-study result and one small positive human trial. What can a contributor do before claiming a treatment works? **Answer:** extract the exact model and population, predefined outcome, effect and uncertainty, adverse events, study limitations, later trials, and corrections; check whether cohorts overlap; then submit a source-linked review. A clinical recommendation requires the appropriate qualified evaluation.

## Concrete contributions this notebook supports

Reproduce the arithmetic from the embedded facts; verify that every claim points to the correct source and population; add a negative or confirmatory result alongside a positive finding; or review a model's stated assumptions. Another useful contribution is accessible measurement software tested with synthetic inputs, with its engineering performance kept separate from patient benefit. Contributors should choose a bounded task and document what would change their conclusion.

The material here is original synthesis of selected official overviews, regulatory text, and publication abstracts inspected on 2026-11-07. Full study methods were not systematically reviewed, and clinical, educator, and learner approval have not been recorded. Third-party articles retain their own rights. This notebook includes no patient-level data, treatment dosing, copied abstracts, or clinical instructions.

## References inspected

1. NIH National Library of Medicine. **Amyotrophic Lateral Sclerosis**, MedlinePlus. Government health overview; supports the disease description and multidisciplinary care discussion.
2. NIH National Library of Medicine. **Amyotrophic lateral sclerosis**, MedlinePlus Genetics. Supports genetic heterogeneity.
3. NIH National Library of Medicine. **SOD1 gene**, MedlinePlus Genetics.
4. NIH National Library of Medicine. **C9orf72 gene**, MedlinePlus Genetics.
5. NIH National Library of Medicine. **TARDBP gene**, MedlinePlus Genetics.
6. NIH National Library of Medicine. **FUS gene**, MedlinePlus Genetics.
7. Miller TM et al. (2022). **Trial of Antisense Oligonucleotide Tofersen for SOD1 ALS.** *New England Journal of Medicine*, 387:1099–1110. Publication abstract inspected through Consensus search and fetch.
8. US FDA (content current April 25, 2023). **FDA approves treatment of amyotrophic lateral sclerosis associated with a mutation in the SOD1 gene.** Official action and accelerated-approval explanation.
9. Miller TM et al. (2026 print issue). **Long-Term Tofersen in SOD1 Amyotrophic Lateral Sclerosis.** *JAMA Neurology*, 83:115–125. DOI: **10.1001/jamaneurol.2025.4946**. Abstract inspected through Consensus; DOI and print issue date checked against Crossref. The search index uses 2025; that is distinct from the 2026 print issue.
10. Paganoni S et al. (2020). **Trial of Sodium Phenylbutyrate–Taurursodiol for Amyotrophic Lateral Sclerosis.** *New England Journal of Medicine*, 383:919–930. Publication abstract inspected through Consensus search and fetch.
11. US FDA (August 29, 2025). **Amylyx Pharmaceuticals, Inc.; Withdrawal of Approval of New Drug Application for RELYVRIO.** Federal Register document **2025-16646**. Official full text and metadata inspected; US jurisdiction.
12. Fernandes JG et al. (2019). **Methodological standards, quality of reporting and regulatory compliance in animal research on amyotrophic lateral sclerosis: a systematic review.** *BMJ Open Science*, 3. Publication abstract inspected through Consensus search and fetch; historical reporting review.

[1]: https://medlineplus.gov/amyotrophiclateralsclerosis.html
[2]: https://medlineplus.gov/genetics/condition/amyotrophic-lateral-sclerosis/
[3]: https://medlineplus.gov/genetics/gene/sod1/
[4]: https://medlineplus.gov/genetics/gene/c9orf72/
[5]: https://medlineplus.gov/genetics/gene/tardbp/
[6]: https://medlineplus.gov/genetics/gene/fus/
[7]: https://consensus.app/papers/trial-of-antisense-oligonucleotide-tofersen-for-sod1-als-miller-cudkowicz/7046a8e53686529d811c0540cd66f2d0/?utm_source=chatgpt
[8]: https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-treatment-amyotrophic-lateral-sclerosis-associated-mutation-sod1-gene
[9]: https://consensus.app/papers/longterm-tofersen-in-sod1-amyotrophic-lateral-sclerosis-miller-cudkowicz/c802029be48f58fea4933274b8db863d/?utm_source=chatgpt
[10]: https://consensus.app/papers/trial-of-sodium-phenylbutyrate–taurursodiol-for-paganoni-macklin/47c2214a5e34556eab364525622c130f/?utm_source=chatgpt
[11]: https://www.federalregister.gov/documents/2025/08/29/2025-16646/amylyx-pharmaceuticals-inc-withdrawal-of-approval-of-new-drug-application-for-relyvrio-sodium
[12]: https://consensus.app/papers/methodological-standards-quality-of-reporting-and-fernandes-franco/5ea0ebb55c015b409802bdc89061c91e/?utm_source=chatgpt
