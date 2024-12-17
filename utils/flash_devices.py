from concurrent.futures import ThreadPoolExecutor

from utils import run_adb_command
from utils.global_path import ADB_PATH


def flash_devices(sideload_devices, path):
    def flash_device(device_id):
        try:
            print(f'Flashing device {device_id}')
            run_adb_command(f'{ADB_PATH} -s {device_id} sideload "{path['firmware']}"')

        except Exception as e:
            print(f'Error flash_device {device_id}: {e}')

    try:
        with ThreadPoolExecutor() as executor:
            executor.map(flash_device, sideload_devices)

    except Exception as e:
        print(f'Error flash_devices: {e}')

    print(f'Flash DONE!')
