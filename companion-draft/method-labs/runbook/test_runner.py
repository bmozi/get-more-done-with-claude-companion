import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from runner import summarize

HERE = Path(__file__).parent


class RunbookTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((HERE / 'fixtures.json').read_text())
        self.key = json.loads((HERE / 'reviewer-key.json').read_text())

    def test_cases_match_independent_key_without_mutation(self):
        before = copy.deepcopy(self.cases)
        for name, case in self.cases.items():
            with self.subTest(case=name):
                actual = summarize(case)
                for field, expected in self.key[name].items():
                    self.assertEqual(actual[field], expected, field)
                self.assertEqual(actual['output_state'], 'draft')
                self.assertEqual(actual['review_state'], 'pending_coordinator_review')
        self.assertEqual(self.cases, before)

    def test_zero_is_known_not_missing(self):
        case = self.cases['normal']
        case['rows'][3]['people'] = 0
        result = summarize(case)
        self.assertEqual(result['people'], 6)
        self.assertEqual(result['count_state'], 'complete')

    def test_amendment_does_not_deduplicate_even_with_missing_count(self):
        case = self.cases['amendment']
        case['rows'][3]['people'] = None
        result = summarize(case)
        self.assertIsNone(result['people'])
        self.assertIsNone(result['known_subtotal'])
        self.assertEqual(result['excluded_source_rows'], [])

    def test_undeclared_duplicate_requires_clarification(self):
        case = self.cases['normal']
        case['rows'][2]['meaning'] = 'current'
        with self.assertRaises(ValueError):
            summarize(case)

    def test_bad_counts_rejected(self):
        for value in (-1, 1.5, True, '2'):
            case = copy.deepcopy(self.cases['normal'])
            case['rows'][0]['people'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                summarize(case)

    def test_cli_all_cases_preserve_fixture_bytes(self):
        fixture = HERE / 'fixtures.json'
        before = fixture.read_bytes()
        for name in self.cases:
            run = subprocess.run([sys.executable, str(HERE / 'runner.py'), '--case', name],
                                 text=True, capture_output=True, check=True, cwd='/tmp')
            result = json.loads(run.stdout)
            self.assertEqual(result['count_state'], self.key[name]['count_state'])
        self.assertEqual(fixture.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
