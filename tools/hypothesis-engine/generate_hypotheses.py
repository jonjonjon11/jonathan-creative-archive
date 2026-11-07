#!/usr/bin/env python3
"""Generate research hypotheses from ALS/aging pathway network.

This script:
1. Loads pathway network from als-aging-pathways.json
2. Loads evidence pack from als-evidence.json
3. Generates mechanistic, therapeutic, and combination hypotheses
4. Ranks by priority and impact
5. Exports ranked hypotheses for research planning
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import date
from hypothesis_engine import HypothesisEngine, Pathway, Intervention, Mechanism


def load_pathway_network(network_path: str) -> dict:
    """Load mechanistic pathway network."""
    try:
        with open(network_path, 'r') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading pathway network: {e}", file=sys.stderr)
        return {}


def populate_engine_from_network(engine: HypothesisEngine, network: dict) -> None:
    """Register all pathways and interventions from network."""
    
    for pathway_data in network.get('pathways', []):
        mechanisms = [
            Mechanism(
                id=m['id'],
                name=m['name'],
                description=m['description'],
                triggers=m.get('triggers', []),
                outcomes=m.get('outcomes', []),
                evidence_confidence=m.get('evidence_confidence', 'moderate'),
                supporting_sources=[]
            )
            for m in pathway_data.get('mechanisms', [])
        ]
        
        pathway = Pathway(
            id=pathway_data['id'],
            name=pathway_data['name'],
            pathway_type=pathway_data['pathway_type'],
            description=pathway_data['description'],
            mechanisms=mechanisms,
            als_relevance=pathway_data.get('als_relevance', 0.5),
            aging_relevance=pathway_data.get('aging_relevance', 0.5),
            regeneration_block=pathway_data.get('regeneration_block'),
            literature_count=pathway_data.get('literature_count', 0)
        )
        engine.register_pathway(pathway)
    
    for intervention_data in network.get('interventions', []):
        intervention = Intervention(
            id=intervention_data['id'],
            name=intervention_data['name'],
            target_pathway=intervention_data['target_pathway'],
            mechanism_of_action=intervention_data['mechanism_of_action'],
            intervention_type=intervention_data['intervention_type'],
            evidence_level=intervention_data['evidence_level'],
            known_effects=intervention_data.get('known_effects', {}),
            known_risks=intervention_data.get('known_risks', []),
            status=intervention_data.get('status', 'proposed')
        )
        engine.register_intervention(intervention)


def generate_hypotheses(engine: HypothesisEngine, network: dict) -> None:
    """Generate all hypothesis types."""
    
    # 1. Mechanistic hypotheses from research gaps
    print("Generating mechanistic hypotheses from research gaps...")
    for gap in network.get('research_gaps', []):
        question = gap['question']
        priority = gap['priority']
        
        # Find most relevant pathway from gap context
        for pathway in engine.pathways.values():
            if 'aging' in question.lower() or 'telomere' in question.lower():
                if pathway.pathway_type in ['telomere_shortening', 'senescence', 'epigenetic_drift']:
                    confidence = 'high' if priority == 'very_high' else 'moderate'
                    engine.generate_mechanistic_hypothesis(
                        pathway.id,
                        question,
                        f"Understanding the role of {pathway.name} is critical to this research gap.",
                        confidence
                    )
                    break
            elif 'senolytics' in question.lower():
                if pathway.pathway_type == 'senescence':
                    engine.generate_mechanistic_hypothesis(
                        pathway.id,
                        question,
                        "Senolytics preferentially target senescent cells; understanding selectivity is crucial.",
                        'moderate'
                    )
                    break
    
    # 2. Therapeutic hypotheses for each intervention
    print("Generating therapeutic hypotheses...")
    intervention_targets = {
        'INT-TOFERSEN': ('motor neuron survival', 'SOD1-ALS'),
        'INT-NAD-BOOST': ('mitochondrial ATP production', 'all ALS'),
        'INT-MICROGLIA-MOD': ('neuroinflammation reduction', 'all ALS'),
        'INT-AUTOPHAGY-ENHANCE': ('protein aggregate clearance', 'all ALS'),
        'INT-SENOLYTICS': ('senescent cell elimination', 'aged/advanced ALS'),
        'INT-HDAC-INHIBITOR': ('regeneration gene expression', 'all ALS'),
        'INT-BDNF-DELIVERY': ('motor neuron survival and regrowth', 'all ALS'),
        'INT-STEM-CELL-TX': ('motor neuron replacement', 'advanced ALS'),
    }
    
    for int_id, (outcome, population) in intervention_targets.items():
        if int_id in engine.interventions:
            engine.generate_therapeutic_hypothesis(int_id, outcome, population)
    
    # 3. Combination hypotheses for high-priority combinations
    print("Generating combination hypotheses...")
    combinations = [
        (['INT-TOFERSEN', 'INT-NAD-BOOST', 'INT-SENOLYTICS'], 
         'Multi-pathway SOD1-ALS intervention'),
        (['INT-MICROGLIA-MOD', 'INT-AUTOPHAGY-ENHANCE'], 
         'Glial support + proteasome rescue'),
        (['INT-HDAC-INHIBITOR', 'INT-BDNF-DELIVERY'], 
         'Epigenetic reactivation + neurotrophic support'),
        (['INT-STEM-CELL-TX', 'INT-BDNF-DELIVERY', 'INT-MICROGLIA-MOD'], 
         'Regeneration + trophic + niche support'),
    ]
    
    for int_ids, synergy_desc in combinations:
        # Check all interventions exist
        if all(iid in engine.interventions for iid in int_ids):
            engine.generate_synergy_hypothesis(int_ids, synergy_desc)


def export_research_plan(engine: HypothesisEngine, output_dir: str) -> None:
    """Export comprehensive research plan."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Export top hypotheses
    top_hypotheses = engine.rank_hypotheses_by_priority(limit=100)
    
    hypotheses_file = output_path / "als-aging-hypotheses.json"
    plan_data = {
        "schema_version": "1.0",
        "generated": date.today().isoformat(),
        "title": "ALS and Aging Research Hypothesis Plan",
        "description": "AI-generated high-priority research hypotheses ranked by impact, confidence, and feasibility.",
        "hypothesis_count": len(engine.hypotheses),
        "pathways_analyzed": len(engine.pathways),
        "interventions_reviewed": len(engine.interventions),
        "top_hypotheses": [
            {
                "rank": i + 1,
                "id": h.id,
                "type": h.hypothesis_type,
                "statement": h.statement,
                "prediction": h.prediction,
                "confidence": h.confidence,
                "priority_score": h.priority_score,
                "timeline_months": h.estimated_timeline_months,
                "pathways": h.pathways_involved,
                "interventions": h.interventions_proposed,
                "experimental_approach": h.experimental_approach
            }
            for i, h in enumerate(top_hypotheses[:30])
        ],
        "all_hypotheses": [
            {
                "id": h.id,
                "type": h.hypothesis_type,
                "statement": h.statement,
                "confidence": h.confidence,
                "priority_score": h.priority_score
            }
            for h in top_hypotheses
        ]
    }
    
    with open(hypotheses_file, 'w') as f:
        json.dump(plan_data, f, indent=2)
    
    print(f"✓ Exported {len(top_hypotheses)} ranked hypotheses to {hypotheses_file}")
    
    # Export pathway network
    engine.export_pathways_json(str(output_path / "als-aging-pathways-enriched.json"))
    
    # Generate summary report
    report_file = output_path / "HYPOTHESIS_GENERATION_REPORT.md"
    with open(report_file, 'w') as f:
        f.write("# ALS and Aging Research Hypothesis Generation Report\n\n")
        f.write(f"**Generated:** {date.today().isoformat()}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Pathways Analyzed:** {len(engine.pathways)}\n")
        f.write(f"- **Interventions Reviewed:** {len(engine.interventions)}\n")
        f.write(f"- **Hypotheses Generated:** {len(engine.hypotheses)}\n")
        f.write(f"- **Top Priorities:** {len(top_hypotheses[:10])}\n\n")
        
        f.write("## Top 10 Research Hypotheses\n\n")
        for i, h in enumerate(top_hypotheses[:10]):
            f.write(f"### {i+1}. {h.statement}\n\n")
            f.write(f"**Type:** {h.hypothesis_type}\n")
            f.write(f"**Confidence:** {h.confidence}\n")
            f.write(f"**Priority Score:** {h.priority_score:.2f}\n")
            f.write(f"**Timeline:** ~{h.estimated_timeline_months} months\n")
            f.write(f"**Prediction:** {h.prediction}\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. **Prioritize testing:** Focus first on high-confidence, high-impact hypotheses (scores > 0.75)\n")
        f.write("2. **Run parallel tracks:** Some hypotheses can be tested simultaneously\n")
        f.write("3. **Integrate results:** Use findings to refine pathway models and generate new hypotheses\n")
        f.write("4. **Coordinate globally:** Share results with other ALS research groups to avoid duplication\n\n")
    
    print(f"✓ Generated research report: {report_file}")


def main():
    script_dir = Path(__file__).parent.parent.parent / "data" / "health"
    
    network_path = script_dir / "als-aging-pathways.json"
    evidence_path = script_dir / "als-evidence.json"
    
    if not network_path.exists():
        print(f"Error: Pathway network not found at {network_path}", file=sys.stderr)
        sys.exit(1)
    
    print("Loading ALS/Aging pathway network...")
    network = load_pathway_network(str(network_path))
    
    print("Initializing hypothesis engine...")
    engine = HypothesisEngine()
    
    if evidence_path.exists():
        print(f"Loading evidence pack from {evidence_path}...")
        engine.load_evidence_pack(str(evidence_path))
    
    print("Populating pathway and intervention registries...")
    populate_engine_from_network(engine, network)
    
    print(f"Registered {len(engine.pathways)} pathways and {len(engine.interventions)} interventions")
    
    print("Generating hypotheses...")
    generate_hypotheses(engine, network)
    
    print(f"Generated {len(engine.hypotheses)} research hypotheses")
    
    print("Exporting research plan...")
    export_research_plan(engine, str(script_dir))
    
    print("\n✓ Hypothesis generation complete!")
    print(f"  Output: {script_dir}")


if __name__ == "__main__":
    main()
