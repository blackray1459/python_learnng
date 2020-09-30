'''
import time


def timing(func):
    def wrapped():
        toc = time.time()
        func()
        tic = time.time()
        print(tic - toc)
        print("DONE")

    return wrapped


@timing
def calc():
    a = 0
    for b in range(6):
        a = a * b


calc()
'''

queue = {}


def calc(q, key):
    value = key * 3
    q[key] = value


a = 0

while type(a) is int:
    a = input()
    if a == "f":
        break
    else:
        a = int(a)
    calc(queue, a)

print(queue)