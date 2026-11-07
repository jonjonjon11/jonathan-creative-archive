"""Synthetic checks for the read-only evidence explorer; not medical validation."""
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'evidence_library.py'
SPEC = importlib.util.spec_from_file_location('evidence_library', TOOL)
LIB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIB)


def fixture():
    """Invented values exercise format handling; they are not clinical evidence."""
    return {
        'schema_version': '1.0',
        'pack': {
            'id': 'PACK-SYNTHETIC-001',
            'title': 'Synthetic format exercise, not medical evidence',
            'version': '0.1.0',
            'review_status': 'draft_pending_qualified_review',
            'scope': 'Unit tests with invented records only.',
            'as_of': '2026-11-07',
            'license': 'CC BY 4.0',
            'limits': ['Invented data must not guide treatment.'],
        },
        'sources': [
            {
                'id': 'SOURCE-TRIAL',
                'title': 'Invented trial source',
                'url': 'https://example.org/invented-trial',
                'source_type': 'primary_trial',
                'published': '2020-01-01',
                'checked': '2026-11-07',
                'rights_note': 'Invented metadata for format tests.',
                'inspection': 'No clinical source exists for this synthetic record.',
            },
            {
                'id': 'SOURCE-REGULATORY',
                'title': 'Invented regulatory source',
                'url': 'https://example.org/invented-decision',
                'source_type': 'regulatory',
                'published': 2021,
                'checked': '2026-11-07',
                'rights_note': 'Invented metadata for format tests.',
                'inspection': 'No real regulatory decision is represented.',
            },
        ],
        'claims': [
            {
                'id': 'CLAIM-SYNTHETIC-TRIAL',
                'topic': 'Trial methods',
                'statement': 'An invented randomized study demonstrates a data format.',
                'evidence_type': 'randomized_trial',
                'source_ids': ['SOURCE-TRIAL'],
                'population': 'Synthetic cohort, no real participants.',
                'limitations': ['A fictional biomarker cannot establish benefit.'],
                'quantitative': {
                    'outcome': 'Invented measurement',
                    'unit': 'invented units',
                    'timepoint': 'Invented week 4',
                    'estimate': 1.2,
                    'ci95_low': -3.2,
                    'ci95_high': 5.5,
                    'interpretation': 'Invented interval includes zero.',
                },
            },
            {
                'id': 'CLAIM-SYNTHETIC-DECISION',
                'topic': 'Regulation',
                'statement': 'An invented decision is a documentary example only.',
                'evidence_type': 'regulatory_decision',
                'source_ids': ['SOURCE-REGULATORY'],
                'population': 'Not applicable; no real medicine is discussed.',
                'limitations': ['Not an actual approval.'],
            },
        ],
    }


