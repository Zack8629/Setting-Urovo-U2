import inspect
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.global_path import ADB_PATH

test_run = False


def get_version():
    version = 'v0.10.0.24'
    if test_run:
        return f'{version} TEST RUN!'

    return version


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
    tap_command = f'{ADB_PATH} -s {device_id} shell input tap {x} {y}'
    run_adb_command(tap_command)
    sleep_in_milliseconds(post_delay)


def invoke_swipe(device_id, start_x, start_y, end_x, end_y, duration=50, pre_delay=500, post_delay=500):
    sleep_in_milliseconds(pre_delay)
    swipe_command = f'{ADB_PATH} -s {device_id} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}'
    run_adb_command(swipe_command)
    sleep_in_milliseconds(post_delay)


def press_home(device_id, pre_delay=500, post_delay=500):
    sleep_in_milliseconds(pre_delay)
    home_command = f'{ADB_PATH} -s {device_id} shell input keyevent KEYCODE_HOME'
    run_adb_command(home_command)
    sleep_in_milliseconds(post_delay)


def run_configuration_for_devices(online_devices, config_functions, paths):
    """
    Выполняет конфигурацию устройств, поддерживая параллельное выполнение.

    :param online_devices: Список идентификаторов устройств.
    :param config_functions: Список функций конфигурации или одна функция.
    :param paths: Словарь путей для конфигурации.
    """
    if not callable(config_functions) and not (
            isinstance(config_functions, list) and all(callable(f) for f in config_functions)):
        raise ValueError('config_functions should be either a callable or a list of callables')

    def configure_device(device_id, func):
        """Выполняет конфигурацию устройства через переданную функцию."""
        print(f'START {func.__name__} for device {device_id}!')
        # Проверяем, нужен ли аргумент paths
        func_signature = inspect.signature(func)
        if 'paths' in func_signature.parameters:
            func(device_id, paths)
        else:
            func(device_id)
        print(f'{func.__name__} for device {device_id} DONE!')

    def execute_function(device_id, func):
        """Исполняет функцию конфигурации для одного устройства."""
        with ThreadPoolExecutor() as executor:
            future = executor.submit(configure_device, device_id, func)
            future.result()

    if callable(config_functions):
        # Случай с одной функцией
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(execute_function, device_id, config_functions) for device_id in online_devices]
            for future in as_completed(futures):
                future.result()

    elif isinstance(config_functions, list):
        # Случай со списком функций
        for func in config_functions:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(execute_function, device_id, func) for device_id in online_devices]
                for future in as_completed(futures):
                    future.result()


def get_keys_and_extensions(dict_of_path):
    """
    Возвращает словарь, где ключи совпадают с ключами исходного словаря,
    а значения - расширения файлов или '*' при отсутствии расширения.
    """
    return {
        key: value.split('.')[-1] if '.' in value else '*'
        for key, value in dict_of_path.items()
    }


def get_empty_path(dict_of_path):
    """
    Возвращает словарь, где ключи совпадают с ключами исходного словаря,
    а значения - пустые строки.
    """
    return {key: '' for key in dict_of_path}
