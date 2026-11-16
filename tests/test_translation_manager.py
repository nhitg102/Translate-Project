
import unittest
from unittest.mock import patch, MagicMock

from src.core.translation_manager import TranslationManager
from src.core.exceptions import UnsupportedProviderError


class TestTranslationManager(unittest.TestCase):

    @patch("src.core.translation_manager.CacheManager")
    @patch("src.core.translation_manager.MicrosoftTranslator")
    def test_translate_cache_hit(
        self,
        mock_translator,
        mock_cache
    ):
        mock_cache.return_value.get.return_value = "Xin chào"

        manager = TranslationManager(provider="microsoft")
        result = manager.translate("Hello")

        self.assertEqual(result, "Xin chào")

        # Không khởi tạo Microsoft Translator
        mock_translator.assert_not_called()

        # Không gọi API
        mock_translator.return_value.translate.assert_not_called()

        # Không lưu lại bản dịch đã có
        mock_cache.return_value.set.assert_not_called()

    @patch("src.core.translation_manager.CacheManager")
    @patch("src.core.translation_manager.MicrosoftTranslator")
    def test_translate_cache_miss(
        self,
        mock_translator,
        mock_cache
    ):
        mock_cache.return_value.get.return_value = None
        mock_translator.return_value.translate.return_value = "Xin chào"

        manager = TranslationManager(provider="microsoft")
        result = manager.translate("Hello")

        self.assertEqual(result, "Xin chào")
        mock_translator.return_value.translate.assert_called_once()
        mock_cache.return_value.set.assert_called_once()

    @patch("src.core.translation_manager.CacheManager")
    @patch("src.core.translation_manager.MicrosoftTranslator")
    def test_translate_with_custom_languages(
        self,
        mock_translator,
        mock_cache
    ):
        mock_cache.return_value.get.return_value = None
        mock_translator.return_value.translate.return_value = "Bonjour"

        manager = TranslationManager(provider="microsoft")

        result = manager.translate(
            "Hello",
            source_language="en",
            target_language="fr"
        )

        self.assertEqual(result, "Bonjour")

        mock_translator.return_value.translate.assert_called_once_with(
            "Hello",
            source_language="en",
            target_language="fr"
        )

    def test_unsupported_provider(self):
        with self.assertRaises(UnsupportedProviderError):
            TranslationManager(provider="google")


if __name__ == "__main__":
    unittest.main()
