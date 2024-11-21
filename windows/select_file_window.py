import json
import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton,
    QFileDialog, QGroupBox
)


class FileDialogWindow(QWidget):
    CONFIG_FILE = 'select_file.txt'
    DEFAULT_PATHS = {
        'firmware': '',
        'launcher': '',
        'voiceman': '',
        'button_settings': '',
        'launcher_settings': '',
        'wallpaper': ''
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Выбор файлов')

        self.paths = {}
        self.text_fields = {}  # Словарь для хранения QLineEdit с их ключами
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.add_file_selector(layout, 'Указать файл прошивки', 'firmware', 'zip')
        layout.addSpacing(20)

        group_box = QGroupBox('Файлы для настройки')
        group_layout = QVBoxLayout(group_box)

        file_selectors = [
            ('Указать APK лаунчера', 'launcher', 'apk'),
            ('Указать APK voiceman', 'voiceman', 'apk'),
            ('Указать настройки кнопок', 'button_settings', 'txt'),
            ('Указать настройки лаунчера', 'launcher_settings', 'zip'),
            ('Указать фоновое изображение', 'wallpaper', 'png')
        ]

        for label, key, file_type in file_selectors:
            self.add_file_selector(group_layout, label, key, file_type)

        layout.addWidget(group_box)
        self.add_buttons(layout)

    def add_file_selector(self, layout, label, key, file_type):
        hbox = QHBoxLayout()
        button = QPushButton(label)
        button.setFixedSize(321, 40)
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)

        button.clicked.connect(lambda: self.open_file_dialog(line_edit, key, file_type))
        hbox.addWidget(button)
        hbox.addWidget(line_edit)
        layout.addLayout(hbox)

        self.text_fields[key] = line_edit  # Сохраняем QLineEdit с ключом

    def showEvent(self, event):
        # Загружаем пути перед показом окна
        self.paths = self.load_paths()
        for key, line_edit in self.text_fields.items():
            line_edit.setText(self.paths.get(key, ''))
        super().showEvent(event)

    def open_file_dialog(self, line_edit, key, file_type):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '', f'{file_type.upper()} Files (*.{file_type});;All Files (*)'
        )
        if file_name:
            line_edit.setText(file_name)
            self.paths[key] = file_name

    def add_buttons(self, layout):
        hbox = QHBoxLayout()
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_paths)
        hbox.addWidget(save_button)

        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.close_without_saving)
        hbox.addWidget(cancel_button)

        layout.addLayout(hbox)

    def save_paths(self):
        try:
            with open(self.CONFIG_FILE, 'w') as file:
                json.dump(self.paths, file, indent=4, ensure_ascii=False)
            print('Изменения сохранены.')
        except Exception as e:
            print(f'Ошибка сохранения файла: {e}')
        self.close()

    def close_without_saving(self):
        self.paths = self.load_paths()
        print('Изменения отменены.')
        self.close()

    def load_paths(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f'Ошибка загрузки файла: {e}')
        return self.DEFAULT_PATHS.copy()
