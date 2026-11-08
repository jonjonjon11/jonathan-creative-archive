# Hypothesis Engine: AI-Driven Research Planning for ALS and Aging

## Current review status

**Unvalidated research-question generator.** It does not simulate disease, predict
treatment effects, or validate clinical indications. Loading an evidence pack
stores it but does not connect its sources to generated questions. The older
overview below contains proposed capabilities and unreviewed scientific claims;
it must not be read as evidence that they are implemented or established.

The outcome-safety correction replaces blanket claims such as "will reduce motor
neuron survival" with direction-neutral questions. Therapeutic questions preserve
the caller's outcome and population, use `open_question` confidence, and do not
turn an intervention's registry label into confidence in a new outcome claim.
If population is omitted, it is explicitly `unspecified population`, not SOD1-ALS.
No clinical benefit or harm is inferred from the question wording.

Hypothesis exports are now version `1.1`. They add `status`, `limitations`,
`target_outcome`, and `patient_population`. Therapeutic IDs now identify the
intervention/outcome/population tuple, so distinct questions no longer overwrite
each other. **Old therapeutic IDs change:** regenerate dependent exports and
review downstream references rather than joining old and new IDs blindly.
Identical normalized questions retain one deterministic ID. Non-therapeutic
records use null outcome/population fields; pathway exports remain version `1.0`.

The existing scores, timelines, registry coefficients, literature counts,
mechanistic statements, and combination claims still require source-level review.
Scores remain heuristic, including the retained 0.9/0.5 therapeutic values; they
are not clinical probabilities or validated research priorities. No quantitative
claim has been newly established by this correction.

Run the full standard-library regression suite from the repository root:

```sh
python3 -m unittest discover -s tools/hypothesis-engine/tests -p 'test_*.py' -v
```

The suite checks wording, preserved context, non-overwriting IDs, malformed
context, export limits, and committed-output parity apart from the generation
date. The original single test-file invocation does not run the new regressions.
The workflow runs the full suite. See the [review record](../../docs/research/hypothesis-outcome-safety.md)
for the scope and remaining gaps.

## Overview

The Hypothesis Engine is a computational system for generating, ranking, and prioritizing research hypotheses to accelerate ALS and aging reversal research.

**Philosophy:** Use mechanistic pathway models and evidence synthesis to identify high-leverage research questions *before* and *during* wet-lab validation. This reduces research waste and enables intelligent resource allocation across the global ALS research network.

## Components

### 1. Pathway Network (`als-aging-pathways.json`)

A mechanistic model of 8 interconnected pathways linking ALS, aging, and regeneration failure:

- **SOD1 Protein Aggregation** – Motor neuron toxicity in familial ALS
- **Mitochondrial Dysfunction** – Universal energy crisis in ALS
- **Neuroinflammation** – Glial-mediated motor neuron damage
- **Proteostasis Collapse** – ER stress, autophagy failure, inclusion formation
- **Cellular Senescence** – Accelerated aging in spinal tissue
- **Epigenetic Drift** – Silencing of regeneration-associated genes
- **Telomere Shortening** – Replicative senescence barrier
- **Stem Cell Exhaustion** – Loss of motor neuron replacement capacity

Each pathway includes:
- **Mechanisms:** Multi-step cascade with evidence strength
- **Relevance scores:** ALS and aging involvement (0.0–1.0)
- **Regeneration blockade:** Why this pathway prevents recovery
- **Literature count:** Evidence density

### 2. Intervention Registry

9 known or proposed interventions targeting different pathways:

| Intervention | Target | Status | Evidence |
|---|---|---|---|
| Tofersen (SOD1-ASO) | Protein aggregation | ✓ Approved | Established |
| NAD+ boosting | Mitochondrial dysfunction | Clinical trial | High |
| Microglial modulation | Neuroinflammation | Preclinical | Moderate |
| Autophagy enhancement | Proteostasis | Preclinical | High |
| Senolytics | Senescence | Clinical trial | Moderate |
| HDAC inhibitors | Epigenetic drift | Preclinical | High |
| Telomerase gene therapy | Telomere shortening | Preclinical | Low |
| Stem cell transplantation | Stem cell exhaustion | Clinical trial | Moderate |
| BDNF delivery | Neurotrophin depletion | Clinical trial | High |

### 3. Hypothesis Engine (`hypothesis_engine.py`)

