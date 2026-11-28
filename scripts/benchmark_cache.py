
import tempfile
import time

from pathlib import Path

from src.cache.memory_cache import MemoryCache
from src.storage.cache_repository import CacheRepository
from src.storage.database import initialize_database


def benchmark():

    test_text = "Hello, how are you?"
    translated_text = "Xin chào, bạn khỏe không?"

    source_lang = "en"
    target_lang = "vi"
    provider = "microsoft"

    # Tạo database tạm để không ảnh hưởng dữ liệu thật
    with tempfile.TemporaryDirectory() as temp_dir:

        db_path = Path(temp_dir) / "benchmark.db"

        initialize_database(db_path)

        CacheRepository.initialize_table(db_path)

        CacheRepository.save(
            source_text=test_text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            provider=provider,
            db_path=db_path
        )

        # Chuẩn bị RAM Cache
        memory_cache = MemoryCache(max_size=2000)

        cache_key = CacheRepository.generate_cache_key(
            test_text,
            source_lang,
            target_lang,
            provider
        )

        memory_cache.set(cache_key, translated_text)

        iterations = 2000

        # Benchmark RAM
        start = time.perf_counter()

        for _ in range(iterations):
            memory_cache.get(cache_key)

        ram_time = time.perf_counter() - start

        # Benchmark SQLite
        start = time.perf_counter()

        for _ in range(iterations):
            CacheRepository.get(
                text=test_text,
                source_lang=source_lang,
                target_lang=target_lang,
                provider=provider,
                db_path=db_path
            )

        sqlite_time = time.perf_counter() - start

        # Tính toán kết quả
        ram_average = ram_time / iterations
        sqlite_average = sqlite_time / iterations

        ram_speed = iterations / ram_time
        sqlite_speed = iterations / sqlite_time

        print("\n========== CACHE BENCHMARK ==========")

        print(f"Số lần kiểm tra: {iterations}")

        print("\n--- RAM CACHE ---")
        print(f"Tổng thời gian: {ram_time:.6f} giây")
        print(f"Trung bình: {ram_average * 1000:.6f} ms/lần")
        print(f"Tốc độ: {ram_speed:.2f} lần/giây")

        print("\n--- SQLITE CACHE ---")
        print(f"Tổng thời gian: {sqlite_time:.6f} giây")
        print(f"Trung bình: {sqlite_average * 1000:.6f} ms/lần")
        print(f"Tốc độ: {sqlite_speed:.2f} lần/giây")

        if ram_time > 0:
            print("\n--- SO SÁNH ---")
            print(
                f"RAM nhanh hơn SQLite khoảng: "
                f"{sqlite_time / ram_time:.2f} lần"
            )

        print("\n=====================================")


if __name__ == "__main__":
    benchmark()