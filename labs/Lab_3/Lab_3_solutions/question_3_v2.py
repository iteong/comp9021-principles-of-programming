# Finds all possible ways of inserting + and - signs
# in the sequence 123456789 (at most one sign before any digit)
# such that the resulting arithmetic expression evaluates to 100.
#
# Written by Eric Martin for COMP9021


def test(expression, i):
    for digit in '23456789':
        one_of_3_options = i % 3
        if one_of_3_options == 2:
            expression += digit
        elif one_of_3_options == 1:
            expression += ' + ' + digit
        else:
            expression += ' - ' + digit
        i //= 3
    if eval(expression) == 100:
        print(expression + ' = 100')

for i in range(3 ** 8):
    test('1', i)
    test('-1', i)

