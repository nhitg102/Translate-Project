
import unittest

from src.ocr.text_stabilizer import OCRTextStabilizer


class TestOCRTextStabilizer(unittest.TestCase):

    def setUp(self):
        self.detector = OCRTextStabilizer(
            stable_frames=2,
            clear_after_blank_frames=2
        )

    def test_wait_for_stability(self):
        self.assertIsNone(
            self.detector.update("Hello")
        )

        self.assertEqual(
            self.detector.update("Hello"),
            "Hello"
        )

    def test_no_repeat_for_same_text(self):
        self.detector.update("Hello")
        self.detector.update("Hello")

        self.assertIsNone(
            self.detector.update("Hello")
        )

        self.assertIsNone(
            self.detector.update("Hello")
        )

    def test_single_frame_noise_is_ignored(self):
        self.detector.update("Hello")
        self.detector.update("Hello")

        self.assertIsNone(
            self.detector.update("Hell0")
        )

        self.assertIsNone(
            self.detector.update("Hello")
        )

    def test_real_change_triggers_translation(self):
        self.detector.update("Hello")
        self.detector.update("Hello")

        self.assertIsNone(
            self.detector.update("Hello world")
        )

        self.assertEqual(
            self.detector.update("Hello world"),
            "Hello world"
        )

    def test_blank_frames_reset(self):
        self.detector.update("Hello")
        self.detector.update("Hello")

        self.detector.update("")
        self.detector.update("")

        self.assertIsNone(
            self.detector.update("Hello")
        )

        self.assertEqual(
            self.detector.update("Hello"),
            "Hello"
        )

    def test_invalid_configuration(self):
        with self.assertRaises(ValueError):
            OCRTextStabilizer(stable_frames=0)

        with self.assertRaises(ValueError):
            OCRTextStabilizer(
                clear_after_blank_frames=0
            )


if __name__ == "__main__":
    unittest.main()
