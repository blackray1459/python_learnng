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
def obertka(func):
    def wrapper(key):
        print("Start wrap")
        timing = time.gmtime()
        func.tdict = tcalc
        func.hdict = hcalc
        if key in func.hdict.keys():
            func.tdict[key] = timing
            print("Key is in value cache")
            return func.hdict[key]
        res = func(key)
        if func.hdict.__len__() == N:
            temp = min_key(func.tdict)
            func.tdict.pop(temp)
            func.hdict.pop(temp)
        func.tdict[key] = timing
        func.hdict[key] = res
        print("Timing {} and value {} appended\n".format(func.tdict[key], func.hdict[key]))
    return wrapper


@obertka
def calc(inp):
    return inp*inp


def min_key(dic):
    temp = min(dic.values())
    res = [key for key in dic.keys() if dic[key] == temp]
    return res[0]


check = True
tcalc = {}
hcalc = {}
N = 3


calc(1)
calc(2)
time.sleep(1)
calc(3)
time.sleep(1)
calc(5)
time.sleep(1)
calc(2)
print("\nTime cache for CALC is {},\nValue cache for CALC is {}".format(tcalc, hcalc))

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

'''
    a = input()
    if a == "f":
        return
    else:
        a = int(a)
'''
