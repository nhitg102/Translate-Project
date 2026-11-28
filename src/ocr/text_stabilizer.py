
from src.storage.cache_repository import CacheRepository


class OCRTextStabilizer:
    """
    Chỉ phát ra văn bản khi OCR nhận diện ổn định.

    Trả về:
        str: Có nội dung mới cần dịch.
        None: Chưa cần dịch.
    """

    def __init__(
        self,
        stable_frames: int = 2,
        clear_after_blank_frames: int = 2
    ):
        if stable_frames < 1:
            raise ValueError("stable_frames phải >= 1")

        if clear_after_blank_frames < 1:
            raise ValueError(
                "clear_after_blank_frames phải >= 1"
            )

        self.stable_frames = stable_frames
        self.clear_after_blank_frames = clear_after_blank_frames
        self.reset()

    def reset(self):
        self._candidate = None
        self._candidate_count = 0
        self._last_emitted = None
        self._blank_count = 0

    def update(self, text: str | None) -> str | None:

        # Sử dụng cùng cách chuẩn hóa với cache
        normalized = (
            CacheRepository.normalize_text(text)
            if text else ""
        )

        # Không phát hiện văn bản
        if not normalized:
            self._blank_count += 1
            self._candidate = None
            self._candidate_count = 0

            # Văn bản đã biến mất đủ lâu.
            # Nếu xuất hiện lại thì có thể xử lý lần nữa.
            if (
                self._blank_count
                >= self.clear_after_blank_frames
            ):
                self._last_emitted = None

            return None

        self._blank_count = 0

        # Theo dõi số khung hình liên tiếp
        if normalized == self._candidate:
            self._candidate_count += 1
        else:
            self._candidate = normalized
            self._candidate_count = 1

        # Văn bản chưa đủ ổn định
        if self._candidate_count < self.stable_frames:
            return None

        # Đã phát nội dung này trước đó
        if normalized == self._last_emitted:
            return None

        # Nội dung mới, đủ ổn định
        self._last_emitted = normalized

        return normalized
