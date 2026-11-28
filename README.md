# Realtime Screen Translator

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

Công cụ hỗ trợ dịch thuật **Anh → Việt** theo thời gian thực trên màn hình. Giao diện desktop được xây dựng bằng **PySide6 (Qt for Python)**.

> README này hướng dẫn cài đặt môi trường, chạy dự án và quy trình làm việc nhóm với Git/GitHub.

---

## Mục lục

1. [Tính năng](#1-tính-năng)
2. [Công nghệ sử dụng](#2-công-nghệ-sử-dụng)
3. [Yêu cầu hệ thống](#3-yêu-cầu-hệ-thống)
4. [Cài đặt nhanh](#4-cài-đặt-nhanh)
5. [Hướng dẫn cài đặt chi tiết](#5-hướng-dẫn-cài-đặt-chi-tiết)
6. [Cài đặt PySide6](#6-cài-đặt-pyside6)
7. [Cấu hình biến môi trường](#7-cấu-hình-biến-môi-trường)
8. [Chạy dự án](#8-chạy-dự-án)
9. [Cấu trúc thư mục](#9-cấu-trúc-thư-mục)
10. [Quy trình làm việc với Git](#10-quy-trình-làm-việc-với-git)
11. [Xử lý sự cố thường gặp](#11-xử-lý-sự-cố-thường-gặp)
12. [Thành viên nhóm](#12-thành-viên-nhóm)

---

## 1. Tính năng

- [ ] Chụp/chọn vùng văn bản trên màn hình
- [ ] Nhận diện và dịch văn bản Anh → Việt
- [ ] Hiển thị kết quả dịch theo thời gian thực
- [ ] Giao diện desktop thân thiện (PySide6)

> Cập nhật danh sách này khi nhóm chốt phạm vi chức năng. Đánh dấu `[x]` cho các mục đã hoàn thành.

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python 3.11 |
| Giao diện | PySide6 |
| Quản lý phiên bản | Git, GitHub |
| Môi trường | Virtual environment (`venv`) |
| Biến môi trường | File `.env` |

## 3. Yêu cầu hệ thống

- Windows 10/11 (64-bit)
- Python 3.10 trở lên (**khuyến nghị Python 3.11**)
- Git
- Visual Studio Code (khuyến nghị)
- Tài khoản GitHub có quyền truy cập repository

Kiểm tra phiên bản đã cài:

```powershell
python --version
git --version
```

## 4. Cài đặt nhanh

Dành cho thành viên đã có sẵn Python và Git:

```powershell
git clone https://github.com/nhitg102/realtime-screen-translator.git
cd realtime-screen-translator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
```

Nếu gặp lỗi ở bước nào, xem phần chi tiết bên dưới.

## 5. Hướng dẫn cài đặt chi tiết

### 5.1. Cài Python 3.11

Cách nhanh bằng `winget`:

```powershell
winget install Python.Python.3.11
winget list Python
```

Kiểm tra phiên bản bằng Python Launcher:

```powershell
py --version
py -3.11 --version
```

> Có thể tải trực tiếp tại [python.org](https://www.python.org/downloads/). Khi cài, nhớ tick **Add python.exe to PATH**.

### 5.2. Clone project

```powershell
git clone https://github.com/nhitg102/realtime-screen-translator.git
cd realtime-screen-translator
```

Nếu đã có project trên máy:

```powershell
cd C:\Users\<TenNguoiDung>\realtime-screen-translator
```

### 5.3. Tạo và kích hoạt môi trường ảo

Tạo môi trường ảo bằng Python 3.11:

```powershell
py -3.11 -m venv .venv
```

Kích hoạt trên **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn chạy script, chọn một trong hai cách:

```powershell
# Cách 1: cho phép script trong phiên PowerShell hiện tại
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

```cmd
:: Cách 2: dùng Command Prompt
.venv\Scripts\activate.bat
```

Khi kích hoạt thành công, đầu dòng lệnh sẽ hiển thị `(.venv)`.

Kiểm tra Python trong môi trường ảo:

```powershell
python --version
```

### 5.4. Nâng cấp pip

```powershell
python -m pip install --upgrade pip
python -m pip --version
```

### 5.5. Cài đặt thư viện của dự án

```powershell
python -m pip install -r requirements.txt
```

## 6. Cài đặt PySide6

> Thực hiện **sau khi đã kích hoạt môi trường ảo** `(.venv)`.

**Bước 1.** Cài PySide6:

```powershell
python -m pip install PySide6
```

**Bước 2.** Kiểm tra cài đặt:

```powershell
python -c "import PySide6; print(PySide6.__version__)"
```

Nếu in ra số phiên bản (ví dụ `6.x.x`) là cài thành công.

**Bước 3.** Lưu thư viện vào `requirements.txt` để cả nhóm dùng chung:

```powershell
python -m pip freeze > requirements.txt
```

**Bước 4.** Các thành viên khác cài lại toàn bộ thư viện của dự án bằng:

```powershell
python -m pip install -r requirements.txt
```

**Bước 5.** Commit `requirements.txt` lên Git:

```powershell
git add requirements.txt
git commit -m "chore: add PySide6 to requirements"
git push
```

> **Lưu ý:** Luôn dùng `python -m pip` (thay vì `pip`) để chắc chắn thư viện được cài vào đúng môi trường ảo đang kích hoạt.

### Kiểm tra nhanh PySide6 hoạt động

Tạo file `test_pyside.py` và chạy thử:

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("PySide6 hoạt động!")
label.resize(300, 100)
label.show()
sys.exit(app.exec())
```

```powershell
python test_pyside.py
```

Nếu cửa sổ nhỏ hiện ra là môi trường đã sẵn sàng.

## 7. Cấu hình biến môi trường

Tạo file `.env` ở thư mục gốc để lưu cấu hình riêng trên máy:

```env
# Điền sau khi nhóm thống nhất dịch vụ API
TRANSLATION_API_KEY=
```

Quy tắc:

- **Không** commit `.env` hoặc API key lên GitHub.
- Tạo `.env.example` chỉ chứa tên biến và giá trị mẫu không nhạy cảm để chia sẻ cấu trúc.
- Thành viên mới sao chép `.env.example` thành `.env` rồi tự điền thông tin được cấp.

```powershell
copy .env.example .env
```

Kiểm tra `.gitignore` có các dòng sau:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
.env.*
!.env.example
.pytest_cache/
.vscode/
```

## 8. Chạy dự án

Sau khi cài thư viện và cấu hình môi trường:

```powershell
python src/main.py
```

> Nếu nhóm dùng entry point khác, cập nhật lệnh chạy tại đây.

## 9. Cấu trúc thư mục

> Cấu trúc dưới đây là gợi ý, cập nhật theo thực tế của dự án.

```text
realtime-screen-translator/
├── src/
│   ├── main.py            # Entry point
│   ├── ui/                # Giao diện PySide6
│   ├── services/          # Xử lý dịch thuật, gọi API
│   └── utils/             # Hàm tiện ích
├── tests/                 # Test
├── .env.example           # Mẫu biến môi trường
├── .gitignore
├── requirements.txt       # Danh sách thư viện
└── README.md
```

## 10. Quy trình làm việc với Git

Repository sử dụng hai nhánh chính:

| Nhánh | Vai trò |
|---|---|
| `main` | Phiên bản ổn định, chỉ cập nhật qua Pull Request |
| `develop` | Nhánh tích hợp các chức năng đang phát triển |

Mỗi công việc làm trên **nhánh riêng tạo từ `develop`**. Không phát triển trực tiếp trên `main`.

### 10.1. Cập nhật `develop` trước khi làm

```powershell
git switch develop
git pull origin develop
```

### 10.2. Tạo nhánh chức năng

```powershell
git switch -c feature/ten-chuc-nang
```

Ví dụ: `git switch -c feature/translation-engine`

| Tiền tố | Mục đích |
|---|---|
| `feature/...` | Phát triển chức năng mới |
| `fix/...` | Sửa lỗi |
| `docs/...` | Cập nhật tài liệu |
| `refactor/...` | Chỉnh sửa cấu trúc code |

### 10.3. Kiểm tra và commit

```powershell
git status
git add .
git commit -m "feat: add translation engine"
```

Quy ước commit message:

| Loại | Ví dụ |
|---|---|
| `feat` | `feat: add text translation` |
| `fix` | `fix: handle translation api errors` |
| `docs` | `docs: update setup guide` |
| `test` | `test: add translation test cases` |
| `refactor` | `refactor: split ui and service layers` |
| `chore` | `chore: add PySide6 to requirements` |

> Trước khi `git add .`, chạy `git status` để chắc chắn không đưa `.env`, `.venv` hoặc file không liên quan vào commit.

### 10.4. Push nhánh lên GitHub

```powershell
# Lần đầu
git push -u origin feature/ten-chuc-nang

# Các lần sau
git push
```

### 10.5. Tạo Pull Request và merge vào `develop`

1. Mở repository trên GitHub.
2. Chọn **Compare & pull request** (hoặc **Pull requests → New pull request**).
3. Chọn **base:** `develop` và **compare:** nhánh chức năng của bạn.
4. Viết tiêu đề và mô tả ngắn về thay đổi.
5. Tạo Pull Request.
6. Thành viên khác review, góp ý và yêu cầu chỉnh sửa nếu cần.
7. Khi đã thống nhất, chọn **Merge pull request**.
8. Sau khi merge, có thể xóa nhánh chức năng trên GitHub.

Không merge nhánh chức năng trực tiếp vào `main`, trừ khi nhóm đã thống nhất phát hành.

### 10.6. Cập nhật máy sau khi merge

```powershell
git switch develop
git pull origin develop
git branch -d feature/ten-chuc-nang
```

### 10.7. Sơ đồ quy trình

```text
develop
   │
   └── feature/ten-chuc-nang
          ├── chỉnh sửa code
          ├── git add + git commit
          ├── git push
          └── Pull Request → develop
                 ├── review
                 └── merge
                        └── mọi người git pull origin develop
```

### 10.8. Lưu ý cho nhóm

- Luôn cập nhật `develop` trước khi bắt đầu công việc mới.
- Mỗi người làm trên nhánh riêng.
- Không push trực tiếp lên `main`.
- Không commit `.env`, API key, mật khẩu hoặc dữ liệu cá nhân.
- Khi có merge conflict, kiểm tra và xử lý từng file, không ghi đè toàn bộ một cách máy móc.
- Sau khi cài thêm thư viện mới, nhớ cập nhật `requirements.txt` và thông báo cho nhóm.

## 11. Xử lý sự cố thường gặp

| Sự cố | Cách xử lý |
|---|---|
| PowerShell báo lỗi *running scripts is disabled* | Chạy `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` rồi kích hoạt lại, hoặc dùng `activate.bat` trong CMD |
| `python` không được nhận diện | Dùng `py` thay thế hoặc cài lại Python và tick **Add to PATH** |
| `ModuleNotFoundError: No module named 'PySide6'` | Kiểm tra đã kích hoạt `(.venv)` chưa, rồi chạy `python -m pip install PySide6` |
| Cài thư viện vào sai môi trường | Luôn dùng `python -m pip ...` khi đã kích hoạt `.venv` |
| Không import được PySide6 sau khi cài | Kiểm tra Python 64-bit và phiên bản Python tương thích; khuyến nghị dùng Python 3.11 |

Khi cần hỗ trợ, gửi cho nhóm:

- Lệnh đã chạy
- Thông báo lỗi đầy đủ trong Terminal
- Nhánh đang dùng (`git branch --show-current`)
- Kết quả `git status`

## 12. Thành viên nhóm

| Họ tên | Vai trò | GitHub |
|---|---|---|
| ... | ... | [@username](https://github.com/username) |

---

> **Ghi chú:** Các lệnh chạy ứng dụng, thư viện và biến môi trường cần được cập nhật khi nhóm chốt cấu trúc code và dịch vụ API thực tế.
