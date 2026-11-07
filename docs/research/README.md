# Research and engineering commons

The purpose is to grow a freely reusable body of science, medicine, engineering, and computing that people and AI can study, check, extend, and apply together. This edition begins with ALS evidence and the engineering of a simple digital input. It contains the knowledge text, selected factual data, source provenance, executable code, synthetic signals, and repeatable checks directly in the repository.

## Read and compute

1. Read the [ALS evidence primer](../health/als-evidence-primer.md): motor neurons, genetic heterogeneity, trial endpoints, treatment evidence, care, and research questions.
2. Inspect the [embedded evidence pack](../../data/health/als-evidence.json) and [published trial facts](../../data/health/als-trial-facts.json). Numerical results retain their population, endpoint, timepoint, and source relationship.
3. Run the [offline evidence library](../../tools/evidence-library/README.md) to validate, search, and print the embedded claims and source notes. Downloading these files is enough for the core workflow; opening original sources is an additional online step.
4. Read [switch-input foundations](../lessons/switch-input-foundations.md) and run the [switch lab](../../tools/switch-input-lab/README.md). Follow the synthetic bouncing signal through a stable-state algorithm and inspect the resulting press and release events.

From the repository root, using Python 3.10 or newer:

```sh
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json validate
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json search tofersen
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json report
```

These commands use the committed data. They do not need an account, model, API key, cloud service, or installed third-party package. Output can be redirected to a local text file for review. The evidence tool does not execute instructions in a source record.

## Cancer foundations

The [cancer evidence primer](../health/cancer-evidence-foundations.md) adds a second self-contained path, including worked examples and exercises. Its [embedded evidence pack](../../data/health/cancer-foundations.json) is searchable with the same code:

```sh
python3 tools/evidence-library/evidence_library.py data/health/cancer-foundations.json validate
python3 tools/evidence-library/evidence_library.py data/health/cancer-foundations.json search biomarker
```

## How these pieces connect

ALS research spans molecular biology, genetics, clinical measurement, statistical inference, patient priorities, rehabilitation, accessible interfaces, and engineering. The evidence library keeps observations attached to their source and study design. The switch lab makes one small electronic/digital principle inspectable rather than hiding it behind a description. The same contribution pattern can support cancer biology, other neurological conditions, infectious disease, electronics, mechanical measurement, and software methods.

A biomarker change, an improvement on a functional scale, a survival result, a regulatory decision, and a person's daily experience are different kinds of information. Keep them distinguishable so later contributors can ask better questions and combine compatible evidence. A later follow-up should be stored alongside the earlier randomized result rather than silently replacing it.

## Contribute something checkable

A useful contribution can be a sourced explanation, corrected number, lawful dataset, calculation notebook, reproducible experiment, benchmark, open implementation, accessible adaptation, or replication report. Include the actual reusable content and the steps for checking it. Clearly label synthetic data. Public records should not contain participant-level medical data or private information.

For a study, retain the population, comparison, endpoint, measurement time, estimate, uncertainty, design, source date, source location, and interpretation. For code, include input definitions, units, examples, expected output, and failure handling. For hardware-related work, distinguish simulation results from measured device behavior. Preserve separate source licenses; a factual citation does not relicense a paper or dataset.

The [source review task](../../data/tasks/task-als-source-review.json) provides a concrete first handoff. [Verification and provenance](verification.md) records the implemented version and checks. Contributor or reviewer roles are voluntary; propose a result and record a real review decision rather than assigning approval to another person.

## Continue the science

- Reproduce the trial tables from the cited original records and check any discrepancy.
- Extend genetic and phenotype coverage with documented inclusion criteria and appropriately reusable data.
- Add another disease evidence pack using the same code, testing whether its design distinctions fit.
- Expand the engineering path from sampled switches to accessible input protocols, signal quality, measurement error, and user-directed evaluation.
- Add research-computation examples that connect uncertainty, models, and experiments across biology, mechanics, electronics, and software.

The long-term mission is broad. Each contribution should leave knowledge and a working method that the next contributor can inspect and improve.
