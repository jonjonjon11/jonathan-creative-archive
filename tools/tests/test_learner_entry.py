"""Selected learner-entry contracts, not usability or accessibility acceptance."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
GUIDES = (
    'README.md', 'START_HERE.md', 'CONTRIBUTING.md', 'docs/QUICKSTART.md',
    'docs/task-templates/verification-report-template.md',
    'docs/task-templates/browser-test-template.md',
)


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def headings(text):
    """GitHub-style anchors for the simple headings used by these guides."""
    return {
        re.sub(r'[^\w\- ]', '', m.lower()).replace(' ', '-')
        for m in re.findall(r'^#{1,6} +(.+)$', text, re.MULTILINE)
    }


class LearnerEntryTests(unittest.TestCase):
    def test_local_links_and_used_fragments_resolve(self):
        for name in GUIDES:
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', read(name)):
                with self.subTest(source=name, link=link):
                    parts = urlsplit(link)
                    if parts.scheme or parts.netloc:
                        continue
                    target = (ROOT / name).parent / unquote(parts.path) if parts.path else ROOT / name
                    target = target.resolve()
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists())
                    if parts.fragment and target.suffix == '.md':
                        self.assertIn(unquote(parts.fragment), headings(target.read_text(encoding='utf-8')))

    def test_readable_lessons_precede_authoring_tools(self):
        text = read('docs/QUICKSTART.md')
        authoring = text.index('## For lesson authors and maintainers')
        for lesson in ('introduction-to-division.md', 'motion-trace-shape.md', 'one-press-one-star.md'):
            self.assertLess(text.index(f'](lessons/{lesson})'), authoring)
            self.assertIn(f'docs/lessons/{lesson}', read('START_HERE.md'))
        self.assertNotIn('```sh', text[:authoring])
        self.assertIn('**Download ZIP**', text)
        self.assertIn('Extract the ZIP', text)
        self.assertIn('plain text', text)
        self.assertNotIn('Ready for real-world use', read('START_HERE.md'))

    def test_worked_adaptation_math_and_source_version(self):
        text = read('docs/QUICKSTART.md')
        pairs = re.findall(r'(\d+) × (\d+) = (\d+)', text)
        self.assertGreaterEqual(len(pairs), 2)
        for a, b, total in pairs:
            self.assertEqual(int(a) * int(b), int(total))
        self.assertIn(('3', '4', '12'), pairs)
        self.assertIn(('3', '5', '15'), pairs)
        module = json.loads(read('data/modules/MOD-math-div-intro-001.json'))['module']
        self.assertIn(module['id'], text)
        self.assertIn(f"version {module['version']}", text)
        self.assertIn('Sharing Twelve Pencils', read('docs/lessons/introduction-to-division.md'))
        self.assertIn('not a report from a real learner', text)
        self.assertIn('pencils per table', text)

    def test_plain_report_retains_provenance_and_uncertainty(self):
        text = read('docs/task-templates/verification-report-template.md')
        for phrase in ('Source link or local file path:', 'Module/version or exact commit',
                       'My prediction before checking:', 'How I checked',
                       'What I could not check', 'review pending',
                       'Original attribution and license:', 'Changes to describe if sharing:',
                       'name or pseudonym (optional)', 'learner-identifying information'):
            self.assertIn(phrase, text)
        self.assertIn('```text', text)

    def test_single_setup_contribution_does_not_complete_task(self):
        task = json.loads(read('data/tasks/task-motion-browser-test.json'))
        self.assertEqual('open', task['status'])
        self.assertFalse(any('two browsers' in item for item in task['stop_conditions']))
        self.assertTrue(any('one browser' in item for item in task['required_permissions']))
        self.assertTrue(any('partial report' in item.lower()
                            for item in task['deliverables'][0]['acceptance_criteria']))
        self.assertTrue(any('do not close' in item for item in task['completion_criteria']))
        self.assertIn('physical-device', ' '.join(task['completion_criteria']))
        self.assertEqual('partial_automated_coverage', task['progress']['status'])
        self.assertTrue((ROOT / task['progress']['report']).is_file())

    def test_browser_report_keeps_partial_results_honest(self):
        text = read('docs/task-templates/browser-test-template.md')
        for phrase in ('One browser or device', 'not tested', 'review pending',
                       'confirm the file actually downloaded', 'name or pseudonym (optional)',
                       'private', 'security warning'):
            self.assertIn(phrase, text)
        self.assertNotIn('Closes TASK-motion-browser-test', text)
        self.assertIn('cannot be imported', text)
        self.assertIn('cannot import', read('docs/QUICKSTART.md'))

    def test_sharing_and_submission_are_optional_and_licensed(self):
        text = read('docs/QUICKSTART.md')
        for phrase in ('keep your work private', 'Posting requires a GitHub account',
                       'no anonymous submission service', 'fork the repository',
                       'Do not assume you can push', 'CC BY 4.0',
                       'retain supplied attribution and notices', 'learner names'):
            self.assertIn(phrase, text)
        self.assertNotIn('git push origin', text)
        self.assertNotIn('start a discussion', text.lower())
        self.assertIn('Discussions are not enabled', text)
        self.assertIn('https://github.com/jonjonjon11/jonathan-creative-archive/issues', text)


if __name__ == '__main__':
    unittest.main()
