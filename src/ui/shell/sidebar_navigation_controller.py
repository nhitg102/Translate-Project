from PySide6.QtCore import QObject
from PySide6.QtWidgets import QStackedWidget, QWidget

from .sidebar_controller import SidebarController

class SidebarNavigationController(QObject):
    def __init__(
        self,
        sidebar_host: QStackedWidget,
        sidebar_controller: SidebarController,
        parent=None
    ):
        super().__init__(parent)

        # 1. Lưu các thành phần cần điều khiển
        self.sidebar_host = sidebar_host
        self.sidebar_controller = sidebar_controller

    def toggle_panel(self, panel: QWidget) -> None:
        # 1. Không chuyển trang khi animation đang chạy
        if self.sidebar_controller.is_animating:
            return

        # 2. Kiểm tra panel đã thuộc Sidebar Host chưa
        if self.sidebar_host.indexOf(panel) == -1:
            raise ValueError(
                "Panel chưa được đăng ký trong sidebarHost."
            )

        # 3. Sidebar đang đóng: chọn panel rồi mở
        if not self.sidebar_controller.is_open:
            self.sidebar_host.setCurrentWidget(panel)
            self.sidebar_controller.open()
            return

        # 4. Đang mở đúng panel: đóng Sidebar
        if self.sidebar_host.currentWidget() is panel:
            self.sidebar_controller.close()
            return

        # 5. Đang mở panel khác: chỉ thay nội dung
        self.sidebar_host.setCurrentWidget(panel)
