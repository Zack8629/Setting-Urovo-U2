from utils.utils import resource_path

settings_U2 = False

CONFIG_FILE = 'specified_files.txt'

BASE_PATH = 'settings_U2/' if settings_U2 else ''

DEFAULT_PATHS = {
    'firmware': f'{BASE_PATH}Firmware/SQ46M_EN_YDE_WE__SS__R01_U_231225_01_rel.zip',
    'launcher': f'{BASE_PATH}APK/RSLauncher3_105.apk',
    'voiceman': f'{BASE_PATH}APK/voiceman_2.23.21_rlm.apk',
    'button_settings': f'{BASE_PATH}Files_to_import/keys_config.txt',
    'launcher_settings': f'{BASE_PATH}Files_to_import/settings.zip',
    'wallpaper': f'{BASE_PATH}Files_to_import/Wallpaper_Urovo.png',
}

DEFAULT_KEYS_AND_EXTENSIONS = {
    key: value.split('.')[-1] if '.' in value else '*' for key, value in DEFAULT_PATHS.items()
}

EMPTY_PATH = {key: '' for key in DEFAULT_PATHS}

# Корень устройства
root_path = '/storage/emulated/0/'

# Путь к adb.exe
adb_path = resource_path('adb/adb.exe')

# Путь до текстовых файлов
TEXT_FILES = {
    'instruction': 'texts/instruction.txt',
    'step_config': 'texts/step_config.txt',
    'about': 'texts/about.txt',
}
