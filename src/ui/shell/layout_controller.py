from PySide6.QtCore import (
    QObject,
    QTimer,
    Signal,
    QEvent
)

from .sidebar_controller import SidebarController

class ResizeWatcher(QObject):
    resized = Signal()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Resize:
            self.resized.emit()

        return super().eventFilter(watched, event)

class LayoutController(QObject):
    def __init__(
        self,
        translation_widget,
        sidebar_widget,
        mode_controls,
        footer_controls,
        panel_layout,
        content_host,
        mode_frame,
        sidebar_controller: SidebarController,
        parent=None
    ):
        super().__init__(parent)

        # 1. Lưu các widget cần điều chỉnh
        self.translation = translation_widget
        self.sidebar = sidebar_widget
        self.mode_controls = mode_controls
        self.footer_controls = footer_controls

        # 2. Lưu các thành phần hỗ trợ
        self.panel_layout = panel_layout
        self.sidebar_controller = sidebar_controller

        # 3. Khởi tạo bộ theo dõi Resize
        self._relayout_pending = False
        self.resize_watcher = ResizeWatcher(self)

        # 4. Kết nối sự kiện
        self.resize_watcher.resized.connect(
            self._schedule_relayout
        )

        self.sidebar_controller.finished.connect(
            self.apply_layout
        )

        # 5. Theo dõi Resize của các vùng giao diện
        content_host.installEventFilter(
            self.resize_watcher
        )

        mode_frame.installEventFilter(
            self.resize_watcher
        )

    def _resize_translation(self):
        size = self.panel_layout.translation_size()
        self.translation.resize(size)

    def center_translation(self):
        # 1. Cập nhật kích thước TranslationPanel
        self._resize_translation()

        # 2. Tính vị trí khi Sidebar đóng
        translation_pos, mode_pos = (
            self.panel_layout.closed_positions()
        )

        # 3. Căn TranslationPanel
        self.translation.move(translation_pos)
        self.translation.show()

        # 4. Căn Mode Bar
        self.mode_controls.move(mode_pos)

        # 5. Căn Footer
        self.footer_controls.move(
            self.panel_layout.footer_position(
                translation_pos.x()
            )
        )

    def _schedule_relayout(self):
        # 1. Tránh hẹn cập nhật nhiều lần cùng lúc
        if self._relayout_pending:
            return

        self._relayout_pending = True

        # 2. Đợi Qt hoàn tất lượt cập nhật layout
        QTimer.singleShot(0, self.apply_layout)

    def apply_layout(self):
        # 1. Đánh dấu đã xử lý lịch cập nhật
        self._relayout_pending = False

        # 2. Không can thiệp khi animation đang chạy
        if self.sidebar_controller.is_animating:
            return

        # 3. Cập nhật kích thước TranslationPanel
        self._resize_translation()

        # 4. Sidebar đang mở
        if self.sidebar_controller.is_open:
            translation_pos, sidebar_pos, mode_pos = (
                self.panel_layout.open_positions()
            )

            self.translation.move(translation_pos)

            sidebar = self.panel_layout.sidebar_geometry()

            self.sidebar.setGeometry(
                sidebar_pos.x(),
                sidebar_pos.y(),
                sidebar.width(),
                sidebar.height()
            )

            self.mode_controls.move(mode_pos)

        # 5. Sidebar đang đóng
        else:
            translation_pos, mode_pos = (
                self.panel_layout.closed_positions()
            )

            self.translation.move(translation_pos)

            self.sidebar.setGeometry(
                self.panel_layout.hidden_sidebar_geometry()
            )

            self.sidebar.hide()
            self.mode_controls.move(mode_pos)

        # 6. Căn Footer theo TranslationPanel
        self.footer_controls.move(
            self.panel_layout.footer_position(
                translation_pos.x()
            )
        )
