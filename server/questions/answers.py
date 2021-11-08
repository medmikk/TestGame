def f1_true(num, degree):
    return pow(num, degree)


def f2_true(array):
    array.sort()
    return array


def f3_true(a: int, b: int) -> int:
    while (a != 0) and (b != 0):
        if a < b:
            a, b = b, a
        a %= b

    return a + b


def f4_true(n: int) -> int:
    a = []
    for i in range(n + 1):
        a.append(i)
    a[1] = 0
    i = 2
    while i <= n:
        if a[i] != 0:
            j = i + i
            while j <= n:
                a[j] = 0
                j = j + i
        i += 1

    a = set(a)
    a.remove(0)

    return a
