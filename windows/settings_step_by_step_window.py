from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

from scripts import get_version, run_configuration_for_devices
from scripts.a_3_0_all_configure_u2 import settings_1, settings_2, settings_3, settings_4, settings_5


class StepConfigWindow(QWidget):
    def __init__(self, main_window, online_devices):
        super().__init__()
        self.main_window = main_window
        self.online_devices = online_devices
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Настройка по шагам {get_version()}')
        layout = QVBoxLayout()

        # Словарь для соответствия кнопок и функций
        self.config_functions = {
            'Настройка 1': settings_1,
            'Настройка 2': settings_2,
            'Настройка 3': settings_3,
            'Настройка 4': settings_4,
            'Настройка 5': settings_5,
        }

        # Сохраняем ссылки на кнопки для их активации/деактивации
        self.buttons = {}

        # Добавляем кнопки для шагов настройки
        for label, func in self.config_functions.items():
            button = QPushButton(label)
            button.clicked.connect(lambda _, f=func: self.run_configuration(f))
            self.buttons[label] = button
            layout.addWidget(button)

        # Добавляем кнопку 'Выключить'
        self.button_shutdown = QPushButton('Выключить')
        self.button_shutdown.clicked.connect(self.main_window.shutdown_devices)
        layout.addWidget(self.button_shutdown)

        # Промежуток пустого места
        layout.addStretch()

        # Добавляем кнопку 'Закрыть окно'
        self.button_close = QPushButton('Закрыть окно')
        self.button_close.clicked.connect(self.close)
        layout.addWidget(self.button_close)

        self.setLayout(layout)
        self.setFixedSize(350, 300)

    def run_configuration(self, config_functions):
        # Деактивируем все кнопки
        self._set_buttons_enabled(False)
        QApplication.processEvents()  # Обновляем интерфейс, чтобы кнопки стали неактивными

        try:
            # Передаем config_functions в run_configuration_for_devices
            run_configuration_for_devices(self.online_devices, config_functions)
        except Exception as e:
            print(f'ERROR!! => {e}')
        finally:
            # Восстанавливаем активность всех кнопок после завершения работы
            self._set_buttons_enabled(True)

    def _set_buttons_enabled(self, enabled):
        # Деактивируем или активируем кнопки для шагов настройки
        for button in self.buttons.values():
            button.setEnabled(enabled)
        # Деактивируем или активируем кнопки 'Выключить' и 'Закрыть окно'
        self.button_shutdown.setEnabled(enabled)
        self.button_close.setEnabled(enabled)

    def close(self):
        self.setParent(None)
        self.deleteLater()
