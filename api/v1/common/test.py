from string import hexdigits
from re import match

good = '122936bdc2a22ca4C0279cf47D87H707'

# success: 2.0 fail: 2.0
def tester1():
    if len(good) != 32:
        return False
    return all(c in hexdigits for c in good)

# success: 0.3 fail 1.3
def tester2():
    if len(good) != 32:
        return False
    try:
        int(good, 16)
    except ValueError:
        return False
    return True

# success 2.0 fail: 2.0
def tester3():
    if len(good) != 32:
        return False
    hexd = '1234567890abcdef'
    return all(c in hexd for c in good.lower())

# success: 1.1 fail: 1.4
def tester4():
    if len(good) != 32:
        return False
    for c in good:
        if c not in hexdigits:
            return False
    return True

# success: 1.1 fail: 1.0
def tester5():
    return match(r'[a-fA-F\d]{32}', good)

# success: 1.2 fail: 1.1
def tester6():
    return match(r'[a-f\d]{32}', good.lower())

def tester7():
    if len(good) != 32:
        return False
    try:
        float.fromhex(good)
    except ValueError:
        return False
    return True

if __name__ == '__main__':
    from timeit import timeit
    print(timeit("tester1()", setup="from __main__ import tester1", number=500000))
    print(timeit("tester2()", setup="from __main__ import tester2", number=500000))
    print(timeit("tester3()", setup="from __main__ import tester3", number=500000))
    print(timeit("tester4()", setup="from __main__ import tester4", number=500000))
    print(timeit("tester5()", setup="from __main__ import tester5", number=500000))
    print(timeit("tester6()", setup="from __main__ import tester6", number=500000))
    print(timeit("tester7()", setup="from __main__ import tester7", number=500000))
