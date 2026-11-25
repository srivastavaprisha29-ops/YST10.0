import io
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from reference_assets import ingest, save_moodboard
from visual_quality import palette_distance

class ReferenceTests(unittest.TestCase):
    def test_ingestion(self):
        b=io.BytesIO()
        Image.new("RGB",(32,32),"pink").save(b,format="PNG")
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            asset=ingest(b.getvalue(),root,rights_confirmed=True)
            self.assertEqual(asset["moderation"],"pending")
            self.assertTrue((root/(asset["id"]+".png")).exists())
            self.assertEqual(palette_distance(asset["palette"],asset["palette"]),0)
            self.assertTrue(save_moodboard(root,"Pink room",[asset],{"medium":"2D"}))
    def test_rights(self):
        with self.assertRaises(ValueError):
            ingest(b"test",Path("."),rights_confirmed=False)
