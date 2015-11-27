from math import log

def convert_1(N):
    _convert_1(N)
    print()

def _convert_1(N):
    if N < 2:
        print(N, end = '')
        return
    _convert_1(N // 2)
    if N % 2:
        print(1, end = '')
    else:
        print(0, end = '')

def convert_2(N):
    _convert_2(N, int(log(N, 2)))
    print()

def _convert_2(N, exp):
    if exp < 0:
        return
    if  2 ** exp <= N:
        print(1, end = '')
        _convert_2(N - 2 ** exp, exp - 1)
    else:
        print(0, end = '')
        _convert_2(N, exp - 1)

convert_1(37)
convert_2(37)
        
