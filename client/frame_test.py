import time

from client.frame_qt import Frame
from server.server_logic import Server
from client.client_logic import ClientLogic
import threading
from pytestqt.qt_compat import qt_api


def test_get_new_task(qtbot):
    thread = threading.Thread(target=Server().run)
    thread.start()
    ui = Frame()
    ui.setup_ui()
    ui.show()
    qtbot.addWidget(ui)
    assert ui.disc_lbl.text() == "TextLabel"
    qtbot.mouseClick(ui.new_game_btn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    assert ui.disc_lbl.text() == "waiting for other players"
    ui.exit_()
    thread.join()


def test_game(qtbot):
    thread = threading.Thread(target=Server().run)
    thread.start()
    ui = Frame()
    ui.setup_ui()
    ui.show()
    ui2 = Frame()
    ui2.setup_ui()
    ui2.show()
    qtbot.addWidget(ui)
    assert ui.textEdit.toPlainText() == ""
    qtbot.mouseClick(ui.new_game_btn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    qtbot.addWidget(ui2)
    qtbot.mouseClick(ui2.new_game_btn, qt_api.QtCore.Qt.MouseButton.LeftButton)
    with qtbot.waitSignal(ui.thread_.new_game_task) as blocker:
        blocker.wait()
        print("blocker text ", blocker.args, "End blocker")
        ui.get_new_task(blocker.args[0])

    assert ui.textEdit.toPlainText() != ""

    ui.exit_()
    thread.join()

