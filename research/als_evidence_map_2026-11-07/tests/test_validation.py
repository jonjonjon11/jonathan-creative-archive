import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate import ValidationError, load, validate
from render import render


class EvidenceValidationTests(unittest.TestCase):
    def setUp(self):
        self.document, self.register = load()
        self.by_id = {r["id"]: r for r in self.document["records"]}

    def rejects(self):
        with self.assertRaises(ValidationError):
            validate(self.document, self.register)

    def test_baseline(self):
        self.assertEqual(self.document["review_status"], "draft_research_candidate_not_independently_ALS_clinician_reviewed")
        self.assertEqual(validate(self.document, self.register), {"records": 6, "sources": 14, "observations": 15})

    def test_render_deterministic_and_current(self):
        first = render(self.document, self.register)
        self.assertEqual(first, render(copy.deepcopy(self.document), copy.deepcopy(self.register)))
        for name, content in first.items():
            self.assertEqual((ROOT / name).read_text(encoding="utf-8"), content)

    def test_unknown_source_rejected(self):
        self.document["records"][0]["observations"][0]["source_ids"] = ["invented"]
        self.rejects()

    def test_negative_primary_cannot_be_rewritten(self):
        self.by_id["dnl343"]["observations"][0]["primary_endpoint_met"] = True
        self.rejects()

    def test_biomarker_cannot_be_primary_success(self):
        observation = next(o for o in self.by_id["tofersen_sod1"]["observations"] if o["kind"] == "biomarker")
        observation["primary_endpoint_met"] = True
        self.rejects()

    def test_sponsor_evidence_cannot_be_promoted(self):
        self.by_id["ulefnersen_fus"]["stage"] = "peer_reviewed_randomized_trial"
        self.rejects()

    def test_mechanism_cannot_be_trial(self):
        self.by_id["unc13a_mechanism"]["trial_ids"] = ["NCT00000000"]
        self.rejects()

    def test_pvalue_bounds(self):
        self.by_id["ulefnersen_fus"]["observations"][0]["statistic"]["p_value"] = 1.5
        self.rejects()

    def test_bayesian_interval_kind_preserved(self):
        self.by_id["dnl343"]["observations"][0]["statistic"]["interval"]["type"] = "confidence"
        self.rejects()

    def test_reversed_interval_rejected(self):
        self.by_id["tofersen_sod1"]["observations"][1]["statistic"]["interval"]["lower"] = 50
        self.rejects()

    def test_future_source_rejected(self):
        self.register["sources"][0]["publication_date"] = "2027-01-01"
        self.rejects()

    def test_missing_caveat_rejected(self):
        self.by_id["qrl201_stmn2"]["caveats"] = []
        self.rejects()

    def test_withdrawal_date_not_announcement(self):
        self.by_id["relyvrio_withdrawal"]["regulatory_status"]["event_date"] = "2024-04-04"
        self.rejects()

    def test_url_credentials_rejected(self):
        self.register["sources"][0]["url"] = "https://name:secret@example.org/paper"
        self.rejects()

    def test_duplicate_source_rejected(self):
        self.register["sources"].append(copy.deepcopy(self.register["sources"][0]))
        self.rejects()

    def test_numeric_regulatory_status_rejected(self):
        self.by_id["ulefnersen_fus"]["regulatory_status"]["status"] = 123
        self.rejects()

    def test_unsupported_approval_rejected(self):
        self.by_id["ulefnersen_fus"]["regulatory_status"]["status"] = "approved"
        self.rejects()

    def test_regulatory_source_outside_parent_rejected(self):
        self.by_id["ulefnersen_fus"]["regulatory_status"]["source_ids"] = ["unc13a_ma_2022"]
        self.rejects()

    def test_irrelevant_in_parent_source_rejected(self):
        record = self.by_id["ulefnersen_fus"]
        record["source_ids"].append("unc13a_ma_2022")
        record["regulatory_status"]["source_ids"] = ["unc13a_ma_2022"]
        self.rejects()

    def test_other_drug_approval_source_rejected(self):
        record = self.by_id["ulefnersen_fus"]
        record["source_ids"].append("qalsody_snapshot")
        record["regulatory_status"] = {"status": "original_accelerated_approval", "jurisdiction": "US", "event_date": "2023-04-25", "source_ids": ["qalsody_snapshot"]}
        self.rejects()

    def test_sponsor_cannot_assert_official_approval(self):
        source = next(s for s in self.register["sources"] if s["id"] == "fusion_ionis_2026")
        source["regulatory_assertions"][0]["status"] = "approved"
        self.by_id["ulefnersen_fus"]["regulatory_status"]["status"] = "approved"
        self.rejects()

    def test_numeric_identifiers_rejected(self):
        self.register["sources"][0]["identifiers"] = 42
        self.rejects()

    def test_numeric_unit_rejected(self):
        self.by_id["tofersen_sod1"]["observations"][1]["statistic"]["unit"] = 42
        self.rejects()

    def test_pvalue_requires_method(self):
        self.by_id["tofersen_sod1"]["observations"][0]["statistic"]["p_value_method"] = None
        self.rejects()

    def test_tofersen_analyses_remain_distinct(self):
        primary, supportive = self.by_id["tofersen_sod1"]["observations"][:2]
        self.assertEqual(primary["statistic"]["p_value"], 0.97)
        self.assertEqual(primary["statistic"]["p_value_method"], "Joint-rank test with multiple imputation")
        self.assertIsNone(primary["statistic"]["value"])
        self.assertEqual(supportive["kind"], "clinical_supportive")
        self.assertEqual(supportive["statistic"]["value"], 1.2)
        self.assertEqual(supportive["statistic"]["p_value"], 0.60)
        self.assertEqual(supportive["statistic"]["p_value_method"], "ANCOVA with multiple imputation")

    def test_scoped_exclusion_cannot_be_extracted_evidence(self):
        self.by_id["tofersen_sod1"]["source_ids"].append("valor_ole_final_2025")
        self.rejects()

    def test_matching_new_regulator_assertion_can_support_new_status(self):
        # Synthetic fixture only: no live claim about FUS approval or live URL.
        # Demonstrates absence of a hardcoded "FUS must be investigational" rule.
        new_source = copy.deepcopy(self.register["sources"][2])
        new_source.update({"id": "synthetic_regulator", "title": "Synthetic test fixture", "url": "https://example.org/synthetic-regulator", "publication_date": "2026-11-01", "date_precision": "day", "regulatory_assertions": [{"record_id": "ulefnersen_fus", "status": "approved", "jurisdiction": "US", "event_date": "2026-11-01", "locator": "Synthetic test fixture only"}]})
        self.register["sources"].append(new_source)
        record = self.by_id["ulefnersen_fus"]
        record["source_ids"].append("synthetic_regulator")
        record["regulatory_status"] = {"status": "approved", "jurisdiction": "US", "event_date": "2026-11-01", "source_ids": ["synthetic_regulator"]}
        self.assertEqual(validate(self.document, self.register)["sources"], 15)


if __name__ == "__main__":
    unittest.main()
