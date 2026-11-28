
import unittest
import tempfile

from pathlib import Path

from src.cache.cache_manager import CacheManager


class TestCacheManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.cache = CacheManager(
            max_memory_size=3,
            db_path=self.db_path
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cache_miss(self):
        result = self.cache.get("Hello")

        self.assertIsNone(result)

    def test_save_and_get(self):
        self.cache.set("Hello", "Xin chào")

        result = self.cache.get("Hello")

        self.assertEqual(result, "Xin chào")

    def test_load_from_sqlite_to_memory(self):
        self.cache.set("Hello", "Xin chào")

        # Xóa RAM nhưng giữ SQLite
        self.cache.clear_memory()

        self.assertEqual(self.cache.memory_size(), 0)

        # Lấy lại từ SQLite
        result = self.cache.get("Hello")

        self.assertEqual(result, "Xin chào")

        # Kết quả đã được nạp lại vào RAM
        self.assertEqual(self.cache.memory_size(), 1)

    def test_memory_cache_hit(self):
        self.cache.set("Hello", "Xin chào")

        # Lấy lần đầu
        self.cache.get("Hello")

        # Lần tiếp theo sẽ lấy trực tiếp từ RAM
        result = self.cache.get("Hello")

        self.assertEqual(result, "Xin chào")


if __name__ == "__main__":
    unittest.main()
