# Finds all possible ways of inserting + and - signs
# in the sequence 123456789 (at most one sign before any digit)
# such that the resulting arithmetic expression evaluates to 100.
#
# Written by Eric Martin for COMP9021


def test(sign, i):
    sum = 0
    number = 1
    for digit in range(2, 10):
        one_of_3_options = i % 3
        if one_of_3_options % 2:
            number = number * 10 + digit
        else:
            sum += sign * number
            number = digit
            one_of_3_options -= 1
            sign = one_of_3_options
        i //= 3
    if sum + sign * number == 100:
        return True
    return False


def print_solution(one_or_minus_one, i):
    print('{:2d}'.format(one_or_minus_one), end = '')
    for digit in range(2, 10):
        one_of_3_options = i % 3
        if one_of_3_options % 2 == 0:
            if one_of_3_options:
                print(' + ', end = '')
            else:
                print(' - ', end = '')
        print(digit, end = '')
        i //= 3
    print(' = 100')



# For each of the 8 digits 2, 3,..., 9, say d, generate one of 3 numbers:
# - 1 causes d to become the rightmost digit of the number being built;
# - 0 causes
#     . the number being built to be considered fully built
#       and subtracted or added to the running sum,
#     . the next number to be built to begin with d and eventually
#       be subtracted to the running sum;
# - 2 causes
#     . the number being built to be considered fully built
#       and subtracted or added to the running sum,
#     . the next number to be built to begin with d and eventually
#       be added to the running sum.
for i in range(3 ** 8):
    # Let the first number be of the form 1...
    if test(1, i):
        print_solution(1, i)
    # Let the first number be of the form -1...
    if test(-1, i):
        print_solution(-1, i)

