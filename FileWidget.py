from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFontMetrics

class FileWidget(QWidget):
    def __init__(self, file_name: str) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.file_label = QLabel(file_name.split("/")[-1])
        layout.addWidget(self.file_label)

        self.delete_button = QPushButton()
        self.delete_button.setText("❌")
        button_size = self.get_delete_button_size()

        self.delete_button.setFixedSize(button_size, button_size)
        self.delete_button.clicked.connect(self.delete_file)
        layout.addWidget(self.delete_button)

        self.file_name = file_name

    def delete_file(self) -> None:
        self.deleteLater()

    def get_delete_button_size(self) -> int:
        font_metrics = QFontMetrics(self.delete_button.font())
        text_width = font_metrics.horizontalAdvance("❌")
        text_height = font_metrics.height()
        return max(text_width, text_height) + 10