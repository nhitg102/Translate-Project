
import unittest
import tempfile
import time

from pathlib import Path
from threading import Barrier
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from src.cache.cache_manager import CacheManager
from src.core.translation_manager import TranslationManager


class TestParallelTranslation(unittest.TestCase):

    @patch("src.core.translation_manager.MicrosoftTranslator")
    def test_same_text_calls_api_once(self, mock_translator):

        def fake_translate(*args, **kwargs):
            # Giả lập thời gian phản hồi API
            time.sleep(0.05)
            return "Xin chào"

        mock_translator.return_value.translate.side_effect = (
            fake_translate
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            cache_manager = CacheManager(
                db_path=Path(temp_dir) / "parallel_test.db"
            )

            manager = TranslationManager(
                provider="microsoft",
                cache_manager=cache_manager
            )

            thread_count = 8
            barrier = Barrier(thread_count)

            def translate_task(_):
                barrier.wait()
                return manager.translate("Hello")

            with ThreadPoolExecutor(
                max_workers=thread_count
            ) as executor:
                results = list(
                    executor.map(
                        translate_task,
                        range(thread_count)
                    )
                )

            self.assertEqual(
                results,
                ["Xin chào"] * thread_count
            )

            # Dù có 8 yêu cầu đồng thời,
            # API chỉ được gọi đúng 1 lần.
            self.assertEqual(
                mock_translator.return_value.translate.call_count,
                1
            )


if __name__ == "__main__":
    unittest.main()
