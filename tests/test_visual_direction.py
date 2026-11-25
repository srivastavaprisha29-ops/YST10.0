import unittest
from visual_direction import Direction, choose_route
class DirectionTests(unittest.TestCase):
    def test_custom_style(self):
        self.assertIn("watercolor", Direction("watercolor").prompt("garden"))
    def test_reference_required(self):
        with self.assertRaises(RuntimeError):
            choose_route(Direction("custom", reference_ids=["ref1"]), "footage", {"text_to_video":{"available":True}})
    def test_dialogue(self):
        self.assertEqual(choose_route(Direction("2D"), "dialogue", {"layered_animation":{"available":True}}), "layered_animation")
