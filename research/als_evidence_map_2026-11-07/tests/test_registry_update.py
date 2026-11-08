import copy
import hashlib
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import ValidationError, load
from registry_update import load_registry_update, validate_registry_update, render_registry_update
from render import render


class RegistryUpdateTests(unittest.TestCase):
    def setUp(self):
        self.doc = load_registry_update()
        self.historical, self.register = load()

    def rejects(self):
        with self.assertRaises(ValidationError):
            validate_registry_update(self.doc, self.historical, self.register)

    def test_baseline_and_exact_render(self):
        self.assertEqual(validate_registry_update(self.doc, self.historical, self.register), {'registry_updates': 1, 'sources': 4, 'history_entries': 3})
        text = render_registry_update(self.doc, self.register)
        self.assertEqual(text, render_registry_update(copy.deepcopy(self.doc), self.register))
        self.assertEqual(text, (ROOT / 'ANQUR_REGISTRY_UPDATE.md').read_text())

    def test_original_json_snapshots_byte_preserved(self):
        expected = {'records.json':'0c5a626df00b7c675d9785d02a45005a9a213f9043793981ef1906555d967e31', 'sources.json':'e6e49bf076d67d594827baca675582bf8e5abb560f6d2335625cf8186fc2de19'}
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / 'data' / name).read_bytes()).hexdigest(), digest)

    def test_correction_visible_inside_anqur_section(self):
        views = render(self.historical, self.register, self.doc)
        section = views['EVIDENCE_MAP.md'].split('## QRL-201 / STMN2:')[1].split('## DNL343:')[0]
        self.assertIn('Registry correction checked 2026-11-08', section)
        self.assertIn('No efficacy inference', section)
        self.assertIn('superseded by the dated correction above', section)
        self.assertIn('subsequently verified', views['SOURCE_ACCESS.md'])

    def test_registry_phase_cannot_be_sponsor_label(self):
        self.doc['current_registration']['phase'] = 'Phase 1/2'
        self.rejects()

    def test_enrollment_type_and_boolean_rejected(self):
        for count, kind in [(True, 'actual'), (64, 'actual'), (69, 'estimated')]:
            self.doc['current_registration']['enrollment'] = {'count':count, 'type':kind}
            self.rejects()

    def test_results_availability_not_upgraded(self):
        for field in ('results_posted', 'full_protocol_or_sap_posted_in_reviewed_record'):
            for value in (True, 0, None):
                self.doc = load_registry_update()
                self.doc['current_registration'][field] = value
                self.rejects()

    def test_primary_safety_and_window_preserved(self):
        for field, value in [('measure', 'ALSFRS-R'), ('time_frame', '24 weeks')]:
            self.doc = load_registry_update()
            self.doc['current_registration']['primary_outcome'][field] = value
            self.rejects()

    def test_secondary_pk_hierarchy_preserved(self):
        self.doc['current_registration']['secondary_outcomes'][0]['measure'] = 'ALSFRS-R'
        self.rejects()

    def test_missing_history_or_wrong_source_rejected(self):
        self.doc['history'][1]['source_refs'][0]['source_id'] = 'anqur_registry_v24'
        self.rejects()
        self.doc = load_registry_update()
        self.doc['history'].pop()
        self.rejects()

    def test_discrepancy_requires_both_sponsor_sources(self):
        self.doc['phase_discrepancy']['source_refs'].pop(0)
        self.rejects()

    def test_missing_locators_and_unknown_sources(self):
        for key, value in [('locator', ''), ('source_id', 'invented')]:
            self.doc = load_registry_update()
            self.doc['current_registration']['source_refs'][0][key] = value
            self.rejects()

    def test_source_class_and_retrieval_required(self):
        for key, value in [('type', 'peer_reviewed_trial'), ('access_level', 'indexed_abstract_only')]:
            self.doc = load_registry_update()
            self.doc['sources'][0][key] = value
            self.rejects()

    def test_submitted_posted_access_dates_distinct(self):
        for key, value in [('access_date', '2026-05-14'), ('record_posted_date', '2026-05-11'), ('version_submitted_dates', ['2026-11-09'])]:
            self.doc = load_registry_update()
            self.doc['sources'][0][key] = value
            self.rejects()
        self.doc = load_registry_update()
        self.doc['current_registration']['posted_date'] = '2026-05-12'
        self.rejects()

    def test_no_invented_efficacy_or_regulatory_fields(self):
        for field in ('efficacy_confirmed', 'regulatory_status'):
            self.doc = load_registry_update()
            self.doc['current_registration'][field] = True
            self.rejects()

    def test_malformed_types_rejected(self):
        for path, value in [(('sources', 0, 'id'), []), (('history', 0, 'id'), []), (('current_registration', 'secondary_outcomes', 0), None), (('current_registration', 'enrollment'), None), (('phase_discrepancy',), [])]:
            self.doc = load_registry_update()
            target = self.doc
            for part in path[:-1]:
                target = target[part]
            target[path[-1]] = value
            self.rejects()

    def test_scope_and_limits_required(self):
        self.doc['limits'] = []
        self.rejects()
        self.doc = load_registry_update()
        self.doc['scope'] = 'clinical_efficacy'
        self.rejects()


if __name__ == '__main__':
    unittest.main()
