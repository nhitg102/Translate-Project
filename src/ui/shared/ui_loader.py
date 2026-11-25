from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

UI_DIR = Path(__file__).resolve().parent.parent / "forms"

def load_ui(filename, parent=None):
    file_path = UI_DIR / filename

    if not file_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy UI: {file_path}")

    ui_file = QFile(str(file_path))

    if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
        raise RuntimeError(f"Không thể mở UI: {file_path}")

    loader = QUiLoader()

    try:
        widget = loader.load(ui_file, parent)
    finally:
        ui_file.close()

    if widget is None:
        raise RuntimeError(
            f"Không thể nạp UI: {loader.errorString()}"
        )

    return widget
