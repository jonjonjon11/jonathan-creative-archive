"""Offline arithmetic, content-parity, and handoff checks; no efficacy claim."""
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def record(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class DivisionLessonChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = record('data/modules/MOD-math-div-intro-001.json')['module']
        cls.content = cls.module['content']
        cls.readable = (ROOT / 'docs/lessons/introduction-to-division.md').read_text(encoding='utf-8')

    def test_arithmetic_against_independent_story_inputs(self):
        # Inputs transcribed independently from the eight written problems.
        inputs = {
            'DIV-WE-001': (12, 3), 'DIV-WE-002': (24, 6),
            'DIV-WE-003': (23, 5), 'DIV-EX-001': (15, 3),
            'DIV-EX-002': (18, 6), 'DIV-EX-003': (0, 4),
            'DIV-EX-004': (29, 4), 'DIV-EX-005': (47, 5),
        }
        items = self.content['worked_examples'] + self.content['exercises']
        self.assertEqual({item['id'] for item in items}, set(inputs))
        for item in items:
            with self.subTest(item=item['id']):
                total, divisor = inputs[item['id']]
                p = item['parameters']
                self.assertEqual((p['total'], p['divisor']), (total, divisor))
                self.assertEqual((p['quotient'], p['remainder']), divmod(total, divisor))
                self.assertLess(p['remainder'], divisor)
                self.assertGreaterEqual(p['remainder'], 0)

    def test_capacity_answers_account_for_leftovers(self):
        for item in self.content['worked_examples'] + self.content['exercises']:
            p = item['parameters']
            if 'containers_needed' in p:
                with self.subTest(item=item['id']):
                    needed = -(-p['total'] // p['divisor'])
                    self.assertEqual(p['containers_needed'], needed)
                    self.assertGreaterEqual(needed * p['divisor'], p['total'])
                    self.assertLess((needed - 1) * p['divisor'], p['total'])

    def test_prose_answers_agree_with_arithmetic(self):
        # Check the actual learner-facing answers, not only metadata numbers.
        example_forms = [
            '12 ÷ 3 = 4; 12 = 3 × 4 + 0',
            '24 ÷ 6 = 4; 24 = 6 × 4 + 0',
            '23 ÷ 5 = 4 remainder 3; 23 = 5 × 4 + 3; envelopes needed = 4 + 1 = 5',
        ]
        self.assertEqual([e['mathematical_form'] for e in self.content['worked_examples']], example_forms)
        answers = [e['answer'] for e in self.content['exercises']]
        for expected, actual in zip(['15 ÷ 3 = 5', '18 ÷ 6 = 3',
                                     '0 ÷ 4 = 0', '29 ÷ 4 = 7 remainder 1',
                                     'Storage: ten containers'], answers):
            self.assertIn(expected, actual)
        self.assertIn('Both 8 ÷ 0 and 0 ÷ 0 are undefined.', answers[2])

    def test_readable_edition_contains_all_teaching_content(self):
        c = self.content
        blocks = [c['introduction']['plain_text'], c['text_only_path'], c['interactive_experience']]
        blocks += self.module['learning_objectives']
        blocks += [s['content'] for s in c['core_lesson']['sections']]
        for e in c['worked_examples']:
            blocks += [e[k] for k in ['title', 'scenario', 'prediction', 'explanation',
                                       'mathematical_form', 'visual_description']]
            blocks += e['step_by_step']
        for e in c['exercises']:
            blocks += [e[k] for k in ['title', 'problem_statement', 'hint', 'solution', 'answer']]
        for source in self.module['sources']:
            blocks += [source['title'], source['url'], source['description']]
        for block in blocks:
            with self.subTest(text=block[:70]):
                self.assertIn(block, self.readable)

    def test_lesson_structure_and_resolvable_prerequisites(self):
        c = self.content
        self.assertTrue(100 <= len(c['introduction']['plain_text'].split()) <= 200)
        self.assertEqual(len(c['core_lesson']['sections']), 2)
        for section in c['core_lesson']['sections']:
            self.assertTrue(200 <= len(section['content'].split()) <= 300)
        self.assertEqual([e['difficulty'] for e in c['worked_examples']],
                         ['beginner', 'intermediate', 'advanced'])
        self.assertEqual(len(c['exercises']), 5)
        ids = [e['id'] for e in c['worked_examples'] + c['exercises']]
        self.assertEqual(len(ids), len(set(ids)))
        for prerequisite in self.module['prerequisites']:
            path = 'data/modules/' + prerequisite['id'] + '.json'
            self.assertEqual(record(path)['module']['id'], prerequisite['id'])
        self.assertEqual(self.module['license'], 'CC BY 4.0')
        self.assertEqual(self.module['review_status'], 'draft_pending_review')

    def test_sources_have_specific_distinct_https_locations(self):
        sources = self.module['sources']
        self.assertGreaterEqual(len(sources), 3)
        urls = [s['url'] for s in sources]
        self.assertEqual(len(urls), len(set(urls)))
        for source in sources:
            location = urlsplit(source['url'])
            self.assertEqual(location.scheme, 'https')
            self.assertNotIn(location.path, ['', '/'])
            self.assertNotIn(location.hostname, ['example.com', 'www.example.com'])
            self.assertTrue(source['description'])
        # Shape checks only. Page retrieval and source relevance are reviewed separately.

    def test_review_handoff_is_linked_without_inventing_approval(self):
        task = record('data/tasks/task-division-review.json')
        project = record('data/projects/proj-arithmetic-foundations.json')
        review = record('data/reviews/review-division-001.json')
        self.assertEqual(task['project_id'], project['project_id'])
        self.assertEqual(review['task_id'], task['task_id'])
        self.assertEqual(review['acceptance_decision'], 'pending')
        self.assertIsNone(review['reviewer'])
        self.assertIsNone(review['review_date'])
        for source in task['inputs']:
            self.assertTrue((ROOT / source['source']).is_file())
        self.assertTrue(task['stop_conditions'])
        self.assertTrue(task['restrictions'])


if __name__ == '__main__':
    unittest.main()
