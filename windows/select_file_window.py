from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QFileDialog, QGroupBox, \
    QSizePolicy

from scripts import get_version


class FileDialogWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Выбор файлов {get_version()}')

        # Используем для сохранения путей
        self.saved_file_paths = {
            'adb': '',
            'firmware': '',
            'launcher': '',
            'voiceman': '',
            'button_settings': '',
            'launcher_settings': '',
            'wallpaper': ''
        }

        # Используем для текущих путей
        self.current_file_paths = {
            'adb': '',
            'firmware': '',
            'launcher': '',
            'voiceman': '',
            'button_settings': '',
            'launcher_settings': '',
            'wallpaper': ''
        }

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Добавляем виджеты QLineEdit из self.current_file_paths в макет
        self.add_file_selector('Указать файл ADB', 'adb', 'exe')

        self.add_file_selector('Указать файл прошивки', 'firmware', 'zip')

        self.layout.addSpacing(20)

        group_box = QGroupBox('Файлы для настройки')
        group_layout = QVBoxLayout()
        group_box.setAlignment(Qt.AlignCenter)
        group_layout.setContentsMargins(10, 10, 10, 10)

        self.add_file_selector('Указать APK лаунчера', 'launcher', 'apk', group_layout)

        self.add_file_selector('Указать APK voiceman', 'voiceman', 'apk', group_layout)

        self.add_file_selector('Указать настройки кнопок', 'button_settings', 'txt', group_layout)

        self.add_file_selector('Указать настройки лаунчера', 'launcher_settings', 'zip', group_layout)

        self.add_file_selector('Указать фоновое изображение', 'wallpaper', 'png', group_layout)

        group_box.setLayout(group_layout)
        self.layout.addWidget(group_box)

        self.add_buttons()

    def add_file_selector(self, button_name, key, file_type, layout=None):
        if layout is None:
            layout = self.layout

        hbox = QHBoxLayout()

        button_width = 170
        button_height = 30

        button = QPushButton(button_name)
        button.setFixedSize(button_width, button_height)

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        hbox.addWidget(button)
        hbox.addWidget(line_edit)

        button.clicked.connect(lambda: self.open_file_dialog(line_edit, key, file_type))

        layout.addLayout(hbox)

    def open_file_dialog(self, line_edit, key, file_type):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_types = f'{file_type.capitalize()} Files (*.{file_type});;All Files (*)'
            file_name, _ = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', file_types, options=options)
            print(f'!!! => {line_edit=}')
            if file_name:
                line_edit.setText(file_name)
                self.current_file_paths[key] = file_name
        except Exception as err:
            print(f'Ошибка диалогового окна! => {err}')

    def add_buttons(self):
        hbox = QHBoxLayout()

        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.accept)
        hbox.addWidget(save_button)

        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)

        self.layout.addLayout(hbox)

    def accept(self):
        # Обновляем saved_file_paths только при сохранении
        for key, file_path in self.current_file_paths.items():
            self.saved_file_paths[key] = file_path

        print('Файлы сохранены:')
        for key, file_path in self.saved_file_paths.items():
            print(f'{key}: {file_path}')

        print()
        self.close()

    def reject(self):
        print('Отменено')
        for key, file_path in self.saved_file_paths.items():
            self.current_file_paths[key] = file_path

        print(f'{self.saved_file_paths=}')
        print(f'{self.current_file_paths=}')
        print()
        self.close()

    def load_saved_paths(self):
        for key, file_path in self.saved_file_paths.items():
            self.current_file_paths[key] = file_path

        print('load_saved_paths')
        print(f'{self.saved_file_paths=}')
        print(f'{self.current_file_paths=}')
        print()
