from concurrent.futures import ThreadPoolExecutor

from scripts import run_adb_command
from scripts.paths import adb_path, CONFIG_FILE, EMPTY_PATH
from utils.utils import read_json_file


def flash_devices(sideload_devices):
    def flash_device(device_id):
        firmware = read_json_file(CONFIG_FILE, EMPTY_PATH)['firmware']

        try:
            print(f'Flashing device {device_id}')
            run_adb_command(f'{adb_path} -s {device_id} sideload {firmware}')

        except Exception as e:
            print(f'Error flash_device {device_id}: {e}')

    try:
        with ThreadPoolExecutor() as executor:
            executor.map(flash_device, sideload_devices)

    except Exception as e:
        print(f'Error flash_devices: {e}')

    print(f'Flash DONE!')
