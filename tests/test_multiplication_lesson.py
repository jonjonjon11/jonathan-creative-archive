"""Offline multiplication/table checks; not educator or accessibility approval."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MultiplicationLessonChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = json.loads(
            (ROOT / 'data/modules/MOD-math-mult-intro-001.json').read_text(encoding='utf-8')
        )['module']
        cls.content = cls.module['content']
        cls.section = cls.content['core_lesson']['sections'][1]['content']

    def table(self):
        lines = [line for line in self.section.splitlines() if line.startswith('|')]
        self.assertEqual(len(lines), 13, 'header, separator, and eleven complete rows required')
        cells = [[cell.strip() for cell in line.strip('|').split('|')] for line in lines]
        self.assertEqual(cells[0], ['Groups / items per group'] + [str(i) for i in range(11)])
        self.assertEqual(cells[1], ['---'] * 12)
        self.assertTrue(all(len(row) == 12 for row in cells[2:]))
        rows = [[int(cell) for cell in row] for row in cells[2:]]
        self.assertEqual([row[0] for row in rows], list(range(11)))
        return {row[0]: row[1:] for row in rows}

    def test_complete_table_has_all_121_correct_products(self):
        rows = self.table()
        for groups in range(11):
            for items_per_group in range(11):
                with self.subTest(groups=groups, items_per_group=items_per_group):
                    # Repeated addition is independent of the table-writing multiplication.
                    expected = sum(items_per_group for _ in range(groups))
                    self.assertEqual(rows[groups][items_per_group], expected)
        self.assertNotIn('...', self.section)

    def test_zero_row_and_zero_column_are_distinct_and_zero(self):
        rows = self.table()
        self.assertEqual(rows[0], [0] * 11)
        self.assertEqual([rows[group][0] for group in range(11)], [0] * 11)
        self.assertIn('Row 0 means zero groups', self.section)
        self.assertIn('Column 0 means zero items in each group', self.section)

    def test_worked_examples_resolve_to_the_written_table(self):
        rows = self.table()
        # Independent transcription of the three written stories/problems.
        cases = [(4, 3, 12), (6, 7, 42), (8, 9, 72)]
        examples = self.content['worked_examples']
        self.assertEqual(len(examples), len(cases))
        for item, (groups, count, total) in zip(examples, cases):
            with self.subTest(example=item['id']):
                self.assertEqual(rows[groups][count], total)
                self.assertEqual(groups * count, total)
                self.assertIn(f'{groups} × {count}', item['mathematical_form'])
                self.assertIn(str(total), item['mathematical_form'])
        self.assertEqual(examples[1]['parameters'], {'factor_1': 6, 'factor_2': 7})
        self.assertEqual(examples[2]['parameters'], {'shelves': 8, 'toys_per_shelf': 9})

    def test_text_only_path_explains_the_missing_row_examples_without_a_grid(self):
        path = self.content['text_only_path']
        self.assertIn('six groups of seven', path.lower())
        self.assertIn('eight groups of nine', path.lower())
        for groups, count, total in [(6, 7, 42), (8, 9, 72)]:
            addition = ' + '.join([str(count)] * groups)
            self.assertIn(f'{groups} × {count} = {addition} = {total}', path)
            self.assertEqual(sum(map(int, addition.split(' + '))), total)
        self.assertIn('0 × 7 = 0', path)
        self.assertIn('7 × 0 = 0', path)

    def test_written_product_and_addition_equations_are_correct(self):
        text = json.dumps(self.content, ensure_ascii=False)
        # Restrict direct products to statements not beginning repeated-addition forms.
        direct = re.findall(r'(\d+) × (\d+) = (\d+)(?!\d| \+| ×| =)', text)
        self.assertGreaterEqual(len(direct), 25)
        for a, b, total in direct:
            with self.subTest(equation=(a, b, total)):
                self.assertEqual(int(a) * int(b), int(total))
        chains = re.findall(r'(\d+(?: \+ \d+)+) = (\d+)', text)
        self.assertGreaterEqual(len(chains), 5)
        for terms, total in chains:
            self.assertEqual(sum(map(int, terms.split(' + '))), int(total))

    def test_review_limits_do_not_claim_human_or_accessibility_acceptance(self):
        self.assertEqual(self.module['review_status'], 'draft_pending_review')
        self.assertEqual(self.module['accessibility_level'], 'unverified')
        self.assertIn('educator', self.module['verification_notes'])
        self.assertIn('screen-reader', self.module['verification_notes'])


if __name__ == '__main__':
    unittest.main()
