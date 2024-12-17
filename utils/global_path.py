import os
import sys


def resource_path(relative_path):
    """Получает путь к файлу в папке, созданной PyInstaller."""
    if getattr(sys, 'frozen', False):  # Если работает как .exe
        base_path = sys._MEIPASS
    else:  # Если работает как скрипт
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


CONFIG_FILE = 'specified_files.json'

# Корень устройства
DEVICE_ROOT_PATH = '/storage/emulated/0'

# Путь к adb.exe
ADB_PATH = resource_path('adb/adb.exe')

# Путь до текстовых файлов
TEXT_FILES = {
    'instruction': 'texts/instruction.txt',
    'about': 'texts/about.txt',
}

DEFAULT_FIRMWARE_PATH = {
    'firmware': 'firmware.zip',
}
