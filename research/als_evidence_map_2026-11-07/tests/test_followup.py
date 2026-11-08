import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import ValidationError, load
from followup import load_followup, validate_followup, render_followup


class FollowupTests(unittest.TestCase):
    def setUp(self):
        self.doc = load_followup()
        self.historical, self.register = load()
        self.obs = {o['id']: o for o in self.doc['observations']}

    def rejects(self):
        with self.assertRaises(ValidationError):
            validate_followup(self.doc, self.historical)

    def test_baseline(self):
        self.assertEqual(validate_followup(self.doc, self.historical), {'followups': 1, 'sources': 2, 'observations': 7})

    def test_generated_view_current_and_deterministic(self):
        rendered = render_followup(self.doc)
        self.assertEqual(rendered, render_followup(copy.deepcopy(self.doc)))
        self.assertEqual(rendered, (ROOT / 'VALOR_OLE_FOLLOWUP.md').read_text())
        self.assertIn('No independent ALS clinician review', rendered)
        self.assertIn('0.0541', rendered)
        self.assertIn('Post hoc', rendered)

    def test_source_identity_and_exact_locators(self):
        for o in self.obs.values():
            self.assertTrue(all(e['locator'] for e in o['source_refs']))
        rank = self.obs['function_alternative_jrt']
        self.assertIn('eFigure 4', rank['source_refs'][1]['locator'])
        self.assertIn('PDF page 20', rank['source_refs'][1]['locator'])

    def test_historical_primary_and_supportive_unchanged(self):
        first = self.historical['records'][0]['observations']
        self.assertEqual(first[0]['statistic']['p_value'], .97)
        self.assertFalse(first[0]['primary_endpoint_met'])
        self.assertEqual(first[1]['statistic']['value'], 1.2)
        self.assertEqual(first[1]['statistic']['p_value'], .6)
        self.assertEqual(self.historical['as_of'], '2026-11-07')
        self.assertEqual(self.register['access_date'], '2026-11-07')

    def test_double_extracted_values(self):
        # Transcription regression, not independent scientific validation.
        a = self.obs['function_ancova']['statistic']
        self.assertEqual((a['value'], a['interval']['lower'], a['interval']['upper'], a['p_value']), (3.6, -1.2, 8.4, .1432))
        self.assertEqual(self.obs['function_jrt']['statistic']['p_value'], .1064)
        self.assertEqual(self.obs['function_alternative_jrt']['statistic']['p_value'], .0541)
        self.assertGreater(self.obs['function_alternative_jrt']['statistic']['p_value'], .05)
        for key, values in [('survival_death_pv', (.64, .28, 1.46, .29)), ('survival_death', (.52, .20, 1.36, .18))]:
            s = self.obs[key]['statistic']
            self.assertEqual((s['value'], s['interval']['lower'], s['interval']['upper'], s['p_value']), values)
        self.assertEqual(self.obs['neurological_safety']['count'], {'numerator':9, 'denominator':104, 'unit':'participants', 'reported_percent':8.7})

    def test_unknown_parent_rejected(self):
        self.doc['parent_record_id'] = 'invented'
        self.rejects()

    def test_followup_cannot_be_placebo_controlled(self):
        self.doc['design']['classification'] = 'randomized_placebo_controlled'
        self.rejects()

    def test_no_primary_success(self):
        self.obs['function_ancova']['primary_endpoint_met'] = True
        self.rejects()

    def test_biomarker_not_clinical(self):
        self.obs['biomarkers']['kind'] = 'clinical_followup'
        self.rejects()

    def test_clinician_review_not_invented(self):
        self.doc['review_status'] = 'clinically_validated'
        self.rejects()

    def test_duplicate_observation_rejected(self):
        self.doc['observations'][-1] = copy.deepcopy(self.doc['observations'][0])
        self.rejects()

    def test_unknown_source_rejected(self):
        self.obs['function_ancova']['source_refs'][0]['source_id'] = 'invented'
        self.rejects()

    def test_missing_claim_locator_rejected(self):
        self.obs['function_ancova']['source_refs'][0]['locator'] = ''
        self.rejects()

    def test_missing_supplement_rejected(self):
        self.obs['function_jrt']['source_refs'].pop()
        self.rejects()

    def test_duplicate_source_rejected(self):
        self.doc['sources'].append(copy.deepcopy(self.doc['sources'][0]))
        self.rejects()

    def test_source_not_read_rejected(self):
        self.doc['sources'][1]['access_level'] = 'indexed_abstract_only'
        self.rejects()

    def test_future_access_rejected(self):
        self.doc['sources'][1]['access_date'] = '2027-01-01'
        self.rejects()

    def test_future_publication_rejected(self):
        self.doc['sources'][1]['publication_date'] = '2027-01-01'
        self.rejects()

    def test_url_credentials_rejected(self):
        self.doc['sources'][0]['url'] = 'https://name:secret@example.org'
        self.rejects()

    def test_safety_denominator_rejected(self):
        self.obs['neurological_safety']['count']['denominator'] = 108
        self.rejects()

    def test_safety_percentage_rejected(self):
        self.obs['neurological_safety']['count']['reported_percent'] = 9.6
        self.rejects()

    def test_completion_denominator_rejected(self):
        self.doc['design']['ole_completed']['early_start'] = 73
        self.rejects()

    def test_rank_does_not_inherit_mean_difference(self):
        self.obs['function_alternative_jrt']['statistic']['value'] = 3.6
        self.rejects()

    def test_nominal_cannot_be_confirmatory(self):
        self.obs['survival_death']['statistic']['p_value_type'] = 'confirmatory'
        self.rejects()

    def test_negative_hazard_ratio_rejected(self):
        self.obs['survival_death']['statistic']['interval']['lower'] = -1
        self.rejects()

    def test_reversed_interval_rejected(self):
        self.obs['function_ancova']['statistic']['interval']['lower'] = 9
        self.rejects()

    def test_nonfinite_statistic_rejected(self):
        self.obs['function_ancova']['statistic']['value'] = float('nan')
        self.rejects()

    def test_boolean_pvalue_rejected(self):
        self.obs['function_ancova']['statistic']['p_value'] = True
        self.rejects()

    def test_statistic_type_confusion_rejected(self):
        self.obs['survival_death']['statistic']['measure'] = 'adjusted_mean_difference'
        self.rejects()

    def test_alternative_rank_cannot_be_standard_rank(self):
        method = self.obs['function_jrt']['statistic']['analysis_method']
        self.obs['function_alternative_jrt']['statistic'].update(analysis_method=method, p_value_method=method)
        self.rejects()

    def test_rank_cannot_be_relabeled_prespecified(self):
        method = 'Prespecified original primary joint-rank analysis'
        self.obs['function_alternative_jrt']['statistic'].update(analysis_method=method, p_value_method=method)
        self.rejects()

    def test_zero_exposed_count_has_controlled_error(self):
        self.doc['design']['ole_entered'] = 0
        self.doc['design']['ole_completed'] = {'early_start': 0, 'delayed_start': 0}
        self.doc['design']['tofersen_exposed'] = 0
        self.obs['neurological_safety']['count'].update(numerator=0, denominator=0)
        self.rejects()

    def test_empty_randomized_group_rejected(self):
        self.doc['design']['randomized'] = {'early_start': 0, 'delayed_start': 108}
        self.doc['design']['ole_completed'] = {'early_start': 0, 'delayed_start': 46}
        self.rejects()

    def test_list_parent_has_controlled_error(self):
        self.doc['parent_record_id'] = ['tofersen_sod1']
        self.rejects()

    def test_list_review_label_has_controlled_error(self):
        self.doc['review']['software_review'] = ['pending']
        self.rejects()

    def test_function_units_required(self):
        for unit in ('ratio', None):
            self.obs['function_ancova']['statistic']['unit'] = unit
            self.rejects()

    def test_unverified_scope_required(self):
        self.doc['unverified'] = []
        self.rejects()

    def test_followup_cannot_change_regulatory_status(self):
        self.doc['regulatory_status'] = 'confirmed_benefit'
        self.rejects()


if __name__ == '__main__':
    unittest.main()
