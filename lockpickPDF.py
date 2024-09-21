import os
import subprocess
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QTextEdit, QProgressBar, QMessageBox
from PyQt6.QtGui import QFont, QPalette, QColor

class PasswordDecryptor(QThread):
    progress_changed = pyqtSignal(int)
    process_finished = pyqtSignal(bool)

    def __init__(self, input_path, output_path, passwords):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.passwords = passwords
        self._is_running = True

    def run(self):
        total_passwords = len(self.passwords)
        for i, password in enumerate(self.passwords):
            if not self._is_running:
                break
            try:
                subprocess.run(['qpdf', '--decrypt', '--password=' + password, self.input_path, self.output_path], check=True)
                self.process_finished.emit(True)
                return
            except subprocess.CalledProcessError:
                pass
            progress = int(((i + 1) / total_passwords) * 100)
            self.progress_changed.emit(progress)
        self.process_finished.emit(False)

    def stop(self):
        self._is_running = False

class LockPickPDF(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LockPickPDF")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        copyright_label = QLabel("Copyright © 2024 Reking - cracked.io/rekingg")
        layout.addWidget(copyright_label)

        ascii_title_label = QLabel(
            """
            ▒█░░░ █▀▀█ █▀▀ █░█ ▒█▀▀█ ░▀░ █▀▀ █░█ ▒█▀▀█ ▒█▀▀▄ ▒█▀▀▀ 
            ▒█░░░ █░░█ █░░ █▀▄ ▒█▄▄█ ▀█▀ █░░ █▀▄ ▒█▄▄█ ▒█░▒█ ▒█▀▀▀ 
            ▒█▄▄█ ▀▀▀▀ ▀▀▀ ▀░▀ ▒█░░░ ▀▀▀ ▀▀▀ ▀░▀ ▒█░░░ ▒█▄▄▀ ▒█░░░
            """
        )
        ascii_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ascii_title_label.setWordWrap(True)
        layout.addWidget(ascii_title_label)

        form_layout = QVBoxLayout()

        # Select File
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Select File:")
        file_layout.addWidget(self.file_label)
        self.file_path = QTextEdit()
        self.file_path.setFixedHeight(30)
        file_layout.addWidget(self.file_path)
        self.select_file_button = QPushButton("Select File")
        self.select_file_button.setFixedWidth(100)
        self.select_file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_file_button)
        form_layout.addLayout(file_layout)

        # Select Folder
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Select Folder:")
        folder_layout.addWidget(self.folder_label)
        self.folder_path = QTextEdit()
        self.folder_path.setFixedHeight(30)
        folder_layout.addWidget(self.folder_path)
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.setFixedWidth(100)
        self.select_folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_folder_button)
        form_layout.addLayout(folder_layout)

        # Save Location
        save_layout = QHBoxLayout()
        self.save_label = QLabel("Save Location:")
        save_layout.addWidget(self.save_label)
        self.save_path = QTextEdit()
        self.save_path.setFixedHeight(30)
        save_layout.addWidget(self.save_path)
        self.save_button = QPushButton("Choose Save Location")
        self.save_button.setFixedWidth(150)
        self.save_button.clicked.connect(self.choose_save_location)
        save_layout.addWidget(self.save_button)
        form_layout.addLayout(save_layout)

        layout.addLayout(form_layout)

        # Process PDFs
        self.process_button = QPushButton("Process PDFs")
        self.process_button.setFixedWidth(120)
        self.process_button.clicked.connect(self.process_pdfs)
        layout.addWidget(self.process_button)

        # Output Log
        self.output_log = QTextEdit()
        layout.addWidget(self.output_log)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        layout.addStretch()

        self.central_widget.setLayout(layout)

        self.decryptor_thread = None

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        self.file_path.setPlainText(file)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path.setPlainText(folder)

    def choose_save_location(self):
        save_location = QFileDialog.getExistingDirectory(self, "Choose Save Location")
        self.save_path.setPlainText(save_location)

    def read_passwords(self):
        with open("passwords.txt", "r") as f:
            passwords = f.read().splitlines()
        return passwords

    def process_pdfs(self):
        file_path = self.file_path.toPlainText()
        folder_path = self.folder_path.toPlainText()
        save_path = self.save_path.toPlainText()

        if file_path:
            input_paths = [file_path]
        elif folder_path:
            input_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.pdf')]
        else:
            self.output_log.append("Please select a file or folder.")
            return

        if not save_path:
            self.output_log.append("Please choose a save location.")
            return

        passwords = self.read_passwords()

        for input_path in input_paths:
            filename = os.path.basename(input_path)
            output_path = os.path.join(save_path, "decrypted_" + filename)
            self.output_log.append(f"Processing {filename}")
            self.decryptor_thread = PasswordDecryptor(input_path, output_path, passwords)
            self.decryptor_thread.progress_changed.connect(self.update_progress)
            self.decryptor_thread.process_finished.connect(self.show_completion_dialog)
            self.decryptor_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def show_completion_dialog(self, success):
        if success:
            QMessageBox.information(self, "Process Completed", "PDF decryption completed successfully.")
        else:
            QMessageBox.warning(self, "Process Failed", "Failed to decrypt PDF. No valid password found.")

    def closeEvent(self, event):
        if self.decryptor_thread and self.decryptor_thread.isRunning():
            self.decryptor_thread.stop()
            self.decryptor_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])

    # Set Fusion style
    app.setStyle("fusion")
    
    # Set dark theme palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(142, 45, 197))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)

    window = LockPickPDF()
    window.show()
    app.exec()
