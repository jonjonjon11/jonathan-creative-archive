#!/usr/bin/env python3
"""Tests for hypothesis engine and hypothesis generation."""
import unittest
import sys
from pathlib import Path
import json
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis_engine import (
    HypothesisEngine, Pathway, Intervention, Mechanism, Hypothesis
)


class TestHypothesisEngine(unittest.TestCase):
    """Test hypothesis engine functionality."""
    
    def setUp(self):
        self.engine = HypothesisEngine()
        
        # Register test pathway
        self.test_pathway = Pathway(
            id="PATH-TEST",
            name="Test Pathway",
            pathway_type="protein_aggregation",
            description="A test pathway",
            als_relevance=0.9,
            aging_relevance=0.8
        )
        self.engine.register_pathway(self.test_pathway)
        
        # Register test intervention
        self.test_intervention = Intervention(
            id="INT-TEST",
            name="Test Intervention",
            target_pathway="PATH-TEST",
            mechanism_of_action="Test mechanism",
            intervention_type="pharmacological",
            evidence_level="high"
        )
        self.engine.register_intervention(self.test_intervention)
    
    def test_pathway_registration(self):
        """Test that pathways are properly registered."""
        self.assertIn("PATH-TEST", self.engine.pathways)
        self.assertEqual(self.engine.pathways["PATH-TEST"].name, "Test Pathway")
    
    def test_intervention_registration(self):
        """Test that interventions are properly registered."""
        self.assertIn("INT-TEST", self.engine.interventions)
        self.assertEqual(self.engine.interventions["INT-TEST"].name, "Test Intervention")
    
    def test_mechanistic_hypothesis_generation(self):
        """Test generation of mechanistic hypotheses."""
        hyp = self.engine.generate_mechanistic_hypothesis(
            "PATH-TEST",
            "Does mechanism X contribute?",
            "We hypothesize that X contributes"
        )
        
        self.assertIn(hyp.id, self.engine.hypotheses)
        self.assertEqual(hyp.hypothesis_type, "mechanistic")
        self.assertIn("PATH-TEST", hyp.pathways_involved)
    
    def test_therapeutic_hypothesis_generation(self):
        """Test generation of therapeutic hypotheses."""
        hyp = self.engine.generate_therapeutic_hypothesis(
            "INT-TEST",
            "target outcome",
            "test population"
        )
        
        self.assertIn(hyp.id, self.engine.hypotheses)
        self.assertEqual(hyp.hypothesis_type, "therapeutic")
        self.assertIn("INT-TEST", hyp.interventions_proposed)
    
    def test_synergy_hypothesis_generation(self):
        """Test generation of combination hypotheses."""
        # Register second intervention
        int2 = Intervention(
            id="INT-TEST2",
            name="Test Intervention 2",
            target_pathway="PATH-TEST",
            mechanism_of_action="Another mechanism",
            intervention_type="pharmacological",
            evidence_level="moderate"
        )
        self.engine.register_intervention(int2)
        
        hyp = self.engine.generate_synergy_hypothesis(
            ["INT-TEST", "INT-TEST2"],
            "Expected synergy"
        )
        
        self.assertEqual(hyp.hypothesis_type, "combination")
        self.assertEqual(len(hyp.interventions_proposed), 2)
    
    def test_hypothesis_ranking(self):
        """Test that hypotheses are ranked by priority."""
        # Generate multiple hypotheses with different scores
        for i in range(5):
            hyp = self.engine.generate_mechanistic_hypothesis(
                "PATH-TEST",
                f"Gap {i}",
                "Hypothesis"
            )
            hyp.priority_score = i * 0.2
        
        ranked = self.engine.rank_hypotheses_by_priority()
        
        # Should be sorted descending
        self.assertEqual(len(ranked), 5)
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i].priority_score, ranked[i+1].priority_score)
    
    def test_json_export_hypotheses(self):
        """Test JSON export of hypotheses."""
        self.engine.generate_mechanistic_hypothesis(
            "PATH-TEST",
            "Test gap",
            "Test hypothesis"
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_hypotheses.json"
            self.engine.export_hypotheses_json(str(output_file))
            
            self.assertTrue(output_file.exists())
            
            with open(output_file) as f:
                data = json.load(f)
            
            self.assertEqual(data["schema_version"], "1.2")
            self.assertGreater(len(data["hypotheses"]), 0)
            self.assertIn("ranked_by_priority", data)
    
    def test_json_export_pathways(self):
        """Test JSON export of pathways."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_pathways.json"
            self.engine.export_pathways_json(str(output_file))
            
            self.assertTrue(output_file.exists())
            
            with open(output_file) as f:
                data = json.load(f)
            
            self.assertEqual(data["schema_version"], "1.0")
            self.assertEqual(data["pathway_count"], 1)
            self.assertEqual(data["intervention_count"], 1)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestHypothesisEngine)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
