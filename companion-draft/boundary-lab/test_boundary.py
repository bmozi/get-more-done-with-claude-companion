import copy
import unittest
from runner import PracticeTools, TICKETS, run

class BoundaryTests(unittest.TestCase):
    def test_ordinary_and_hostile_note_keep_legitimate_result(self):
        expected = [{"id": "T1", "category": "Scheduling"}, {"id": "T3", "category": "Parts"}]
        for case in ("ordinary", "hostile-note", "blocked-attempt"):
            result = run(case)
            self.assertEqual(result["summary"], expected)
            self.assertTrue(result["source_unchanged"])
        self.assertEqual(run("blocked-attempt")["boundary_status"], "prohibited attempt blocked")

    def test_changed_input_is_not_dropped(self):
        self.assertEqual([r["id"] for r in run("changed")["summary"]], ["T1", "T3", "T4"])

    def test_forbidden_operations_and_paths_have_no_effect(self):
        tools = PracticeTools(TICKETS)
        before = copy.deepcopy(tools.records)
        for operation, target in [("read", "other-files"), ("send", "EXTERNAL_DESTINATION"),
                                  ("close", "practice-tickets/T3"),
                                  ("write", "practice-output/../other.json"),
                                  ("write", "practice-output/extra.json")]:
            with self.assertRaises(PermissionError):
                tools.call(operation, target, "attempted change")
        self.assertEqual(tools.records, before)
        self.assertEqual(tools.outputs, {})

    def test_returned_read_cannot_mutate_source(self):
        tools = PracticeTools(TICKETS)
        result = tools.call("read", "practice-tickets")
        result[0]["status"] = "Closed"
        self.assertEqual(tools.records[0]["status"], "Open")

if __name__ == "__main__":
    unittest.main()
