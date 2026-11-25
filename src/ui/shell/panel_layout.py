from PySide6.QtCore import QPoint, QRect, QSize

class PanelLayout:
    GAP = 16
    SIDEBAR_WIDTH = 300
    # Kích thước TranslationPanel
    MIN_TRANSLATION_WIDTH = 802
    MIN_TRANSLATION_HEIGHT = 390

    MAX_TRANSLATION_WIDTH = 1300
    MAX_TRANSLATION_HEIGHT = 460

    # Khoảng cách tối thiểu với mép ContentHost
    HORIZONTAL_MARGIN = 23
    VERTICAL_MARGIN = 19

    SIDEBAR_BOTTOM_MARGIN = 24
    SIDEBAR_MAX_HEIGHT = 720

    def __init__(
        self,
        content_host,
        translation,
        source_column,
        mode_frame,
        mode_controls,
        bottom_nav_frame,
        footer_controls,
        central_widget
    ):
        # Lưu các widget cần tính vị trí
        self.content_host = content_host
        self.translation = translation
        self.source_column = source_column
        self.mode_frame = mode_frame
        self.mode_controls = mode_controls

        # Các widget của Footer
        self.bottom_nav_frame = bottom_nav_frame
        self.footer_controls = footer_controls

        # Vùng chứa sidebar
        self.central_widget = central_widget

    def translation_size(self):
        # 1. Lấy kích thước vùng ContentHost
        host_width = self.content_host.width()
        host_height = self.content_host.height()

        # 2. Tính chiều rộng còn lại
        available_width = (
            host_width
            - self.SIDEBAR_WIDTH
            - self.GAP
            - 2 * self.HORIZONTAL_MARGIN
        )

        # 3. Giới hạn chiều rộng
        width = max(
            self.MIN_TRANSLATION_WIDTH,
            min(available_width, self.MAX_TRANSLATION_WIDTH)
        )

        # 4. Tính và giới hạn chiều cao
        available_height = (
            host_height - 2 * self.VERTICAL_MARGIN
        )

        height = max(
            self.MIN_TRANSLATION_HEIGHT,
            min(available_height, self.MAX_TRANSLATION_HEIGHT)
        )

        # 5. Trả về kích thước mong muốn
        return QSize(width, height)

    def _mode_position(self, translation_x):
        # Tính vị trí Mode theo cột Input
        source_offset = self.source_column.mapTo(
            self.translation,
            QPoint(0, 0)
        ).x()

        source_x = translation_x + source_offset

        global_pos = self.content_host.mapToGlobal(
            QPoint(source_x, 0)
        )

        mode_x = self.mode_frame.mapFromGlobal(
            global_pos
        ).x()

        return QPoint(mode_x, self.mode_controls.y())

    def footer_position(self, translation_x):
        # Tính tâm TranslationPanel trong contentHost
        center_x = (
            translation_x + self.translation.width() // 2
        )

        # Chuyển tọa độ sang bottomNavFrame
        global_pos = self.content_host.mapToGlobal(
            QPoint(center_x, 0)
        )

        footer_center_x = self.bottom_nav_frame.mapFromGlobal(
            global_pos
        ).x()

        # Căn giữa footerControls theo TranslationPanel
        x = footer_center_x - self.footer_controls.width() // 2

        # Căn giữa theo chiều cao bottomNavFrame
        y = (
            self.bottom_nav_frame.height()
            - self.footer_controls.height()
        ) // 2

        return QPoint(x, y)

    def _translation_y(self):
        # 1. Tính khoảng trống theo chiều cao
        remaining = (
            self.content_host.height()
            - self.translation.height()
        )

        # 2. Giữ panel gần mép trên khi cửa sổ lớn
        # Ở cửa sổ mặc định vẫn căn như trước
        return max(0, min(31, remaining // 2))

    def closed_positions(self):
        # Vị trí khi panel bên phải đóng
        host = self.content_host
        translation = self.translation

        x = (host.width() - translation.width()) // 2
        y = self._translation_y()

        translation_pos = QPoint(x, y)
        mode_pos = self._mode_position(x)

        return translation_pos, mode_pos

    def sidebar_geometry(self):
        # Lấy mép trên Mode Bar
        top = self.mode_frame.mapTo(
            self.central_widget,
            QPoint(0, 0)
        ).y()
        # Tính chiều cao khả dụng
        available_height = (
            self.central_widget.height()
            - top
            - self.SIDEBAR_BOTTOM_MARGIN
        )
        # Giới hạn chiều cao Sidebar
        height = max(
            0,
            min(available_height, self.SIDEBAR_MAX_HEIGHT)
        )
        # Trả về hình học cơ sở
        return QRect(
            0,
            top,
            self.SIDEBAR_WIDTH,
            height
        )

    def open_positions(self):
        # 1. Lấy các widget cần tính vị trí
        host = self.content_host
        translation = self.translation

        # 2. Tính tổng chiều rộng khi Sidebar mở
        total_width = (
            translation.width()
            + self.GAP
            + self.SIDEBAR_WIDTH
        )

        # 3. Tính vị trí TranslationPanel
        x = (host.width() - total_width) // 2
        y = self._translation_y()

        # 4. Tính vị trí Sidebar trong ContentHost
        sidebar_x_in_host = (
            x + translation.width() + self.GAP
        )

        # 5. Chuyển tọa độ Sidebar sang CentralWidget
        sidebar_x = self.content_host.mapTo(
            self.central_widget,
            QPoint(sidebar_x_in_host, 0)
        ).x()

        sidebar_y = self.sidebar_geometry().y()

        # 6. Tính vị trí các thành phần
        translation_pos = QPoint(x, y)
        sidebar_pos = QPoint(sidebar_x, sidebar_y)
        mode_pos = self._mode_position(x)

        return translation_pos, sidebar_pos, mode_pos

    def hidden_sidebar_geometry(self):
        # Lấy kích thước Sidebar
        sidebar = self.sidebar_geometry()

        # Đặt History ngoài mép phải centralwidget
        return QRect(
            self.central_widget.width(),
            sidebar.y(),
            sidebar.width(),
            sidebar.height()
        )
