import random


def func(inc=10,limit=100):
    a = 0
    b = 0
    while True:
        a = a + 1
        b += inc
        if b > limit:
            return
        yield a


a = func(1,10)
for v in a:
    print(v)
