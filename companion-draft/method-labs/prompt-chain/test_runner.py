import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

import runner

ROOT = Path(__file__).resolve().parent


class ChainChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads((ROOT / "expected.json").read_text())

    def test_base_full_record(self):
        self.assertEqual(runner.run(), self.expected["base"])

    def test_changed_occupancy_full_record(self):
        self.assertEqual(runner.run("occupancy11"), self.expected["occupancy11"])

    def test_missing_fee_rejects_before_recommendation(self):
        self.assertEqual(runner.run("omitted-cleaning"), self.expected["omitted-cleaning"])

    def test_false_availability_and_wrong_source_are_rejected(self):
        for field, value in [("availability", "confirmed"), ("availability_source", "Q2"),
                             ("reserve", 0), ("includes_volunteers", False)]:
            with self.subTest(field=field):
                handoff = copy.deepcopy(self.expected["base"]["extraction"])
                handoff[field] = value
                result = runner.run(handoff_override=handoff)
                self.assertEqual(result["status"], "rejected")
                self.assertIsNone(result["calculation"])
                self.assertIsNone(result["explanation"])

    def test_booking_invention_rejected(self):
        handoff = copy.deepcopy(self.expected["base"]["extraction"])
        handoff["booking"] = "confirmed"
        result = runner.run(handoff_override=handoff)
        self.assertEqual(result["status"], "rejected")
        self.assertIsNone(result["explanation"])

    def test_cli_all_cases_and_preserved_source(self):
        original = (ROOT / "source.json").read_bytes()
        for case in self.expected:
            with self.subTest(case=case):
                result = subprocess.run([sys.executable, str(ROOT / "runner.py"), "--case", case],
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 2 if case == "omitted-cleaning" else 0)
                self.assertEqual(json.loads(result.stdout), self.expected[case])
                self.assertEqual(result.stderr, "")
        self.assertEqual((ROOT / "source.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
