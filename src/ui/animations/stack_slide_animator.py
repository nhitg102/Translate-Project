from PySide6.QtCore import QObject, Signal, QPoint
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QStackedWidget
)

from .position_animator import PositionAnimator

class StackSlideAnimator(QObject):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Sử dụng PositionAnimator để tạo chuyển động
        self._position_animator = PositionAnimator(self)

        # 2. Lưu các lớp ảnh tạm thời
        self._overlays: list[QLabel] = []

        # 3. Kết nối sự kiện hoàn thành
        self._position_animator.finished.connect(
            self._on_finished
        )

    @property
    def is_animating(self) -> bool:
        return self._position_animator.is_animating

    def slide_stack(
        self,
        stack: QStackedWidget,
        target_page: QWidget,
        direction: str
    ) -> None:
        # 1. Kiểm tra trạng thái
        if self.is_animating:
            return

        if stack.currentWidget() is target_page:
            return

        if direction not in ("forward", "backward"):
            raise ValueError("direction không hợp lệ")

        # 2. Lấy kích thước vùng chuyển trang
        width = stack.width()
        height = stack.height()

        if width <= 0 or height <= 0:
            stack.setCurrentWidget(target_page)
            return

        # 3. Chụp trang hiện tại
        old_pixmap = stack.grab()

        # 4. Chuyển trang và chụp trang mới
        stack.setCurrentWidget(target_page)
        new_pixmap = stack.grab()

        # 5. Tạo hai lớp ảnh tạm
        old_layer = QLabel(stack)
        new_layer = QLabel(stack)

        old_layer.setPixmap(old_pixmap)
        new_layer.setPixmap(new_pixmap)

        # 6. Xác định hướng trượt
        offset = (
            width if direction == "forward" else -width
        )

        old_layer.setGeometry(
            0, 0, width, height
        )

        new_layer.setGeometry(
            offset, 0, width, height
        )

        # 7. Hiển thị các lớp ảnh
        old_layer.show()
        new_layer.show()

        old_layer.raise_()
        new_layer.raise_()

        self._overlays = [old_layer, new_layer]

        # 8. Chạy animation
        self._position_animator.animate_positions(
            [
                (old_layer, QPoint(-offset, 0)),
                (new_layer, QPoint(0, 0))
            ],
            duration=220
        )

    def _on_finished(self) -> None:
        # 1. Xóa các lớp ảnh tạm
        for layer in self._overlays:
            layer.hide()
            layer.deleteLater()

        self._overlays.clear()

        # 2. Thông báo animation hoàn thành
        self.finished.emit()
