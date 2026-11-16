
import unittest
import tempfile
from pathlib import Path

from src.storage.database import initialize_database
from src.storage.cache_repository import CacheRepository


class TestCacheRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        initialize_database(self.db_path)
        CacheRepository.initialize_table(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_get_translation(self):
        CacheRepository.save(
            "Hello",
            "Xin chào",
            db_path=self.db_path
        )

        result = CacheRepository.get(
            "Hello",
            db_path=self.db_path
        )

        self.assertEqual(result, "Xin chào")

    def test_cache_miss(self):
        result = CacheRepository.get(
            "Good morning",
            db_path=self.db_path
        )

        self.assertIsNone(result)

    def test_same_text_returns_cached_translation(self):
        CacheRepository.save(
            "Hello",
            "Xin chào",
            db_path=self.db_path
        )

        CacheRepository.save(
            "Hello",
            "Chào bạn",
            db_path=self.db_path
        )

        result = CacheRepository.get(
            "Hello",
            db_path=self.db_path
        )

        self.assertEqual(result, "Xin chào")


if __name__ == "__main__":
    unittest.main()
