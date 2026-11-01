import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runner import classify


class PlaybookTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / 'policy.json').read_text())
        self.updated = json.loads((ROOT / 'policy-ten-confirmed.json').read_text())
        self.cases = json.loads((ROOT / 'cases.json').read_text())
        self.key = json.loads((ROOT / 'expected-key.json').read_text())

    def test_five_cases_against_designed_key(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                actual = classify(self.policy, case)
                for field, expected in self.key['seven_confirmed'][case['id']].items():
                    self.assertEqual(actual[field], expected)
                self.assertEqual(actual['apparent_remaining'], 5)
                self.assertEqual(actual['allocated_places'], 0)
                self.assertFalse(actual['sent'])
                self.assertFalse(actual['confirmation_authorized'])

    def test_updated_snapshot_reevaluates_every_pending_case(self):
        for case in self.cases:
            actual = classify(self.updated, case)
            self.assertEqual(actual['branches'], self.key['ten_confirmed'][case['id']])
            self.assertEqual(actual['apparent_remaining'], 2)
            self.assertEqual(actual['snapshot_id'], 'fictional-ten-confirmed')
        overlap = classify(self.updated, self.cases[4])
        self.assertIn('access_unconfirmed', overlap['blocking_conditions'])
        self.assertIn('capacity_conflict', overlap['blocking_conditions'])
        self.assertIn('No partial allocation is proposed.', overlap['draft'])
        self.assertEqual(overlap['allocated_places'], 0)

    def test_missing_address_stays_unknown(self):
        for value in (None, '', '   '):
            with self.subTest(address=value):
                self.policy['approved_address'] = value
                result = classify(self.policy, self.cases[0])
                self.assertEqual(result['branches'], ['missing_address'])
                self.assertIn('approved_address', result['missing_facts'])
                self.assertNotIn('Cedar Hall', result['draft'])

    def test_previous_attendance_does_not_confirm_current_registration(self):
        case = dict(self.cases[0], registration_status='unknown',
                    message='We came last month. Please send directions again.')
        result = classify(self.policy, case)
        self.assertEqual(result['branches'], ['clarify_registration'])
        self.assertNotIn('Cedar Hall', result['draft'])

    def test_exact_capacity_still_requires_review(self):
        result = classify(self.policy, dict(self.cases[1], requested_count=5))
        self.assertEqual(result['branches'], ['capacity_review'])
        self.assertEqual(result['blocking_conditions'], ['coordinator_register_check_required'])
        self.assertFalse(result['confirmation_authorized'])

    def test_unknown_count_and_access_both_survive(self):
        result = classify(self.policy, dict(self.cases[4], requested_count=None))
        self.assertEqual(result['branches'], ['clarify_count', 'access_review'])
        self.assertEqual(result['missing_facts'], ['requested_count', 'coordinator_access_confirmation'])

    def test_missing_address_and_access_both_survive(self):
        self.policy.pop('approved_address')
        result = classify(self.policy, dict(self.cases[0], access_requested=True))
        self.assertEqual(result['branches'], ['missing_address', 'access_review'])

    def test_confirmed_access_does_not_authorize_allocation(self):
        result = classify(self.policy, dict(self.cases[4], access_confirmed=True))
        self.assertEqual(result['branches'], ['capacity_review'])
        self.assertFalse(result['confirmation_authorized'])

    def test_invalid_counts_are_not_treated_as_requests(self):
        for count in (-1, 0, 1.5, True, '3'):
            with self.subTest(count=count), self.assertRaises(ValueError):
                classify(self.policy, dict(self.cases[1], requested_count=count))

    def test_input_objects_preserved(self):
        before = copy.deepcopy((self.policy, self.cases))
        for case in self.cases:
            classify(self.policy, case)
        self.assertEqual((self.policy, self.cases), before)

    def test_cli_works_from_another_directory(self):
        result = subprocess.run([sys.executable, str(ROOT / 'runner.py')],
                                cwd=ROOT.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 5)

    def test_missing_policy_fails_without_success_output(self):
        result = subprocess.run([sys.executable, str(ROOT / 'runner.py'),
                                 '--policy', str(ROOT / 'absent-policy.json')],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('Input error:', result.stderr)


if __name__ == '__main__':
    unittest.main()
