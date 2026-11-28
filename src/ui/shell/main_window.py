import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QToolButton,
    QStackedWidget
)

from ..shared.ui_loader import load_ui
from ..translation.translation_panel import TranslationPanel
from ..history.history_panel import HistoryPanel
from ..workers.task_manager import TaskManager

from .panel_layout import PanelLayout
from .sidebar_controller import SidebarController
from .sidebar_navigation_controller import SidebarNavigationController
from .layout_controller import LayoutController

class MainWindow:
    def __init__(self):
        # 1. Nạp giao diện chính
        self.window = load_ui("main_window.ui")

        # 2. Tìm các widget trong MainWindow
        central_widget = self.window.findChild(
            QWidget, "centralwidget"
        )
        content_host = self.window.findChild(
            QFrame, "contentHost"
        )
        history_button = self.window.findChild(
            QToolButton, "historyButton"
        )
        mode_frame = self.window.findChild(
            QFrame, "modeFrame"
        )
        mode_controls = self.window.findChild(
            QWidget, "modeControls"
        )
        bottom_nav_frame = self.window.findChild(
            QFrame, "bottomNavFrame"
        )
        footer_controls = self.window.findChild(
            QWidget, "footerControls"
        )

        # 3. Kiểm tra widget
        if (
            content_host is None
            or history_button is None
            or mode_frame is None
            or mode_controls is None
            or bottom_nav_frame is None
            or footer_controls is None
            or central_widget is None
        ):
            raise RuntimeError("Thiếu widget trong main_window.ui")

        # 4. Lưu các widget
        self.content_host = content_host
        self.history_button = history_button
        self.mode_frame = mode_frame
        self.mode_controls = mode_controls
        self.bottom_nav_frame = bottom_nav_frame
        self.footer_controls = footer_controls
        self.central_widget = central_widget

        # 5. Khởi tạo các panel
        self.translation = TranslationPanel(self.content_host)

        # Tạo vùng chứa Sidebar dùng chung
        self.sidebar_host = QStackedWidget(self.central_widget)

        # Khởi tạo HistoryPanel bên trong Sidebar Host
        self.history = HistoryPanel(self.sidebar_host)

        # Đăng ký History là trang đầu tiên
        self.sidebar_host.addWidget(self.history.widget)
        self.sidebar_host.setCurrentWidget(self.history.widget)

        # Ban đầu Sidebar chưa mở
        self.sidebar_host.hide()

        # 6. Tìm widget bên trong các panel
        source_column = self.translation.widget.findChild(
            QWidget, "sourceColumn"
        )
        close_button = self.history.widget.findChild(
            QToolButton, "closeHistoryButton"
        )

        # 7. Kiểm tra widget của các panel
        if source_column is None or close_button is None:
            raise RuntimeError("Thiếu widget bên trong panel")

        self.source_column = source_column
        self.close_history_button = close_button

        # Khởi tạo bộ tính toán bố cục
        self.panel_layout = PanelLayout(
            self.content_host,
            self.translation.widget,
            self.source_column,
            self.mode_frame,
            self.mode_controls,
            self.bottom_nav_frame,
            self.footer_controls,
            self.central_widget
        )

        # 8. Thiết lập giao diện ban đầu

        # QSS tạm thời để kiểm tra viền HistoryPanel
        self.history.widget.setStyleSheet("""
            QWidget#historyPanel {
                background-color: #353535;
                border: 1px solid #808080;
            }
        """)

        # 9. Khởi tạo SidebarController
        self.sidebar_controller = SidebarController(
            translation_widget=self.translation.widget,
            sidebar_widget=self.sidebar_host,
            mode_controls=self.mode_controls,
            footer_controls=self.footer_controls,
            panel_layout=self.panel_layout,
            parent=self.window
        )

        # 10. Khởi tạo SidebarNavigationController
        self.sidebar_navigation = SidebarNavigationController(
            sidebar_host=self.sidebar_host,
            sidebar_controller=self.sidebar_controller,
            parent=self.window
        )

        # 11. Khởi tạo LayoutController
        self.layout_controller = LayoutController(
            translation_widget=self.translation.widget,
            sidebar_widget=self.sidebar_host,
            mode_controls=self.mode_controls,
            footer_controls=self.footer_controls,
            panel_layout=self.panel_layout,
            content_host=self.content_host,
            mode_frame=self.mode_frame,
            sidebar_controller=self.sidebar_controller,
            parent=self.window
        )

        # Khởi tạo bộ quản lý tác vụ nền
        self.task_manager = TaskManager(parent=self.window)

        # 12. Kết nối sự kiện
        self.history_button.clicked.connect(
            lambda: self.sidebar_navigation.toggle_panel(
                self.history.widget
            )
        )

        self.close_history_button.clicked.connect(
            self.sidebar_controller.close
        )

    def show(self):
        self.window.resize(1200, 700)
        self.window.show()

        QTimer.singleShot(
            0,
            self.layout_controller.center_translation
        )

def main():
    app = QApplication(sys.argv)

    # 1. Không tự thoát khi cửa sổ cuối đóng
    app.setQuitOnLastWindowClosed(False)

    # 2. Khởi tạo MainWindow
    window = MainWindow()

    # 3. Yêu cầu đóng TaskManager khi hết cửa sổ
    app.lastWindowClosed.connect(
        window.task_manager.request_shutdown
    )

    # 4. Thoát khi mọi Worker đã hoàn tất
    window.task_manager.all_tasks_finished.connect(
        app.quit
    )

    # 5. Hiển thị giao diện
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
