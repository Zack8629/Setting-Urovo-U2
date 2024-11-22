from utils.utils import resource_path

CONFIG_FILE = 'specified_files.txt'

DEFAULT_PATHS = {
    'firmware': 'Firmware/SQ46M_EN_YDE_WE__SS__R01_U_231225_01_rel.zip',
    'launcher': 'APK/RSLauncher3_105.apk',
    'voiceman': 'APK/voiceman_2.23.21_rlm.apk',
    'button_settings': 'Files_to_import/keys_config.txt',
    'launcher_settings': 'Files_to_import/settings.zip',
    'wallpaper': 'Files_to_import/Wallpaper_Urovo.png'
}


def get_empty_paths(path):
    empty_paths = {key: '' for key in path}
    return empty_paths


# Корень устройства
root_path = '/storage/emulated/0/'

# Путь к adb.exe
adb_path = resource_path('adb/adb.exe')

# Путь к прошивке
# zip_path = 'C:/ADB/Settings_U2/Firmware/SQ46M_EN_YDE_WE__SS__R01_U_231225_01_rel.zip'
zip_path = DEFAULT_PATHS['firmware']

# Путь до APK которые надо устанавливать
# launcher_apk_path = 'C:/ADB/Settings_U2/APK/RSLauncher3_105.apk'
launcher_apk_path = DEFAULT_PATHS['launcher']

# voiceman_apk_path = 'C:/ADB/Settings_U2/APK/voiceman_2.23.21_rlm.apk'
voiceman_apk_path = DEFAULT_PATHS['voiceman']

# Путь до файлов которые надо копировать
# keys_config_path = 'C:/ADB/Settings_U2/Files_to_import/keys_config.txt'
keys_config_path = DEFAULT_PATHS['button_settings']

# settings_zip_path = 'C:/ADB/Settings_U2/Files_to_import/settings.zip'
settings_zip_path = DEFAULT_PATHS['launcher_settings']

# wallpaper_path = 'C:/ADB/Settings_U2/Files_to_import/Wallpaper_Urovo.png'
wallpaper_path = DEFAULT_PATHS['wallpaper']

instruction_text = 'texts/instruction.txt'
step_config_text = 'texts/step_config.txt'
about_text = 'texts/about.txt'
