# Prints out the representation of a positive number in base 2,
# using two recursive procedures, one of which is tail-recursive.
#
# Written by Eric Martin for COMP9021


from math import log, floor


def print_binary_representation_1(n):
    _print_binary_representation_1(n)
    print()
    
def _print_binary_representation_1(n):
    if n >= 2:
        _print_binary_representation_1(n // 2)
    print(n % 2, end = '')


def print_binary_representation_2(n):
    _print_binary_representation_2(n, floor(log(n, 2)))
    print()
    
def _print_binary_representation_2(n, exp):
    if exp < 0:
        return       
    if 2 ** exp <= n:
        print(1, end = '')
        _print_binary_representation_2(n - 2 ** exp, exp - 1)
    else:
        print(0, end = '')
        _print_binary_representation_2(n, exp - 1)

if __name__ == '__main__':
    print('Printing out 1, 2, 5 and 23 in binary, first method:')
    print_binary_representation_1(1)
    print_binary_representation_1(2)
    print_binary_representation_1(5)
    print_binary_representation_1(23)
    print()
    print('Printing out 1, 2, 5 and 23 in binary, second method:')
    print_binary_representation_2(1)
    print_binary_representation_2(2)
    print_binary_representation_2(5)
    print_binary_representation_2(23)


    
