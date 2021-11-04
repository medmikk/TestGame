from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from client.client_logic import ClientLogic


class Receiving(QThread):
    def __init__(self, main_window, sock, parent=None):
        super(Receiving, self).__init__()
        self.__main_window = main_window


    def run(self):
        pass


class Frame(QtWidgets.QMainWindow):
    def __init__(self):
        super(Frame, self).__init__()
        self.__client = ClientLogic()
        self.__client.start_thread()


    def setup_ui(self):
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget()

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)

        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()

        self.new_game_btn = QtWidgets.QPushButton(self.centralwidget)
        self.new_game_btn.setMinimumSize(QtCore.QSize(150, 50))
        self.new_game_btn.clicked.connect(lambda: self.__client.send_request())

        self.verticalLayout_2.addWidget(self.new_game_btn)
        self.disc_lbl = QtWidgets.QLabel(self.centralwidget)

        self.verticalLayout_2.addWidget(self.disc_lbl)
        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)

        self.verticalLayout.addWidget(self.send_btn)
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)

        self.verticalLayout.addWidget(self.exit_btn)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()

        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def set_ui(self, data: List[str]):
        self.textEdit.setText(data[0])
        self.disc_lbl.setText(data[1])

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new_game_btn.setText(_translate("MainWindow", "New game"))
        self.disc_lbl.setText(_translate("MainWindow", "TextLabel"))
        self.send_btn.setText(_translate("MainWindow", "Send"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Frame()
    ui.setup_ui()
    ui.show()
    sys.exit(app.exec_())
