import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import run_adb_command, run_configuration_for_devices, ADB_PATH
from utils.global_path import DEVICE_ROOT_PATH


def install_apk(device_id, apk):
    run_adb_command(f'{ADB_PATH} -s {device_id} install "{apk}"')


def copy_file(device_id, file, path):
    run_adb_command(f'{ADB_PATH} -s {device_id} push "{file}" {path}')


def shell_command(device_id, command):
    run_adb_command(f'{ADB_PATH} -s {device_id} shell {command}')


def run_in_parallel(commands):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(command) for command in commands]
        for future in as_completed(futures):
            future.result()


def settings(device_id, paths):
    command = f'{ADB_PATH} -s {device_id} shell settings put secure ui_night_mode 2'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell settings put system screen_brightness 60'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell settings put system screen_off_timeout 120000'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell locksettings set-disabled true'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} push "{paths['wallpaper']}" "{DEVICE_ROOT_PATH}/Pictures/wallpaperUrovo.png"'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} push "{paths['keys_config']}" "{DEVICE_ROOT_PATH}"'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} push "{paths['settings_property']}" "{DEVICE_ROOT_PATH}/Custom_Local/settings_property.json"'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} shell am start -n com.ubx.keyremap/.component.RemapResultActivity'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} shell input tap 440 88'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell input tap 440 88'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} install "{paths['voiceman_apk']}"'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} shell input keyevent KEYCODE_BACK'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell input keyevent KEYCODE_BACK'
    run_adb_command(command)

    command = f'{ADB_PATH} -s {device_id} shell input tap 530 320'
    run_adb_command(command)
    command = f'{ADB_PATH} -s {device_id} shell input tap 50 430'
    run_adb_command(command)


def start_new_configuration(online_devices, paths):
    time_start = time.time()
    run_configuration_for_devices(online_devices, settings, paths)
    time_end = time.time()
    print(f'Time spent on configuration = {time_end - time_start}')
    print('All Configure DONE!')
