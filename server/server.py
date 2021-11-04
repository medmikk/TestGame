import socket
from random import randint


class Server:
    def __init__(self):
        self.__host = "localhost"
        self.__port = 228
        self.__clients = []
        self.__sock = None
        self.__ready_players = []
        self.__response = ""

    def __init_socket(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__host, self.__port))

    def run(self):
        self.__init_socket()
        working = True

        while working:
            try:
                data, addr = self.__sock.recvfrom(1024)

                print(f"addr {addr}")

                if addr not in self.__clients:
                    self.__clients.append(addr)

            except KeyboardInterrupt as e:
                print("Stop working")
                working = False

    def request_handler(self, data: bytes, addr):
        data = data.decode("utf-8")
        if data == "ready":
            if addr not in self.__ready_players:
                self.__ready_players.append(addr)
            if len(self.__ready_players) >= 2:
                number = randint(1, 2) #TODO make more question files
                self.__response = self.get_question(number) + "###" + self.get_desc(number)
                for player_addr in self.__ready_players:
                    self.__sock.sendto(self.__response, player_addr)
        elif data == "new_game":
            pass

    def get_question(self, num) -> str:
        try:
            with open(f"f{num}") as file:
                question = file.read()
        except Exception:
            question = ""
        return question

    def get_desc(self, num) -> str:
        with open(f"f{num}_desc") as file:
            desc = file.read()

        return desc

    def __del__(self):
        if self.__sock:
            print("Closed")
            self.__sock.close()


if __name__ == "__main__":
    server = Server()
    server.run()