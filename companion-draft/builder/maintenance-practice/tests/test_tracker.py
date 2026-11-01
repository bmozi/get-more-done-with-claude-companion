import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tracker import report

class TrackerTests(unittest.TestCase):
    def test_boundaries_and_source_preservation(self):
        p = ROOT / 'data/maintenance.csv'
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        r = report(p, date(2026, 10, 17))
        self.assertEqual([x['id'] for x in r['due']], ['M01', 'M02'])
        self.assertEqual([x['id'] for x in r['future']], ['M03'])
        self.assertEqual([x['id'] for x in r['done']], ['M04'])
        self.assertEqual([x['id'] for x in r['unknown']], ['M05'])
        self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest())

    def run_case(self, rows):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.csv'
            p.write_text('id,item,due_date,status\n' + rows)
            return report(p, date(2026, 10, 17))

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.run_case('A,Thing,2026-10-16,open\nA,Other,2026-10-18,open\n')

    def test_invalid_dates_rejected(self):
        for value in ['2026-02-30', 'tomorrow', '20261017']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.run_case(f'A,Thing,{value},open\n')

    def test_status_rejected(self):
        with self.assertRaisesRegex(ValueError, 'status'):
            self.run_case('A,Thing,2026-10-17,maybe\n')

    def test_empty_dataset(self):
        self.assertTrue(all(not v for v in self.run_case('').values()))

    def test_missing_field_rejected(self):
        with self.assertRaisesRegex(ValueError, 'fields'):
            self.run_case('A,Thing,2026-10-17\n')

    def test_cli_success(self):
        r = subprocess.run([sys.executable, str(ROOT/'tracker.py'), str(ROOT/'data/maintenance.csv'), '--as-of', '2026-10-17'],capture_output=True,text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(json.loads(r.stdout)['due']), 2)

    def test_cli_missing_input(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT/'tracker.py'), str(Path(d)/'absent.csv'), '--as-of', '2026-10-17'],capture_output=True,text=True)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, '')
        self.assertIn('Cannot produce report', r.stderr)

if __name__ == '__main__':
    unittest.main()
