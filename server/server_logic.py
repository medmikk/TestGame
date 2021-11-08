import os
import socket
import importlib
from typing import List, Dict
from random import randint
from server.questions.answers import *
import server.questions.tmp as res


class Server:
    def __init__(self, port=228):
        self.__host = socket.gethostbyname(socket.gethostname())
        self.__port = port
        self.__clients: List[int] = []  # collect addresses of clients
        self.__sock = None
        self.__ready_players: Dict[int, int] = {}  # key - address value - task number
        self.__response = ""
        self.__is_game_started = False
        self.__current_task = 0

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
                print(data.decode("utf-8"))
                if addr not in self.__clients:
                    print(f"connected from {addr}")
                    self.__clients.append(addr)
                data = str(data.decode("utf-8")).split("@@@")
                if data[0] == "exit":
                    break
                self.request_handler(data, addr)

            except KeyboardInterrupt as e:
                print("Stop working")
                working = False

    def request_handler(self, data: List[str], addr):
        if data[0] == "ready":
            if addr not in self.__ready_players:
                # number of task
                print(f"Ready {addr}")
                self.__ready_players[addr] = 0
            if len(self.__ready_players) >= 2:

                if not self.__is_game_started:
                    self.__current_task = randint(1, 4)
                    self.__is_game_started = True
                    self.__response = f"task###{self.get_question(self.__current_task)}###{self.get_desc(self.__current_task)}"
                    self.__ready_players[addr] = self.__current_task
                    for player_addr in self.__ready_players.keys():
                        self.__sock.sendto(self.__response.encode("utf-8"), player_addr)
                        print(self.__response)
                else:
                    self.__response = f"task###{self.get_question(self.__current_task)}###{self.get_desc(self.__current_task)}"
                    self.__sock.sendto(self.__response.encode("utf-8"), addr)
        elif data[0] == "answer":
            ans = self.check_answer(self.__current_task, data[1])
            self.send_result(ans, addr)

    def send_result(self, ans, addr):
        self.__response = f"result###{ans}"
        if ans is None:
            self.__response = "result###import error"
        elif self.__response == "result###win":
            self.end_game(addr)
        else:
            self.__sock.sendto(self.__response.encode("utf-8"), addr)

    def end_game(self, addr):
        self.__sock.sendto(self.__response.encode("utf-8"), addr)
        self.__response = "result###lose"
        for player_addr in self.__ready_players.keys():
            if player_addr != addr:
                self.__sock.sendto(self.__response.encode("utf-8"), player_addr)
        self.__ready_players = {}
        self.__current_task = 0
        self.__is_game_started = False

    # TODO Refact
    def check_answer(self, num, data):
        with open(f"questions\\tmp.py", "w") as file:
            file.write(data)
        try:
            importlib.reload(res)
            if num == 1:
                a = randint(-1000, 1000)
                b = randint(-1000, 1000)
                try:
                    if f1_true(a, b) == res.f1(a, b):
                        return "win"
                    else:
                        return "assertion error"
                except Exception:
                    return "syntax error"

            elif num == 2:
                l = [randint(-100, 200) for _ in range(10)]
                try:
                    if f2_true(l) == res.f2(l):
                        return "win"
                    else:
                        return "assertion error"
                except Exception:
                    return "syntax error"

            elif num == 3:
                a = randint(0, 1000)
                b = randint(0, 1000)
                try:
                    if f3_true(a, b) == res.f3(a, b):
                        return "win"
                    else:
                        return "assertion error"
                except Exception:
                    return "syntax error"

            elif num == 4:
                a = randint(1, 1000)
                try:
                    if f4_true(a) == res.f4(a):
                        return "win"
                    else:
                        return "assertion error"
                except Exception:
                    return "syntax error"
        except Exception as e:
            print(e)
            with open(f"questions\\tmp.py", "w") as file:
                file.write("")
            return "import error"

    def get_question(self, num) -> str:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{dir_path}\\questions\\f{num}.py") as file:
                question = file.read()
        except Exception:
            question = ""
        return question

    def get_desc(self, num) -> str:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{dir_path}\\questions\\f{num}_desc.txt") as file:
                desc = file.read()
        except Exception:
            desc = ""
        return desc

    def __del__(self):
        if self.__sock:
            print("Closed")
            self.__sock.close()


if __name__ == "__main__":
    server = Server()
    server.run()
