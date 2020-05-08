import sys  # sys нужен для передачи argv в QApplication
from medotLSB import EncryptorGIF, DecryptorGIF
from widgetLSB import Ui_steganograghy_widget
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QInputDialog, QMessageBox


class MainWindow(QMainWindow, Ui_steganograghy_widget):
    def __init__(self):
        super().__init__()  # не очень понял зачем супер
        self.setupUi(self)
        self.file_name = ''
        self.open_button.clicked.connect(self.open_image)
        self.encode_button.clicked.connect(self.load_encode)
        self.decode_button.clicked.connect(self.load_decode)

    def open_image(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Open file', 'desktop/your_image',
                                                     "Images (*.gif)")[0]  # why [0]?!
        self.image_place.setPixmap(QtGui.QPixmap(self.file_name))
        self.line_status.setText(self.file_name)

    # @staticmethod  по идее
    def save_image(self):
        new_file_name = QFileDialog.getSaveFileName(self, 'Save file', 'desktop/your_image',
                                                    "Images (*.gif)")[0]
        return new_file_name

    def load_encode(self):
        if self.file_name == '':
            self.errors(41)
            return
        Encryptor = EncryptorGIF(self.file_name)
        temporary_value = Encryptor.check_format()
        if not temporary_value:
            self.errors(temporary_value)
            return
        entered_message = Encryptor.compare_message_size(self.show_dialog('message'))  # str()
        if not entered_message:
            self.errors(31)
            return
        Encryptor.insert_decryption_key()
        length = str(len(entered_message))
        while len(length) != 3:
            length = '0' + length
        Encryptor.symbol_insertion(length)
        Encryptor.symbol_insertion(entered_message)
        Encryptor.create_new_GIF(self.save_image())

    def load_decode(self):
        if self.file_name == '':
            self.errors(41)
            return
        Decryptor = DecryptorGIF(self.file_name)
        temporary_value = Decryptor.check_format()
        if not temporary_value:
            self.errors(temporary_value)
            return
        if not Decryptor.check_key():
            self.errors(51)
            return
        length_message = int(Decryptor.find_message(3))
        QMessageBox.information(self, 'Закодированное сообщение было', Decryptor.find_message(length_message))

    def show_dialog(self, for_what):
        if for_what == 'message':   # можно и кейсами если больше будет
            for_what = 'Введите сообщение которое хотите закодировать :'
        elif for_what == 'name_new_file':
            for_what = 'Введите имя нового файла :'
        text, ok = QInputDialog.getText(self, 'Input Dialog', for_what)

        if ok:
            return text

    def errors(self, error_number):
        warning_errors = {
            21: 'Не является GIF форматом',
            22: 'Не работает с таким GIF форматом',
            31: 'Длинна сообщения превышает максимальный размер/текст не введен',
            41: 'Не выбран файл',
            51: 'Нет закодированного текста/неверный ключ',
            61: '',
            100: ''
        }
        QMessageBox.warning(self, 'Ошибочка', warning_errors[error_number])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
