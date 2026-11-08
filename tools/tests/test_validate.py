"""Regression checks for authoring structure, not lesson truth."""
import contextlib
import copy
import importlib.util
import io
import json
import math
import re
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('commons_validate', ROOT / 'tools/validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module = json.loads((ROOT / 'data/modules.json').read_text())
        self.task = json.loads((ROOT / 'data/tasks/task-motion-add-example.json').read_text())
        self.project = json.loads((ROOT / 'data/projects/proj-motion-trace-shape.json').read_text())

    def file(self, data, name='record.json', raw=False):
        p = self.root / name
        p.write_text(data if raw else json.dumps(data), encoding='utf-8')
        return str(p)

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = v.main(list(args))
        return result, out.getvalue()

    def test_existing_records(self):
        for path in [ROOT/'data/modules.json', *(ROOT/'data/modules').glob('*.json')]:
            self.assertEqual([], v.validate_module(path), str(path))
        self.assertEqual([], v._task(self.task))
        self.assertEqual([], v._project(self.project))

    def test_wrong_root_types(self):
        for data in [None, [], True, 3, 'hello']:
            for validator in [v.validate_module, v.validate_project, v.validate_task]:
                with self.subTest(data=data, validator=validator):
                    self.assertTrue(validator(self.file(data)))

    def test_missing_unreadable_and_bad_utf8(self):
        self.assertTrue(v.validate_module(self.root/'missing'))
        self.assertTrue(v.validate_module(self.root))
        p = self.root/'bad.json'; p.write_bytes(b'\xff')
        self.assertTrue(v.validate_module(p))

    def test_invalid_json(self):
        for text in ['{', '{"a":1,"a":2}', '{"module":{"id":1,"id":2}}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}']:
            with self.subTest(text=text):
                self.assertTrue(v.validate_module(self.file(text, raw=True)))

    def test_bad_module_shapes(self):
        for key in ['module', 'schema_version']:
            for value in [None, [], True, 1, '']:
                data = copy.deepcopy(self.module); data[key] = value
                self.assertTrue(v._module(data))
        for value in [None, [], 'abc', True]:
            data = copy.deepcopy(self.module); data['module']['content'] = value
            self.assertTrue(v._module(data))

    def test_empty_required_strings(self):
        for field in ['id', 'version', 'title', 'license']:
            for value in ['', '  ', [], None, 1]:
                data = copy.deepcopy(self.module); data['module'][field] = value
                self.assertTrue(v._module(data))

    def test_objectives_and_prerequisites_types(self):
        for field, bad in [('learning_objectives', [None, {}, 'abc', [], [None], ['']]), ('prerequisites', [None, {}, 'abc', [None]])]:
            for value in bad:
                data = copy.deepcopy(self.module); data['module'][field] = value
                self.assertTrue(v._module(data))
        self.module['module']['prerequisites'] = []
        self.assertEqual([], v._module(self.module))

    def test_example_exercise_shapes_and_minimums(self):
        for field in ['worked_examples', 'exercises']:
            for value in [None, {}, 'abcdef', [], [None]*5, ['id']*5]:
                data = copy.deepcopy(self.module); data['module']['content'][field] = value
                self.assertTrue(v._module(data))

    def test_exercise_needs_question_and_solution(self):
        data = copy.deepcopy(self.module)
        data['module']['content']['exercises'][0] = {'id':'x'}
        self.assertTrue(v._module(data))
        data['module']['content']['exercises'][0] = {'problem_statement':'Question', 'solution':'Reasoning'}
        self.assertEqual([], v._module(data))

    def test_example_needs_identity_or_title(self):
        self.module['module']['content']['worked_examples'][0] = {}
        self.assertTrue(v._module(self.module))

    def test_duplicate_local_ids(self):
        for field in ['worked_examples', 'exercises']:
            data = copy.deepcopy(self.module)
            data['module']['content'][field][0]['id'] = 'duplicate'
            data['module']['content'][field][1]['id'] = ' duplicate '
            self.assertTrue(any('duplicates' in e for e in v._module(data)))

    def test_local_id_shapes(self):
        for value in [None, [], {}, '', ' ']:
            data = copy.deepcopy(self.module)
            data['module']['content']['exercises'][0]['id'] = value
            self.assertTrue(v._module(data))

    def test_legacy_locations_supported_but_not_malformed_fallback(self):
        m = self.module['module']
        for field in ['worked_examples', 'exercises']:
            m[field] = m['content'].pop(field)
        self.assertEqual([], v._module(self.module))
        m['content']['exercises'] = None
        self.assertTrue(v._module(self.module))

    def test_project_bad_status_shapes(self):
        for value in [None, [], {}, '', 'done']:
            self.project['status'] = value
            self.assertTrue(v._project(self.project))

    def test_task_hours(self):
        for value in [True, False, 0, -1, '2', None, float('nan'), float('inf'), 1e309]:
            self.task['time_estimate_hours'] = value
            self.assertTrue(v._task(self.task))
        for value in [0.25, 1, 100]:
            self.task['time_estimate_hours'] = value
            self.assertEqual([], v._task(self.task))

    def test_task_lists(self):
        for field in ['scope', 'deliverables']:
            for value in [None, {}, 'abc', [], [None], ['']]:
                data = copy.deepcopy(self.task); data[field] = value
                self.assertTrue(v._task(data))
        self.task['deliverables'] = ['A report']
        self.assertEqual([], v._task(self.task))
        self.task['deliverables'] = [{'name':'report'}]
        self.assertTrue(v._task(self.task))

    def test_task_status_difficulty(self):
        for field in ['status', 'difficulty']:
            for value in [None, [], {}, '', 'imaginary']:
                data = copy.deepcopy(self.task); data[field] = value
                self.assertTrue(v._task(data))

    def test_cli_duplicate_ids_all_types(self):
        for kind, data in [('module',self.module), ('project',self.project), ('task',self.task)]:
            result, text = self.run_cli(kind, self.file(data,'a.json'), self.file(data,'b.json'))
            self.assertEqual(1,result)
            self.assertIn('Duplicate '+kind+' ID',text)

    def test_cli_continues_after_failure(self):
        result, text = self.run_cli('module', self.file([], 'bad.json'), self.file(self.module,'good.json'))
        self.assertEqual(1,result); self.assertIn('PASS:',text); self.assertIn('FAIL:',text)

    def test_cli_usage(self):
        self.assertEqual(0,self.run_cli()[0]); self.assertEqual(0,self.run_cli('--help')[0])
        self.assertEqual(1,self.run_cli('module')[0]); self.assertEqual(1,self.run_cli('unknown','file')[0])

    def test_template_does_not_assert_verification(self):
        m=json.loads((ROOT/'tools/module-template.json').read_text())['module']
        self.assertEqual('draft_unreviewed',m['review_status'])
        self.assertEqual('unverified',m['accessibility_level'])

    def test_guide_uses_canonical_lesson_not_copied_lesson(self):
        guide=(ROOT/'docs/knowledge-module-schema.md').read_text()
        self.assertIn('../data/modules.json',guide)
        self.assertNotIn('"worked_examples": [',guide)
        self.assertNotIn('3-pointed or flower-like',guide)

    def test_surrogate_diagnostics_do_not_abort_batch(self):
        for raw in ['{"\\ud800":1,"\\ud800":2}', json.dumps(dict(self.project, project_id='\ud800'))]:
            bad=self.file(raw,'bad.json',raw=True)
            good=self.file(self.project,'good.json')
            result=subprocess.run([sys.executable,str(ROOT/'tools/validate.py'),'project',bad,good],capture_output=True,text=True)
            self.assertEqual(1,result.returncode)
            self.assertEqual('',result.stderr)
            self.assertIn('PASS:',result.stdout)
            self.assertIn('FAIL:',result.stdout)

    def test_worked_specimen_identity_and_checkpoints(self):
        text=(ROOT/'docs/task-templates/new-example-template.md').read_text()
        specimen=json.loads(re.search(r'```json\n(.*?)\n```', text, re.S).group(1))
        p=specimen['parameters']
        self.assertEqual((1,3,0,8),(p['x_frequency'],p['y_frequency'],p['phase_offset_degrees'],p['time_window_seconds']))
        self.assertEqual(list(range(9)),[r['t_seconds'] for r in specimen['verification_samples']])
        for sample in specimen['verification_samples']:
            u=2*math.pi*sample['t_seconds']/p['time_window_seconds']
            self.assertAlmostEqual(sample['x'],math.sin(p['x_frequency']*u),places=12)
            self.assertAlmostEqual(sample['y'],math.sin(p['y_frequency']*u),places=12)
        relation=specimen['derived_relation']
        self.assertEqual('y = a*x + b*x^3',relation['form'])
        for i in range(401):
            u=2*math.pi*i/400; x=math.sin(u)
            self.assertAlmostEqual(math.sin(3*u),relation['a']*x+relation['b']*x**3,places=12)
        candidate=copy.deepcopy(self.module)
        candidate['module']['content']['worked_examples'].append(specimen)
        self.assertEqual([],v._module(candidate))

if __name__ == '__main__':
    unittest.main()
