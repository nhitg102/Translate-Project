from PySide6.QtCore import QObject, Signal, QEvent, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QToolButton, QFrame

from .ui_loader import load_ui

class TranslationCard(QObject):
    favorite_changed = Signal(bool)
    delete_requested = Signal()
    open_requested = Signal()

    def __init__(
        self,
        direction,
        source_text,
        translated_text,
        date_text,
        is_favorite=False,
        parent=None
    ):
        super().__init__(parent)

        # Lưu dữ liệu của bản dịch
        self.direction = direction
        self.source_text = source_text
        self.translated_text = translated_text
        self.date_text = date_text
        self.is_favorite = is_favorite

        self.widget = load_ui("translation_card.ui", parent)

        # Tìm các widget
        direction_label = self.widget.findChild(QLabel, "directionLabel")
        source_label = self.widget.findChild(QLabel, "sourceTextLabel")
        translated_label = self.widget.findChild(
            QLabel, "translatedTextLabel"
        )
        date_label = self.widget.findChild(QLabel, "dateLabel")

        favorite_button = self.widget.findChild(
            QToolButton, "favoriteButton"
        )
        delete_button = self.widget.findChild(
            QToolButton, "deleteButton"
        )

        # Kiểm tra widget
        if (
            direction_label is None
            or source_label is None
            or translated_label is None
            or date_label is None
            or favorite_button is None
            or delete_button is None
        ):
            raise RuntimeError("Thiếu widget trong translation_card.ui")

        # Lưu các widget
        self.direction_label = direction_label
        self.source_label = source_label
        self.translated_label = translated_label
        self.date_label = date_label

        self.favorite_button = favorite_button
        self.delete_button = delete_button

        # Hiển thị dữ liệu
        self.direction_label.setText(self.direction)
        self.source_label.setText(self.source_text)
        self.translated_label.setText(self.translated_text)
        self.date_label.setText(self.date_text)

        self.favorite_button.setChecked(self.is_favorite)

        # Kết nối sự kiện
        self.favorite_button.toggled.connect(
            self._on_favorite_toggled
        )
        self.delete_button.clicked.connect(
            self._request_delete
        )

        # Cho phép nhấn vào nội dung card để xem chi tiết
        click_areas = [
            self.widget,
            *self.widget.findChildren(QFrame),
            *self.widget.findChildren(QLabel)
        ]

        for area in click_areas:
            area.installEventFilter(self)
            area.setCursor(Qt.CursorShape.PointingHandCursor)

    def _on_favorite_toggled(self, checked: bool) -> None:
        self.is_favorite = checked
        self.favorite_changed.emit(checked)

    def _request_delete(self):
        self.delete_requested.emit()

    def eventFilter(self, watched, event):
        if (
            event.type() == QEvent.Type.MouseButtonRelease
            and isinstance(event, QMouseEvent)
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.open_requested.emit()
            return True

        return super().eventFilter(watched, event)
