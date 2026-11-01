import concurrent.futures
import json
from pathlib import Path
import tempfile
import unittest
from report_runner import connect, inspect, run
import sqlite3

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = str(Path(self.temp.name)/'runs.sqlite')
        self.source = Path(self.temp.name)/'input.json'
        self.data = json.loads(Path(__file__).with_name('maintenance.json').read_text())
        self.save()
    def save(self):
        self.source.write_text(json.dumps(self.data))
    def call(self, fault=None, period='2026-11-02', day='2026-11-02'):
        return run(self.db, self.source, period, day, fault)
    def test_normal_and_duplicate(self):
        self.assertEqual(self.call()['status'], 'completed')
        self.assertEqual(self.call()['status'], 'skipped')
        report = inspect(self.db)['reports']
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]['due'], ['H1'])
        self.assertEqual(report[0]['unknown'], ['H4'])
    def test_interruption_and_resume(self):
        self.assertEqual(self.call('after-prepare')['status'], 'interrupted')
        self.assertEqual(inspect(self.db)['reports'], [])
        self.assertEqual(self.call()['status'], 'completed')
        self.assertEqual([a['status'] for a in inspect(self.db)['attempts']], ['interrupted','completed'])
    def test_lost_acknowledgement(self):
        self.assertEqual(self.call('after-commit')['status'], 'acknowledgement-lost')
        self.assertEqual(self.call()['status'], 'skipped')
        self.assertEqual(len(inspect(self.db)['reports']), 1)
    def test_stale_and_late_recovery(self):
        self.assertEqual(self.call(period='2026-11-09',day='2026-11-09')['status'], 'failed')
        self.data['confirmed'] = '2026-11-10'
        self.data['tasks'][1]['due'] = '2026-11-10'
        self.save()
        self.assertEqual(self.call(period='2026-11-09',day='2026-11-10')['status'], 'completed')
        self.assertEqual(inspect(self.db)['reports'][0]['due'], ['H1'])
    def test_missing_source(self):
        self.source.unlink()
        self.assertEqual(self.call()['status'], 'failed')
        self.assertEqual(inspect(self.db)['reports'], [])
    def test_changed_condition(self):
        self.data['tasks'][1]['due']='2026-11-02'; self.save()
        self.call()
        self.assertEqual(inspect(self.db)['reports'][0]['due'], ['H1','H2'])
    def test_bad_inputs_remain_unpublished(self):
        for kind in ('duplicate','date','status','future'):
            with self.subTest(kind=kind):
                original=json.loads(self.source.read_text())
                if kind=='duplicate': self.data['tasks'].append(self.data['tasks'][0])
                if kind=='date': self.data['tasks'][0]['due']='not a date'
                if kind=='status': self.data['tasks'][0]['status']='Maybe'
                if kind=='future': self.data['confirmed']='2026-11-03'
                self.save()
                self.assertEqual(self.call()['status'],'failed')
                self.assertEqual(inspect(self.db)['reports'],[])
                self.data=original;self.save()
    def test_wrong_container_is_rejected(self):
        for tasks in ({}, '', None, [42]):
            with self.subTest(tasks=tasks):
                self.data['tasks']=tasks; self.save()
                self.assertEqual(self.call()['status'], 'failed')
                self.assertEqual(inspect(self.db)['reports'], [])
    def test_inspection_never_creates_missing_ledger(self):
        with self.assertRaises(sqlite3.OperationalError): inspect(self.db)
        self.assertFalse(Path(self.db).exists())
    def test_inspection_rejects_wrong_schema(self):
        sqlite3.connect(self.db).close()
        with self.assertRaises(sqlite3.OperationalError): inspect(self.db)
    def test_competing_workers(self):
        connect(self.db).close()  # explicitly create schema before competing calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:self.call(),range(2)))
        self.assertEqual(sorted(r['status'] for r in results), ['completed','skipped'])
        self.assertEqual(len(inspect(self.db)['reports']),1)

if __name__=='__main__': unittest.main()
