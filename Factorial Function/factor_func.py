# РЕАЛИЗАЦИЯ ВЫВОДА ПОСЛЕДНИХ 10 ЦИФР ОТ ФАКТОРИАЛА ВВЕДЕННОГО ЧИСЛА

def factorial_last_ten_digits(n):
    try:
        n = int(n)
    except ValueError:
        raise ValueError
    if n == 0:
        print(1)
        return
    elif n < 0:
        print("Value should be greater than zero.")
        return
    res = 1
    while n != 1:
        if len(str(res)) >= 11:
            res = int(str(res)[-10:])
        res *= n
        print(res)
        n -= 1
    print(res)
    return


factorial_last_ten_digits(input())
