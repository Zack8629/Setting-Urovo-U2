from PyQt5.QtWidgets import QWidget


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Настройки')
