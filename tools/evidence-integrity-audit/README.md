# Evidence integrity audit (candidate)

A bounded, offline, read-only integrity checker for the ALS hypothesis-plan JSON export in Jonathan's Creative Archive. It inspects local records and documented provenance. It does **not** validate scientific claims, infer treatment efficacy, or generate clinical recommendations.

## Scope and safety

- Python 3.10+; standard library only. No install, model, browser, credentials, or network access required. There is no network mode.
- Reads three named JSON files under a user-selected local root. It never imports or executes repository code, follows source links, generates hypotheses, rewrites inputs, or updates a checksum baseline.
- Expects only these three public research JSON files. Do not supply patient data. The checker does not detect or sanitize private/clinical content.
- Writes only to stdout. Shell redirection is an explicit caller action. Run with `python -B` when importing/running tests to avoid Python bytecode caches.
- CLI refuses input paths that resolve outside the selected root and non-regular files. Inputs are bounded to 5 MiB each, 100,000 JSON values, and depth 40. Duplicate object keys and non-finite numbers are rejected, including overflow such as `1e999`.
- A no-findings result means **only** no findings within these rules, not readiness for experiments, publication, or patient use. Human scientific and rights review is still necessary.
- Source links are checked for HTTP(S) syntax, not availability, content, authorship, factual support, licensing, retractions, or whether the host is safe to visit. No URL is fetched. A valid link is not evidence that a claim is true.

## Run

For a local checkout containing the three named ALS export files:

```sh
python -B tools/evidence-integrity-audit/audit.py --repo .
python -B tools/evidence-integrity-audit/audit.py --repo . --format json
python -B -m unittest discover -s tools/evidence-integrity-audit/tests -v
```

The audit reads exactly:

- `data/health/als-evidence.json`: schema version `1.0`, source registry and claim registry.
- `data/health/als-aging-pathways.json`: schema version `1.0`, pathways and interventions.
- `data/health/als-aging-hypotheses.json`: schema version `1.0`, `all_hypotheses` and `top_hypotheses` research-plan arrays.

This is the `export_research_plan` shape inspected at the pinned revision below, **not** the separate `export_hypotheses_json` shape. Other shapes yield explicit findings rather than an apparent clean audit. Summary rows in `all_hypotheses` need not repeat top-detail provenance. Every present score is validated; present source/pathway/intervention/contradiction links and present experimental fields are checked even outside the top list. Missing details in summary-only rows are not interpreted as full hypothesis records. Unknown fields are not interpreted. This is not a complete JSON Schema validator.

Exit codes:

- `0`: no findings within scope. Never a scientific approval.
- `1`: structural errors and/or provenance-review warnings. Intentional on the inspected PR snapshot.
- `2`: missing/unreadable/unsafe input, malformed/oversized JSON, or invalid CLI usage. File errors produce a structured report; argparse usage errors go to stderr.

Text and JSON reports contain input SHA-256 hashes, observed record counts, exact JSON-pointer-like locations, severity, rule code, and limitations. Locations begin with the input role (`network`, `evidence`, `hypotheses`). Within each role, object keys are escaped using JSON Pointer conventions. Text output quotes locations to avoid interpreting terminal control characters.

## Deterministic rules

**Errors** include malformed source URLs; unknown, duplicate, or malformed IDs/references; invalid/non-finite/boolean scores; non-integer/boolean/negative counts; counts that disagree with the corresponding complete record arrays; unknown pathway/effect targets; and fields that disagree exactly between matching top/all hypothesis records. Numerically equal JSON numbers such as `1` and `1.0` do not conflict. A shortened top list is allowed and is not confused with the complete count.

**Warnings** indicate records present without explicit citations, score methods, effect context, experiments, or contradiction-review fields. These mean information is **not documented in the checked fields**, not that it does not exist elsewhere. Empty arrays and omitted fields have different meanings: an empty `contradicting_evidence` array is not called a contradiction, proof of a complete review, or proof that no contradicting studies exist.

The checker does not compare natural-language claims, interpret biological causal direction, establish that a hypothesis is testable, or verify the generator's reasoning. For example, a directionally incorrect prose prediction will require human review even if its fields have citations. This is an integrity aid, not an automated scientific referee.

### Explicit provenance conventions

These optional conventions let a future writer document metadata without this candidate editing the existing export or imposing an upstream schema change:

