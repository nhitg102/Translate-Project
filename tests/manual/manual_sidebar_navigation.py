import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QToolButton,
    QVBoxLayout
)

from src.ui.shell.main_window import MainWindow


def main():
    # 1. Khởi tạo ứng dụng
    app = QApplication(sys.argv)
    window = MainWindow()

    # 2. Tạo Favorites giả lập
    favorites_demo = QFrame()
    favorites_demo.setObjectName("favoritesDemo")

    favorites_demo.setStyleSheet("""
        QFrame#favoritesDemo {
            background-color: #353535;
            border: 1px solid #808080;
        }
        QLabel {
            color: white;
            font-size: 20px;
        }
    """)

    # 3. Thêm nội dung để phân biệt với History
    demo_layout = QVBoxLayout(favorites_demo)

    demo_label = QLabel("FAVORITES - DEMO")
    demo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    demo_layout.addWidget(demo_label)

    # 4. Đăng ký panel vào Sidebar Host
    window.sidebar_host.addWidget(favorites_demo)

    # 5. Tìm nút Favorites
    favorites_button = window.window.findChild(
        QToolButton,
        "favoritesButton"
    )

    if favorites_button is None:
        raise RuntimeError("Không tìm thấy favoritesButton.")

    # 6. Kết nối nút Favorites với SidebarNavigationController
    favorites_button.clicked.connect(
        lambda: window.sidebar_navigation.toggle_panel(
            favorites_demo
        )
    )

    # 7. Hiển thị ứng dụng
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())