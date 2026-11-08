#!/usr/bin/env python3
"""Template-based, unvalidated research questions from a pathway registry.

This code does not simulate disease, appraise evidence, or predict treatment
effects. Loading an evidence pack stores it; generation does not analyze it.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum
from pathlib import Path
import sys
from typing import Optional, Any
import hashlib


HYPOTHESIS_LIMITATIONS = [
    "Generated statements are unvalidated research questions, not clinical predictions or treatment recommendations.",
    "Outcome direction and effect size are not inferred for therapeutic questions; populations are caller-supplied labels, not validated indications.",
    "Priority scores and timelines are unvalidated heuristics/defaults, not probabilities, clinical effect estimates, or a validated research ranking.",
    "Loading an evidence pack does not appraise it or connect its sources to a generated question. Literature counts and registry coefficients are not verified here.",
    "Mechanistic and combination proposals remain unvalidated; caller-supplied descriptions do not establish causality, efficacy, or synergy.",
]


def _question_text(name: str, value: str) -> str:
    """Normalize caller context without inferring its scientific meaning."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    return value.strip()


def _question_id(prefix: str, context: list) -> str:
    """Hash structured context with field boundaries, not concatenated text."""
    identity = json.dumps(context, ensure_ascii=False, separators=(",", ":"))
    return f"{prefix}{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16].upper()}"


class PathwayType(Enum):
    """Categories of biological pathways relevant to ALS/aging/regeneration."""
    PROTEIN_AGGREGATION = "protein_aggregation"
    MITOCHONDRIAL_DYSFUNCTION = "mitochondrial_dysfunction"
    NEUROINFLAMMATION = "neuroinflammation"
    AXONAL_DEGENERATION = "axonal_degeneration"
    MOTOR_NEURON_LOSS = "motor_neuron_loss"
    SENESCENCE = "senescence"
    EPIGENETIC_DRIFT = "epigenetic_drift"
    TELOMERE_SHORTENING = "telomere_shortening"
    STEM_CELL_EXHAUSTION = "stem_cell_exhaustion"
    PROTEOSTASIS_COLLAPSE = "proteostasis_collapse"
    ROS_ACCUMULATION = "ros_accumulation"
    NEUROTROPHIN_DEPLETION = "neurotrophin_depletion"


class HypothesisType(Enum):
    """Categories of testable research hypotheses."""
    MECHANISTIC = "mechanistic"
    THERAPEUTIC = "therapeutic"
    BIOMARKER = "biomarker"
    COMBINATION = "combination"
    REJUVENATION = "rejuvenation"


class ConfidenceLevel(Enum):
    """Evidence strength for hypothesis support."""
    ESTABLISHED = "established"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    OPEN_QUESTION = "open_question"


@dataclass
class Mechanism:
    """A single step in a biological pathway."""
    id: str
    name: str
    description: str
    triggers: list[str] = field(default_factory=list)
    outcomes: list[str] = field(default_factory=list)
    evidence_confidence: str = "moderate"
    supporting_sources: list[str] = field(default_factory=list)


@dataclass
class Pathway:
    """A multi-step biological pathway implicated in disease/aging."""
    id: str
    name: str
    pathway_type: str
    description: str
    mechanisms: list[Mechanism] = field(default_factory=list)
    als_relevance: float = 0.5
    aging_relevance: float = 0.5
    regeneration_block: Optional[str] = None
    literature_count: int = 0


@dataclass
class Intervention:
    """A proposed treatment or manipulation."""
    id: str
    name: str
    target_pathway: str
    mechanism_of_action: str
    intervention_type: str
    evidence_level: str
    known_effects: dict[str, float] = field(default_factory=dict)
    known_risks: list[str] = field(default_factory=list)
    status: str = "proposed"


@dataclass
class Hypothesis:
    """A testable research hypothesis."""
    id: str
    hypothesis_type: str
    statement: str
    prediction: str
    pathways_involved: list[str] = field(default_factory=list)
    interventions_proposed: list[str] = field(default_factory=list)
    confidence: str = "moderate"
    supporting_evidence: list[str] = field(default_factory=list)
    contradicting_evidence: list[str] = field(default_factory=list)
    experimental_approach: str = ""
    estimated_timeline_months: int = 24
    priority_score: float = 0.5
    target_outcome: Optional[str] = None
    patient_population: Optional[str] = None
    gap_description: Optional[str] = None
    proposed_mechanism: Optional[str] = None
    expected_synergy: Optional[str] = None


