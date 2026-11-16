
import unittest

from src.cache.memory_cache import MemoryCache


class TestMemoryCache(unittest.TestCase):

    def setUp(self):
        self.cache = MemoryCache(max_size=3)

    def test_set_and_get(self):
        self.cache.set("A", "Xin chào")

        result = self.cache.get("A")

        self.assertEqual(result, "Xin chào")

    def test_cache_miss(self):
        result = self.cache.get("UNKNOWN")

        self.assertIsNone(result)

    def test_lru_eviction(self):
        self.cache.set("A", "Dịch A")
        self.cache.set("B", "Dịch B")
        self.cache.set("C", "Dịch C")

        # Sử dụng lại A để đưa A lên vị trí mới nhất
        self.cache.get("A")

        # Thêm D, B phải bị xóa
        self.cache.set("D", "Dịch D")

        self.assertIsNone(self.cache.get("B"))
        self.assertEqual(self.cache.get("A"), "Dịch A")
        self.assertEqual(self.cache.get("D"), "Dịch D")

    def test_update_existing_key(self):
        self.cache.set("A", "Bản dịch cũ")
        self.cache.set("A", "Bản dịch mới")

        self.assertEqual(
            self.cache.get("A"),
            "Bản dịch mới"
        )

        self.assertEqual(self.cache.size(), 1)

    def test_delete(self):
        self.cache.set("A", "Xin chào")

        self.assertTrue(self.cache.delete("A"))
        self.assertFalse(self.cache.delete("A"))

    def test_clear(self):
        self.cache.set("A", "Xin chào")
        self.cache.clear()

        self.assertEqual(self.cache.size(), 0)

    def test_invalid_max_size(self):
        with self.assertRaises(ValueError):
            MemoryCache(max_size=0)


if __name__ == "__main__":
    unittest.main()