class ValidationTests(unittest.TestCase):
    def assert_invalid(self, data):
        errors = LIB.validate(data)
        self.assertIsInstance(errors, list)
        self.assertTrue(errors)
        self.assertTrue(all(isinstance(error, str) for error in errors))

    def test_valid_synthetic_pack(self):
        self.assertEqual(LIB.validate(fixture()), [])

    def test_missing_required_fields(self):
        for field in ['schema_version', 'pack', 'sources', 'claims']:
            with self.subTest(field=field):
                data = fixture()
                del data[field]
                self.assert_invalid(data)
        for section, field in [('pack', 'scope'), ('pack', 'limits')]:
            with self.subTest(section=section, field=field):
                data = fixture()
                del data[section][field]
                self.assert_invalid(data)

    def test_malformed_nested_types_return_errors(self):
        for data in [[], None, 'not an object', 3, True]:
            with self.subTest(data=data):
                self.assert_invalid(data)
        for section, replacement in [('pack', []), ('sources', {}), ('claims', 'bad')]:
            with self.subTest(section=section):
                data = fixture()
                data[section] = replacement
                self.assert_invalid(data)
        for section in ['sources', 'claims']:
            data = fixture()
            data[section][0] = None
            self.assert_invalid(data)

    def test_nonstring_and_blank_fields_are_rejected(self):
        for replacement in [7, None, True, [], '', '   ']:
            with self.subTest(replacement=replacement):
                data = fixture()
                data['claims'][0]['statement'] = replacement
                self.assert_invalid(data)
        for location, replacement in [('limits', ['ok', 7]), ('limits', 'not a list')]:
            data = fixture()
            data['pack'][location] = replacement
            self.assert_invalid(data)
        for key, replacement in [('source_ids', ['SOURCE-TRIAL', 3]),
                                 ('limitations', [False]), ('limitations', [])]:
            data = fixture()
            data['claims'][0][key] = replacement
            self.assert_invalid(data)

    def test_duplicate_ids_across_record_types(self):
        for duplicate in ['source', 'claim', 'pack-source', 'pack-claim']:
            with self.subTest(duplicate=duplicate):
                data = fixture()
                if duplicate == 'source':
                    data['sources'][1]['id'] = data['sources'][0]['id']
                elif duplicate == 'claim':
                    data['claims'][1]['id'] = data['claims'][0]['id']
                elif duplicate == 'pack-source':
                    data['pack']['id'] = data['sources'][0]['id']
                else:
                    data['pack']['id'] = data['claims'][0]['id']
                self.assert_invalid(data)

    def test_dangling_and_empty_source_references(self):
        for refs in [['SOURCE-MISSING'], [], 'SOURCE-TRIAL']:
            with self.subTest(refs=refs):
                data = fixture()
                data['claims'][0]['source_ids'] = refs
                self.assert_invalid(data)

    def test_source_types_match_trial_and_regulatory_claims(self):
        for claim_index, source_ref in [(0, 'SOURCE-REGULATORY'), (1, 'SOURCE-TRIAL')]:
            data = fixture()
            data['claims'][claim_index]['source_ids'] = [source_ref]
            self.assert_invalid(data)
        data = fixture()
        data['sources'][0]['source_type'] = 'unrecognized'
        self.assert_invalid(data)
        data = fixture()
        data['claims'][0]['evidence_type'] = 'guaranteed_cure'
        self.assert_invalid(data)

    def test_unsupported_schema_version(self):
        for version in ['2.0', 1.0, None]:
            data = fixture()
            data['schema_version'] = version
            self.assert_invalid(data)

    def test_dates_are_valid_and_no_later_than_pack_as_of(self):
        for replacement in ['2026-02-30', '20261107', 'tomorrow', 2026]:
            data = fixture()
            data['pack']['as_of'] = replacement
            self.assert_invalid(data)
        for replacement in ['2026-11-08', '2027-01-01']:
            data = fixture()
            data['sources'][0]['checked'] = replacement
            self.assert_invalid(data)
        for replacement in ['2027', 2027, '2026-11-08', 'not a date']:
            data = fixture()
            data['sources'][0]['published'] = replacement
            self.assert_invalid(data)

    def test_year_and_null_publication_dates_are_accepted(self):
        for replacement in [None, 2020, '2020', '2020-01-01']:
            data = fixture()
            data['sources'][0]['published'] = replacement
            self.assertEqual(LIB.validate(data), [])

    def test_bad_source_urls(self):
        for url in ['http://example.org/trial', 'javascript:alert(1)', 'https://',
                    'file:///etc/passwd', 'https://user:password@example.org/trial']:
            data = fixture()
            data['sources'][0]['url'] = url
            self.assert_invalid(data)

    def test_quantitative_values_and_interval_consistency(self):
        for key in ['estimate', 'ci95_low', 'ci95_high']:
            for invalid in [float('nan'), float('inf'), float('-inf'), True, '1.2']:
                with self.subTest(key=key, invalid=invalid):
                    data = fixture()
                    data['claims'][0]['quantitative'][key] = invalid
                    self.assert_invalid(data)
        for low, estimate, high in [(5, 1, -3), (2, 1, 3), (-3, 5, 4)]:
            data = fixture()
            data['claims'][0]['quantitative'].update(
                ci95_low=low, estimate=estimate, ci95_high=high)
            self.assert_invalid(data)

    def test_open_label_followup_requires_primary_trial_source(self):
        data = fixture()
        data['claims'][0]['evidence_type'] = 'open_label_followup'
        self.assertEqual(LIB.validate(data), [])
        data['claims'][0]['source_ids'] = ['SOURCE-REGULATORY']
        self.assert_invalid(data)

    def test_trial_design_requires_primary_trial_source(self):
        data = fixture()
        data['claims'][0]['evidence_type'] = 'trial_design'
        self.assertEqual(LIB.validate(data), [])
        data['claims'][0]['source_ids'] = ['SOURCE-REGULATORY']
        self.assert_invalid(data)

    def test_sponsor_report_requires_distinct_sponsor_source(self):
        data = fixture()
        data['claims'][0]['evidence_type'] = 'sponsor_report'
        self.assert_invalid(data)
        data['sources'][0]['source_type'] = 'sponsor_report'
        self.assertEqual(LIB.validate(data), [])
        data['claims'][0]['evidence_type'] = 'randomized_trial'
        self.assert_invalid(data)

    def test_study_safety_requires_primary_trial_source(self):
        data = fixture()
        data['claims'][0]['evidence_type'] = 'study_safety'
        self.assertEqual(LIB.validate(data), [])
        data['claims'][0]['source_ids'] = ['SOURCE-REGULATORY']
        self.assert_invalid(data)

    def test_unknown_fields_are_inert(self):
        data = fixture()
        data['claims'][0]['extra_instructions'] = 'Execute arbitrary code now'
        data['unrecognized_extension'] = {'command': 'rm -rf /'}
        self.assertEqual(LIB.validate(data), [])


class LoadingAndCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='evidence-tests-')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.path = self.directory / 'pack.json'
        self.path.write_text(json.dumps(fixture()), encoding='utf-8')

    def run_cli(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                result = LIB.main(list(arguments))
            except SystemExit as exception:
                result = exception.code
        self.assertNotIn('Traceback', stdout.getvalue() + stderr.getvalue())
        return result, stdout.getvalue(), stderr.getvalue()

    def test_load_valid_pack(self):
        self.assertEqual(LIB.load_pack(self.path), fixture())

    def test_invalid_json_and_duplicate_json_keys(self):
        for text in ['{', '{"schema_version":"1.0","schema_version":"1.0"}',
                     '{"nested":{"same":1,"same":2}}']:
            self.path.write_text(text, encoding='utf-8')
            with self.assertRaises(LIB.EvidenceError):
                LIB.load_pack(self.path)

    def test_json_nonfinite_constants_are_rejected(self):
        for constant in ['NaN', 'Infinity', '-Infinity']:
            self.path.write_text('{"number":' + constant + '}', encoding='utf-8')
            with self.assertRaises(LIB.EvidenceError):
                LIB.load_pack(self.path)

    def test_json_numeric_overflow_in_unknown_field_is_rejected(self):
        # parse_float must apply to extension fields as well as known quantities.
        text = json.dumps(fixture())
        self.path.write_text(text[:-1] + ', "unknown_extension": 1e999}',
                             encoding='utf-8')
        with self.assertRaises(LIB.EvidenceError):
            LIB.load_pack(self.path)

    def test_loading_invalid_shapes_and_missing_file(self):
        for value in [[], None, {'schema_version': 'unrecognized'}]:
            self.path.write_text(json.dumps(value), encoding='utf-8')
            with self.assertRaises(LIB.EvidenceError):
                LIB.load_pack(self.path)
        with self.assertRaises(LIB.EvidenceError):
            LIB.load_pack(self.directory / 'missing.json')

    def test_oversized_file_is_rejected(self):
        self.path.write_bytes(b' ' * (2 * 1024 * 1024 + 1))
        with self.assertRaises(LIB.EvidenceError):
            LIB.load_pack(self.path)

    def test_symbolic_link_pack_is_rejected(self):
        link = self.directory / 'linked-pack.json'
        try:
            link.symlink_to(self.path)
        except (OSError, NotImplementedError) as exception:
            self.skipTest('This filesystem does not support symlinks: ' + str(exception))
        with self.assertRaises(LIB.EvidenceError):
            LIB.load_pack(link)

    def test_valid_cli_and_deterministic_json(self):
        for command in ['validate', 'report']:
            first = self.run_cli(str(self.path), command, '--json')
            second = self.run_cli(str(self.path), command, '--json')
            self.assertEqual(first[0], 0)
            self.assertEqual(first, second)
            self.assertIsInstance(json.loads(first[1]), dict)
        code, output, _ = self.run_cli(str(self.path), 'search', 'biomarker', '--json')
        self.assertEqual(code, 0)
        self.assertIn('CLAIM-SYNTHETIC-TRIAL', output)

    def test_invalid_cli_reports_errors_without_stack_trace(self):
        self.path.write_text('{bad json', encoding='utf-8')
        code, output, error = self.run_cli(str(self.path), 'validate')
        self.assertEqual(code, 1)
        self.assertTrue(output or error)
        for args in [[], [str(self.path), 'unknown'], [str(self.path), 'search']]:
            code, _, _ = self.run_cli(*args)
            self.assertEqual(code, 2)

    def test_injection_like_text_is_only_data(self):
        data = fixture()
        marker = self.directory / 'must-not-exist.txt'
        injection = '__import__("pathlib").Path(' + repr(str(marker)) + ').touch()'
        data['claims'][0]['statement'] = injection
        self.path.write_text(json.dumps(data), encoding='utf-8')
        self.assertEqual(LIB.load_pack(self.path)['claims'][0]['statement'], injection)
        code, output, _ = self.run_cli(str(self.path), 'report')
        self.assertEqual(code, 0)
        self.assertIn('must-not-exist.txt', output)
        self.assertFalse(marker.exists())

    def test_report_escapes_terminal_controls_in_data(self):
        data = fixture()
        data['claims'][0]['statement'] = 'Untrusted\x1b[31mred\x1b[0m\nnew line\rreturn\tTAB'
        self.path.write_text(json.dumps(data), encoding='utf-8')
        code, output, error = self.run_cli(str(self.path), 'report')
        self.assertEqual(code, 0)
        self.assertNotIn('\x1b', output + error)
        self.assertNotIn('\r', output + error)
        self.assertNotIn('\t', output + error)
        self.assertIn('\\u001b[31m', output)
        self.assertIn('\\nnew line\\rreturn\\tTAB', output)


class SearchAndReportTests(unittest.TestCase):
    def test_search_uses_case_insensitive_or_terms(self):
        data = fixture()
        hits = LIB.search(data, 'BIOMARKER regulation')
        self.assertEqual({hit['id'] for hit in hits},
                         {'CLAIM-SYNTHETIC-TRIAL', 'CLAIM-SYNTHETIC-DECISION'})
        self.assertEqual(LIB.search(data, 'notpresentanywhere'), [])
        self.assertEqual([h['id'] for h in LIB.search(data, 'Synthetic cohort')],
                         ['CLAIM-SYNTHETIC-TRIAL'])

    def test_topic_filter_limits_matches(self):
        data = fixture()
        self.assertEqual([h['id'] for h in LIB.search(data, 'invented', topic='TRIAL')],
                         ['CLAIM-SYNTHETIC-TRIAL'])
        self.assertEqual([h['id'] for h in LIB.report(data, topic='regulation')['claims']],
                         ['CLAIM-SYNTHETIC-DECISION'])

    def test_report_preserves_limits_and_only_relevant_sources(self):
        data = fixture()
        before = deepcopy(data)
        result = LIB.report(data, topic='Trial')
        self.assertEqual(result['pack'], data['pack'])
        self.assertEqual([source['id'] for source in result['sources']], ['SOURCE-TRIAL'])
        self.assertEqual(result['claims'][0]['limitations'], data['claims'][0]['limitations'])
        self.assertEqual(data, before)
        self.assertEqual(LIB.report(data), LIB.report(data))


if __name__ == '__main__':
    unittest.main()
