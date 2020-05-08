# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lsb.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_steganograghy_widget(object):
    def setupUi(self, steganograghy_widget):
        steganograghy_widget.setObjectName("steganograghy_widget")
        steganograghy_widget.resize(560, 480)
        steganograghy_widget.setMinimumSize(QtCore.QSize(560, 480))
        steganograghy_widget.setMaximumSize(QtCore.QSize(560, 480))
        self.open_button = QtWidgets.QPushButton(steganograghy_widget)
        self.open_button.setGeometry(QtCore.QRect(260, 430, 80, 30))
        self.open_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.open_button.setObjectName("open_button")
        self.image_place = QtWidgets.QLabel(steganograghy_widget)
        self.image_place.setGeometry(QtCore.QRect(80, 30, 400, 321))
        self.image_place.setText("")
        self.image_place.setPixmap(QtGui.QPixmap("Daxak.png"))
        self.image_place.setScaledContents(False)
        self.image_place.setAlignment(QtCore.Qt.AlignCenter)
        self.image_place.setObjectName("image_place")
        self.label_status = QtWidgets.QLabel(steganograghy_widget)
        self.label_status.setGeometry(QtCore.QRect(80, 363, 91, 16))
        self.label_status.setObjectName("label_status")
        self.encode_button = QtWidgets.QPushButton(steganograghy_widget)
        self.encode_button.setGeometry(QtCore.QRect(380, 430, 80, 30))
        self.encode_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.encode_button.setObjectName("encode_button")
        self.decode_button = QtWidgets.QPushButton(steganograghy_widget)
        self.decode_button.setGeometry(QtCore.QRect(460, 430, 80, 30))
        self.decode_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.decode_button.setObjectName("decode_button")
        self.groupBox = QtWidgets.QGroupBox(steganograghy_widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 520, 410))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.line_status = QtWidgets.QLabel(self.groupBox)
        self.line_status.setGeometry(QtCore.QRect(60, 380, 451, 16))
        self.line_status.setText("")
        self.line_status.setObjectName("line_status")

        self.retranslateUi(steganograghy_widget)
        QtCore.QMetaObject.connectSlotsByName(steganograghy_widget)

    def retranslateUi(self, steganograghy_widget):
        _translate = QtCore.QCoreApplication.translate
        steganograghy_widget.setWindowTitle(_translate("steganograghy_widget", "Form"))
        self.open_button.setText(_translate("steganograghy_widget", "Open image"))
        self.label_status.setText(_translate("steganograghy_widget", "Image directory :"))
        self.encode_button.setText(_translate("steganograghy_widget", "ENCODE"))
        self.decode_button.setText(_translate("steganograghy_widget", "DECODE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    steganograghy_widget = QtWidgets.QWidget()
    ui = Ui_steganograghy_widget()
    ui.setupUi(steganograghy_widget)
    steganograghy_widget.show()
    sys.exit(app.exec_())
