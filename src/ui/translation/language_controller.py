# Phụ trách bộ phận chọn ngôn ngữ.

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QButtonGroup, QToolButton

class LanguageController(QObject):
    direction_changed = Signal(str, str)

    def __init__(self, ui):
        super().__init__(ui)

        # Tìm bốn nút ngôn ngữ trong giao diện
        self.source_en = self._find_button(ui, "sourceEnglishButton")
        self.source_vi = self._find_button(ui, "sourceVietnameseButton")
        self.target_en = self._find_button(ui, "targetEnglishButton")
        self.target_vi = self._find_button(ui, "targetVietnameseButton")

        # Tạo hai nhóm nút độc lập
        self.source_group = QButtonGroup(self)
        self.target_group = QButtonGroup(self)

        self.source_group.setExclusive(True)
        self.target_group.setExclusive(True)

        self.source_group.addButton(self.source_en)
        self.source_group.addButton(self.source_vi)

        self.target_group.addButton(self.target_en)
        self.target_group.addButton(self.target_vi)

        # Chiều dịch mặc định: Anh -> Việt
        self.source_en.setChecked(True)
        self.target_vi.setChecked(True)

        self._direction = ("en", "vi")

        # Kết nối sự kiện
        self.source_group.buttonClicked.connect(self._source_clicked)
        self.target_group.buttonClicked.connect(self._target_clicked)

    def _find_button(self, ui, name):
        button = ui.findChild(QToolButton, name)

        if button is None:
            raise RuntimeError(f"Không tìm thấy nút: {name}")

        return button

    def get_languages(self):
        source = "en" if self.source_en.isChecked() else "vi"
        target = "en" if self.target_en.isChecked() else "vi"

        return source, target

    def _source_clicked(self, button):
        if button is self.source_en:
            self.target_vi.setChecked(True)
        else:
            self.target_en.setChecked(True)

        self._emit_if_changed()

    def _target_clicked(self, button):
        if button is self.target_en:
            self.source_vi.setChecked(True)
        else:
            self.source_en.setChecked(True)

        self._emit_if_changed()

    def _emit_if_changed(self):
        new_direction = self.get_languages()

        if new_direction != self._direction:
            self._direction = new_direction
            self.direction_changed.emit(*new_direction)
