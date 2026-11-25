from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QThread, Signal

class BackgroundWorker(QThread):
    result_ready = Signal(object)
    error_occurred = Signal(str)

    def __init__(
        self,
        task: Callable[[], Any],
        parent=None
    ):
        super().__init__(parent)

        # Lưu công việc cần thực hiện
        self._task = task

    def run(self) -> None:
        try:
            # 1. Thực hiện tác vụ trong luồng nền
            result = self._task()

        except Exception as error:
            # 2. Thông báo nếu tác vụ thất bại
            self.error_occurred.emit(str(error))

        else:
            # 3. Trả kết quả khi tác vụ thành công
            self.result_ready.emit(result)
