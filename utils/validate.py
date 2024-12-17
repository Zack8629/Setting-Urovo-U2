import os

from PyQt5.QtWidgets import QMessageBox

from utils import get_keys_and_extensions, test_run


def validate_file_from_config(dict_of_path, window):
    """
    Проверяет конфигурацию и возвращает True, если все проверки пройдены.
    Иначе возвращает False и отображает соответствующую ошибку.
    """
    try:
        for key, expected_extension in get_keys_and_extensions(dict_of_path).items():
            if key not in dict_of_path:
                msg = f'Ключ "{key}" отсутствует в конфигурации.'
                print(f'{msg}')
                show_error(msg, window)
                return False

            file_path = dict_of_path[key]
            if not file_path:
                msg = f'Файл с ключом "{key}" не указан в конфигурации.'
                print(f'{msg}')
                show_error(msg, window)
                return False

            if not os.path.isfile(file_path):
                msg = f'Файл "{file_path}" не найден.'
                print(f'{msg}')
                show_error(msg, window)
                return False

            if not file_path.endswith(expected_extension):
                msg = f'Файл "{file_path}" имеет неправильное расширение. Ожидается "{expected_extension}".'
                print(f'{msg}')
                show_error(msg, window)
                return False

        if test_run:
            show_error('Все проверки прошли успешно!')
            return True
        else:
            return True

    except Exception as e:
        msg = f'Ошибка проверки конфигурации: {e}'
        print(f'{msg}')
        show_error(msg, window)
        return False


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
