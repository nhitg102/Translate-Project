
import time
from dataclasses import dataclass

from src.core.translation_manager import TranslationManager
from src.ocr.text_stabilizer import OCRTextStabilizer


@dataclass(frozen=True)
class OCRTranslationResult:
    source_text: str
    translated_text: str


class OCRTranslationPipeline:

    def __init__(
        self,
        translation_manager: TranslationManager,
        stabilizer: OCRTextStabilizer | None = None,
        retry_delay_seconds: float = 3.0
    ):
        if retry_delay_seconds < 0:
            raise ValueError(
                "retry_delay_seconds không được âm"
            )

        self.translation_manager = translation_manager

        self.stabilizer = (
            stabilizer
            if stabilizer is not None
            else OCRTextStabilizer(stable_frames=2)
        )

        self.retry_delay_seconds = retry_delay_seconds
        self._failed_text = None
        self._retry_at = 0.0

    def process_frame(
        self,
        ocr_text: str | None
    ) -> OCRTranslationResult | None:

        # 1. Lọc văn bản OCR không ổn định
        stable_text = self.stabilizer.update(ocr_text)

        if stable_text is None:
            return None

        # 2. Tránh gọi API liên tục nếu vừa gặp lỗi
        if (
            stable_text == self._failed_text
            and time.monotonic() < self._retry_at
        ):
            self.stabilizer.reset()
            return None

        # 3. Dịch: TranslationManager tự kiểm tra cache
        try:
            translated_text = (
                self.translation_manager.translate(stable_text)
            )
        except Exception:
            # Cho phép thử lại nếu dịch thất bại,
            # nhưng phải qua thời gian chờ.
            self._failed_text = stable_text
            self._retry_at = (
                time.monotonic()
                + self.retry_delay_seconds
            )
            self.stabilizer.reset()
            raise

        # 4. Dịch thành công
        self._failed_text = None
        self._retry_at = 0.0

        return OCRTranslationResult(
            source_text=stable_text,
            translated_text=translated_text
        )

    def reset(self):
        self.stabilizer.reset()
        self._failed_text = None
        self._retry_at = 0.0
