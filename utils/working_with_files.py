import json
import os

from new_settings.paths import PATH_TO_NEW_DEFAULT_SETTINGS
from old_settings.paths import PATH_TO_OLD_DEFAULT_SETTINGS
from utils.global_path import resource_path, CONFIG_FILE, DEFAULT_FIRMWARE_PATH


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


def ensure_config_file_exists():
    combined_paths = {
        "firmware": DEFAULT_FIRMWARE_PATH,
        "old_settings": PATH_TO_OLD_DEFAULT_SETTINGS,
        "new_settings": PATH_TO_NEW_DEFAULT_SETTINGS
    }
    """
    Проверяет наличие файла конфигурации и создаёт его с данными по умолчанию, если файла нет.
    """
    if not os.path.exists(CONFIG_FILE):
        write_json_file(CONFIG_FILE, combined_paths)
        print(f'Создан файл {CONFIG_FILE} ')
