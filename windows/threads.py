import time

from PyQt5.QtCore import QThread, pyqtSignal


class DeviceThread(QThread):
    finished = pyqtSignal()
    result_ready = pyqtSignal(dict)

    def __init__(self, main_window, func, devices=None, paths=None):
        super().__init__()
        self.main_window = main_window
        self.func = func
        self.devices = devices
        self.paths = paths

    def run(self):
        try:
            if self.devices:
                result = self.func(self.devices, self.paths)
            else:
                result = self.func()

            self.finished.emit()

            if isinstance(result, dict):
                self.result_ready.emit(result)

        except Exception as err:
            print(f'FAIL RUN => {err}')

    def start_execution(self, buttons_to_disable, check_shutdown=False):
        buttons_to_disable = list(set(buttons_to_disable))
        for button in buttons_to_disable:
            button.setEnabled(False)

        self.finished.connect(lambda: self.on_finished(buttons_to_disable, check_shutdown))
        self.result_ready.connect(self.main_window.update_text_fields)
        self.start()

    def on_finished(self, buttons_to_enable, check_shutdown):
        try:
            for button in buttons_to_enable:
                button.setEnabled(True)
        except Exception as e:
            print(f'Fail button.setEnabled(True) => {e}')

        try:
            if check_shutdown and self.main_window.checkbox_shutdown_menu.isChecked():
                time.sleep(5)
                self.main_window.shutdown_devices()
        except Exception as e:
            print(f'FAIL check_shutdown => {e}')
