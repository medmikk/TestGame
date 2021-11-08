import socket
import threading
import sys


class ClientLogic:

    def __init__(self):
        self.__port = 0
        self.__host = socket.gethostbyname(socket.gethostname())
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__host, self.__port))
        self.__socket.setblocking(False)
        self.__server = (socket.gethostbyname(socket.gethostname()), 228)
        self.__working = False

    def __del__(self):
        self.__socket.close()

    def start_game(self):
        self.__socket.sendto("ready".encode("utf8"), self.__server)

    def send_request(self, request: str) -> None:
        self.__socket.sendto(request.encode("utf-8"), self.__server)

    @property
    def socket(self):
        return self.__socket


if __name__ == "__main__":
    _client = ClientLogic()
