import unittest
from research import normalize, notes

class ResearchTests(unittest.TestCase):
    def test_provenance(self):
        result=normalize({"query":{"pages":[{"title":"Example","fullurl":"https://en.wikipedia.org/wiki/Example","extract":"Evidence","lastrevid":12}]}})
        self.assertEqual(result[0]["id"],1)
        self.assertEqual(result[0]["review_status"],"unverified")
        self.assertIn("revision 12",notes(result)[0])
    def test_missing(self):
        self.assertEqual(normalize({"query":{"pages":[{"title":"Missing"}]}}),[])
