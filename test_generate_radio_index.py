import tempfile
import unittest
from pathlib import Path

from generate_radio_index import build_index


class RadioIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "LEDERG FM").mkdir()
        (self.root / "LEDERG RAP").mkdir()
        (self.root / "LEDERG FM" / "README.md").write_text("placeholder", encoding="utf-8")
        (self.root / "LEDERG FM" / "song.mp3").write_bytes(b"music-one")
        (self.root / "LEDERG RAP" / "rap.ogg").write_bytes(b"music-two")
        (self.root / "LEDERG RAP" / "ignored.txt").write_text("not audio", encoding="utf-8")
        (self.root / "LEDERG RAP" / "nested").mkdir()
        (self.root / "LEDERG RAP" / "nested" / "ignored.mp3").write_bytes(b"nested")

    def tearDown(self):
        self.temp.cleanup()

    def test_folder_names_are_indexed_and_only_direct_audio_files_are_tracks(self):
        result = build_index(self.root)
        self.assertEqual(result["stations"], ["LEDERG FM", "LEDERG RAP"])
        self.assertEqual(
            [item["path"] for item in result["files"]],
            ["LEDERG FM/song.mp3", "LEDERG RAP/rap.ogg"],
        )
        self.assertEqual(len(result["fingerprint"]), 64)

    def test_deleting_a_station_folder_removes_it_and_its_tracks_from_index(self):
        import shutil
        shutil.rmtree(self.root / "LEDERG FM")
        result = build_index(self.root)
        self.assertEqual(result["stations"], ["LEDERG RAP"])
        self.assertEqual([item["path"] for item in result["files"]], ["LEDERG RAP/rap.ogg"])

    def test_changed_track_content_changes_fingerprint(self):
        first = build_index(self.root)
        (self.root / "LEDERG FM" / "song.mp3").write_bytes(b"music-ONE")
        second = build_index(self.root)
        self.assertNotEqual(first["fingerprint"], second["fingerprint"])

    def test_invalid_station_name_is_rejected(self):
        (self.root / ("x" * 49)).mkdir()
        with self.assertRaises(ValueError):
            build_index(self.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
