import sys

from PySide6.QtWidgets import QApplication

from MergeWidget import PDFDragDropWidget

app = QApplication(sys.argv)
window = PDFDragDropWidget()
window.show()
sys.exit(app.exec())