class HypothesisEngine:
    """Generate and rank research hypotheses from mechanistic knowledge."""

    def __init__(self):
        self.pathways: dict[str, Pathway] = {}
        self.mechanisms: dict[str, Mechanism] = {}
        self.interventions: dict[str, Intervention] = {}
        self.hypotheses: dict[str, Hypothesis] = {}
        self.evidence_pack: dict[str, Any] = {}

    def load_evidence_pack(self, pack_path: str) -> None:
        """Store a pack without appraising it or using it in generation/scoring."""
        try:
            with open(pack_path, 'r') as f:
                self.evidence_pack = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load evidence pack: {e}", file=sys.stderr)

    def register_pathway(self, pathway: Pathway) -> None:
        """Register a biological pathway."""
        self.pathways[pathway.id] = pathway
        for mechanism in pathway.mechanisms:
            self.mechanisms[mechanism.id] = mechanism

    def register_intervention(self, intervention: Intervention) -> None:
        """Register a known or proposed intervention."""
        self.interventions[intervention.id] = intervention

    def generate_mechanistic_hypothesis(
        self,
        pathway_id: str,
        gap_description: str,
        proposed_mechanism: str,
        confidence: str = "moderate"
    ) -> Hypothesis:
        """Identify a question by pathway, normalized gap, and proposed mechanism.

        Confidence is updateable metadata, not part of question identity.
        """
        pathway = self.pathways.get(pathway_id)
        if not pathway:
            raise ValueError(f"Unknown pathway: {pathway_id}")

        gap_description = _question_text("gap_description", gap_description)
        proposed_mechanism = _question_text("proposed_mechanism", proposed_mechanism)
        hyp_id = _question_id("HYP-MEC-", [pathway_id, gap_description, proposed_mechanism])
        hyp = Hypothesis(
            id=hyp_id,
            hypothesis_type="mechanistic",
            statement=f"{pathway.name}: {gap_description}",
            prediction=f"We hypothesize that {proposed_mechanism} in {pathway.name}",
            pathways_involved=[pathway_id],
            confidence=confidence,
            priority_score=pathway.als_relevance * pathway.aging_relevance,
            gap_description=gap_description,
            proposed_mechanism=proposed_mechanism,
        )
        self.hypotheses[hyp.id] = hyp
        return hyp

    def generate_therapeutic_hypothesis(
        self,
        intervention_id: str,
        target_outcome: str,
        patient_population: str = "unspecified population"
    ) -> Hypothesis:
        """Pose an untested, direction-neutral intervention/outcome question.

        A registry mechanism or evidence label does not establish an effect on
        the requested outcome. Preserve the supplied population and distinguish
        questions for different outcomes or populations. No evidence appraisal
        or numerical prediction is performed.
        """
        intervention = self.interventions.get(intervention_id)
        if not intervention:
            raise ValueError(f"Unknown intervention: {intervention_id}")

        target_outcome = _question_text("target_outcome", target_outcome)
        patient_population = _question_text("patient_population", patient_population)
        hyp_id = _question_id("HYP-THR-", [intervention_id, target_outcome, patient_population])
        hyp = Hypothesis(
            id=hyp_id,
            hypothesis_type="therapeutic",
            statement=f"Does {intervention.name} change {target_outcome} in {patient_population}?",
            prediction=(f"Test whether {intervention.name} changes {target_outcome} in {patient_population} "
                        "relative to a prespecified comparator; direction and effect size are not inferred "
                        "from registry metadata."),
            pathways_involved=[intervention.target_pathway],
            interventions_proposed=[intervention_id],
            confidence="open_question",
            # Retained for compatibility, not validated as research priority.
            priority_score=0.9 if intervention.evidence_level == 'established' else 0.5,
            target_outcome=target_outcome,
            patient_population=patient_population,
        )
        self.hypotheses[hyp.id] = hyp
        return hyp

    def generate_synergy_hypothesis(
        self,
        intervention_ids: list[str],
        expected_synergy: str
    ) -> Hypothesis:
        """Preserve the ordered intervention list and proposed interaction.

        Order is retained, not interpreted as a dosing/timing protocol. Reject
        incomplete combinations instead of silently dropping unknown members.
        """
        if (not isinstance(intervention_ids, list) or len(intervention_ids) < 2
                or any(not isinstance(iid, str) or not iid.strip() for iid in intervention_ids)):
            raise ValueError("intervention_ids must be a list of at least two distinct nonempty IDs")
        if len(set(intervention_ids)) != len(intervention_ids):
            raise ValueError("intervention_ids must contain distinct IDs")
        for iid in intervention_ids:
            if iid not in self.interventions:
                raise ValueError(f"Unknown intervention: {iid}")
        expected_synergy = _question_text("expected_synergy", expected_synergy)
        intervention_ids = list(intervention_ids)
        hyp_id = _question_id("HYP-SYN-", [intervention_ids, expected_synergy])
        interventions = [self.interventions[iid] for iid in intervention_ids]

        target_pathways = [i.target_pathway for i in interventions]
        names = " + ".join([i.name for i in interventions])

        hyp = Hypothesis(
            id=hyp_id,
            hypothesis_type="combination",
            statement=f"Combination question: {names}",
            prediction=(f"Test whether {names} has the proposed combined effect: {expected_synergy}. "
                        "This is an untested hypothesis, not demonstrated synergy."),
            pathways_involved=target_pathways,
            interventions_proposed=intervention_ids,
            confidence="open_question",
            priority_score=0.7,
            expected_synergy=expected_synergy,
        )
        self.hypotheses[hyp.id] = hyp
        return hyp

    def rank_hypotheses_by_priority(self, limit: Optional[int] = 20) -> list[Hypothesis]:
        """Sort heuristic scores; None requests all records, otherwise a preview.

        Scores are not a validated priority model. The default remains 20.
        """
        if limit is not None and (type(limit) is not int or limit < 0):
            raise ValueError("limit must be a nonnegative integer or None")
        ranked = sorted(
            self.hypotheses.values(),
            key=lambda h: (h.priority_score, len(h.supporting_evidence)),
            reverse=True
        )
        return ranked[:limit]

    def export_hypotheses_json(self, output_path: str) -> None:
        """Export hypotheses as structured JSON for downstream analysis."""
        export_data = {
            "schema_version": "1.2",
            "status": "unvalidated_research_questions",
            "limitations": HYPOTHESIS_LIMITATIONS,
            "generated": date.today().isoformat(),
            "hypothesis_count": len(self.hypotheses),
            "hypotheses": [asdict(h) for h in self.hypotheses.values()],
            "ranked_by_priority": [
                {"id": h.id, "statement": h.statement, "priority": h.priority_score}
                for h in self.rank_hypotheses_by_priority(limit=None)
            ]
        }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        print(f"Exported {len(self.hypotheses)} hypotheses to {output_path}")

    def export_pathways_json(self, output_path: str) -> None:
        """Export pathway network for visualization/analysis."""
        export_data = {
            "schema_version": "1.0",
            "generated": date.today().isoformat(),
            "pathways": [asdict(p) for p in self.pathways.values()],
            "interventions": [asdict(i) for i in self.interventions.values()],
            "pathway_count": len(self.pathways),
            "intervention_count": len(self.interventions)
        }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        print(f"Exported {len(self.pathways)} pathways and {len(self.interventions)} interventions to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        engine = HypothesisEngine()

        sod1_pathway = Pathway(
            id="PATH-SOD1-AGG",
            name="SOD1 Protein Aggregation and Toxicity",
            pathway_type="protein_aggregation",
            description="Mutant SOD1 misfolds, aggregates, and causes motor neuron toxicity",
            als_relevance=0.95,
            aging_relevance=0.6
        )
        engine.register_pathway(sod1_pathway)

        tofersen = Intervention(
            id="INT-TOFERSEN",
            name="Tofersen (SOD1 antisense oligonucleotide)",
            target_pathway="PATH-SOD1-AGG",
            mechanism_of_action="Reduces SOD1 mRNA translation",
            intervention_type="pharmacological",
            evidence_level="high",
            status="approved"
        )
        engine.register_intervention(tofersen)

        hyp1 = engine.generate_mechanistic_hypothesis(
            "PATH-SOD1-AGG",
            "Does early SOD1 reduction prevent aggregate seeding?",
            "Early intervention in SOD1-ALS prevents initial aggregate nucleation"
        )
        
        hyp2 = engine.generate_therapeutic_hypothesis(
            "INT-TOFERSEN",
            "motor neuron survival",
            "SOD1-ALS patients with early diagnosis"
        )

        print(f"Generated {len(engine.hypotheses)} hypotheses")
        print(f"Top hypothesis: {engine.rank_hypotheses_by_priority(1)[0].statement}")
        print("✓ Hypothesis engine validation passed")

    else:
        print("Hypothesis Engine Ready")
        print("Use: hypothesis_engine.py --test")
        print("Or import as module: from hypothesis_engine import HypothesisEngine")
