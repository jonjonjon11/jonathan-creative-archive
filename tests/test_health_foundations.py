"""Check the committed scientific records and the documented offline examples."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('committed_evidence_library', ROOT / 'tools/evidence-library/evidence_library.py')
LIB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIB)


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class HealthFoundationsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.als = LIB.load_pack(ROOT / 'data/health/als-evidence.json')
        cls.cancer = LIB.load_pack(ROOT / 'data/health/cancer-foundations.json')
        cls.trials = read('data/health/als-trial-facts.json')

    def test_both_disease_packs_use_the_same_offline_format(self):
        for pack in (self.als, self.cancer):
            self.assertEqual(LIB.validate(pack), [])
            self.assertTrue(pack['sources'])
            self.assertTrue(pack['claims'])
            self.assertEqual(pack['pack']['review_status'], 'draft_pending_qualified_review')
        ids = [x['id'] for p in (self.als, self.cancer)
               for x in [p['pack']] + p['sources'] + p['claims']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_trial_source_references_and_response_hashes(self):
        sources = {s['id']: s for s in self.trials['sources']}
        rows = self.trials['records']
        self.assertEqual(len(rows), 4)
        self.assertEqual(len({r['id'] for r in rows}), len(rows))
        for source in sources.values():
            self.assertRegex(source['source_response_sha256'], r'^[a-f0-9]{64}$')
            self.assertTrue(source['source_url'].startswith('https://'))
            self.assertTrue(source['inspection'])
            self.assertTrue(source['rights_note'])
        for row in rows:
            self.assertRegex(row['trial_nct'], r'^NCT\d{8}$')
            self.assertTrue(row['field_provenance'])
            self.assertTrue(set(row['source_ids']) <= set(sources))
            # Current registry status was not acquired by this contribution.
            self.assertIsNone(row['registry_status'])
            if row['randomized_groups']:
                self.assertEqual(sum(row['randomized_groups'].values()), row['enrollment_randomized'])

    def test_transcribed_estimates_agree_between_embedded_records(self):
        claims = {c['id']: c for c in self.als['claims']}
        trials = {r['trial_name']: r for r in self.trials['records']}
        for name, claim_id in [('VALOR', 'ALS-CLAIM-007'), ('CENTAUR', 'ALS-CLAIM-011')]:
            with self.subTest(trial=name):
                outcome = trials[name]['primary_result']
                quantitative = claims[claim_id]['quantitative']
                for key in ('estimate', 'ci95_low', 'ci95_high', 'unit'):
                    self.assertEqual(quantitative[key], outcome[key])
        valor = trials['VALOR']
        self.assertEqual(valor['enrollment_randomized'], 108)
        self.assertEqual(sum(valor['primary_analysis_group_counts'].values()), 60)
        # Preserve the reported estimate rather than replacing it with rounded-arm arithmetic.
        changes = valor['primary_result']['group_changes']
        self.assertAlmostEqual(changes['tofersen'] - changes['placebo'], 1.16)
        self.assertEqual(valor['primary_result']['estimate'], 1.2)
        centaur = trials['CENTAUR']['primary_result']
        rates = centaur['group_rates']
        self.assertAlmostEqual(rates['active_combination'] - rates['placebo'], centaur['estimate'])
        self.assertNotEqual(valor['primary_result']['unit'], centaur['unit'])

    def test_sponsor_design_followup_and_safety_are_distinct(self):
        kinds = {c['id']: c['evidence_type'] for c in self.als['claims']}
        self.assertEqual(kinds['ALS-CLAIM-007'], 'randomized_trial')
        self.assertEqual(kinds['ALS-CLAIM-009'], 'open_label_followup')
        self.assertEqual(kinds['ALS-CLAIM-017'], 'sponsor_report')
        self.assertEqual(kinds['ALS-CLAIM-018'], 'trial_design')
        self.assertEqual(kinds['ALS-CLAIM-019'], 'study_safety')
        rows = {r['trial_name']: r for r in self.trials['records']}
        for key in ('estimate', 'ci95_low', 'ci95_high'):
            self.assertIsNone(rows['PHOENIX']['primary_result'][key])
        self.assertAlmostEqual(rows['PHOENIX']['primary_result']['p_value'], 0.667)
        self.assertIsNone(rows['ATLAS']['primary_result'])
        self.assertIsNone(rows['ATLAS']['enrollment_randomized'])

    def test_documented_evidence_command_has_repeatable_json_output(self):
        command = [sys.executable, 'tools/evidence-library/evidence_library.py',
                   'data/health/als-evidence.json', 'search', 'tofersen', '--json']
        first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
        second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(json.loads(first.stdout))
        cancer = subprocess.run([sys.executable, 'tools/evidence-library/evidence_library.py',
                                 'data/health/cancer-foundations.json', 'report', '--json'],
                                cwd=ROOT, text=True, capture_output=True, check=True)
        self.assertTrue(json.loads(cancer.stdout))

    def test_documented_synthetic_switch_example(self):
        result = subprocess.run([sys.executable, 'tools/switch-input-lab/switch_input.py',
                                 'tools/switch-input-lab/fixtures/synthetic-bounce.json', '--json'],
                                cwd=ROOT, text=True, capture_output=True, check=True)
        value = json.loads(result.stdout)
        self.assertIs(value['synthetic'], True)
        self.assertEqual([(e['timestamp_ms'], e['event']) for e in value['events']],
                         [(45, 'press'), (90, 'release')])
        self.assertIs(value['final_pressed'], False)

    def test_review_task_inputs_are_present_and_decision_is_pending(self):
        task = read('data/tasks/task-als-source-review.json')
        project = read('data/projects/proj-health-and-assistive-foundations.json')
        review = read('data/reviews/review-als-foundations-001.json')
        self.assertEqual(task['project_id'], project['project_id'])
        self.assertEqual(task['task_id'], review['task_id'])
        self.assertEqual(review['acceptance_decision'], 'pending')
        self.assertIsNone(review['reviewer'])
        for path in task['inputs']:
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == '__main__':
    unittest.main()
