import json
import os
import sys


def resource_path(relative_path):
    """Получает путь к файлу в папке, созданной PyInstaller."""
    if getattr(sys, 'frozen', False):  # Если работает как .exe
        base_path = sys._MEIPASS
    else:  # Если работает как скрипт
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_text(file_path):
    try:
        file_path = resource_path(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f'Файл не найден: {file_path}. Проверьте наличие файла.'
    except Exception as e:
        return f'Ошибка при загрузке файла {file_path}: {e}'


def read_json_file(file_path, default_data=None):
    """
    Читает JSON файл. Если файл отсутствует или возникает ошибка, возвращает default_data.

    :param file_path: Путь к JSON файлу.
    :param default_data: Данные по умолчанию, возвращаемые в случае ошибки.
    :return: Данные из файла или default_data.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f'Ошибка при чтении файла {file_path}: {e}')
    return default_data.copy() if default_data else {}


def write_json_file(file_path, data):
    """
    Сохраняет данные в JSON файл.

    :param file_path: Путь к JSON файлу.
    :param data: Данные для записи.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Ошибка при записи файла {file_path}: {e}')


def ensure_config_file_exists(config_files, default_paths):
    """
    Проверяет наличие файла конфигурации и создаёт его с данными по умолчанию, если файла нет.
    """
    if not os.path.exists(config_files):
        write_json_file(config_files, default_paths)
        print(f'Создан файл {config_files} ')
