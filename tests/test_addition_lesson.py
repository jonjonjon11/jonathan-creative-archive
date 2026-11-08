"""Selected written arithmetic regressions, not learner/accessibility acceptance."""
import ast
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def value(expression):
    """Evaluate only integer addition/subtraction, without executing lesson text."""
    node = ast.parse(expression.strip(), mode='eval').body
    def visit(part):
        if isinstance(part, ast.Constant) and type(part.value) is int:
            return part.value
        if isinstance(part, ast.BinOp) and isinstance(part.op, (ast.Add, ast.Sub)):
            left, right = visit(part.left), visit(part.right)
            return left + right if isinstance(part.op, ast.Add) else left - right
        raise ValueError('Unexpected arithmetic expression')
    return visit(node)


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for child in node.values():
            yield from strings(child)
    elif isinstance(node, list):
        for child in node:
            yield from strings(child)


class AdditionLessonChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = json.loads((ROOT / 'data/modules/MOD-math-add-001.json').read_text(encoding='utf-8'))['module']
        cls.content = cls.module['content']
        cls.sections = cls.content['core_lesson']['sections']

    def test_written_numeric_equations_are_true(self):
        count = 0
        for text in strings(self.content):
            # Check complete numeric equalities only; missing-number prompts are separate.
            for left, right in re.findall(r'(?<![\w?])((?:\d+|\([\d +\-]+\))(?: [+-] \d+)*) = (\d+(?: [+-] \d+)*)', text):
                with self.subTest(equation=f'{left} = {right}'):
                    self.assertEqual(value(left), value(right))
                count += 1
        self.assertGreaterEqual(count, 20)

    def test_equality_compares_both_sides_in_core_and_text_path(self):
        for text in (self.sections[0]['content'], self.content['text_only_path']):
            self.assertIn('same value', text)
            self.assertIn('both sides', text)
            self.assertIn('5 = 3 + 2', text)
            self.assertIn('3 + 2 = 4 + 1', text)
        prose = '\n'.join(strings(self.content))
        self.assertNotIn('tells you what the total is', prose)
        self.assertNotIn('equals sign (=) tells you the result', prose)

    def test_zero_and_whole_number_scope_are_explicit(self):
        self.assertIn('whole numbers', self.content['introduction']['plain_text'])
        for text in (self.sections[0]['content'], self.content['text_only_path']):
            self.assertIn('Adding zero', text)
            self.assertIn('5 + 0 = 5', text)
        for text in (self.sections[1]['content'], self.content['text_only_path']):
            self.assertIn('5 - 0 = 5', text)
            self.assertIn('5 - 5 = 0', text)
        self.assertIn('no more items than the starting collection contains', self.sections[1]['content'])

    def test_named_worked_examples_preserve_items_and_results(self):
        examples = self.content['worked_examples']
        self.assertEqual(len(examples), 3)
        specifications = [
            ('car', ['A', 'B'], ['C', 'D', 'E'], [], list('ABCDE'), 5),
            ('cracker', list('ABCDEFG'), [], list('ABC'), list('DEFG'), 4),
            ('block', list('ABCDEF'), list('GH'), list('ABCD'), list('EFGH'), 4),
        ]
        for example, (noun, start, added, removed, remaining, total) in zip(examples, specifications):
            with self.subTest(example=example['id']):
                trace = example['item_trace']
                self.assertEqual(trace['starting_items'], start)
                self.assertEqual(trace['added_items'], added)
                self.assertEqual(trace['removed_items'], removed)
                self.assertEqual(trace['remaining_items'], remaining)
                combined = start + added
                self.assertEqual(len(set(combined)), len(combined))
                self.assertTrue(set(removed).issubset(combined))
                self.assertEqual([item for item in combined if item not in removed], remaining)
                self.assertEqual(len(remaining), total)
                written = '\n'.join(example['step_by_step'])
                counts = re.findall(rf'{noun} ([A-Z]): (\d+)', written, re.I)
                self.assertEqual(counts, [(item, str(i)) for i, item in enumerate(remaining, 1)])
                self.assertIn('optional', written.lower())
        self.assertEqual([value(e['mathematical_form'].split(' = ')[0]) for e in examples], [5, 4, 4])

    def test_comparison_matches_pairs_without_taking_away(self):
        for text in (self.sections[1]['content'], self.content['text_only_path']):
            for pair in ('A with P', 'B with Q', 'C with R', 'D with S'):
                self.assertIn(pair, text)
            self.assertIn('E, F and G', text)
            self.assertIn('7 - 4 = 3', text)
            self.assertIn('Neither collection loses any apples', text)

    def test_text_route_is_worked_and_does_not_require_objects(self):
        text = self.content['text_only_path']
        self.assertIn('No picture or physical objects are required', text)
        self.assertIn('2 + 3 = 5', text)
        self.assertIn('7 - 3 = 4', text)
        for noun, items in (('car', 'ABCDE'), ('cracker', 'DEFG')):
            counts = re.findall(rf'{noun} ([A-Z]): (\d+)', text, re.I)
            self.assertEqual(counts, [(item, str(i)) for i, item in enumerate(items, 1)])
        self.assertIn('communicate', text)
        self.assertNotIn('Practice both operations with objects you have at home', text)

    def test_existing_exercise_answers_remain_correct(self):
        exercises = self.content['exercises']
        self.assertEqual([e['answer'] for e in exercises],
                         ['4 + 1 = 5', '8 - 3 = 5', '5 + 4 = 9 pencils', '9 - 3 = 6 birds', '4'])
        self.assertIn('3 + 4 = 7', exercises[-1]['solution'])
        for exercise, operation in zip(exercises, ('+', '-', '+', '-', 'missing')):
            quantities = [int(n) for n in re.findall(r'\d+', exercise['problem_statement'])]
            first, second = quantities[:2]
            computed = second - first if operation == 'missing' else value(f'{first} {operation} {second}')
            recorded = int(re.findall(r'\d+', exercise['answer'])[-1])
            self.assertEqual(computed, recorded)

    def test_optional_methods_and_stable_collection_visual(self):
        introduction = self.content['introduction']['plain_text']
        for phrase in ('Looking', 'handwriting', 'spoken answers', 'optional'):
            self.assertIn(phrase, introduction)
        visual = self.content['worked_examples'][0]['visual_description']
        self.assertIn('five cars before and after', visual)
        self.assertNotIn('from 2 to 3 to 5', visual)
        self.assertIn('optional', self.content['interactive_experience'].lower())

    def test_review_limits_and_identity_are_explicit(self):
        self.assertEqual(self.module['id'], 'MOD-math-add-001')
        self.assertEqual(self.module['license'], 'CC BY 4.0')
        self.assertEqual(self.module['prerequisites'][0]['id'], 'MOD-math-count-001')
        self.assertEqual(self.module['review_status'], 'draft_pending_review')
        self.assertEqual(self.module['accessibility_level'], 'unverified')
        notes = self.module['verification_notes']
        for phrase in ('Educator', 'learner', 'screen-reader', 'browser-rendering', 'not been performed', 'not been re-inspected'):
            self.assertIn(phrase, notes)
        self.assertIn('not a report of accessibility or learner testing', self.content['introduction']['plain_text'])


if __name__ == '__main__':
    unittest.main()
