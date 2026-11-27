from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal, Slot

from .background_worker import BackgroundWorker

class TaskManager(QObject):
    task_succeeded = Signal(int, object)
    task_failed = Signal(int, str)
    task_finished = Signal(int)

    all_tasks_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Quản lý Worker
        self._active_workers: dict[QObject, int] = {}
        self._next_task_id = 1

        # 2. Trạng thái đóng ứng dụng
        self._shutdown_requested = False

    @property
    def active_count(self) -> int:
        return len(self._active_workers)

    def start_task(self, task: Callable[[], Any]) -> int:
        # 1. Không nhận tác vụ mới khi đang đóng
        if self._shutdown_requested:
            raise RuntimeError(
                "TaskManager đang đóng, không nhận tác vụ mới."
            )

        # 2. Tạo ID và Worker
        task_id = self._next_task_id
        self._next_task_id += 1

        worker = BackgroundWorker(task)

        # 3. Giữ tham chiếu
        self._active_workers[worker] = task_id

        # 4. Kết nối sự kiện
        worker.result_ready.connect(self._on_result)
        worker.error_occurred.connect(self._on_error)
        worker.finished.connect(self._on_finished)

        # 5. Bắt đầu
        worker.start()

        return task_id

    def request_shutdown(self) -> None:
        # 1. Tránh xử lý yêu cầu đóng nhiều lần
        if self._shutdown_requested:
            return

        # 2. Ngừng nhận tác vụ mới
        self._shutdown_requested = True

        # 3. Nếu không còn Worker, cho phép thoát
        if not self._active_workers:
            self.all_tasks_finished.emit()

    @Slot(object)
    def _on_result(self, result: object) -> None:
        worker = self.sender()

        if worker is None:
            return

        task_id = self._active_workers.get(worker)

        if task_id is not None:
            self.task_succeeded.emit(task_id, result)

    @Slot(str)
    def _on_error(self, error: str) -> None:
        worker = self.sender()

        if worker is None:
            return

        task_id = self._active_workers.get(worker)

        if task_id is not None:
            self.task_failed.emit(task_id, error)

    @Slot()
    def _on_finished(self) -> None:
        worker = self.sender()

        if worker is None:
            return

        # 1. Xóa Worker khỏi danh sách
        task_id = self._active_workers.pop(worker, None)

        if task_id is None:
            return

        # 2. Hẹn giải phóng QObject
        worker.deleteLater()

        # 3. Thông báo hoàn thành
        self.task_finished.emit(task_id)

        # 4. Nếu đang đóng và không còn Worker
        if (
            self._shutdown_requested
            and not self._active_workers
        ):
            self.all_tasks_finished.emit()
