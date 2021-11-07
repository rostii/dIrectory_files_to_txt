from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QVBoxLayout, QLabel, QWidget, \
    QListWidget, QHBoxLayout, QLineEdit
import os


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setMinimumSize(QSize(300, 100))

        self.dir_name = ''
        self.file_list_in_directory = []
        self.filtered_file_list = []

        layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()

        file_dialog_button = QPushButton('Select directory')
        file_dialog_button.setFixedSize(QSize(160, 50))
        file_dialog_button.released.connect(self.file_dialog_button_clicked)
        horizontal_layout.addWidget(file_dialog_button)

        save_list_button = QPushButton('Save file list')
        save_list_button.setFixedSize(QSize(160, 50))
        save_list_button.released.connect(self.save_list_button_clicked)
        horizontal_layout.addWidget(save_list_button)

        line_edit_label = QLabel('Filter: ')
        horizontal_layout.addWidget(line_edit_label)

        self.filter_extension = QLineEdit(self)
        self.filter_extension.setMinimumWidth(160)
        self.filter_extension.setPlaceholderText('Define a file extension')
        self.filter_extension.textChanged.connect(self.line_edit_text_changed)
        horizontal_layout.addWidget(self.filter_extension)

        horizontal_layout.addStretch(1)

        layout.addLayout(horizontal_layout)

        self.dir_name_label = QLabel()
        layout.addWidget(self.dir_name_label)

        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)

        self.setLayout(layout)

    def file_dialog_button_clicked(self):
        file_dialog = QFileDialog()
        selected_dir_name = file_dialog.getExistingDirectory(self)

        if selected_dir_name == '':
            return

        self.dir_name = selected_dir_name
        self.file_list_in_directory = []
        self.filtered_file_list = []
        self.dir_name_label.clear()
        self.file_list_widget.clear()

        self.dir_name_label.setText('Selected directory: ' + "<font color=\"green\">" + self.dir_name + "</font>")

        self.list_files_in_directory()
        self.filter_file_list(self.filter_extension.text())

        self.file_list_widget.addItems(self.filtered_file_list)

    def list_files_in_directory(self):
        for item_name in os.listdir(self.dir_name):
            path_name = os.path.join(self.dir_name, item_name)
            if os.path.isfile(path_name):
                self.file_list_in_directory.append(item_name)

    def save_list_button_clicked(self):
        file_dialog = QFileDialog()
        file_list_name, _ = file_dialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory=os.path.join(self.dir_name, 'file_list.txt'),
            initialFilter='Text Files (*.txt)'
        )

        if file_list_name == '':
            return

        with open(file_list_name, 'w') as f:
            f.writelines(file + '\n' for file in self.filtered_file_list)

    def line_edit_text_changed(self):
        self.filter_file_list(self.filter_extension.text())

        self.file_list_widget.clear()
        self.file_list_widget.addItems(self.filtered_file_list)

    def filter_file_list(self, text):
        if text == '':
            self.filtered_file_list = self.file_list_in_directory
            return

        self.filtered_file_list = [file_name
                                   for file_name in self.file_list_in_directory
                                   if os.path.splitext(file_name)[1] == ('.' + text)]


if __name__ == '__main__':
    App = QApplication([])

    window = MainWindow()
    window.show()

    App.exec()
