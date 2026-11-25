import unittest
from PIL import Image
from motion_timeline import Action, validate, speech_actions, sample_keys
from layered_motion import compose
class MotionTests(unittest.TestCase):
    def test_parallel(self):
        a=[Action("A","body",0,24,"walk"),Action("A","mouth",0,24,"talk")]
        self.assertEqual(len(validate(a,24,{"A"})),2)
    def test_conflict(self):
        a=[Action("A","body",0,24,"walk"),Action("A","body",12,24,"sit")]
        with self.assertRaises(ValueError): validate(a,24,{"A"})
    def test_sync(self):
        self.assertEqual(speech_actions("A",[{"start":0.5,"end":1,"viseme":"open"}],24)[0].start,12)
    def test_layer(self):
        bg=Image.new("RGBA",(32,32),"white")
        art=Image.new("RGBA",(4,4),"red")
        result=compose(bg,[{"image":art,"x":[(0,0),(10,20)]}],5)
        self.assertEqual(result.getpixel((10,0)),(255,0,0,255))
        self.assertEqual(sample_keys([(0,0),(10,20)],5),10)
