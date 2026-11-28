
import unittest
import requests

from unittest.mock import patch, Mock

from src.translator.microsoft_translator import MicrosoftTranslator
from src.core.exceptions import (
    TranslationAPIError,
    TranslationTimeoutError,
)


@patch(
    "src.translator.microsoft_translator.MICROSOFT_TRANSLATOR_KEY",
    "test-api-key"
)
@patch(
    "src.translator.microsoft_translator.MICROSOFT_TRANSLATOR_REGION",
    "eastasia"
)
class TestMicrosoftTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = MicrosoftTranslator()

    @patch("src.translator.microsoft_translator.requests.post")
    def test_translate_success(self, mock_post):
        mock_response = Mock()

        mock_response.json.return_value = [
            {
                "translations": [
                    {"text": "Xin chào"}
                ]
            }
        ]

        mock_post.return_value = mock_response

        result = self.translator.translate("Hello")

        self.assertEqual(result, "Xin chào")
        mock_response.raise_for_status.assert_called_once()

    @patch("src.translator.microsoft_translator.requests.post")
    def test_empty_text(self, mock_post):
        with self.assertRaises(ValueError):
            self.translator.translate("")

        mock_post.assert_not_called()

    @patch("src.translator.microsoft_translator.requests.post")
    def test_timeout_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout

        with self.assertRaises(TranslationTimeoutError):
            self.translator.translate("Hello")

    @patch("src.translator.microsoft_translator.requests.post")
    def test_http_error(self, mock_post):
        mock_response = Mock()

        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("401 Unauthorized")
        )

        mock_post.return_value = mock_response

        with self.assertRaises(TranslationAPIError):
            self.translator.translate("Hello")


if __name__ == "__main__":
    unittest.main()
