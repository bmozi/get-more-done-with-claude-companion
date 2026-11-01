import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from make_request import build

class PreparationTests(unittest.TestCase):
    def test_cases_match_key_and_request_has_no_key(self):
        root=Path(__file__).parent
        cases=json.loads((root/'cases.json').read_text());key=json.loads((root/'answer-key.json').read_text())
        self.assertEqual({c['id'] for c in cases}, set(key)-{'evidence'})
        for c in cases:
            r=build(c['id'],'fictional-local-model:small')
            self.assertEqual(r['prompt'],c['task']+'\nSOURCE:\n'+c['source'])
            self.assertFalse(r['stream']);self.assertEqual(r['options']['num_predict'],256)
    def test_reject_placeholder_cloud_and_unknown_case(self):
        for m in ('YOUR_RECORDED_LOCAL_MODEL','example:cloud','bad name',''):
            with self.assertRaises(ValueError):build('L1',m)
        with self.assertRaises(ValueError):build('missing','example:local')
    def test_never_overwrite_saved_request(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'request.json';path.write_text('retained failure')
            r=subprocess.run([sys.executable,str(Path(__file__).with_name('make_request.py')),
                              '--case','L1','--model','example:local','--out',str(path)],capture_output=True)
            self.assertNotEqual(r.returncode,0);self.assertEqual(path.read_text(),'retained failure')
    def test_cost_arithmetic(self):
        p=json.loads(Path(__file__).with_name('cost-example.json').read_text())
        hardware=p['hardware_purchase']*p['ai_use_fraction']/p['useful_months']
        power=p['incremental_watts']/1000*p['active_hours_month']*p['electricity_per_kwh']
        maintenance=p['maintenance_hours_month']*p['time_value_per_hour']
        review=p['attempted_tasks']*p['review_minutes_per_attempt']/60*p['time_value_per_hour']
        total=hardware+power+maintenance+review
        self.assertEqual(round(total,2),p['calculated']['allocated_economic_total'])
        self.assertEqual(round(total/p['accepted_tasks'],2),p['calculated']['allocated_per_accepted'])
        self.assertEqual(round(total/p['changed_condition_accepted_tasks'],2),p['calculated']['changed_condition_per_accepted'])

if __name__=='__main__':unittest.main()
