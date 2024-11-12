import subprocess
import time

from concurrent.futures import ThreadPoolExecutor, as_completed


def get_version():
    return 'v0.8.3.12'


# Полный путь к adb.exe
# adb_path = 'C:\\ADB\\adb.exe'
adb_path = '/ADB\\adb.exe'

# Корень устройства
root_path = '/storage/emulated/0/'

# Путь к прошивке
zip_path = 'C:\\ADB\\Settings_U2\\Firmware\\SQ46M_EN_YDE_WE__SS__R01_U_231225_01_rel.zip'

# Путь до APK которые надо устанавливать
launcher_apk_path = 'C:\\ADB\\Settings_U2\\APK\\RSLauncher3_105.apk'
voiceman_apk_path = 'C:\\ADB\\Settings_U2\\APK\\voiceman_2.23.21_rlm.apk'

# Путь до файлов которые надо копировать
keys_config_path = 'C:\\ADB\\Settings_U2\\Files_to_import\\keys_config.txt'
settings_zip_path = 'C:\\ADB\\Settings_U2\\Files_to_import\\settings.zip'
wallpaper_path = 'C:\\ADB\\Settings_U2\\Files_to_import\\Wallpaper_Urovo.png'


def sleep_in_milliseconds(milliseconds):
    time.sleep(milliseconds / 1000)


def run_adb_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error executing command: {command}')
        print(f'stdout: {result.stdout}')
        print(f'stderr: {result.stderr}')
        print(result.stderr)
    return result.stdout


def invoke_tap(device_id, x, y, pre_delay=500, post_delay=500):
    sleep_in_milliseconds(pre_delay)
    tap_command = f'{adb_path} -s {device_id} shell input tap {x} {y}'
    run_adb_command(tap_command)
    sleep_in_milliseconds(post_delay)


def invoke_swipe(device_id, start_x, start_y, end_x, end_y, duration=50, pre_delay=500, post_delay=500):
    sleep_in_milliseconds(pre_delay)
    swipe_command = f'{adb_path} -s {device_id} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}'
    run_adb_command(swipe_command)
    sleep_in_milliseconds(post_delay)


def press_home(device_id, pre_delay=500, post_delay=500):
    sleep_in_milliseconds(pre_delay)
    home_command = f'{adb_path} -s {device_id} shell input keyevent KEYCODE_HOME'
    run_adb_command(home_command)
    sleep_in_milliseconds(post_delay)


def run_configuration_for_devices(online_devices, config_functions):
    if not callable(config_functions) and not (
            isinstance(config_functions, list) and all(callable(f) for f in config_functions)):
        raise ValueError('config_functions should be either a callable or a list of callables')

    def configure_device(device_id, func):
        print(f'START {func.__name__} for device {device_id}!')
        func(device_id)
        print(f'{func.__name__} for device {device_id} DONE!')

    def execute_function(device_id, func):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(configure_device, device_id, func)
            future.result()

    if callable(config_functions):
        # Single function case
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(execute_function, device_id, config_functions) for device_id in online_devices]
            for future in as_completed(futures):
                future.result()

    elif isinstance(config_functions, list):
        # List of functions case
        for func in config_functions:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(execute_function, device_id, func) for device_id in online_devices]
                for future in as_completed(futures):
                    future.result()
