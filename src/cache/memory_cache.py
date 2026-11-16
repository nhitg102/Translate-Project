
from collections import OrderedDict
from threading import RLock
from typing import Optional


class MemoryCache:

    def __init__(self, max_size: int = 2000):
        if max_size <= 0:
            raise ValueError(
                "max_size phải lớn hơn 0."
            )

        self.max_size = max_size
        self.cache = OrderedDict()
        self._lock = RLock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key not in self.cache:
                return None

            self.cache.move_to_end(key)
            return self.cache[key]

    def set(self, key: str, value: str) -> None:
        if not key or not value:
            return

        with self._lock:
            if key in self.cache:
                self.cache[key] = value
                self.cache.move_to_end(key)
                return

            self.cache[key] = value

            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key not in self.cache:
                return False

            del self.cache[key]
            return True

    def clear(self) -> None:
        with self._lock:
            self.cache.clear()

    def size(self) -> int:
        with self._lock:
            return len(self.cache)

    def contains(self, key: str) -> bool:
        with self._lock:
            return key in self.cache
