import sys

from PySide6.QtWidgets import QApplication
from src.ui.shell.main_window import MainWindow


def add_sample_history(main):
    # 1. Dữ liệu giả để kiểm thử History
    sample_data = [
        (
            "Anh → Việt",
            "Hello world!",
            "Xin chào thế giới!",
            "24/11/2026 18:30",
            False
        ),
        (
            "Việt → Anh",
            "Hôm nay thời tiết rất đẹp.",
            "The weather is beautiful today.",
            "24/11/2026 17:15",
            True
        ),
        (
            "Anh → Việt",
            "Knowledge is power.",
            "Tri thức là sức mạnh.",
            "23/11/2026 20:10",
            False
        ),
        (
            "Anh → Việt",
            "The stars are beautiful tonight.\n"
            "I wish we could see them together.",
            "Những vì sao đêm nay thật đẹp.\n"
            "Ước gì chúng ta có thể ngắm chúng cùng nhau.",
            "22/11/2026 21:40",
            True
        ),
        (
            "Việt → Anh",
            "Đây là dữ liệu dùng để kiểm thử giao diện.",
            "This is data used to test the interface.",
            "21/11/2026 09:25",
            False
        )
    ]

    # 2. Thêm từng bản dịch vào HistoryPanel
    for direction, source, translated, date, favorite in sample_data:
        main.history.add_card(
            direction,
            source,
            translated,
            date,
            favorite
        )


def main():
    # 3. Khởi tạo ứng dụng Qt
    app = QApplication(sys.argv)

    # 4. Tạo MainWindow thật
    window = MainWindow()

    # 5. Nạp dữ liệu kiểm thử
    add_sample_history(window)

    # 6. Hiển thị và chạy ứng dụng
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
