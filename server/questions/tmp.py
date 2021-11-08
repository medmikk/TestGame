def f3(a: int, b: int) -> int:
    while (a != 0) and (b != 0):
        if a < b:
            a, b = b, a
        a %= b

    return a + b