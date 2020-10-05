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


check = True


def obertka(func):

    def wrapper(arg):
        print("Start wrap")
        timing = time.time()
        res = func(arg)
        if check:
            func.tdict[arg] = timing
            func.hdict[arg] = res
            print("Timing {} and value {} appended".format(func.tdict[arg], func.hdict[arg]))
        else:
            print('Check is False')
    return wrapper


@obertka
def calc(inp):
    calc.tdict = tcalc
    calc.hdict = hcalc
    return inp*inp


tcalc = {}
hcalc = {}


def min_key(dic):
    temp = min(dic.values())
    res = [key for key in dic.keys() if dic[key] == temp]
    return res[0]


def calc_cache(key):  # КОД К ПРОВЕРКЕ
    global t, h, N
    timing = time.time()
    if key in h.keys():
        t[key] = timing
        return h[key]
    result = calc(key)
    if h.__len__() == N:
        temp = min_key(t)
        t.pop(temp)
        h.pop(temp)
    t[key] = timing
    h[key] = result
    return result


@obertka
def funcc(arg):
    funcc.tdict = tfuncc
    funcc.hdict = hfuncc
    return arg+arg


tfuncc = {}
hfuncc = {}


calc(1)
calc(2)
calc(3)
funcc(1)
funcc(2)
funcc(3)
print("Time cache for CALC is {},\nValue cache for CALC is {}".format(tcalc, hcalc))
print()
print("Time cache for FUNCC is {},\nValue cache for FUNCC is {}".format(tfuncc, hfuncc))

'''
dir(calc)
__annotations__
__call__
__class__
__closure__
__code__
__defaults__
__delattr__
__dict__
__dir__
__doc__
__eq__
__format__
__ge__
__get__
__getattribute__
__globals__
__gt__
__hash__
__init__
__init_subclass__
__kwdefaults__
__le__
__lt__
__module__
__name__
__ne__
__new__
__qualname__
__reduce__
__reduce_ex__
__repr__
__setattr__
__sizeof__
__str__
__subclasshook__
'''
for i in range(len(dir(calc))):
    print(dir(calc)[i])

'''
    a = input()
    if a == "f":
        return
    else:
        a = int(a)
'''
