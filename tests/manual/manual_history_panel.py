import sys

from PySide6.QtWidgets import QApplication

from src.ui.history.history_panel import HistoryPanel

def main():
    app = QApplication(sys.argv)

    # 1. Khởi tạo HistoryPanel
    panel = HistoryPanel()

    # 2. Thêm dữ liệu mẫu
    panel.add_card(
        "Eng → Viet",
        "Hello, how are you?",
        "Xin chào, bạn khỏe không?",
        "22/11/2026"
    )

    panel.add_card(
        "Viet → Eng",
        "Cảm ơn bạn",
        "Thank you",
        "22/11/2026",
        True
    )

    panel.add_card(
        "Eng → Viet",
        "Good morning",
        "Chào buổi sáng",
        "21/11/2026"
    )

    # 3. Hiển thị HistoryPanel
    panel.widget.resize(500, 700)
    panel.widget.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
