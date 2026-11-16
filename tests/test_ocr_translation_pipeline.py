
import unittest
import tempfile

from pathlib import Path
from unittest.mock import Mock, patch

from src.cache.cache_manager import CacheManager
from src.core.translation_manager import TranslationManager
from src.core.exceptions import TranslationAPIError
from src.services.ocr_translation_pipeline import (
    OCRTranslationPipeline,
    OCRTranslationResult
)


class TestOCRTranslationPipeline(unittest.TestCase):

    def test_stabilizer_and_translation(self):
        manager = Mock()
        manager.translate.return_value = "Xin chào"

        pipeline = OCRTranslationPipeline(manager)

        # Khung hình đầu: chưa đủ ổn định
        self.assertIsNone(
            pipeline.process_frame("Hello")
        )

        # Khung hình thứ hai: bắt đầu dịch
        result = pipeline.process_frame("Hello")

        self.assertEqual(
            result,
            OCRTranslationResult("Hello", "Xin chào")
        )

        # Cùng văn bản: không dịch lại
        self.assertIsNone(
            pipeline.process_frame("Hello")
        )

        # Nhiễu OCR trong một khung hình
        self.assertIsNone(
            pipeline.process_frame("Hell0")
        )

        self.assertIsNone(
            pipeline.process_frame("Hello")
        )

        manager.translate.assert_called_once_with("Hello")

    @patch("src.core.translation_manager.MicrosoftTranslator")
    def test_pipeline_reuses_translation_cache(
        self,
        mock_translator
    ):
        mock_translator.return_value.translate.return_value = (
            "Xin chào"
        )

        with tempfile.TemporaryDirectory() as temp_dir:

            cache = CacheManager(
                db_path=Path(temp_dir) / "pipeline_test.db"
            )

            manager = TranslationManager(
                provider="microsoft",
                cache_manager=cache
            )

            pipeline = OCRTranslationPipeline(manager)

            pipeline.process_frame("Hello")
            first = pipeline.process_frame("Hello")

            self.assertEqual(
                first.translated_text,
                "Xin chào"
            )

            # Văn bản biến mất khỏi màn hình
            pipeline.process_frame("")
            pipeline.process_frame("")

            # Văn bản xuất hiện trở lại
            pipeline.process_frame("Hello")
            second = pipeline.process_frame("Hello")

            self.assertEqual(
                second.translated_text,
                "Xin chào"
            )

            # Đã dịch hai lượt, nhưng API chỉ gọi một lần
            self.assertEqual(
                mock_translator.return_value.translate.call_count,
                1
            )

    def test_new_text_is_translated(self):
        manager = Mock()
        manager.translate.side_effect = [
            "Xin chào",
            "Xin chào thế giới"
        ]

        pipeline = OCRTranslationPipeline(manager)

        pipeline.process_frame("Hello")
        pipeline.process_frame("Hello")

        self.assertIsNone(
            pipeline.process_frame("Hello world")
        )

        result = pipeline.process_frame("Hello world")

        self.assertEqual(
            result.translated_text,
            "Xin chào thế giới"
        )

        self.assertEqual(
            manager.translate.call_count,
            2
        )

    def test_retry_after_api_error(self):
        manager = Mock()
        manager.translate.side_effect = [
            TranslationAPIError("API unavailable"),
            "Xin chào"
        ]

        # Chờ 0 giây để kiểm tra cơ chế retry
        pipeline = OCRTranslationPipeline(
            manager,
            retry_delay_seconds=0
        )

        pipeline.process_frame("Hello")

        with self.assertRaises(TranslationAPIError):
            pipeline.process_frame("Hello")

        # Sau lỗi, cần ổn định lại
        self.assertIsNone(
            pipeline.process_frame("Hello")
        )

        result = pipeline.process_frame("Hello")

        self.assertEqual(
            result.translated_text,
            "Xin chào"
        )


if __name__ == "__main__":
    unittest.main()
