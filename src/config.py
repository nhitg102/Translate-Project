import os
from pathlib import Path
from dotenv import load_dotenv


# Xác định thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# Đọc file .env tại thư mục gốc
load_dotenv(BASE_DIR / ".env")


# Lấy các giá trị cấu hình
APP_NAME = os.getenv("APP_NAME", "RealtimeScreenTranslator")
APP_ENV = os.getenv("APP_ENV", "development")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"