from scripts import run_adb_command, adb_path

test_run = True


def check_devices():
    try:
        # Получение списка всех подключенных устройств
        result = run_adb_command(f'{adb_path} devices')

        # Парсинг вывода для извлечения идентификаторов устройств и их статусов
        sideload_device = []
        online_device = []
        other_device = []

        lines = result.splitlines()
        for line in lines:
            line = line.strip()

            if line and line != 'List of devices attached':
                parts = line.split()
                device_id = parts[0]
                device_status = parts[1] if len(parts) > 1 else ''

                if device_status == 'sideload':
                    sideload_device.append(device_id)

                elif device_status == 'device':
                    online_device.append(device_id)

                else:
                    other_device.append(device_id)

        if test_run:
            add_all_test_devics(sideload_device, online_device, other_device)

        output = {
            'sideload_device': sideload_device,
            'online_device': online_device,
            'other_device': other_device
        }

        print(output)
        return output

    except Exception as err:
        print(f'CHECK ERROR! => {err}')


def add_test_divaces(list_divace, test_list_divace):
    for device in test_list_divace:
        list_divace.append(device)


def add_all_test_devics(sideload_device, online_device, other_device):
    test_list_sideload_device = [
        'sideload_device_1',
        'sideload_device_2',
        'sideload_device_3',
        'sideload_device_4',
        'sideload_device_5',
        'sideload_device_6',
        'sideload_device_7',
        'sideload_device_8',
        'sideload_device_9',
    ]
    add_test_divaces(sideload_device, test_list_sideload_device)

    test_list_online_device = [
        'online_device_1',
        'online_device_2',
    ]
    add_test_divaces(online_device, test_list_online_device)

    test_list_other_device = [
        'other_device_1',
        'other_device_2',
        'other_device_3',
        'other_device_4',
        'other_device_5',
    ]
    add_test_divaces(other_device, test_list_other_device)
