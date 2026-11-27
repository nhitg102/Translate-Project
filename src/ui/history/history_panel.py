from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QScrollArea,
    QStackedWidget
)

from ..shared.ui_loader import load_ui
from ..shared.translation_card import TranslationCard
from ..shared.translation_detail import TranslationDetail
from ..shared.detail_navigation_controller import DetailNavigationController

from .history_list_controller import HistoryListController

class HistoryPanel:
    def __init__(self, parent=None):
        # 1. Nạp giao diện History
        self.widget = load_ui("history_panel.ui", parent)

        # 2. Tìm các widget của History List
        search_input = self.widget.findChild(
            QLineEdit, "historySearchInput"
        )
        scroll_area = self.widget.findChild(
            QScrollArea, "historyScrollArea"
        )
        list_container = self.widget.findChild(
            QWidget, "historyListContainer"
        )
        empty_state = self.widget.findChild(
            QWidget, "emptyState"
        )
        empty_label = self.widget.findChild(
            QLabel, "emptyMessageLabel"
        )

        # 3. Tìm các widget chuyển trang
        history_stack = self.widget.findChild(
            QStackedWidget, "historyStack"
        )
        list_page = self.widget.findChild(
            QWidget, "historyListPage"
        )
        detail_page = self.widget.findChild(
            QWidget, "historyDetailPage"
        )

        # 4. Kiểm tra widget
        if (
            search_input is None
            or scroll_area is None
            or list_container is None
            or empty_state is None
            or empty_label is None
            or history_stack is None
            or list_page is None
            or detail_page is None
        ):
            raise RuntimeError(
                "Thiếu widget trong history_panel.ui"
            )

        # 5. Lưu các widget chuyển trang
        self.history_stack = history_stack
        self.list_page = list_page
        self.detail_page = detail_page

        # 6. Khởi tạo HistoryListController
        self.list_controller = HistoryListController(
            search_input=search_input,
            scroll_area=scroll_area,
            list_container=list_container,
            empty_state=empty_state,
            empty_label=empty_label,
            parent=self.widget
        )

        # Giữ thuộc tính cho tương thích
        self.search_input = search_input

        # 7. Khởi tạo giao diện Details
        self.detail_view = TranslationDetail(
            self.detail_page
        )

        # 8. Khởi tạo controller điều hướng
        self.detail_navigation = DetailNavigationController(
            stack=self.history_stack,
            list_page=self.list_page,
            detail_page=self.detail_page,
            detail_widget=self.detail_view.widget,
            back_button=self.detail_view.back_button,
            parent=self.widget
        )

        # 9. Kết nối yêu cầu mở Details
        self.list_controller.open_requested.connect(
            self._open_details
        )

    @property
    def cards(self):
        return self.list_controller.cards

    def add_card(
        self,
        direction: str,
        source_text: str,
        translated_text: str,
        date_text: str,
        is_favorite: bool = False
    ) -> TranslationCard:
        return self.list_controller.add_card(
            direction=direction,
            source_text=source_text,
            translated_text=translated_text,
            date_text=date_text,
            is_favorite=is_favorite
        )

    def _open_details(self, card: TranslationCard) -> None:
        # 1. Kiểm tra animation
        if self.detail_navigation.is_animating:
            return

        # 2. Cập nhật nội dung Details
        self.detail_view.set_content(
            source_text=card.source_text,
            translated_text=card.translated_text
        )

        # 3. Yêu cầu chuyển sang Details
        self.detail_navigation.show_details()
