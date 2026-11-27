from PySide6.QtWidgets import QLabel, QToolButton

from .ui_loader import load_ui

class TranslationDetail:
    def __init__(self, parent=None):
        # 1. Nạp giao diện Details
        self.widget = load_ui("translation_detail.ui",parent)

        # 2. Tìm các widget
        back_button = self.widget.findChild(
            QToolButton, "backButton"
        )
        source_label = self.widget.findChild(
            QLabel, "detailSourceText"
        )
        pronunciation_label = self.widget.findChild(
            QLabel, "detailPronunciation"
        )
        translated_label = self.widget.findChild(
            QLabel, "detailPlaceholder"
        )

        # 3. Kiểm tra widget trước khi sử dụng
        if (
            back_button is None
            or source_label is None
            or pronunciation_label is None
            or translated_label is None
        ):
            raise RuntimeError(
                "Thiếu widget trong translation_detail.ui"
            )

        # 4. Lưu các widget đã được kiểm tra
        self.back_button = back_button
        self.source_label = source_label
        self.pronunciation_label = pronunciation_label
        self.translated_label = translated_label

    def set_content(
        self,
        source_text: str,
        translated_text: str,
        pronunciation: str = ""
    ) -> None:
        # 1. Hiển thị văn bản gốc
        self.source_label.setText(source_text)

        # 2. Hiển thị phiên âm
        self.pronunciation_label.setText(pronunciation)

        # 3. Hiển thị bản dịch
        self.translated_label.setText(translated_text)
