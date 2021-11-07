import socket
import threading
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from client.frame_qt import Frame


class ClientLogic:

    def __init__(self):
        self.__port = 230
        self.__host = socket.gethostbyname(socket.gethostname())
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.setblocking(False)
        self.__server = (socket.gethostbyname(socket.gethostname()), 228)
        self.__working = False
        self.__supp_thread: threading.Thread = None

        self.__frame = Frame()

    def __del__(self):
        if self.__supp_thread is not None:
            self.__supp_thread.join()
        self.__socket.close()

    def app(self):
        app = QtWidgets.QApplication(sys.argv)
        self.__frame.setup_ui()
        self.__frame.new_game_btn.clicked.connect(lambda: self.send_request("ready"))
        self.__frame.show()
        sys.exit(app.exec_())


    def start_thread(self):
        self.__supp_thread = threading.Thread(target=self.receiving)
        self.__supp_thread.start()

    def start_game(self):
        self.__socket.sendto("ready".encode("utf8"), self.__server)

    def receiving(self):
        while self.__working:
            try:
                while True:
                    data, addr = self.__socket.recvfrom(1024)
                    print(str(data.decode('utf-8')))
                    if data is not None:
                        #1st function, 2nd description
                        self.__frame.set_ui(str(data.decode('utf-8')).split("###"))

            except Exception as e:
                pass

    def set_ui(self):
        pass

    def send_request(self, request: str) -> None:
        self.__socket.sendto(request.encode("utf-8"), self.__server)


if __name__ == "__main__":
    _client = ClientLogic()
    _client.app()
