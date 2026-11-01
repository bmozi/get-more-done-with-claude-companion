from concurrent.futures import ThreadPoolExecutor
import unittest
from core import CASES, SOURCES, Store, ToolLimitError, baseline, reference_answer, validate_answer

class CoreTests(unittest.TestCase):
    def test_all_baseline_cases(self):
        for name, task in CASES.items():
            with self.subTest(case=name):
                result = baseline(task)
                self.assertEqual(result['answer']['action_state'], 'draft_only')
                self.assertNotIn('model_output', result['evidence_kind'])
        self.assertEqual(baseline(CASES['known-a'])['answer']['records'][0]['part'], 'FILTER-A-02')
        self.assertEqual(baseline(CASES['home-use'])['answer']['status'], 'unsupported')
        self.assertEqual(baseline(CASES['missing-model'])['answer']['status'], 'needs_input')
        self.assertEqual(len(baseline(CASES['compare'])['answer']['records']), 2)

    def test_metadata_agrees_with_original_manuals(self):
        for sid, meta in SOURCES.items():
            source = Store().read(sid)
            self.assertIn(meta['part'], source['text'])
            self.assertIn({'A1': 'six', 'A2': 'three', 'B1': 'twelve'}[sid], source['text'])

    def test_stale_source_rejected_even_if_well_formed(self):
        answer = reference_answer(CASES['known-a'])
        answer['records'][0].update(source_id='A1', part='FILTER-A-01')
        with self.assertRaisesRegex(ValueError, 'stale'):
            validate_answer(CASES['known-a'], answer, {'A1'})

    def test_unread_citation_rejected(self):
        with self.assertRaisesRegex(ValueError, 'not actually read'):
            validate_answer(CASES['known-a'], reference_answer(CASES['known-a']), set())

    def test_home_interval_cannot_borrow_commercial_value(self):
        invented = reference_answer(CASES['commercial-a'])
        with self.assertRaises(ValueError):
            validate_answer(CASES['home-use'], invented, {'A2'})

    def test_action_field_rejected(self):
        answer = reference_answer(CASES['known-a'])
        answer['send_email'] = True
        with self.assertRaises(ValueError):
            validate_answer(CASES['known-a'], answer, {'A2'})

    def test_arbitrary_path_is_not_a_source_id(self):
        store = Store()
        with self.assertRaises(ValueError):
            store.read('../../publishing/book.json')
        self.assertEqual(store.trace[-1]['status'], 'denied')

    def test_limit_includes_catalog_and_read_calls(self):
        store = Store(max_calls=2)
        store.catalog()
        store.read('A2')
        with self.assertRaises(ToolLimitError):
            store.read('B1')
        self.assertEqual(store.read_ids, {'A2'})

    def test_parallel_requests_share_one_hard_tool_budget(self):
        store = Store(max_calls=1)
        def attempt(_):
            try:
                store.catalog()
                return 'ran'
            except ToolLimitError:
                return 'blocked'
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(attempt, range(24)))
        self.assertEqual(results.count('ran'), 1)
        self.assertEqual(len(store.trace), 1)

    def test_read_failure_is_not_a_completed_read(self):
        store = Store(fail_ids={'A2'})
        with self.assertRaises(TimeoutError):
            store.read('A2')
        self.assertEqual(store.read_ids, set())
        self.assertEqual(store.trace[-1]['status'], 'failed')

    def test_boolean_interval_does_not_pass_integer_contract(self):
        # Mutate a local expected source briefly to expose Python's bool/int equality.
        old = SOURCES['A2']['months']
        try:
            SOURCES['A2']['months'] = 1
            answer = reference_answer(CASES['commercial-a'])
            answer['records'][0]['months'] = True
            with self.assertRaisesRegex(ValueError, 'boolean'):
                validate_answer(CASES['commercial-a'], answer, {'A2'})
        finally:
            SOURCES['A2']['months'] = old

if __name__ == '__main__':
    unittest.main()
