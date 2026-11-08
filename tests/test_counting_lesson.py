"""Selected written-counting regressions, not learner or accessibility approval."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORDS = ('zero one two three four five six seven eight nine ten eleven twelve '
         'thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty').split()


class CountingLessonChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = json.loads(
            (ROOT / 'data/modules/MOD-math-count-001.json').read_text(encoding='utf-8')
        )['module']
        cls.content = cls.module['content']
        cls.sections = cls.content['core_lesson']['sections']

    def assert_trace(self, text, noun, letters):
        pairs = re.findall(rf'\b{noun} ([A-Z]): (\d+) \((\w+)\)', text, re.IGNORECASE)
        self.assertEqual([label for label, _, _ in pairs], list(letters))
        self.assertEqual(len({label for label, _, _ in pairs}), len(letters))
        for index, (_, number, word) in enumerate(pairs, 1):
            self.assertEqual(int(number), index)
            self.assertEqual(word, WORDS[index])
        return len(pairs)

    def test_full_numeral_name_sequence_in_lesson_and_text_path(self):
        expected = [(str(i), word) for i, word in enumerate(WORDS)]
        for text in (self.sections[1]['content'], self.content['text_only_path']):
            with self.subTest(text=text[:60]):
                # The explicitly labeled full sequence is separate from worked examples.
                self.assertIn('0 (zero), 1 (one)', text)
                self.assertIn('20 (twenty)', text)
                start = text.index('0 (zero), 1 (one)')
                end = text.index('20 (twenty)', start) + len('20 (twenty)')
                self.assertEqual(re.findall(r'(\d+) \((\w+)\)', text[start:end]), expected)

    def test_three_worked_examples_count_each_named_item_once(self):
        examples = self.content['worked_examples']
        self.assertEqual(len(examples), 3)
        for example, noun, letters in zip(examples, ('Block', 'Star', 'Button'),
                                         ('ABCD', 'ABCDEFG', 'ABCDEFGHIJKL')):
            with self.subTest(example=example['id']):
                collection = example['scenario'].split('collection consists of ', 1)[1].split('.')[0]
                self.assertEqual(re.findall(r'\b[A-Z]\b', collection), list(letters))
                count = self.assert_trace('\n'.join(example['step_by_step']), noun, letters)
                self.assertEqual(count, example['parameters']['quantity'])
                self.assertIn(str(count), example['mathematical_form'])
                self.assertIn('optional', '\n'.join(example['step_by_step']).lower())
        self.assertEqual(examples[1]['parameters']['numeral'], 7)
        self.assertIn(12, examples[2]['parameters']['available_numerals'])

    def test_exercises_have_checked_counts_and_explanations(self):
        exercises = self.content['exercises']
        self.assertEqual(len(exercises), 5)
        for index, noun, letters, expected in ((0, 'car', 'ABCDEF', 6),
                                                (4, 'stick', 'ABCDEFGHIJKLMNO', 15)):
            collection = exercises[index]['problem_statement'].split('.')[0]
            self.assertEqual(re.findall(r'\b[A-Z]\b', collection), list(letters))
            self.assertEqual(self.assert_trace(exercises[index]['solution'], noun, letters), expected)
            self.assertEqual(exercises[index]['answer'], str(expected))
        self.assertEqual(exercises[1]['answer'], '8 objects')
        self.assertIn('one, two, three, four, five, six, seven, eight', exercises[1]['solution'])
        self.assertEqual(exercises[3]['answer'], '0')
        self.assertIn('no crackers', exercises[3]['problem_statement'].lower())

    def test_reordered_collection_keeps_item_identity_and_number_order(self):
        exercise = self.content['exercises'][2]
        collection = exercise['problem_statement'].split('.')[0]
        self.assertEqual(re.findall(r'\b[A-Z]\b', collection), list('ABCDE'))
        self.assertIn('C, A, E, B, D', exercise['problem_statement'])
        counts = re.findall(r'([A-E]) is (one|two|three|four|five)', exercise['solution'])
        self.assertEqual(len(counts), 10)
        for assignments, order in ((counts[:5], 'ABCDE'), (counts[5:], 'CAEBD')):
            self.assertEqual([label for label, _ in assignments], list(order))
            self.assertEqual([word for _, word in assignments], WORDS[1:6])
            self.assertEqual(set(label for label, _ in assignments), set('ABCDE'))
        self.assertIn('unchanged collection', exercise['answer'])
        objective = self.module['learning_objectives'][0]
        self.assertIn('item order', objective)
        self.assertIn('number sequence in order', objective)

    def test_zero_is_empty_and_not_the_first_nonempty_count(self):
        lesson = self.sections[0]['content']
        self.assertIn('empty collection', lesson)
        self.assertIn('Do not assign zero to the first item', lesson)
        path = self.content['text_only_path']
        self.assertIn('assign 1 (one) to the first item, not zero', path)
        self.assertIn('no item is skipped or counted twice', path)

    def test_text_path_contains_usable_no_picture_count_and_recount(self):
        path = self.content['text_only_path']
        for label, index in zip('ABCD', range(1, 5)):
            self.assertIn(f'block {label} to {index} ({WORDS[index]})', path)
        reordered = re.findall(r'([A-D]) is (one|two|three|four)', path)
        self.assertEqual(reordered, list(zip('DBAC', WORDS[1:5])))
        self.assertIn('No picture, physical collection, pointing or handwriting is required', path)
        self.assertIn('silently or using your preferred communication method', path)
        self.assertIn('one item name at a time', path)
        self.assertNotIn('by seeing them', path)

    def test_quantity_matching_is_not_numeral_form_mastery(self):
        section = self.sections[1]['content']
        self.assertIn('not the same skill as recognizing the printed or tactile form', section)
        self.assertIn('does not teach Braille notation', section)
        self.assertIn('12 uses two digits, 1 followed by 2', section)
        self.assertIn('does not establish printed or tactile numeral recognition',
                      self.content['text_only_path'])

    def test_review_limits_do_not_claim_accessibility_or_human_acceptance(self):
        self.assertEqual(self.module['review_status'], 'draft_pending_review')
        self.assertEqual(self.module['accessibility_level'], 'unverified')
        notes = self.module['verification_notes']
        for phrase in ('Educator, learner, screen-reader', 'have not been performed',
                       'inherited book references have not been re-inspected',
                       'no source-page verification or accessibility certification'):
            self.assertIn(phrase, notes)

    def test_identity_sources_and_license_preserved(self):
        self.assertEqual(self.module['id'], 'MOD-math-count-001')
        self.assertEqual(self.module['version'], '1.0.1')
        self.assertEqual(self.module['license'], 'CC BY 4.0')
        self.assertEqual(self.module['prerequisites'], [])
        self.assertEqual(self.module['sources'], [
            {'title': 'Principles and Standards for School Mathematics',
             'authors': 'National Council of Teachers of Mathematics', 'publication_year': 2000},
            {'title': 'Knowing and Teaching Elementary Mathematics',
             'authors': 'Liping Ma', 'publication_year': 1999},
        ])


if __name__ == '__main__':
    unittest.main()
