from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QCheckBox, QProgressBar

from scripts import get_version
from scripts.a_1_check import check_devices
from scripts.a_2_flash import flash_devices
from scripts.a_3_0_all_configure_u2 import start_all_config, settings_6
from .select_file_window import FileDialogWindow
from .settings_step_by_step_window import StepConfigWindow
from .threads import DeviceThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_dialog = None
        self.thread = None
        self.sideload_device = []
        self.online_device = []
        self.other_device = []

        # Основные компоненты интерфейса
        self.main_layout = QVBoxLayout()
        self.columns_layout = QHBoxLayout()

        # Левый столбец - прошивка
        self.left_column_layout = QVBoxLayout()
        self.label_firmware = QLabel('На прошивку: 0')
        self.textedit_firmware = QTextEdit()
        self.progress_bar_firmware = QProgressBar()

        self.button_flash = QPushButton('Прошить')
        self.button_flash.setEnabled(False)

        # Средний столбец - неавторизованные
        self.middle_column_layout = QVBoxLayout()
        self.label_unauthorized = QLabel('Не авторизованных: 0')
        self.textedit_unauthorized = QTextEdit()

        self.button_step_config = QPushButton('Настройка по шагам')
        # self.button_step_config.setEnabled(False)

        self.button_select_files = QPushButton('Указать файлы')
        # self.button_select_files.setEnabled(False)

        # Правый столбец - настройка
        self.right_column_layout = QVBoxLayout()
        self.label_configuration = QLabel('На настройку: 0')
        self.textedit_configuration = QTextEdit()
        self.progress_bar_configuration = QProgressBar()

        self.button_configure = QPushButton('Настроить')
        self.button_configure.setEnabled(False)

        self.checkbox_shutdown = QCheckBox('Выключить после настройки')
        self.button_shutdown = QPushButton('Выключить')
        self.button_shutdown.setEnabled(False)

        # Кнопка 'Проверить' под всеми столбцами
        self.button_check_all = QPushButton('Проверить')

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Прошивка Urovo U2 {get_version()}')

        # Основные компоненты интерфейса
        self.setLayout(self.main_layout)

        self.main_layout.addLayout(self.columns_layout)

        # Левый столбец - прошивка
        self.columns_layout.addLayout(self.left_column_layout)

        self.left_column_layout.addWidget(self.label_firmware)

        self.textedit_firmware.setReadOnly(True)
        self.left_column_layout.addWidget(self.textedit_firmware)

        self.progress_bar_firmware.setValue(0)
        self.progress_bar_firmware.setMinimum(0)
        self.progress_bar_firmware.setMaximum(100)
        self.progress_bar_firmware.setAlignment(Qt.AlignCenter)
        self.left_column_layout.addWidget(self.progress_bar_firmware)

        self.button_flash.clicked.connect(self.flash_devices)
        self.left_column_layout.addWidget(self.button_flash)

        # Средний столбец - неавторизованные
        self.columns_layout.addLayout(self.middle_column_layout)

        self.middle_column_layout.addWidget(self.label_unauthorized)

        self.textedit_unauthorized.setReadOnly(True)
        self.middle_column_layout.addWidget(self.textedit_unauthorized)

        self.button_select_files.clicked.connect(self.show_file_dialog)
        self.middle_column_layout.addWidget(self.button_select_files)

        self.button_step_config.clicked.connect(self.show_step_config)
        self.middle_column_layout.addWidget(self.button_step_config)

        # Правый столбец - настройка
        self.columns_layout.addLayout(self.right_column_layout)

        self.right_column_layout.addWidget(self.label_configuration)

        self.textedit_configuration.setReadOnly(True)
        self.right_column_layout.addWidget(self.textedit_configuration)

        self.progress_bar_configuration.setValue(0)
        self.progress_bar_configuration.setMinimum(0)
        self.progress_bar_configuration.setMaximum(100)
        self.progress_bar_configuration.setAlignment(Qt.AlignCenter)
        self.right_column_layout.addWidget(self.progress_bar_configuration)

        self.button_configure.clicked.connect(self.start_all_config_clicked)
        self.right_column_layout.addWidget(self.button_configure)

        self.right_column_layout.addWidget(self.checkbox_shutdown)

        self.button_shutdown.clicked.connect(self.shutdown_devices)
        self.right_column_layout.addWidget(self.button_shutdown)

        self.button_check_all.clicked.connect(self.check_devices_clicked)
        self.main_layout.addWidget(self.button_check_all)

        # Установка размеров окна
        self.setFixedSize(1000, 500)

        self.show()

        self.show_file_dialog()
        # self.show_step_config()

    def show_file_dialog(self):
        if not self.file_dialog:
            self.file_dialog = FileDialogWindow()
            self.file_dialog.setWindowModality(Qt.ApplicationModal)
        # self.file_dialog.load_saved_paths()
        self.file_dialog.show()

    def show_step_config(self):
        self.step_config_window = StepConfigWindow(self, self.online_device)
        self.step_config_window.setWindowModality(Qt.ApplicationModal)
        self.step_config_window.show()

    @staticmethod
    def update_count(label, buttons=(), count=0, text_template=''):
        label.setText(f'{text_template} {count}')
        if buttons:
            for button in buttons:
                button.setEnabled(count > 0)

    def update_text_fields(self, devices):
        self.sideload_device = devices.get('sideload_device', [])
        self.online_device = devices.get('online_device', [])
        self.other_device = devices.get('other_device', [])

        self.textedit_firmware.setPlainText('\n'.join(self.sideload_device))
        self.textedit_unauthorized.setPlainText('\n'.join(self.other_device))
        self.textedit_configuration.setPlainText('\n'.join(self.online_device))

        self.update_count(label=self.label_firmware, buttons=[self.button_flash],
                          count=len(self.sideload_device), text_template='На прошивку:')

        self.update_count(label=self.label_unauthorized, buttons=(),
                          count=len(self.other_device), text_template='Не авторизованных:')

        self.update_count(label=self.label_configuration,
                          buttons=[self.button_configure, self.button_shutdown, self.button_step_config],
                          count=len(self.online_device), text_template='На настройку:')

    def check_devices_clicked(self):
        try:
            self.thread = DeviceThread(self, check_devices)
            self.thread.start_execution([self.button_check_all])
        except Exception as e:
            print(f'ERR check_devices_clicked => {e}')

    def flash_devices(self):
        self.thread = DeviceThread(self, flash_devices, self.sideload_device)
        buttons_to_disable = [self.button_flash, self.button_check_all, self.button_step_config]
        self.thread.start_execution(buttons_to_disable)

    def start_all_config_clicked(self):
        self.thread = DeviceThread(self, start_all_config, self.online_device)
        buttons_to_disable = [self.button_configure, self.button_shutdown, self.button_check_all,
                              self.button_step_config]
        self.thread.start_execution(buttons_to_disable, check_shutdown=True)

    def shutdown_devices(self):
        self.thread = DeviceThread(self, settings_6, self.online_device)
        buttons_to_disable = [self.button_configure, self.button_shutdown, self.button_step_config]
        self.thread.start_execution(buttons_to_disable)
