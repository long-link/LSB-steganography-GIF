import sys
from medotLSB import EncryptorGIF, DecryptorGIF
from widgetLSB import Ui_steganograghy_widget
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QInputDialog, QMessageBox


class MainWindow(QMainWindow, Ui_steganograghy_widget):
    def __init__(self):
        super().__init__()  # не очень понял зачем супер
        self.setupUi(self)
        self.file_name = ''
        self.new_file_name = ''
        self.open_button.clicked.connect(self.open_image)
        self.encode_button.clicked.connect(self.load_encode)
        self.decode_button.clicked.connect(self.load_decode)

    def open_image(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Open file', 'desktop/your_image',
                                                     "Images (*.gif)")[0]  # why [0]?!
        self.image_place.setPixmap(QtGui.QPixmap(self.file_name))
        self.line_status.setText(self.file_name)

    def save_image(self):
        self.new_file_name = QFileDialog.getSaveFileName(self, 'Save file', 'desktop/your_image',
                                                         "Images (*.gif)")[0]

    def load_encode(self):
        # вся эта тема с if мб не правильно, в плане чистого кода
        if self.file_name == '':
            self.errors(41)
            return
        Encryptor = EncryptorGIF(self.file_name)
        temporary_value = Encryptor.check_format()
        if not temporary_value:
            self.errors(temporary_value)
            return
        entered_message = Encryptor.compare_message_size(self.show_dialog())
        if not entered_message:
            self.errors(31)
            return
        Encryptor.insert_decryption_key()
        length = str(Encryptor.find_size_message_bytes(entered_message))
        while len(length) != 3:
            length = '0' + length
        Encryptor.symbol_insertion(length, 17)
        Encryptor.symbol_insertion(entered_message, 29)
        self.save_image()
        if self.new_file_name == '':
            self.errors(61)
            return
        Encryptor.create_new_GIF(self.new_file_name)

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
        length_message = int(Decryptor.find_message(3, 17))
        QMessageBox.information(self, 'Закодированное сообщение было', Decryptor.find_message(length_message, 29))

    def show_dialog(self):
        text, ok = QInputDialog.getText(self, 'Dialog', 'Введите сообщение которое хотите закодировать :')
        if ok:
            return text

    # не уверен, что так нужно делать с ошибками. И вся эта тема с return id ошибки наверное не очень
    def errors(self, error_number):
        warning_errors = {
            21: 'Не является GIF форматом',
            22: 'Не работает с таким GIF форматом',
            31: 'Длинна сообщения превышает максимальный размер/текст не введен',
            41: 'Не выбран файл',
            51: 'Нет закодированного текста/неверный ключ',
            61: 'Вы не захотели сохранить файл. Желательно загрузить файл заново',
            100: ''
        }
        QMessageBox.warning(self, 'Ошибочка', warning_errors[error_number])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
