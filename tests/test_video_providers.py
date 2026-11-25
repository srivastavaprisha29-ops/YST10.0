import unittest
from video_providers import Provider, select, ComfyLocal
class ProviderTests(unittest.TestCase):
    def test_zero_budget(self):
        paid=Provider("paid",("i2v",),("watercolor",),100,2,5,True)
        local=Provider("local",("i2v",),("watercolor",),100,0,4,True)
        self.assertEqual(select([paid,local],"i2v","watercolor",5,0),local)
    def test_no_unapproved(self):
        with self.assertRaises(RuntimeError):
            select([Provider("x",("i2v",),("pixel",),100,0,5)],"i2v","pixel",5,0)
    def test_workflow_gate(self):
        with self.assertRaises(PermissionError):
            ComfyLocal().submit({},[])
