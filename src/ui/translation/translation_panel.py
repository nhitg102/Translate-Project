from PySide6.QtWidgets import QTextEdit, QPushButton, QLabel

from ..shared.ui_loader import load_ui

from .language_controller import LanguageController
from .text_rules import MAX_WORDS, count_words, contains_letters
from .translation_pair import TranslationPair

class TranslationPanel:
    def __init__(self, parent=None):
        self.widget = load_ui("translation_panel.ui", parent)

        # Tìm các widget
        input_text = self.widget.findChild(QTextEdit, "inputText")
        result_text = self.widget.findChild(QTextEdit, "resultText")
        clear_button = self.widget.findChild(QPushButton, "clearButton")
        translate_button = self.widget.findChild(QPushButton, "translateButton")
        word_count_label = self.widget.findChild(QLabel, "wordCountLabel")

        # Kiểm tra widget có tồn tại không
        if (
            input_text is None
            or result_text is None
            or clear_button is None
            or translate_button is None
        ):
            raise RuntimeError("Thiếu widget trong translation_panel.ui")

        if word_count_label is None:
            raise RuntimeError(
                "Không tìm thấy wordCountLabel trong translation_panel.ui"
            )

        # Lưu các widget
        self.input_text = input_text
        self.result_text = result_text
        self.clear_button = clear_button
        self.translate_button = translate_button
        self.word_count_label = word_count_label

        # Khởi tạo trạng thái và controller
        self._valid_pair: TranslationPair | None = None
        # Phân biệt chỉnh sửa của người dùng và cập nhật bằng code
        self._changing_input_programmatically = False
        self.language_controller = LanguageController(self.widget)

        # Kết nối sự kiện
        self.clear_button.clicked.connect(self.clear_text)
        self.translate_button.clicked.connect(self._translate_clicked)

        self.language_controller.direction_changed.connect(
            self._direction_changed
        )

        self.input_text.textChanged.connect(
            self._on_input_changed
        )

        self._update_word_count()

    # Hiển thị các trạng thái dịch
    def show_loading(self):
        self._valid_pair = None
        self.translate_button.setEnabled(False)
        self.result_text.setPlainText("Đang dịch...")

    def show_error(self, message):
        self._valid_pair = None
        self.translate_button.setEnabled(True)
        self.result_text.setPlainText(message)

    def set_translation_result(self, translated_text):
        # 1. Lấy văn bản hiện tại
        source_text = self.input_text.toPlainText()

        source_lang, target_lang = (
            self.language_controller.get_languages()
        )

        # 2. Hiển thị bản dịch
        self.result_text.setPlainText(translated_text)
        self.translate_button.setEnabled(True)

        # 3. Lưu cặp dịch hợp lệ
        if source_text.strip() and translated_text.strip():
            self._valid_pair = TranslationPair(
                source_language=source_lang,
                target_language=target_lang,
                source_text=source_text,
                translated_text=translated_text
            )
        else:
            self._valid_pair = None

    def _direction_changed(self, source_lang, target_lang):
        pair = self._valid_pair

        # 1. Kiểm tra có thể hoán đổi cặp dịch không
        if (
            pair is not None
            and pair.can_swap(
                new_source_language=source_lang,
                new_target_language=target_lang,
                current_source_text=self.input_text.toPlainText(),
                current_translated_text=self.result_text.toPlainText()
            )
        ):
            # 2. Hoán đổi nội dung hai ô
            self._set_input_text(pair.translated_text)
            self.result_text.setPlainText(pair.source_text)

            # 3. Lưu cặp dịch theo chiều mới
            self._valid_pair = pair.swapped()

        else:
            # 4. Không có cặp dịch hợp lệ
            self._valid_pair = None
            self.result_text.clear()

            # 5. Cập nhật placeholder
            if self.input_text.toPlainText().strip():
                self.result_text.setPlaceholderText(
                    "Nhấn Dịch để xem kết quả."
                )
            else:
                self.result_text.setPlaceholderText(
                    "Bản dịch..."
                )

    def clear_text(self):
        # 1. Xóa nội dung hai ô
        self.input_text.clear()
        self.result_text.clear()

        # 2. Khôi phục placeholder mặc định
        self.result_text.setPlaceholderText("Bản dịch...")

        # 3. Xóa cặp dịch cũ
        self._valid_pair = None

        # 4. Cho phép bấm Dịch
        self.translate_button.setEnabled(True)

    def _translate_clicked(self):
        # 1. Đọc nội dung Input
        text = self.input_text.toPlainText()

        # 2. Kiểm tra Input rỗng
        if not text.strip():
            self.result_text.setPlainText(
                "Vui lòng nhập văn bản cần dịch."
            )
            self._valid_pair = None
            return

        # 3. Kiểm tra giới hạn 1000 từ
        word_count = count_words(text)

        if word_count > MAX_WORDS:
            self.result_text.setPlainText(
                "Vượt giới hạn 1000 từ.\n"
                "Vui lòng rút ngắn nội dung trước khi dịch."
            )
            self._valid_pair = None
            return

        # 4. Không có chữ cái: giữ nguyên nội dung
        if not contains_letters(text):
            self.result_text.setPlainText(text)
            self._valid_pair = None
            return

        # 5. Văn bản hợp lệ: chuẩn bị yêu cầu dịch
        source, target = (
            self.language_controller.get_languages()
        )

        print(f"Yêu cầu dịch: {source} -> {target}")
        print(f"Nội dung: {text}")

    def _update_word_count(self):
        # 1. Đọc nội dung Input
        text = self.input_text.toPlainText()

        # 2. Đếm từ
        count = count_words(text)

        # 3. Định dạng số lượng từ
        formatted_count = f"{count:,}".replace(",", ".")

        # 4. Cập nhật QLabel
        self.word_count_label.setText(
            f"{formatted_count} / 1.000 từ"
        )

    def _on_input_changed(self):
        # 1. Cập nhật bộ đếm từ
        self._update_word_count()

        # 2. Bỏ qua phần xóa kết quả nếu Python đang đổi Input
        if self._changing_input_programmatically:
            return

        # 3. Xóa kết quả cũ nếu có
        if self.result_text.toPlainText():
            self.result_text.clear()

            self.result_text.setPlaceholderText(
                "Nội dung đã thay đổi. "
                "Nhấn Dịch để cập nhật kết quả."
            )

        # 4. Hủy cặp dịch cũ
        self._valid_pair = None

    def _set_input_text(self, text):
        # 5. Đánh dấu việc thay đổi Input bằng Python
        self._changing_input_programmatically = True

        try:
            self.input_text.setPlainText(text)
        finally:
            self._changing_input_programmatically = False
