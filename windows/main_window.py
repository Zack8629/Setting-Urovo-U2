from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QProgressBar, \
    QMenuBar, QAction, QDialog

from new_settings.configure_u2 import start_new_configuration
from old_settings.configure_u2 import start_all_config
from utils import get_version
from utils.check_devices import check_devices
from utils.flash_devices import flash_devices
from utils.global_path import resource_path, TEXT_FILES, CONFIG_FILE
from utils.shutdown_devices import shutdown_devices
from utils.validate import validate_file_from_config
from utils.working_with_files import load_text, read_json_file
from .file_select_window_new_setting import FileDialogWindowNewSetting
from .file_select_window_old_setting import FileDialogWindowOldSetting
from .select_firmware import SelectFirmware
from .settings_window import SettingsWindow
from .threads import DeviceThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_dialog = None
        self.thread = None
        self.sideload_device = []
        self.other_device = []
        self.online_device = []
        self.buttons_to_disable = []

        # Устанавливаем иконку для окна
        self.setWindowIcon(QIcon(resource_path('icons/main.ico')))

        # Основные компоненты интерфейса
        self.main_layout = QVBoxLayout()
        self.columns_layout = QHBoxLayout()

        # Создание меню
        self.menu_bar = QMenuBar(self)

        self.file_menu = self.menu_bar.addMenu('Файл')
        self.old_setting = self.menu_bar.addMenu('Старая настройка')
        self.help_menu = self.menu_bar.addMenu('Справка')

        # Левый столбец - прошивка
        self.left_column_layout = QVBoxLayout()
        self.label_firmware = QLabel('На прошивку: 0')
        self.textedit_firmware = QTextEdit()
        self.progress_bar_firmware = QProgressBar()

        self.button_select_firmware = QPushButton('Указать файл прошивки')
        self.button_select_firmware.clicked.connect(self.show_select_firmware)

        self.button_flash = QPushButton('Прошить')
        self.button_flash.setEnabled(False)

        # Средний столбец - неавторизованные
        self.middle_column_layout = QVBoxLayout()
        self.label_unauthorized = QLabel('Не авторизованных: 0')
        self.textedit_unauthorized = QTextEdit()

        self.button_select_files_new_setting = QPushButton('Указать файлы новой настройки')

        # Правый столбец - настройка
        self.right_column_layout = QVBoxLayout()
        self.label_configuration = QLabel('На настройку: 0')
        self.textedit_configuration = QTextEdit()
        self.progress_bar_configuration = QProgressBar()

        self.button_configure = QPushButton('Настроить')
        self.button_configure.setEnabled(False)

        self.button_shutdown = QPushButton('Выключить')
        self.button_shutdown.setEnabled(False)

        # Кнопка 'Проверить' под всеми столбцами
        self.button_check_all = QPushButton('Проверить')

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Прошивка Urovo U2 {get_version()}')

        # Добавление меню в главное окно
        self.main_layout.setMenuBar(self.menu_bar)

        # Создание действий для меню 'Файл'
        settings_window = QAction('Настройки программы', self)
        settings_window.triggered.connect(self.show_settings_window)
        settings_window.setEnabled(False)

        self.old_setting_files = QAction('Указать файлы для старой настройки', self)
        self.old_setting_files.triggered.connect(self.show_file_dialog_old_setting)

        self.start_old_configuration_button = QAction('Запустить старую настройку', self)
        self.start_old_configuration_button.triggered.connect(self.start_old_configuration)
        self.start_old_configuration_button.setEnabled(False)

        self.checkbox_shutdown_menu = QAction('Выключить устройства после настройки', self)
        self.checkbox_shutdown_menu.setCheckable(True)
        self.checkbox_shutdown_menu.setChecked(False)

        self.exit_action = QAction('Выход', self)
        self.exit_action.triggered.connect(self.close)

        self.file_menu.addAction(settings_window)
        self.file_menu.addAction(self.checkbox_shutdown_menu)
        self.file_menu.addAction(self.exit_action)

        self.old_setting.addAction(self.old_setting_files)
        self.old_setting.addAction(self.start_old_configuration_button)

        instruction_action = QAction('Инструкция', self)
        instruction_action.triggered.connect(self.show_instruction_dialog)

        # Создание действий для меню 'Справка'
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about_dialog)

        self.help_menu.addAction(instruction_action)
        self.help_menu.addAction(about_action)

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
        self.left_column_layout.addWidget(self.button_select_firmware)
        self.left_column_layout.addWidget(self.button_flash)

        # Средний столбец - неавторизованные
        self.columns_layout.addLayout(self.middle_column_layout)

        self.middle_column_layout.addWidget(self.label_unauthorized)

        self.textedit_unauthorized.setReadOnly(True)
        self.middle_column_layout.addWidget(self.textedit_unauthorized)

        self.button_select_files_new_setting.clicked.connect(self.show_file_dialog_new_setting)
        self.middle_column_layout.addWidget(self.button_select_files_new_setting)

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

        self.button_configure.clicked.connect(self.start_new_configuration)
        self.right_column_layout.addWidget(self.button_configure)

        self.button_shutdown.clicked.connect(self.shutdown_devices)
        self.right_column_layout.addWidget(self.button_shutdown)

        self.button_check_all.clicked.connect(self.check_devices_clicked)
        self.main_layout.addWidget(self.button_check_all)

        self.buttons_to_disable = [self.button_flash, self.button_check_all, self.old_setting_files,
                                   self.button_select_files_new_setting, self.button_configure, self.button_shutdown,
                                   self.button_select_firmware, self.start_old_configuration_button,
                                   self.old_setting_files, self.exit_action]

        # Установка размеров окна
        self.setFixedSize(1000, 600)

        self.check_devices_clicked()
        self.show()

    def show_file_dialog_old_setting(self):
        self.file_dialog = FileDialogWindowOldSetting()
        self.file_dialog.setWindowModality(Qt.ApplicationModal)
        self.file_dialog.show()

    def show_file_dialog_new_setting(self):
        self.file_dialog = FileDialogWindowNewSetting()
        self.file_dialog.setWindowModality(Qt.ApplicationModal)
        self.file_dialog.show()

    def show_select_firmware(self):
        try:
            self.file_dialog = SelectFirmware()
            self.file_dialog.setWindowModality(Qt.ApplicationModal)
            self.file_dialog.show()
        except Exception as e:
            print(f'ERR show_select_firmware => {e}')

    def create_text_dialog(self, title, text, size=(800, 400), font_size=12):
        """
          Создаёт диалоговое окно с текстом.

          :param title: Заголовок окна.
          :param text: Отображаемый текст.
          :param size: Размер окна (ширина, высота).
          :param font_size: Размер шрифта текста.
          """
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(*size)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)
        layout.addWidget(text_edit)

        # Настройка шрифта
        font = QFont()
        font.setPointSize(font_size)  # Установка размера шрифта
        text_edit.setFont(font)

        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        return dialog

    def show_instruction_dialog(self):
        size_window = (1234, 800)
        text = load_text(TEXT_FILES['instruction'])
        self.create_text_dialog('Инструкция', text, size_window).exec_()

    def show_about_dialog(self):
        size_window = (800, 400)
        text = load_text(TEXT_FILES['about'])
        text = text.replace('get_version()', get_version())
        self.create_text_dialog('О программе', text, size_window).exec_()

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
                          buttons=[self.button_configure, self.button_shutdown, self.start_old_configuration_button],
                          count=len(self.online_device), text_template='На настройку:')

    def check_devices_clicked(self):
        try:
            self.thread = DeviceThread(self, check_devices)
            self.thread.start_execution([self.button_check_all])
        except Exception as e:
            print(f'ERR check_devices_clicked => {e}')

    def flash_devices(self):
        try:
            path_firmware = read_json_file(CONFIG_FILE).get('firmware')
            if validate_file_from_config(path_firmware, self):
                self.thread = DeviceThread(self, flash_devices, self.sideload_device, path_firmware)
                self.thread.start_execution(self.buttons_to_disable)
        except Exception as e:
            print(f'flash_devices ERROR! => {e}')

    def start_old_configuration(self):
        try:
            path_old_settings = read_json_file(CONFIG_FILE)['old_settings']
            if validate_file_from_config(path_old_settings, self):
                self.thread = DeviceThread(self, start_all_config, self.online_device, path_old_settings)
                self.thread.start_execution(self.buttons_to_disable, check_shutdown=True)
        except Exception as e:
            print(f'start_old_configuration ERROR! => {e}')

    def start_new_configuration(self):
        try:
            path_new_settings = read_json_file(CONFIG_FILE)['new_settings']
            if validate_file_from_config(path_new_settings, self):
                self.thread = DeviceThread(self, start_new_configuration, self.online_device, path_new_settings)
                self.thread.start_execution(self.buttons_to_disable, check_shutdown=True)
        except Exception as e:
            print(f'start_new_configuration ERROR! => {e}')

    def shutdown_devices(self):
        self.thread = DeviceThread(self, shutdown_devices, self.online_device)
        self.thread.start_execution(self.buttons_to_disable)

    def show_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