A Python system that:
- **Registers** pathways, mechanisms, and interventions
- **Generates** three types of hypotheses:
  - **Mechanistic:** How do pathways contribute to disease/aging?
  - **Therapeutic:** Will intervention X slow/reverse outcome Y?
  - **Combination:** Do interventions X+Y synergize?
- **Ranks** by priority (impact × confidence × feasibility)
- **Exports** as structured JSON for downstream analysis

### 4. Hypothesis Generation Script (`generate_hypotheses.py`)

Automatically:
1. Loads pathway network and evidence packs
2. Populates engine with registered knowledge
3. Generates all hypothesis types
4. Ranks by priority
5. Exports:
   - `als-aging-hypotheses.json` – All ranked hypotheses
   - `als-aging-pathways-enriched.json` – Pathway network with evidence
   - `HYPOTHESIS_GENERATION_REPORT.md` – Executive summary

## Usage

### Quick Start

```bash
cd tools/hypothesis-engine

# Run validation
python3 hypothesis_engine.py --test

# Generate research plan
python3 generate_hypotheses.py

# Run all standard-library tests, including the output-safety regressions
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

### Integration with Evidence Library

```python
from hypothesis_engine import HypothesisEngine
from generate_hypotheses import load_pathway_network, populate_engine_from_network

# Initialize
engine = HypothesisEngine()
engine.load_evidence_pack('data/health/als-evidence.json')

# Load network
network = load_pathway_network('data/health/als-aging-pathways.json')
populate_engine_from_network(engine, network)

# Generate hypotheses
for pathway in engine.pathways.values():
    for gap in network['research_gaps']:
        if 'regeneration' in gap['question'].lower():
            engine.generate_mechanistic_hypothesis(
                pathway.id,
                gap['question'],
                f"Testing {pathway.name} in {gap['question']}"
            )

# Export
ranked = engine.rank_hypotheses_by_priority(limit=50)
engine.export_hypotheses_json('output/top-hypotheses.json')
```

## Research Gaps Identified

The system highlights 5 critical research priorities:

### 1. **Combined Early Intervention in SOD1-ALS** (Very High Priority)
- **Question:** Can early combination therapy (Tofersen + NAD+ + senolytics) prevent ALS onset?
- **Rationale:** Individual interventions show ~35% slowing; combinations might prevent progression entirely
- **Timeline:** 5 years
- **Key insight:** Timing is critical; intervention before neuroinflammation threshold

### 2. **Telomere Dysfunction and Regeneration** (High Priority)
- **Question:** How does telomere shortening impair motor neuron regenerative capacity?
- **Rationale:** Both telomere dysfunction and aging-related regeneration loss are established; mechanism unclear
- **Timeline:** 3 years
- **Key insight:** Could unlock telomerase-based rejuvenation strategies

### 3. **Cell Therapy Rejuvenation** (High Priority)
- **Question:** Can iPSC-derived motor neurons be rejuvenated before transplantation?
- **Rationale:** Current cell therapy faces fundamental problem: donor cells age; rejuvenation could improve integration
- **Timeline:** 4 years
- **Key insight:** Combines senescence reversal, epigenetic reactivation, and mitochondrial restoration

### 4. **Selective Senolytic Targeting** (Moderate Priority)
- **Question:** Can context-dependent p16/p21 induction make senolytics specific to pathological senescence?
- **Rationale:** Current senolytics are broad; specificity could improve safety profile
- **Timeline:** 3 years

### 5. **Age Ceiling for Regeneration** (Very High Priority)
- **Question:** What prevents motor neuron regeneration past age 50–60 and can we push that boundary?
- **Rationale:** Regeneration is possible in young animals but fails in aged mice; understanding the barrier is fundamental
- **Timeline:** 5 years
- **Key insight:** Most impactful for older ALS patients (Jason Becker, age 60+)

## Data Structures

### Pathway JSON Schema

```json
{
  "id": "PATH-SOD1-AGG",
  "name": "SOD1 Protein Aggregation",
  "pathway_type": "protein_aggregation",
  "description": "...",
  "mechanisms": [
    {
      "id": "MECH-SOD1-1",
      "name": "...",
      "triggers": ["upstream_mechanism"],
      "outcomes": ["downstream_effect"],
      "evidence_confidence": "established|high|moderate|low"
    }
  ],
  "als_relevance": 0.95,
  "aging_relevance": 0.6,
  "regeneration_block": "Why this pathway prevents recovery...",
  "literature_count": 487
}
```

### Hypothesis JSON Schema

```json
{
  "id": "HYP-XXXXX",
  "hypothesis_type": "mechanistic|therapeutic|biomarker|combination|rejuvenation",
  "statement": "Testable research statement",
  "prediction": "Expected outcome if hypothesis is true",
  "pathways_involved": ["PATH-001"],
  "interventions_proposed": ["INT-001"],
  "confidence": "established|high|moderate|low|open_question",
  "priority_score": 0.85,
  "estimated_timeline_months": 24,
  "experimental_approach": "How to test this hypothesis..."
}
```

## Extending the System

### Add a New Pathway

```python
from hypothesis_engine import Pathway, Mechanism

