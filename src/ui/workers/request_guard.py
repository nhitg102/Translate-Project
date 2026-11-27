class RequestGuard:
    def __init__(self):
        # 1. Lưu yêu cầu đang được chấp nhận
        self._active_task_id: int | None = None
        self._request_context: tuple[object, ...] | None = None

    def activate(
        self,
        task_id: int,
        context: tuple[object, ...]
    ) -> None:
        # 2. Đánh dấu yêu cầu mới nhất
        self._active_task_id = task_id
        self._request_context = context

    def invalidate(self) -> None:
        # 3. Hủy hiệu lực của yêu cầu hiện tại
        self._active_task_id = None
        self._request_context = None

    def is_current(
        self,
        task_id: int,
        current_context: tuple[object, ...]
    ) -> bool:
        # 4. Kiểm tra ID và dữ liệu còn khớp không
        return (
            self._active_task_id == task_id
            and self._request_context == current_context
        )

    def consume(
        self,
        task_id: int,
        current_context: tuple[object, ...]
    ) -> bool:
        # 5. Chỉ chấp nhận kết quả hợp lệ
        if not self.is_current(task_id, current_context):
            return False

        # 6. Không cho xử lý lại cùng một kết quả
        self.invalidate()

        return True