import os
import time

from scripts import get_version

version = get_version()

name_exe = f'Flash and Settings U2 {version}'

# Команда для PyInstaller
command = (
    f'pyinstaller --onefile '
    f'--icon=icons/main.ico '
    f'--name="{name_exe}" '
    f'--add-data "adb;adb" '
    f'--add-data "icons;icons" '
    f'--add-data "texts;texts" '
    'run.py'
)


def del_spec_file(name_spec_file):
    name_spec_file = f'{name_spec_file}.spec'
    if os.path.exists(name_spec_file):
        os.remove(name_spec_file)


if __name__ == '__main__':
    os.system(command)

    time.sleep(1)
    del_spec_file(name_exe)

    print('Build exe file done!')
