import unittest
from planner import validate

class PlannerTests(unittest.TestCase):
    def scene(self):
        return {"title":"Intro","narration":"Example narration.","visual_prompt":"A city skyline","source_ids":[1]}
    def test_valid(self):
        result=validate({"scenes":[self.scene()]}, ["source"], 1)
        self.assertEqual(result[0]["fact_check_status"], "unverified")
    def test_invented_source(self):
        with self.assertRaises(ValueError):
            validate({"scenes":[self.scene()]}, [], 1)
    def test_count(self):
        with self.assertRaises(ValueError):
            validate({"scenes":[self.scene()]}, ["source"], 2)
    def test_empty_narration(self):
        s=self.scene()
        s["narration"]=""
        with self.assertRaises(ValueError):
            validate({"scenes":[s]}, ["source"], 1)

if __name__ == "__main__":
    unittest.main()
