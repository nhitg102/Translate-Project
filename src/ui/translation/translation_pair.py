from dataclasses import dataclass

@dataclass(frozen=True)
class TranslationPair:
    source_language: str
    target_language: str
    source_text: str
    translated_text: str

    def can_swap(
        self,
        new_source_language: str,
        new_target_language: str,
        current_source_text: str,
        current_translated_text: str
    ) -> bool:
        # 1. Kiểm tra chiều dịch mới có đảo ngược chiều cũ
        direction_reversed = (
            self.source_language == new_target_language
            and self.target_language == new_source_language
        )

        # 2. Kiểm tra nội dung hai ô chưa thay đổi
        content_unchanged = (
            self.source_text == current_source_text
            and self.translated_text == current_translated_text
        )

        # 3. Chỉ cho phép hoán đổi khi cả hai điều kiện đúng
        return direction_reversed and content_unchanged

    def swapped(self) -> "TranslationPair":
        # Tạo cặp dịch mới với chiều và nội dung đảo ngược
        return TranslationPair(
            source_language=self.target_language,
            target_language=self.source_language,
            source_text=self.translated_text,
            translated_text=self.source_text
        )
