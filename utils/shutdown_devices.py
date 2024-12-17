from utils import run_adb_command, ADB_PATH


def shutdown_devices(online_device, paths=None):
    for device_id in online_device:
        print(f'Shutdown device: {device_id}')
        run_adb_command(f'{ADB_PATH} -s {device_id} shell reboot -p')

    print('Shutdown devices DONE!')
