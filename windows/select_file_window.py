from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton,
    QFileDialog, QGroupBox
)

from scripts.paths import CONFIG_FILE, DEFAULT_PATHS, DEFAULT_KEYS_AND_EXTENSIONS, EMPTY_PATH
from utils.utils import write_json_file, read_json_file, resource_path


class FileDialogWindow(QWidget):
    LABELS_MAP = {
        'firmware': 'Указать файл прошивки',
        'launcher': 'Указать APK лаунчера',
        'voiceman': 'Указать APK voiceman',
        'button_settings': 'Указать настройки кнопок',
        'launcher_settings': 'Указать настройки лаунчера',
        'wallpaper': 'Указать фоновое изображение',
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Выбор файлов')
        self.setWindowIcon(QIcon(resource_path('icons/main.ico')))

        self.FILE_SELECTORS = [
            (self.LABELS_MAP[key], key, ext) for key, ext in DEFAULT_KEYS_AND_EXTENSIONS.items()
        ]

        self.paths = {}
        self.text_fields = {}  # Словарь для хранения QLineEdit с их ключами
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.add_file_selector(layout, *self.FILE_SELECTORS[0])
        layout.addSpacing(20)

        group_box = QGroupBox('Файлы для настройки')
        group_layout = QVBoxLayout(group_box)

        for label, key, file_type in self.FILE_SELECTORS[1:]:
            self.add_file_selector(group_layout, label, key, file_type)

        layout.addWidget(group_box)

        self.add_buttons(layout)

    def add_file_selector(self, layout, label, key, file_type):
        hbox = QHBoxLayout()
        button = QPushButton(label)
        button.setFixedSize(321, 35)
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)

        button.clicked.connect(lambda: self.open_file_dialog(line_edit, key, file_type))
        hbox.addWidget(button)
        hbox.addWidget(line_edit)
        layout.addLayout(hbox)

        self.text_fields[key] = line_edit  # Сохраняем QLineEdit с ключом

    def showEvent(self, event):
        # Загружаем пути перед показом окна
        try:
            self.paths = read_json_file(CONFIG_FILE, EMPTY_PATH)
            for key, line_edit in self.text_fields.items():
                line_edit.setText(self.paths.get(key, ''))
            super().showEvent(event)
        except Exception as e:
            print(f'Ошибка отображения окна => {e}')

    def open_file_dialog(self, line_edit, key, file_type):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, 'Выбрать файл', '', f'{file_type.upper()} Files (*.{file_type});;All Files (*)'
            )
            if file_name:
                line_edit.setText(file_name)
                self.paths[key] = file_name
        except Exception as e:
            print(f'Ошибка при выборе файла: {e}')

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
        write_json_file(CONFIG_FILE, self.paths)
        print('Изменения сохранены.')
        self.close()

    def close_without_saving(self):
        self.paths = read_json_file(CONFIG_FILE, DEFAULT_PATHS)
        print('Изменения отменены.')
        self.close()
