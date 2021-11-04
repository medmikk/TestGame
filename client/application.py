from client.frame_qt import Frame
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Frame()
    ui.setup_ui()
    ui.show()
    sys.exit(app.exec_())