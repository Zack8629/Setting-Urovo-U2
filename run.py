import sys
import traceback

from PyQt5.QtWidgets import QApplication

from scripts.paths import CONFIG_FILE, DEFAULT_PATHS
from utils.utils import ensure_config_file_exists
from windows.main_window import MainWindow

if __name__ == '__main__':
    try:
        ensure_config_file_exists(CONFIG_FILE, DEFAULT_PATHS)

        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f'Необработанная ошибка: {e}')
        traceback.print_exc()
        sys.exit(1)
