# TNT Translate — Frontend

## 1. Tổng quan

Frontend của TNT Translate được phát triển bằng Python và PySide6.

Các file `.ui` được thiết kế bằng Qt Designer, sau đó được nạp và điều khiển thông qua các module Python.

Mã nguồn được tổ chức theo trách nhiệm của từng thành phần nhằm:

- Tách biệt giao diện, logic điều khiển và xử lý tác vụ nền.
- Tái sử dụng những thành phần chung giữa các màn hình.
- Thuận tiện cho việc mở rộng các chế độ dịch.
- Hỗ trợ tích hợp Frontend với Backend.

**Nhánh phát triển:** `feature/frontend-phase2`

**Trạng thái:** Đã xây dựng nền tảng Frontend giai đoạn 2. Chưa tích hợp Backend và chưa hoàn thiện QSS.

---

## 2. Cấu trúc thư mục

```text
src/ui/
├── animations/
│   ├── position_animator.py
│   └── stack_slide_animator.py
│
├── forms/
│   ├── main_window.ui
│   ├── translation_panel.ui
│   ├── history_panel.ui
│   ├── translation_card.ui
│   └── translation_detail.ui
│
├── history/
│   ├── history_panel.py
│   └── history_list_controller.py
│
├── shared/
│   ├── ui_loader.py
│   ├── translation_card.py
│   ├── translation_detail.py
│   └── detail_navigation_controller.py
│
├── shell/
│   ├── main_window.py
│   ├── layout_controller.py
│   ├── panel_layout.py
│   ├── sidebar_controller.py
│   └── sidebar_navigation_controller.py
│
├── translation/
│   ├── translation_panel.py
│   ├── language_controller.py
│   ├── text_rules.py
│   └── translation_pair.py
│
├── workers/
│   ├── background_worker.py
│   ├── task_manager.py
│   └── request_guard.py
│
└── README.md
```

### Trách nhiệm của từng thư mục

| Thư mục | Trách nhiệm |
|---|---|
| `animations/` | Quản lý animation của các thành phần giao diện. |
| `forms/` | Lưu các file giao diện Qt Designer. |
| `history/` | Quản lý giao diện và thao tác với danh sách lịch sử. |
| `shared/` | Chứa các thành phần dùng chung như Card, Details và UI Loader. |
| `shell/` | Quản lý MainWindow, bố cục, Sidebar và điều hướng. |
| `translation/` | Quản lý giao diện và logic phía Frontend của dịch văn bản. |
| `workers/` | Cung cấp hạ tầng xử lý tác vụ nền và kiểm soát kết quả. |

---

## 3. Tiến độ Frontend giai đoạn 2

Theo phiếu phân công công việc, Frontend giai đoạn 2 gồm các nhiệm vụ STT 26–34.

### 3.1. Những phần đã triển khai

**Giao diện dịch văn bản — STT 26–30**

- Xây dựng khu vực nhập văn bản.
- Xây dựng khu vực hiển thị kết quả.
- Xây dựng nút Dịch và nút Xóa.
- Chuyển đổi chiều dịch Anh - Việt.
- Quản lý trạng thái cặp văn bản nguồn và kết quả dịch.
- Kiểm tra giới hạn 1.000 từ.
- Xử lý Input rỗng và các trường hợp đầu vào đặc biệt.
- Hiển thị trạng thái đang dịch và thông báo lỗi.
- Cập nhật trạng thái kết quả khi Input thay đổi.

**Giao diện History — STT 31–33**

- Hiển thị danh sách lịch sử.
- Hiển thị từng bản ghi bằng TranslationCard.
- Tìm kiếm trong danh sách.
- Hiển thị trạng thái danh sách trống.
- Đánh dấu yêu thích trên giao diện.
- Xóa bản ghi khỏi danh sách hiện tại.
- Xem chi tiết bản ghi.
- Điều hướng giữa danh sách và Details.

**Các phần hỗ trợ đã triển khai thêm**

- Animation mở và đóng Sidebar.
- Animation chuyển đổi giữa danh sách và Details.
- Điều chỉnh bố cục giao diện khi thay đổi kích thước cửa sổ.
- Tách các thành phần dùng chung để hỗ trợ tái sử dụng.
- Tổ chức lại mã nguồn Frontend thành các module theo trách nhiệm.
- Xây dựng hạ tầng Worker phía Frontend.

### 3.2. Những phần chưa hoàn thiện

**STT 34 — Hoàn thiện và rà soát giao diện**

