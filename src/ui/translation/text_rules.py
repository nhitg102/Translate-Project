import re
import unicodedata

# Giới hạn số từ của chế độ dịch văn bản
MAX_WORDS = 1000

# Mẫu nhận diện từ
WORD_PATTERN = re.compile(
    r"[^\W_]+(?:['’][^\W_]+)*",
    re.UNICODE
)

def count_words(text: str) -> int:
    # 1. Chuẩn hóa Unicode
    normalized_text = unicodedata.normalize(
        "NFC",
        text
    )

    # 2. Tìm các đơn vị từ
    words = WORD_PATTERN.findall(normalized_text)

    return len(words)

def contains_letters(text: str) -> bool:
    # Kiểm tra văn bản có chứa chữ cái hay không
    return any(char.isalpha() for char in text)
