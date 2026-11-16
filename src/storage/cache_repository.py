
import hashlib
import unicodedata

from src.storage.database import get_connection, initialize_database

class CacheRepository:

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Chuẩn hóa văn bản trước khi tạo cache key.
        Không chuyển chữ hoa thành chữ thường.
        """

        text = unicodedata.normalize("NFC", text)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        return text.strip()

    @classmethod
    def generate_cache_key(
        cls,
        text: str,
        source_lang: str,
        target_lang: str,
        provider: str
    ) -> str:

        normalized_text = cls.normalize_text(text)

        raw_key = (
            f"{provider.lower()}|"
            f"{source_lang.lower()}|"
            f"{target_lang.lower()}|"
            f"{normalized_text}"
        )

        return hashlib.sha256(
            raw_key.encode("utf-8")
        ).hexdigest()

    @classmethod
    def initialize_table(cls, db_path=None):

        # Đảm bảo database sử dụng WAL trước khi tạo bảng
        initialize_database(db_path)

        with get_connection(db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS translation_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT NOT NULL UNIQUE,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_used_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    hit_count INTEGER NOT NULL DEFAULT 0
                )
            """)

    
    
    @classmethod
    def get(
        cls,
        text: str,
        source_lang: str = "en",
        target_lang: str = "vi",
        provider: str = "microsoft",
        db_path=None
    ):

        if not text or not text.strip():
            return None

        normalized_text = cls.normalize_text(text)

        cache_key = cls.generate_cache_key(
            normalized_text,
            source_lang,
            target_lang,
            provider
        )

        with get_connection(db_path) as connection:

            result = connection.execute("""
                SELECT translated_text
                FROM translation_cache
                WHERE cache_key = ?
                  AND source_text = ?
            """, (cache_key, normalized_text)).fetchone()

            if result is None:
                return None

            return result["translated_text"]



    @classmethod
    def save(
        cls,
        source_text: str,
        translated_text: str,
        source_lang: str = "en",
        target_lang: str = "vi",
        provider: str = "microsoft",
        db_path=None
    ):

        normalized_text = cls.normalize_text(source_text)

        cache_key = cls.generate_cache_key(
            normalized_text,
            source_lang,
            target_lang,
            provider
        )

        with get_connection(db_path) as connection:

            connection.execute("""
                INSERT INTO translation_cache (
                    cache_key,
                    source_text,
                    translated_text,
                    source_lang,
                    target_lang,
                    provider
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(cache_key) DO NOTHING
            """, (
                cache_key,
                normalized_text,
                translated_text,
                source_lang,
                target_lang,
                provider
            ))
