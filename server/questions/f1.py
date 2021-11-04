def f1(num: int, degree: int) -> int:
    n = num
    for i in range(0, degree - 1):
        n *= num
    return n
