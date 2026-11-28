from PySide6.QtCore import (
    QObject,
    Signal,
    QPoint,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve
)

from PySide6.QtWidgets import QWidget

class PositionAnimator(QObject):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Lưu nhóm animation đang chạy
        self._group: QParallelAnimationGroup | None = None

    @property
    def is_animating(self) -> bool:
        return self._group is not None

    def animate_positions(
        self,
        movements: list[tuple[QWidget, QPoint]],
        duration: int = 320
    ) -> None:
        # 1. Không tạo animation mới khi đang chạy
        if self.is_animating:
            return

        # 2. Tạo nhóm animation
        group = QParallelAnimationGroup(self)

        # 3. Tạo animation cho từng widget
        for widget, end_pos in movements:
            animation = QPropertyAnimation(
                widget,
                b"pos",
                group
            )

            animation.setDuration(duration)
            animation.setStartValue(widget.pos())
            animation.setEndValue(end_pos)

            animation.setEasingCurve(
                QEasingCurve.Type.InOutCubic
            )

            group.addAnimation(animation)

        # 4. Kết nối tín hiệu hoàn thành
        group.finished.connect(self._on_finished)

        # 5. Lưu và khởi chạy animation
        self._group = group
        group.start()

    def _on_finished(self) -> None:
        # 1. Giải phóng nhóm animation
        if self._group is not None:
            self._group.deleteLater()
            self._group = None

        # 2. Phát tín hiệu hoàn thành
        self.finished.emit()
