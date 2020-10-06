def multiply(factor):
    def outer(func):
        def wrapper(arg):
            res = func(arg)*factor
            print("Text in WRAPPER")
            return "Result is {}, arg is {}".format(res, arg)
        print("Text in OUTER")
        return wrapper
    print("Text in MULTIPLY")
    return outer


@multiply(2)
def f(x):
    return x


@multiply(3)
def g(x):
    return x * x


print(f(2))
print(f(5))
print(g(2))
print(g(3))
