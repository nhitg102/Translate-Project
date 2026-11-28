import sys

from PySide6.QtWidgets import QApplication

from src.ui.shared.translation_card import TranslationCard

def main():
    # 1. Khởi tạo ứng dụng
    app = QApplication(sys.argv)

    # 2. Tạo Card mẫu
    card = TranslationCard(
        direction="Eng → Viet",
        source_text="Hello, how are you?",
        translated_text="Xin chào, bạn khỏe không?",
        date_text="25/11/2026",
        is_favorite=False
    )

    # 3. Kết nối các sự kiện để kiểm thử
    card.favorite_changed.connect(
        lambda checked: print(f"Favorite: {checked}")
    )

    card.delete_requested.connect(
        lambda: print("Yêu cầu xóa TranslationCard")
    )

    card.open_requested.connect(
        lambda: print("Yêu cầu mở Details")
    )

    # 4. Hiển thị Card
    card.widget.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())