import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, QObject

from client_logic import ClientLogic


class Receiving(QThread):
    game_result = QtCore.pyqtSignal(str)
    new_game_task = QtCore.pyqtSignal(str)

    def __init__(self, main_window, sock, parent=None):
        super(Receiving, self).__init__()
        self.__main_window = main_window
        self.__working = True
        self.__socket = sock
        self.data = None

    def run(self):
        while self.__working:
            try:
                while True:
                    data, addr = self.__socket.recvfrom(1024)
                    if data is not None:
                        str_data = str(data.decode("utf-8"))
                        f_data = str_data.split("###")

                        self.data = f_data
                        if self.data[0] == "result":
                            self.game_result.emit(self.data[1])
                        elif self.data[0] == "task":
                            self.new_game_task.emit(str_data)
            except Exception:
                pass


class Frame(QtWidgets.QMainWindow):
    def __init__(self):
        super(Frame, self).__init__()
        self.__client = ClientLogic()
        self.setup_ui()

        self.__thread = Receiving(self, self.__client.socket)
        self.__thread.game_result.connect(self.get_result)
        self.__thread.new_game_task.connect(self.get_new_task)
        self.__thread.start()

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
        self.new_game_btn.clicked.connect(self.set_ui)

        self.verticalLayout_2.addWidget(self.new_game_btn)
        self.disc_lbl = QtWidgets.QLabel(self.centralwidget)

        self.verticalLayout_2.addWidget(self.disc_lbl)
        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.send_btn)
        self.send_btn.clicked.connect(self.send_text)
        self.send_btn.setDisabled(True)
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.clicked.connect(sys.exit)

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

    def set_ui(self):
        self.disc_lbl.setText("waiting for other players")
        self.__client.send_request("ready")

    def send_text(self):
        self.__client.send_request(f"answer@@@{self.textEdit.toPlainText()}")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new_game_btn.setText(_translate("MainWindow", "New game"))
        self.disc_lbl.setText(_translate("MainWindow", "TextLabel"))
        self.send_btn.setText(_translate("MainWindow", "Send"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))

    @QtCore.pyqtSlot(str)
    def get_result(self, data):
        if data == "lose" or data == "win":
            self.textEdit.clear()
            self.new_game_btn.setDisabled(False)
            self.send_btn.setDisabled(True)
        AlertBox(f"U {data}")

    @QtCore.pyqtSlot(str)
    def get_new_task(self, task: str):
        task = task.split("###")
        if task[0] == "task":
            self.new_game_btn.setDisabled(True)
            self.send_btn.setDisabled(False)
            self.textEdit.setText(task[1])
            self.disc_lbl.setText(task[2])

    def exit_(self):
        self.__client.send_request("exit")

    @property
    def thread_(self):
        return self.__thread


class AlertBox(QtWidgets.QMessageBox):
    def __init__(self, error_text, description=""):
        super(AlertBox, self).__init__()
        self.setText(error_text)
        self.setInformativeText(description)
        self.setWindowTitle("Game result")
        self.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Frame()
    ui.setup_ui()
    ui.show()
    sys.exit(app.exec_())
