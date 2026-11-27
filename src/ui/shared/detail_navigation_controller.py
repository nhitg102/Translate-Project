from PySide6.QtCore import QObject
from PySide6.QtWidgets import (
    QWidget,
    QAbstractButton,
    QStackedWidget,
    QVBoxLayout
)

from ..animations.stack_slide_animator import StackSlideAnimator

class DetailNavigationController(QObject):
    def __init__(
        self,
        stack: QStackedWidget,
        list_page: QWidget,
        detail_page: QWidget,
        detail_widget: QWidget,
        back_button: QAbstractButton,
        parent=None
    ):
        super().__init__(parent)

        # 1. Lưu các widget chuyển trang
        self.stack = stack
        self.list_page = list_page
        self.detail_page = detail_page

        # 2. Kiểm tra layout của trang Details
        detail_layout = self.detail_page.layout()

        if detail_layout is None:
            detail_layout = QVBoxLayout(self.detail_page)

        elif not isinstance(detail_layout, QVBoxLayout):
            raise RuntimeError(
                "Trang Details cần QVBoxLayout"
            )

        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(0)

        # 3. Đưa giao diện Details vào trang chứa
        detail_layout.addWidget(detail_widget)

        # 4. Khởi tạo animation chuyển trang
        self.animator = StackSlideAnimator(self)

        # 5. Kết nối nút Back
        back_button.clicked.connect(
            self.back_to_list
        )

        # 6. Hiển thị danh sách ban đầu
        self.stack.setCurrentWidget(
            self.list_page
        )

    @property
    def is_animating(self) -> bool:
        return self.animator.is_animating

    def show_details(self) -> None:
        if self.is_animating:
            return

        # Trượt sang trang Details
        self.animator.slide_stack(
            self.stack,
            self.detail_page,
            "forward"
        )

    def back_to_list(self) -> None:
        if self.is_animating:
            return

        # Trượt về trang danh sách
        self.animator.slide_stack(
            self.stack,
            self.list_page,
            "backward"
        )
