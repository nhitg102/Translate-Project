from PySide6.QtCore import QObject, Signal

from ..animations.position_animator import PositionAnimator

class SidebarController(QObject):
    finished = Signal()

    def __init__(
        self,
        translation_widget,
        sidebar_widget,
        mode_controls,
        footer_controls,
        panel_layout,
        parent=None
    ):
        super().__init__(parent)

        # 1. Lưu các widget cần điều khiển
        self.translation = translation_widget
        self.sidebar = sidebar_widget
        self.mode_controls = mode_controls
        self.footer_controls = footer_controls
        self.panel_layout = panel_layout

        # 2. Khởi tạo trạng thái và animation
        self._is_open = False
        self.animations = PositionAnimator(self)

        # 3. Kết nối sự kiện
        self.animations.finished.connect(
            self._animation_finished
        )

    @property
    def is_open(self):
        return self._is_open

    @property
    def is_animating(self):
        return self.animations.is_animating

    def _resize_translation(self):
        self.translation.resize(
            self.panel_layout.translation_size()
        )

    def toggle(self):
        if self.is_animating:
            return

        if self._is_open:
            self.close()
        else:
            self.open()

    def open(self):
        # 1. Kiểm tra trạng thái
        if self.is_animating or self._is_open:
            return

        # 2. Tính vị trí
        self._resize_translation()

        translation_pos, sidebar_pos, mode_pos = (
            self.panel_layout.open_positions()
        )

        footer_pos = self.panel_layout.footer_position(
            translation_pos.x()
        )

        # 3. Chuẩn bị Sidebar
        self.sidebar.setGeometry(
            self.panel_layout.hidden_sidebar_geometry()
        )

        self.sidebar.raise_()
        self.sidebar.show()

        # 4. Cập nhật trạng thái
        self._is_open = True

        # 5. Chạy animation
        self.animations.animate_positions([
            (self.translation, translation_pos),
            (self.sidebar, sidebar_pos),
            (self.mode_controls, mode_pos),
            (self.footer_controls, footer_pos)
        ])

    def close(self):
        # 1. Kiểm tra trạng thái
        if self.is_animating or not self._is_open:
            return

        # 2. Tính vị trí
        self._resize_translation()

        translation_pos, mode_pos = (
            self.panel_layout.closed_positions()
        )

        sidebar_pos = (
            self.panel_layout.hidden_sidebar_geometry().topLeft()
        )

        footer_pos = self.panel_layout.footer_position(
            translation_pos.x()
        )

        # 3. Cập nhật trạng thái
        self._is_open = False

        # 4. Chạy animation
        self.animations.animate_positions([
            (self.translation, translation_pos),
            (self.sidebar, sidebar_pos),
            (self.mode_controls, mode_pos),
            (self.footer_controls, footer_pos)
        ])

    def _animation_finished(self):
        # 1. Ẩn Sidebar sau khi đóng
        if not self._is_open:
            self.sidebar.hide()

        # 2. Thông báo animation đã hoàn tất
        self.finished.emit()
