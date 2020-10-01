import time

'''
#  ДЕКОРАТОР ПОДСЧЕТА ВРЕМЕНИ РАБОТЫ ФУНКЦИИ

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
N = 4
t = {1: 4, 2: 5, 3: 1}
h = {}


def calc(inp):
    return inp*inp


def min_key(dic):
    temp = min(dic.values())
    res = [key for key in dic.keys() if dic[key] == temp]
    return res[0]


def calc_cache(key):  # def calc(q, h, key):
    global t, h, N
    timing = time.time()
    if key in h.keys():
        t[key] = timing
        return h[key]
    result = calc(key)
    if h.__len__() == N:
        temp = min_key(h)
        h.pop(temp)


check = True


def obertka(func):
    global check

    def wrapper(arg):
        print("Start wrap")
        if check:
            func(arg)
        else:
            print('Check is False')
    return wrapper


@obertka
def funcc(arg):
    if arg == 1:
        print("Function just worked, code 1")
    elif arg == 2:
        print("Function just worked, code 2")


funcc(1)
'''
    a = input()
    if a == "f":
        return
    else:
        a = int(a)
'''
