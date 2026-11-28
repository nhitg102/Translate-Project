
import time
import tempfile
from pathlib import Path

from src.cache.memory_cache import MemoryCache
from src.storage.cache_repository import CacheRepository
from src.storage.database import get_connection


ITERATIONS = 2000


def benchmark(name, function):
    start = time.perf_counter()

    for _ in range(ITERATIONS):
        result = function()
        assert result == "Xin chào"

    elapsed = time.perf_counter() - start

    print(f"\n--- {name} ---")
    print(f"Tổng thời gian: {elapsed:.6f} giây")
    print(f"Trung bình: {elapsed / ITERATIONS * 1000:.6f} ms/lần")
    print(f"Tốc độ: {ITERATIONS / elapsed:.2f} lần/giây")

    return elapsed


def main():
    text = "Hello"
    translation = "Xin chào"

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "benchmark.db"

        CacheRepository.initialize_table(db_path)

        CacheRepository.save(
            source_text=text,
            translated_text=translation,
            db_path=db_path
        )

        cache_key = CacheRepository.generate_cache_key(
            text, "en", "vi", "microsoft"
        )

        memory_cache = MemoryCache(max_size=2000)
        memory_cache.set(cache_key, translation)

        query = """
            SELECT translated_text
            FROM translation_cache
            WHERE cache_key = ?
              AND source_text = ?
        """

        params = (cache_key, text)

        def sqlite_new_connection():
            with get_connection(db_path) as connection:
                row = connection.execute(
                    query, params
                ).fetchone()

                return row["translated_text"] if row else None

        print("\n========== CACHE BENCHMARK V2 ==========")
        print(f"Số lần kiểm tra: {ITERATIONS}")

        ram_time = benchmark(
            "RAM CACHE",
            lambda: memory_cache.get(cache_key)
        )

        sqlite_time = benchmark(
            "SQLITE - MOI LAN MO KET NOI",
            sqlite_new_connection
        )

        # Mở kết nối một lần, sau đó tái sử dụng.
        with get_connection(db_path) as connection:

            def sqlite_reused_connection():
                row = connection.execute(
                    query, params
                ).fetchone()

                return row["translated_text"] if row else None

            reuse_time = benchmark(
                "SQLITE - TAI SU DUNG KET NOI",
                sqlite_reused_connection
            )

        print("\n========== SO SANH ==========")
        print(
            "SQLite reuse nhanh hơn SQLite thông thường: "
            f"{sqlite_time / reuse_time:.2f} lần"
        )
        print(
            "RAM nhanh hơn SQLite reuse: "
            f"{reuse_time / ram_time:.2f} lần"
        )


if __name__ == "__main__":
    main()