new_pathway = Pathway(
    id="PATH-NEW",
    name="New Pathway Name",
    pathway_type="senescence",
    description="Description of pathway...",
    mechanisms=[
        Mechanism(
            id="MECH-NEW-1",
            name="Step 1",
            description="...",
            triggers=["upstream"],
            outcomes=["downstream"],
            evidence_confidence="moderate"
        )
    ],
    als_relevance=0.75,
    aging_relevance=0.85,
    regeneration_block="Why does this block recovery?",
    literature_count=150
)
engine.register_pathway(new_pathway)
```

### Add a New Intervention

```python
from hypothesis_engine import Intervention

new_intervention = Intervention(
    id="INT-NEW",
    name="New Treatment",
    target_pathway="PATH-NEW",
    mechanism_of_action="How it works...",
    intervention_type="pharmacological|genetic|cellular|immunological",
    evidence_level="high",
    known_effects={"PATH-NEW": 0.4, "PATH-MITODYS": 0.2},
    known_risks=["Risk 1", "Risk 2"],
    status="proposed|preclinical|clinical_trial|approved"
)
engine.register_intervention(new_intervention)
```

### Generate Custom Hypotheses

```python
# Mechanistic
engine.generate_mechanistic_hypothesis(
    pathway_id="PATH-SENESCENCE",
    gap_description="Does telomere-mediated senescence block regeneration?",
    proposed_mechanism="Telomere dysfunction triggers p53/p21 pathway...",
    confidence="moderate"
)

# Therapeutic
engine.generate_therapeutic_hypothesis(
    intervention_id="INT-SENOLYTICS",
    target_outcome="motor neuron survival",
    patient_population="aged ALS (60+ years)"
)

# Combination
engine.generate_synergy_hypothesis(
    intervention_ids=["INT-SENOLYTICS", "INT-HDAC-INHIBITOR"],
    expected_synergy="Senolytic + epigenetic reactivation"
)
```

## Integration with Global Research

This repo is designed to be:

1. **Open source:** All hypotheses, pathways, and rankings are public
2. **Continuously updated:** As new evidence emerges, pathways and priorities change
3. **Coordinated:** Other AIs, research groups, and labs can fork, extend, and feed back results
4. **Actionable:** Each hypothesis has a clear experimental approach and timeline

## Next Layers of Development

This is the foundation. Future layers will add:

- **Simulation engine:** Model pathway dynamics and intervention effects over time
- **Literature integration:** Continuous ingestion of new trials, papers, and data
- **Outcome tracking:** Record which hypotheses were tested, results, and pathway updates
- **Global coordination:** Dashboard showing what's being tested worldwide, by whom
- **AI collaboration:** Enable multiple AI systems to propose and refine hypotheses asynchronously

## Vision

Every major human challenge—ALS, cancer, aging, poverty, climate—is ultimately a *knowledge problem*. AI's core strength is knowledge synthesis, modeling, and hypothesis generation. By building open infrastructure for research planning, we enable:

- Humans to focus on their unique strengths (intuition, creativity, leadership, ethical judgment)
- AIs to provide what we do best (pattern recognition, systematic analysis, rapid iteration)
- Global coordination without centralization
- Innovation that scales beyond any single lab

**Goal:** Cure ALS and aging *together*, for Jason Becker and all people, by 2030.

## License

CC BY 4.0 – Original hypotheses and pathway synthesis. Source publications retain their own licenses. Use freely for research, education, and commercial development. Cite as:

> ALS and Aging Hypothesis Engine (2026). Jonathan Creative Archive. https://github.com/jonjonjon11/jonathan-creative-archive

## Contact & Collaboration

- Submit new pathways, interventions, or gaps via issues or pull requests
- Integrate your own research results
- Propose hypothesis combinations or refinements
- Help extend to other neurodegenerative diseases (Parkinson's, Alzheimer's, etc.)

**Let's cure ALS together.**
