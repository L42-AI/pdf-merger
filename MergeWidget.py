from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QFileDialog, QHBoxLayout, QMessageBox
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PyPDF2 import PdfMerger

from FileWidget import FileWidget

class PDFDragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Create a scroll area for added files
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Widget to contain added files
        self.files_widget = QWidget()
        self.files_layout = QVBoxLayout(self.files_widget)
        self.scroll_area.setWidget(self.files_widget)

        # Add scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)


        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Button to upload files
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload_files)
        button_layout.addWidget(self.upload_button)

        # Button to merge PDF files
        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge_pdfs)
        button_layout.addWidget(self.merge_button)

        self.main_layout.addLayout(button_layout)

        # List to store added PDF files
        self.added_files = []

        # Accept drops
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            pdf_files = [url.toLocalFile() for url in mime_data.urls() if url.isLocalFile() and url.toLocalFile().endswith('.pdf')]
            if pdf_files:
                self.add_files(pdf_files)
                event.acceptProposedAction()

    def upload_files(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.add_files(selected_files)

    def add_files(self, files):
        for file in files:
            self.added_files.append(file)
            file_widget = FileWidget(file)
            self.files_layout.addWidget(file_widget)

    def merge_pdfs(self):
        if self.added_files:
            merger = PdfMerger()
            for file in self.added_files:
                merger.append(file)
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", filter="PDF Files (*.pdf)")
            if output_file:
                merger.write(output_file)
                merger.close()
                QMessageBox.information(self, "Success", f"Merged PDF saved as '{output_file}'")