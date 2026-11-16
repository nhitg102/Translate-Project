
from threading import Lock

from src.config import (
    TRANSLATION_PROVIDER,
    SOURCE_LANGUAGE,
    TARGET_LANGUAGE,
)
from src.translator import MicrosoftTranslator
from src.cache import CacheManager
from src.storage.cache_repository import CacheRepository
from src.core.exceptions import UnsupportedProviderError


class TranslationManager:

    def __init__(self, provider=None, cache_manager=None):
        self.provider_name = (
            provider or TRANSLATION_PROVIDER
        ).lower()

        if self.provider_name != "microsoft":
            raise UnsupportedProviderError(
                f"Provider không được hỗ trợ: {self.provider_name}"
            )

        self.cache_manager = (
            cache_manager
            if cache_manager is not None
            else CacheManager()
        )

        self.translator = None
        self._translator_lock = Lock()

        # 64 khóa cố định: tránh tạo vô hạn khóa
        # khi OCR xuất hiện nhiều đoạn văn bản khác nhau.
        self._key_locks = [
            Lock() for _ in range(64)
        ]

    def _get_translator(self):
        # Chỉ khởi tạo MicrosoftTranslator một lần,
        # kể cả khi nhiều thread cùng gọi.
        with self._translator_lock:
            if self.translator is None:
                self.translator = MicrosoftTranslator()

            return self.translator

    def _get_key_lock(self, cache_key):
        lock_index = (
            int(cache_key[:8], 16)
            % len(self._key_locks)
        )
        return self._key_locks[lock_index]

    def translate(
        self,
        text: str,
        source_language: str = None,
        target_language: str = None
    ) -> str:

        if not text or not text.strip():
            raise ValueError(
                "Văn bản cần dịch không được để trống."
            )

        source_language = (
            source_language or SOURCE_LANGUAGE
        )
        target_language = (
            target_language or TARGET_LANGUAGE
        )

        cache_params = {
            "text": text,
            "source_lang": source_language,
            "target_lang": target_language,
            "provider": self.provider_name
        }

        # BƯỚC 1: Kiểm tra cache thông thường
        result = self.cache_manager.get(**cache_params)

        if result is not None:
            return result

        cache_key = CacheRepository.generate_cache_key(
            text,
            source_language,
            target_language,
            self.provider_name
        )

        key_lock = self._get_key_lock(cache_key)

        # BƯỚC 2: Chỉ một luồng xử lý cache key này
        with key_lock:

            # Kiểm tra lại vì luồng khác có thể
            # vừa dịch và lưu kết quả vào cache.
            result = self.cache_manager.get(**cache_params)

            if result is not None:
                return result

            # BƯỚC 3: Thực sự gọi API
            translator = self._get_translator()

            translated_text = translator.translate(
                text,
                source_language=source_language,
                target_language=target_language
            )

            # BƯỚC 4: Lưu kết quả vào RAM và SQLite
            self.cache_manager.set(
                source_text=text,
                translated_text=translated_text,
                source_lang=source_language,
                target_lang=target_language,
                provider=self.provider_name
            )

            return translated_text
