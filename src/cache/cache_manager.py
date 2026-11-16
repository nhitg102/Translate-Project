
from pathlib import Path
from typing import Optional

from src.cache.memory_cache import MemoryCache
from src.storage.cache_repository import CacheRepository


class CacheManager:
    """
    Quản lý hệ thống cache hai tầng:
    1. RAM Cache
    2. SQLite Cache
    """

    def __init__(
        self,
        max_memory_size: int = 2000,
        db_path: Optional[Path] = None
    ):

        self.memory_cache = MemoryCache(
            max_size=max_memory_size
        )

        self.db_path = db_path

        # Đảm bảo bảng cache đã tồn tại
        CacheRepository.initialize_table(
            db_path=self.db_path
        )

    def get(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "vi",
        provider: str = "microsoft"
    ) -> Optional[str]:
        """
        Tìm bản dịch theo thứ tự:
        RAM -> SQLite.

        Nếu tìm thấy trong SQLite thì nạp lại vào RAM.
        """

        if not text or not text.strip():
            return None

        # Tạo khóa để tìm kiếm
        cache_key = CacheRepository.generate_cache_key(
            text,
            source_lang,
            target_lang,
            provider
        )

        # Tầng 1: Tìm trong RAM
        result = self.memory_cache.get(cache_key)

        if result is not None:
            return result

        # Tầng 2: Tìm trong SQLite
        result = CacheRepository.get(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            provider=provider,
            db_path=self.db_path
        )

        if result is not None:

            # Nạp kết quả từ SQLite vào RAM
            self.memory_cache.set(
                cache_key,
                result
            )

            return result

        # Không tìm thấy trong cả hai tầng
        return None

    def set(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str = "en",
        target_lang: str = "vi",
        provider: str = "microsoft"
    ) -> None:
        """
        Lưu bản dịch vào cả SQLite và RAM.
        """

        if not source_text or not source_text.strip():
            return

        if not translated_text or not translated_text.strip():
            return

        cache_key = CacheRepository.generate_cache_key(
            source_text,
            source_lang,
            target_lang,
            provider
        )

        # Lưu lâu dài vào SQLite
        CacheRepository.save(
            source_text=source_text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            provider=provider,
            db_path=self.db_path
        )

        # Lưu vào RAM để truy xuất nhanh
        self.memory_cache.set(
            cache_key,
            translated_text
        )

    def clear_memory(self) -> None:
        """
        Chỉ xóa cache trong RAM.
        Không xóa dữ liệu trong SQLite.
        """

        self.memory_cache.clear()

    def memory_size(self) -> int:
        """
        Số lượng bản dịch hiện đang lưu trong RAM.
        """

        return self.memory_cache.size()
