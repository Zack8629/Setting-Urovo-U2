from utils import get_empty_path, get_keys_and_extensions

PATH_TO_OLD_DEFAULT_SETTINGS = {
    'launcher': f'old settings u2/apk/RSLauncher3_105.apk',
    'voiceman': f'old settings u2/apk/voiceman_2.23.21_rlm.apk',
    'button_settings': f'old settings u2/files to import/keys_config.txt',
    'launcher_settings': f'old settings u2/files to import/settings.zip',
    'wallpaper': f'old settings u2/files to import/wallpaperUrovo.png',
}

DEFAULT_KEYS_AND_EXTENSIONS_OLD_SETTINGS = get_keys_and_extensions(PATH_TO_OLD_DEFAULT_SETTINGS)
EMPTY_PATH_OLD_SETTINGS = get_empty_path(PATH_TO_OLD_DEFAULT_SETTINGS)