Các chức năng hiện có đã được kiểm thử thủ công, nhưng giao diện vẫn cần hoàn thiện QSS và rà soát thẩm mỹ.

**Tích hợp Backend**

Giao diện dịch văn bản và History chưa được kết nối với các chức năng Backend thực tế.

Hiện tại:

- Chưa gửi yêu cầu dịch thật từ giao diện đến Translation Engine.
- Chưa kết nối Translation Cache.
- Chưa kết nối lưu trữ và truy xuất Translation History.
- Chưa kết nối thao tác quản lý lịch sử với nguồn dữ liệu lâu dài.

Các nội dung tích hợp này thuộc STT 35–37, do thành viên Backend phụ trách theo phiếu phân công.

---

## 4. Hạ tầng Worker

Frontend đã chuẩn bị các thành phần sau:

### BackgroundWorker

File: `workers/background_worker.py`

Chạy một tác vụ trong luồng nền nhằm tránh chặn luồng giao diện chính.

### TaskManager

File: `workers/task_manager.py`

Quản lý các tác vụ nền, bao gồm:

- Khởi chạy tác vụ.
- Theo dõi các tác vụ đang hoạt động.
- Phát tín hiệu khi tác vụ thành công.
- Phát tín hiệu khi tác vụ thất bại.
- Phát tín hiệu khi tác vụ kết thúc.
- Hỗ trợ chờ các tác vụ đang chạy hoàn tất khi đóng ứng dụng.

### RequestGuard

File: `workers/request_guard.py`

Hỗ trợ kiểm tra kết quả trả về có còn thuộc yêu cầu hiện hành hay không.

Thành phần này được chuẩn bị để tránh trường hợp một kết quả cũ cập nhật lên giao diện sau khi người dùng đã thay đổi nội dung hoặc ngôn ngữ.

### Trạng thái hiện tại

Các thành phần Worker đã được kiểm tra độc lập bằng tác vụ mô phỏng.

Đã kiểm tra khả năng chạy đồng thời nhiều tác vụ.

**Worker hiện chưa được kết nối với TranslationPanel hoặc dịch vụ Backend thực tế.**

---

## 5. Hướng dẫn tích hợp Frontend — Backend

Phần này dành cho thành viên thực hiện tích hợp hệ thống.

### 5.1. Giao diện dịch văn bản

File chính:

`translation/translation_panel.py`

Module này quản lý:

- Nội dung Input và Output.
- Chiều dịch hiện tại.
- Quy tắc kiểm tra đầu vào.
- Trạng thái đang xử lý.
- Hiển thị kết quả và thông báo lỗi.

Các phương thức xử lý trạng thái kết quả đã được chuẩn bị, bao gồm:

- `show_loading()`
- `show_error()`
- `set_translation_result()`

Khi tích hợp, cần đối chiếu chữ ký phương thức trong mã nguồn hiện tại trước khi gọi.

Luồng tích hợp dự kiến:

1. Người dùng nhập văn bản và nhấn Dịch.
2. Frontend kiểm tra dữ liệu đầu vào.
3. Frontend chuyển yêu cầu hợp lệ cho thành phần xử lý.
4. Backend thực hiện quy trình Cache và Translation Engine.
5. Frontend nhận kết quả hoặc lỗi.
6. Frontend cập nhật Output nếu kết quả còn hợp lệ.

Không nên thực hiện lời gọi API đồng bộ làm chặn luồng giao diện Qt.

### 5.2. Worker

Các file liên quan:

- `workers/background_worker.py`
- `workers/task_manager.py`
- `workers/request_guard.py`

TaskManager cung cấp hạ tầng chạy tác vụ nền và nhận tín hiệu kết quả.

RequestGuard có thể được sử dụng để kiểm tra yêu cầu hiện hành trước khi cập nhật giao diện.

Cần kết nối các thành phần này với luồng dịch thực tế và kiểm tra lại hành vi khi:

- Người dùng thay đổi Input trong lúc đang dịch.
- Người dùng đổi chiều ngôn ngữ.
- Nhiều yêu cầu được gửi liên tiếp.
- API trả về lỗi hoặc hết thời gian chờ.
- Người dùng đóng ứng dụng khi tác vụ chưa hoàn tất.

### 5.3. History

Các file chính:

- `history/history_panel.py`
- `history/history_list_controller.py`

Thành phần dùng chung:

- `shared/translation_card.py`
- `shared/translation_detail.py`

Giao diện History đã hỗ trợ các thao tác danh sách, tìm kiếm, xóa và xem chi tiết.

