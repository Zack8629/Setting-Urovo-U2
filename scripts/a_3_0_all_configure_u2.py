from concurrent.futures import ThreadPoolExecutor, as_completed

from scripts import run_adb_command, adb_path, launcher_apk_path, voiceman_apk_path, \
    root_path, wallpaper_path, keys_config_path, settings_zip_path, invoke_tap, press_home, invoke_swipe, \
    run_configuration_for_devices


def install_apk(device_id, apk):
    run_adb_command(f'{adb_path} -s {device_id} install "{apk}"')


def copy_file(device_id, file, path):
    run_adb_command(f'{adb_path} -s {device_id} push "{file}" {path}')


def shell_command(device_id, command):
    run_adb_command(f'{adb_path} -s {device_id} shell {command}')


def run_in_parallel(commands):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(command) for command in commands]
        for future in as_completed(futures):
            future.result()


def settings_1(device_id):
    commands = [
        lambda: install_apk(device_id, launcher_apk_path),
        lambda: install_apk(device_id, voiceman_apk_path),
        lambda: copy_file(device_id, wallpaper_path, f'{root_path}/Download'),
        lambda: copy_file(device_id, keys_config_path, root_path),
        lambda: copy_file(device_id, settings_zip_path, root_path),
        lambda: shell_command(device_id, 'settings put secure ui_night_mode 2'),
        lambda: shell_command(device_id, 'settings put system status_bar_show_battery_percent 1'),
        lambda: shell_command(device_id, 'settings put system screen_brightness 60'),
        lambda: shell_command(device_id, 'settings put system screen_off_timeout 120000'),
        lambda: shell_command(device_id, 'pm disable-user --user 0 com.google.android.googlequicksearchbox'),
        lambda: shell_command(device_id, 'locksettings set-disabled true'),
        lambda: invoke_tap(device_id, x=530, y=320, pre_delay=900, post_delay=900)
    ]

    run_in_parallel(commands)


def settings_2(device_id):
    # НАЖАТИЕ 'ПРОПУСТИТЬ'
    invoke_tap(device_id, x=50, y=430, pre_delay=900, post_delay=900)

    # ВЫБОР ПРИЛОЖЕНИЯ
    invoke_tap(device_id, x=300, y=350, pre_delay=900, post_delay=900)

    # НАЖАТИЕ 'ВСЕГДА'
    invoke_tap(device_id, x=600, y=425, pre_delay=900, post_delay=900)

    # НАЖАТИЕ 'CONFIRM'
    invoke_tap(device_id, x=760, y=450, pre_delay=900, post_delay=900)


def settings_3(device_id):
    # УСТАНОВКА ОБОЕВ
    command = (
        f'{adb_path} -s {device_id} shell am start -a android.intent.action.ATTACH_DATA '
        f'-d file://{root_path}/Download/Wallpaper_Urovo.png -t image/png '
        f'-e mimeType image/png --grant-read-uri-permission'
    )
    run_adb_command(command)

    # ВЫБОР ПРИЛОЖЕНИЯ
    invoke_tap(device_id, x=400, y=264, pre_delay=800, post_delay=800)

    # НАЖАТИЕ 'ТОЛЬКО В ЭТОТ РАЗ'
    invoke_tap(device_id, x=485, y=420, pre_delay=800, post_delay=800)

    # НАЖАТИЕ 'УСТАНОВИТЬ ОБОИ'
    invoke_tap(device_id, x=100, y=40, pre_delay=800, post_delay=800)

    # НАЖАТИЕ 'УСТАНОВИТЬ ОБОИ'
    invoke_tap(device_id, x=400, y=340, pre_delay=800, post_delay=800)


def settings_4(device_id):
    # ЗАПУСК RemapResultActivity
    command = f'{adb_path} -s {device_id} shell am start -n com.ubx.keyremap/.component.RemapResultActivity'
    run_adb_command(command)

    # ВЫПОЛНЕНИЕ ИМПОРТА
    invoke_tap(device_id, x=440, y=88, pre_delay=300, post_delay=300)
    invoke_tap(device_id, x=440, y=88, pre_delay=300, post_delay=300)

    # НАЖАТИЕ КНОПКИ 'ДОМОЙ'
    press_home(device_id, pre_delay=1234, post_delay=0)


def settings_5(device_id):
    # НАЖАТИЕ НА МЕНЮ
    invoke_tap(device_id, x=733, y=250, pre_delay=400, post_delay=400)

    # ОТКРЫТИЕ ПОЛЯ ДЛЯ ВВОДА ПАРОЛЯ
    invoke_tap(device_id, x=300, y=244, pre_delay=400, post_delay=400)
    invoke_tap(device_id, x=300, y=244, pre_delay=400, post_delay=400)

    # УДАЛЕНИЕ ПЕРВОГО СИМВОЛА
    invoke_tap(device_id, x=740, y=409, pre_delay=200, post_delay=100)

    # СМЕНА ЯЗЫКА
    invoke_tap(device_id, x=242, y=453, pre_delay=200, post_delay=200)

    # ВВОД ПАРОЛЯ 'a', 'd', 'm', 'i', 'n'
    password_coordinates = [
        {'X': 95, 'Y': 355},  # 'a'
        {'X': 250, 'Y': 355},  # 'd'
        {'X': 636, 'Y': 404},  # 'm'
        {'X': 600, 'Y': 305},  # 'i'
        {'X': 569, 'Y': 395}  # 'n'
    ]
    for coord in password_coordinates:
        invoke_tap(device_id, coord['X'], coord['Y'], pre_delay=100, post_delay=100)

    # НАЖАТИЕ 'ГОТОВО'
    invoke_tap(device_id, x=730, y=140, pre_delay=200, post_delay=500)

    # НАЖАТИЕ 'ОК'
    invoke_tap(device_id, x=525, y=380, pre_delay=500, post_delay=500)

    # НАЖАТИЕ 'НАСТРОЙКИ'
    invoke_tap(device_id, x=150, y=80, pre_delay=900, post_delay=900)

    # НАЖАТИЕ 'ИМПОРТ'
    invoke_tap(device_id, x=400, y=472, pre_delay=500, post_delay=500)

    # ВЫПОЛЕНИЕ СВАЙПА
    invoke_swipe(device_id, 400, 300, 400, 30, duration=50, pre_delay=500, post_delay=500)

    # НАЖАТИЕ 'settings.zip'
    invoke_tap(device_id, x=400, y=282, pre_delay=500, post_delay=500)

    # НАЖАТИЕ 'ОК'
    invoke_tap(device_id, x=590, y=430, pre_delay=500, post_delay=500)

    # НАЖАТИЕ КНОПКИ 'ДОМОЙ'
    press_home(device_id, pre_delay=500, post_delay=0)

    # НАЖАТИЕ 'APK VOICEMAN'
    invoke_tap(device_id, x=784, y=90, pre_delay=900, post_delay=900)

    # НАЖАТИЕ 'CONFIRM'
    invoke_tap(device_id, x=755, y=460, pre_delay=900, post_delay=900)


def settings_6(online_device):
    for device_id in online_device:
        print(f'Shutdown device {device_id}')
        run_adb_command(f'{adb_path} -s {device_id} shell reboot -p')


def start_all_config(online_devices):
    configs = [settings_1, settings_2, settings_3, settings_4, settings_5]
    run_configuration_for_devices(online_devices, configs)
    print('All Configure DONE!')