- `source_ids` and `supporting_sources`: arrays of IDs in the evidence-pack `sources` registry. Each source needs a valid `url` or `source_url`.
- `supporting_evidence` / `contradicting_evidence`: arrays of source IDs or claim IDs. Claims must themselves resolve to source links. Duplicate source/claim IDs are not accepted as unique evidence.
- `score_provenance.<field>.method`: nonempty explanation for `als_relevance`, `aging_relevance`, or `priority_score`. Optional `source_ids` are checked. A method can accurately describe an arbitrary heuristic; documenting it does not make it empirically calibrated.
- `effect_provenance.<pathway_id>`: for a numeric `known_effects` coefficient, either (a) source IDs plus nonempty `unit`, `population`, `endpoint`, and `timepoint`, or (b) `kind: "illustrative"` plus a nonempty `note`. Labeling a coefficient illustrative must reflect its actual origin. These fields are checked for presence, not scientific correctness. Uncertainty intervals, study design, comparison groups, statistical estimands, and exact source locations remain unchecked; this is not a complete empirical-provenance specification.
- `literature_source_ids`: the explicitly enumerated, deduplicated source IDs corresponding to a pathway's `literature_count`. Counts without this enumeration get `LITERATURE_COUNT_UNENUMERATED`, not a claim that the number is false. A selected evidence pack is never assumed exhaustive.

`literature_count_field_sum` is the sum of pathway count fields. It is **not a verified publication count or a unique-paper count**; the same paper may occur in multiple pathways. The checker does not parse README/PR prose counts or treat the evidence-pack source count as the total literature count.

## Synthetic examples and tests

The `fixtures/clean-synthetic` and `fixtures/review-synthetic` directories use invented IDs, values, and `example.org` URLs. There are no real participants, study estimates, clinical claims, or imported source texts. To run:

```sh
python -B tools/evidence-integrity-audit/audit.py --repo tools/evidence-integrity-audit/fixtures/clean-synthetic
python -B tools/evidence-integrity-audit/audit.py --repo tools/evidence-integrity-audit/fixtures/review-synthetic
```

The first produces no findings within scope; the second produces review findings. The tests cover wrong-type mutations across every existing fixture field, malformed input, empty evidence, missing/ambiguous sources, source references, scores, provenance, exact conflicts, truncated exports, counts, no input mutation, stable output, and blocked network calls.

## Pinned snapshot and verification limits

The real-data audit assessed **only commit `f67042770e06c9fd0d12fe80003712014a2e0584`** from [PR #5](https://github.com/jonjonjon11/jonathan-creative-archive/pull/5), not the current or future head of that pull request or `main`. The three input hashes are recorded in the audit output when run against that exact local snapshot. No real research input files or generated audit report are bundled here.

That run produced **0 structural errors and 158 provenance/coverage warnings**, with exit code 1. The warnings overlap and describe missing metadata in the checked fields. **158 is not a verified research-error count**, an assessment of evidence quality, or a claim that the underlying information does not exist elsewhere. The literature-count field sum is not a count of verified or unique publications.

At the draft's base, `main` commit `f3168d5cd6460a8e82d02afcf7c3c84a6c17707f`, the three `data/health` inputs do not exist. Running `--repo .` there correctly returns exit code 2. Use the bundled synthetic examples for a self-contained demonstration, or separately obtain and review the public inputs from the exact pinned commit. This draft does not merge PR #5 or change it.

All 43 synthetic/adversarial tests passed under Python 3.12.14. Python 3.10/3.11 and other operating systems were not tested. An independent adversarial review exercised wrong-type and malformed inputs plus offline/read-only guards. This is software-behavior evidence, not scientific or clinical validation.

## Integration and rights

The original PR #6 was a focused candidate addition: it did not change the generator, evidence pack or generated plan. Its ten files initially lacked shared checksum entries, and its extensionless license was outside the older validator allowlist. The [2026-11-08 integration record](../../docs/reviews/main-integration-2026-11-08.md) documents the explicit repairs and expanded CI separately. The hypothesis engine and its real inputs remain outside main. The 158 warnings above remain a historical result for the pinned PR #5 snapshot, not a baseline to suppress and not an audit of current main. Do not describe green CI as scientific validation. Any later use against a research export requires checking schema compatibility, rerunning the audit on that exact revision, and independent scientific review before research use.

Original auditor, documentation, and invented fixtures are proposed under the archive's existing CC BY 4.0 license; see the included `LICENSE`. Attribution: Jonathan's Creative Archive, by Jonathan (jonjonjon11), 2026, https://github.com/jonjonjon11/jonathan-creative-archive. This addition is a later original integrity-checking tool, not recovered historical work. The underlying publications retain their own rights. No third-party publication text, assets, or datasets are bundled.
