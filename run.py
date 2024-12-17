import sys
import traceback

from PyQt5.QtWidgets import QApplication

from utils.working_with_files import ensure_config_file_exists
from windows.main_window import MainWindow

if __name__ == '__main__':
    try:
        ensure_config_file_exists()

        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
    except Exception as e:
        print(f'Необработанная ошибка: {e}')
        traceback.print_exc()
        sys.exit(1)
