import unittest
from PIL import Image
from temporal_quality import inspect_frames
class TemporalTests(unittest.TestCase):
    def test_static(self):
        a=Image.new("RGB",(32,32),"red")
        self.assertEqual(inspect_frames([a,a,a])["max_frame_change"],0)
    def test_change(self):
        a=Image.new("RGB",(32,32),"black")
        b=Image.new("RGB",(32,32),"white")
        self.assertEqual(inspect_frames([a,a,b])["max_frame_change"],1)
