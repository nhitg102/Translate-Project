
import sqlite3
import atexit

from pathlib import Path
from contextlib import contextmanager
from threading import local
from typing import Iterator

from src.config import BASE_DIR


DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "translator.db"

# Mỗi thread có trạng thái kết nối riêng
_thread_state = local()


def _create_connection(db_path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(db_path),
        timeout=10
    )

    try:
        connection.row_factory = sqlite3.Row

        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA synchronous = NORMAL")

        return connection

    except Exception:
        connection.close()
        raise


def close_thread_connection():
    """Đóng kết nối được tái sử dụng trong thread hiện tại."""

    connection = getattr(
        _thread_state,
        "connection",
        None
    )

    if connection is not None:
        try:
            connection.close()
        finally:
            _thread_state.connection = None
            _thread_state.db_path = None


def _get_thread_connection(db_path):
    """Lấy hoặc tạo kết nối riêng cho thread hiện tại."""

    db_path = Path(db_path).resolve()

    connection = getattr(
        _thread_state,
        "connection",
        None
    )

    saved_path = getattr(
        _thread_state,
        "db_path",
        None
    )

    if connection is not None and saved_path != db_path:
        close_thread_connection()
        connection = None

    if connection is None:
        connection = _create_connection(db_path)

        _thread_state.connection = connection
        _thread_state.db_path = db_path

    return connection


@contextmanager
def get_connection(db_path=None) -> Iterator[sqlite3.Connection]:

    # Chỉ tái sử dụng kết nối cho database mặc định.
    # Database được truyền đường dẫn riêng vẫn đóng sau khi dùng,
    # giúp các unit test sử dụng TemporaryDirectory an toàn.
    persistent = db_path is None

    if persistent:
        connection = _get_thread_connection(DB_PATH)
    else:
        connection = _create_connection(db_path)

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        if not persistent:
            connection.close()


def initialize_database(db_path=None) -> None:

    with get_connection(db_path) as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")


# Đóng kết nối thread chính khi Python thoát bình thường.
atexit.register(close_thread_connection)
