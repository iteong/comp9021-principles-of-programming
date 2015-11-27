# Finds all sequences of consecutive prime 5-digit numbers,
# say (a, b, c, d, e, f), such that
# b = a + 2, c = b + 4, d = c + 6, e = d + 8, and f = e + 10.
#
# Written by Eric Martin for COMP9021


from math import sqrt


smallest_five_digit_odd_number = 10001
largest_five_digit_odd_number = 99999

print('The solutions are:\n')
# Number of primes found so far
count = 0
# Equal to 0 if first prime in sequence still has to be found;
# otherwise, equal to 1 plus number of odd nonprime numbers seen since last prime
gap = 0
for i in range(smallest_five_digit_odd_number, largest_five_digit_odd_number + 1, 2):
    is_prime = True
    for k in range(3, round(sqrt(i)) + 1, 2):
        if i % k == 0:
            is_prime = False
            break
    if is_prime:
        # First prime in tentative sequence of 6, or
        # new prime at correct distance
        if count == 0 or gap == count:
            count += 1               
            gap = 1
        # New prime y too close to previous one x;
        # x will start a new sequence if y is the third prime in the current sequence,
        # otherwise y will start a new sequence */
        elif count > 2:
            count = gap = 1
        if count == 6:
            print(i - 30, i - 28, i - 24, i - 18, i - 10, i)
    # If in the process of validating a sequence (because count != 0),
    # increases gap by 1 and checks that distance from last prime
    # is not too large---otherwise, next prime will start new sequence */
    elif count:
        gap += 1
        if gap > count:
            count = gap = 0

