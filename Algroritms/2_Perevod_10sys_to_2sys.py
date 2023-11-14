"""Перевод десятичного числа в двоичный формат"""

def func(num):
    string = ""
    while num > 0:
        string = f'{num % 2}{string}'
        num //= 2
    return (8-len(string))*'0'+ string
end = func(72)
print(end)