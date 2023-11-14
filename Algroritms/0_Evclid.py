"""Алгоритмы Евклида, нахождение общего делителя"""

# Долго считает каждый раз минусуя
def func(m, n):
    while m != n:
        if m > n:
            m -= n
        else:
            n -= m
    return m
end = func(240, 100000)
print(end)
# Каждый раз выделяется больше памяти и может поломаться от перегрузки рекурсии
def func(m, n):
    if n == 0:
        return m
    return func(n, m % n)
end = func(240, 100000)
print(end)
# Самый эффективный способо через цикл и деление
def func(m, n):
    while n != 0:
        m, n = n, m % n
    return m
end = func(240, 100000)
print(end)