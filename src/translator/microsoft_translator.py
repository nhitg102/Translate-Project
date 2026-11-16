
import requests

from src.config import (
    MICROSOFT_TRANSLATOR_KEY,
    MICROSOFT_TRANSLATOR_REGION,
    MICROSOFT_TRANSLATOR_ENDPOINT,
    SOURCE_LANGUAGE,
    TARGET_LANGUAGE,
)

from src.core.exceptions import (
    TranslationConfigurationError,
    TranslationAPIError,
    TranslationTimeoutError,
)


class MicrosoftTranslator:

    def __init__(self):
        self.api_key = MICROSOFT_TRANSLATOR_KEY
        self.region = MICROSOFT_TRANSLATOR_REGION
        self.endpoint = MICROSOFT_TRANSLATOR_ENDPOINT.rstrip("/")

        if not self.api_key:
            raise TranslationConfigurationError(
                "Chưa cấu hình MICROSOFT_TRANSLATOR_KEY trong file .env"
            )

        if not self.region:
            raise TranslationConfigurationError(
                "Chưa cấu hình MICROSOFT_TRANSLATOR_REGION trong file .env"
            )

    def translate(
        self,
        text: str,
        source_language: str = SOURCE_LANGUAGE,
        target_language: str = TARGET_LANGUAGE,
    ) -> str:

        if not text or not text.strip():
            raise ValueError("Văn bản cần dịch không được để trống.")

        url = f"{self.endpoint}/translate"

        params = {
            "api-version": "3.0",
            "from": source_language,
            "to": target_language,
        }

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-Type": "application/json",
        }

        body = [{"text": text}]

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=15,
            )

            response.raise_for_status()

            result = response.json()

            return result[0]["translations"][0]["text"]

        except requests.exceptions.Timeout as error:
            raise TranslationTimeoutError(
                "Microsoft Translator phản hồi quá lâu."
            ) from error

        except requests.exceptions.HTTPError as error:
            raise TranslationAPIError(
                f"Microsoft Translator trả về lỗi HTTP: {error}"
            ) from error

        except requests.exceptions.RequestException as error:
            raise TranslationAPIError(
                f"Không thể kết nối Microsoft Translator: {error}"
            ) from error

        except (KeyError, IndexError, ValueError) as error:
            raise TranslationAPIError(
                "Dữ liệu trả về từ Microsoft Translator không hợp lệ."
            ) from error
