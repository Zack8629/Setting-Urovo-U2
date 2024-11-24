import os

from PyQt5.QtWidgets import QMessageBox

from scripts.paths import CONFIG_FILE, EMPTY_PATH, DEFAULT_KEYS_AND_EXTENSIONS
from utils.utils import read_json_file


def validate_file_from_config(key: str, window=None) -> bool:
    """
    Проверяет файл из конфигурации на наличие и корректное расширение.

    :param key: Ключ файла в конфигурации.
    :param window: Ссылка на окно для отображения сообщений (если требуется).
    :return: True, если файл существует и имеет правильное расширение, иначе False.
    """
    # Чтение конфигурации
    expected_extension = DEFAULT_KEYS_AND_EXTENSIONS[key]
    paths = read_json_file(CONFIG_FILE, EMPTY_PATH)
    file_path = paths.get(key, '')

    if key not in DEFAULT_KEYS_AND_EXTENSIONS:
        show_error(f'Ключ "{key}" отсутствует в конфигурации.', window)
        return False

    if not file_path:
        show_error(f'Файл с ключом "{key}" не указан в конфигурации.', window)
        return False

    if not os.path.isfile(file_path):
        show_error(f'Файл "{file_path}" не найден.', window)
        return False

    if not file_path.endswith(expected_extension):
        show_error(f'Файл "{file_path}" имеет неправильное расширение. Ожидается "{expected_extension}".', window)
        return False

    return True


def show_error(message: str, window=None):
    """
    Отображает сообщение об ошибке в QMessageBox.

    :param message: Текст сообщения.
    :param window: Ссылка на окно для модальности.
    """
    msg = QMessageBox(window)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle('Ошибка проверки файла')
    msg.setText(message)
    msg.exec_()
