
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout
)

from ..shared.translation_card import TranslationCard

class HistoryListController(QObject):
    open_requested = Signal(object)
    favorite_changed = Signal(object, bool)

    def __init__(
        self,
        search_input: QLineEdit,
        scroll_area: QScrollArea,
        list_container: QWidget,
        empty_state: QWidget,
        empty_label: QLabel,
        parent=None
    ):
        super().__init__(parent)

        # 1. Lưu các widget cần quản lý
        self.search_input = search_input
        self.scroll_area = scroll_area
        self.list_container = list_container
        self.empty_state = empty_state
        self.empty_label = empty_label

        # 2. Kiểm tra layout danh sách
        list_layout = self.list_container.layout()

        if not isinstance(list_layout, QVBoxLayout):
            raise RuntimeError(
                "historyListContainer cần QVBoxLayout"
            )

        self.list_layout = list_layout

        # 3. Khởi tạo danh sách
        self.cards: list[TranslationCard] = []
        self.scroll_area.setWidgetResizable(True)

        # 4. Kết nối tìm kiếm
        self.search_input.textChanged.connect(
            self.filter_cards
        )

        # 5. Cập nhật trạng thái ban đầu
        self.filter_cards("")

    def add_card(
        self,
        direction: str,
        source_text: str,
        translated_text: str,
        date_text: str,
        is_favorite: bool = False
    ) -> TranslationCard:
        # 1. Tạo History Card
        card = TranslationCard(
            direction=direction,
            source_text=source_text,
            translated_text=translated_text,
            date_text=date_text,
            is_favorite=is_favorite,
            parent=self.list_container
        )

        # 2. Lưu card
        self.cards.append(card)

        # 3. Chèn card trước spacer cuối layout
        position = max(
            0,
            self.list_layout.count() - 1
        )

        self.list_layout.insertWidget(
            position,
            card.widget
        )

        # 4. Kết nối yêu cầu xóa
        card.delete_requested.connect(
            lambda c=card: self._remove_card(c)
        )

        # 5. Chuyển tiếp yêu cầu mở Details
        card.open_requested.connect(
            lambda c=card: self.open_requested.emit(c)
        )

        # 6. Chuyển tiếp thay đổi Favorites
        card.favorite_changed.connect(
            lambda checked, c=card:
                self.favorite_changed.emit(c, checked)
        )

        # 7. Cập nhật danh sách
        self.filter_cards(
            self.search_input.text()
        )

        return card

    def _remove_card(self, card: TranslationCard) -> None:
        if card not in self.cards:
            return

        # 1. Bỏ card khỏi danh sách
        self.cards.remove(card)

        # 2. Gỡ widget khỏi layout
        self.list_layout.removeWidget(card.widget)

        card.widget.hide()
        card.widget.deleteLater()
        card.deleteLater()

        # 3. Cập nhật trạng thái danh sách
        self.filter_cards(
            self.search_input.text()
        )

    def filter_cards(self, query: str) -> None:
        query = query.strip().casefold()
        visible_count = 0

        # 1. Tìm kiếm trong các card
        for card in self.cards:
            content = " ".join([
                card.direction,
                card.source_text,
                card.translated_text,
                card.date_text
            ]).casefold()

            matched = query in content
            card.widget.setVisible(matched)

            if matched:
                visible_count += 1

        # 2. Danh sách hoàn toàn trống
        if not self.cards:
            self.search_input.hide()
            self.scroll_area.hide()

            self.empty_label.setText(
                "Không có bản dịch nào gần đây"
            )

            self.empty_state.show()

        # 3. Không tìm thấy kết quả
        elif visible_count == 0:
            self.search_input.show()
            self.scroll_area.hide()

            self.empty_label.setText(
                "Không tìm thấy kết quả phù hợp"
            )

            self.empty_state.show()

        # 4. Có kết quả hiển thị
        else:
            self.search_input.show()
            self.scroll_area.show()
            self.empty_state.hide()
