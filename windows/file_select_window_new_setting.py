from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QFileDialog, QGroupBox

from new_settings.paths import DEFAULT_KEYS_AND_EXTENSIONS_NEW_SETTINGS, EMPTY_PATH_NEW_SETTINGS
from utils.global_path import resource_path, CONFIG_FILE
from utils.working_with_files import read_json_file, write_json_file


class FileDialogWindowNewSetting(QWidget):
    LABELS_MAP = {
        'wallpaper': 'Указать фоновое изображение',
        'keys_config': 'Указать настройки кнопок',
        'settings_property': 'Указать настройки лаунчера',
        'voiceman_apk': 'Указать APK voiceman',
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Выбор файлов для новой настройки')
        self.setWindowIcon(QIcon(resource_path('icons/main.ico')))

        self.FILE_SELECTORS = [
            (self.LABELS_MAP[key], key, ext) for key, ext in DEFAULT_KEYS_AND_EXTENSIONS_NEW_SETTINGS.items()
        ]

        self.paths = {}
        self.text_fields = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        for label, key, ext in self.FILE_SELECTORS:
            self.add_file_selector(layout, label, key, ext)

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

        self.text_fields[key] = line_edit

    def showEvent(self, event):
        # Загружаем пути перед показом окна
        try:
            self.paths = read_json_file(CONFIG_FILE, EMPTY_PATH_NEW_SETTINGS)['new_settings']
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
        cancel_button.clicked.connect(self.close)
        hbox.addWidget(cancel_button)

        layout.addLayout(hbox)

    def save_paths(self):
        try:
            current_data = read_json_file(CONFIG_FILE)
            current_data['new_settings'] = self.paths
            write_json_file(CONFIG_FILE, current_data)
            print('Изменения сохранены.')
        except Exception as e:
            print(f'Ошибка при сохранении: {e}')
        self.close()
