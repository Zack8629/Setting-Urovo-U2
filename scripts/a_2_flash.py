from concurrent.futures import ThreadPoolExecutor

from scripts import run_adb_command
from scripts.paths import adb_path, zip_path


def flash_devices(sideload_devices):
    def flash_device(device_id):
        try:
            print(f'Flashing device {device_id}')
            run_adb_command(f'{adb_path} -s {device_id} sideload {zip_path}')

        except Exception as e:
            print(f'Error flash_device {device_id}: {e}')

    try:
        with ThreadPoolExecutor() as executor:
            executor.map(flash_device, sideload_devices)

    except Exception as e:
        print(f'Error flash_devices: {e}')

    print(f'Flash DONE!')
