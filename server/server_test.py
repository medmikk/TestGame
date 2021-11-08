from server.server_logic import Server

server = Server()


def test_get_question(num = 1):
    with open(f"questions\\f{num}.py") as file:
        expected = file.read()
    actual = server.get_question(num)
    assert actual == expected


def test_get_description(num = 1):
    with open(f"questions\\f{num}_desc.txt") as file:
        expected = file.read()
    actual = server.get_desc(num)
    assert actual == expected


def test_check_answer():
    num = 3
    with open(f"questions\\test_func3.py") as file:
        data = file.read()
    actual = server.check_answer(num, data)
    expected = "win"
    assert actual == expected


if __name__ == "__main__":
    test_get_question()
    test_get_description()
    test_check_answer()
