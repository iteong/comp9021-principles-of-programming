# Describes all sets of positive integers {x, y, z} such that
# x, y and z have no occurrence of 0,
# every nonzero digit occurs exactly once in one of x, y or z,
# and x, y and z are perfect squares.
# Uses python builtin set.
#
# Written by Eric Martin for COMP9021


from math import sqrt, ceil
    

def completed_set_of_digits_if_ok(number, digits_seen_so_far):
    digits_seen_now = set(digits_seen_so_far)
    while number:
        # Extract rightmost digit, d, from number
        digit = number % 10
        if digit in digits_seen_now:
            return None
        digits_seen_now.add(digit)
        # Get rid of rightmost digit of number
        number //= 10
    return digits_seen_now


# If it was a perfect square, max_square would, associated with 1 and 4,
# be the largest member of a possible solution. */
max_square = 9876532
nb_of_solutions = 0
limit = ceil(sqrt(max_square))
set_of_all_digits = set(range(10))
for x in range(1, limit):
    x_square = x * x
    # digits_in_x_square_and_0 is not None iff all digits in x_square are distinct and not equal to 0 (encoded as 1)
    digits_in_x_square_and_0 = completed_set_of_digits_if_ok(x_square, {0})
    if not digits_in_x_square_and_0:
        continue
    for y in range(x + 1, limit):
        y_square = y * y
        # digits_in_x_square_and_y_square_and_0 is not None iff all digits in y_square are distinct, distinct to 0,
        # and distinct to all digits in x_square
        digits_in_x_square_and_y_square_and_0 = completed_set_of_digits_if_ok(y_square, digits_in_x_square_and_0)
        if not digits_in_x_square_and_y_square_and_0:
            continue
        for z in range(y + 1, limit):
            z_square = z * z
            # digits_in_x_square_and_y_square_and_z_square_and_0 is not None iff all digits in z_square are distinct, distinct to 0,
            # and distinct to all digits in x_square and y_square
            digits_in_x_square_and_y_square_and_z_square_and_0 = completed_set_of_digits_if_ok(z_square, digits_in_x_square_and_y_square_and_0)
            if not digits_in_x_square_and_y_square_and_z_square_and_0:
                continue
            if digits_in_x_square_and_y_square_and_z_square_and_0 != set_of_all_digits:
                continue
            print('{:7d} {:7d} {:7d}'.format(x_square, y_square, z_square))
            nb_of_solutions += 1
print('\nAltogether, {:} solutions have been found.'.format(nb_of_solutions))

