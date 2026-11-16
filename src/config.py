import os
from pathlib import Path
from dotenv import load_dotenv


# Xác định thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# Đọc file .env tại thư mục gốc
load_dotenv(BASE_DIR / ".env")


# ==============================
# CẤU HÌNH ỨNG DỤNG
# ==============================

APP_NAME = os.getenv("APP_NAME", "RealtimeScreenTranslator")
APP_ENV = os.getenv("APP_ENV", "development")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# ==============================
# CẤU HÌNH DỊCH THUẬT
# ==============================

TRANSLATION_PROVIDER = os.getenv(
    "TRANSLATION_PROVIDER", "microsoft"
)

SOURCE_LANGUAGE = os.getenv("SOURCE_LANGUAGE", "en")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "vi")


# ==============================
# MICROSOFT TRANSLATOR
# ==============================

MICROSOFT_TRANSLATOR_KEY = os.getenv(
    "MICROSOFT_TRANSLATOR_KEY"
)

MICROSOFT_TRANSLATOR_REGION = os.getenv(
    "MICROSOFT_TRANSLATOR_REGION", "eastasia"
)

MICROSOFT_TRANSLATOR_ENDPOINT = os.getenv(
    "MICROSOFT_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com"
)