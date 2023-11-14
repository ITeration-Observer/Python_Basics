"""Решето Эратосфена, нахождение простых чисел"""

def func(n):
    mas = [_ for _ in range(n)]
    mas[1] = 0

    for num in range(2, n):
        if mas[num] != 0:
            next = num * 2
            while next < n:
                mas[next] = 0
                next += num
    result = [i for i in mas if i != 0]
    return result

end = func(100)
print(end)