Khi tích hợp Backend, cần kết nối:

- Lấy danh sách bản ghi đã lưu.
- Hiển thị bản ghi từ nguồn dữ liệu thực tế.
- Tìm kiếm và lọc lịch sử.
- Xóa bản ghi.
- Đồng bộ trạng thái sau khi có thay đổi dữ liệu.

Translation Cache và Translation History là hai thành phần có mục đích khác nhau. Cache không được xem là nguồn lưu trữ lịch sử.

### 5.4. Những nội dung cần thống nhất

Trước khi tích hợp, cần xác định:

- Cấu trúc dữ liệu yêu cầu dịch.
- Cấu trúc kết quả trả về.
- Mã ngôn ngữ nguồn và đích.
- Cách biểu diễn lỗi.
- Cách xác định trạng thái yêu cầu.
- Cấu trúc một bản ghi History.
- Cách cập nhật giao diện sau thao tác thêm hoặc xóa dữ liệu.

Các dữ liệu mô phỏng hiện tại không phải hợp đồng API chính thức.

### 5.5. Phân công tích hợp

Theo phiếu phân công giai đoạn 2:

- STT 35: Tích hợp Translation Engine, Cache và History vào Backend — Võ Minh Nhí.
- STT 36: Kết nối giao diện dịch văn bản với Backend — Võ Minh Nhí.
- STT 37: Kết nối giao diện lịch sử với chức năng truy xuất và quản lý — Võ Minh Nhí.

Các thay đổi về phân công cần được thống nhất giữa các thành viên.

---

## 6. Công việc giai đoạn 3 và hướng mở rộng

Theo phiếu phân công, các hạng mục Frontend giai đoạn 3 bao gồm:

- Giao diện dịch hình ảnh.
- Giao diện dịch tài liệu.
- Hiển thị nội dung OCR và kết quả dịch.
- Giao diện điều khiển dịch màn hình.
- Giao diện Personal Vocabulary List (Favorites).
- Details và thao tác quản lý từ vựng cá nhân.
- Đồng bộ giao diện giữa các chức năng.

Những chức năng này chưa được triển khai hoàn chỉnh trong nhánh hiện tại.

Các thành phần `shared/`, `animations/`, `shell/` và `workers/` được xây dựng với mục tiêu hỗ trợ việc mở rộng.

Một số chức năng bổ sung được nhóm cân nhắc:

- Giao diện Settings.
- Tùy chỉnh phím tắt.
- Hoàn thiện QSS.
- Các cơ chế tương tác nâng cao cho Overlay.

Các hạng mục bổ sung cần được xác định phạm vi trước khi triển khai.

Theo phiếu phân công giai đoạn 3, việc tích hợp giao diện OCR, tài liệu, dịch màn hình và Personal Vocabulary có sự tham gia của thành viên Frontend. Phân chia công việc cụ thể cần được nhóm xác nhận khi bắt đầu giai đoạn này.

---

## 7. Chạy và kiểm thử

Thực hiện các lệnh tại thư mục gốc của repository.

### Chạy giao diện chính

```powershell
.venv\Scripts\python.exe -m src.ui.shell.main_window
```

### Kiểm thử thủ công

```powershell
.venv\Scripts\python.exe -m tests.manual.manual_history_main
```

```powershell
.venv\Scripts\python.exe -m tests.manual.manual_history_panel
```

```powershell
.venv\Scripts\python.exe -m tests.manual.manual_sidebar_navigation
```

```powershell
.venv\Scripts\python.exe -m tests.manual.manual_translation_card
```

### Kiểm tra cú pháp

```powershell
.venv\Scripts\python.exe -m compileall -q src/ui tests/manual
```

Các chương trình trong `tests/manual/` phục vụ kiểm thử thủ công và mô phỏng.

Chúng không thay thế cho kiểm thử tích hợp Backend hoặc bộ kiểm thử tự động của dự án.

---

## 8. Lưu ý khi tiếp tục phát triển

- Giữ trách nhiệm của từng module rõ ràng.
- Ưu tiên tái sử dụng các thành phần chung khi phù hợp.
- Không đưa logic gọi API trực tiếp vào các thành phần giao diện.
- Kiểm tra các luồng đang hoạt động sau khi chỉnh sửa module dùng chung.
- Cập nhật tài liệu khi có thay đổi về kiến trúc hoặc trạng thái chức năng.

**README này mô tả nền tảng Frontend tại thời điểm chuẩn bị commit giai đoạn 2, không phải tuyên bố hoàn thành toàn bộ dự án.**