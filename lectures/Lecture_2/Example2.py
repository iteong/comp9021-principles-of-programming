from math import ceil, sqrt

#ceiling rounding up to integer
upper_bound = ceil(sqrt(9876532))

def ok(number, set_of_digits):
    while number:
        d = number % 10
        if d not in set_of_digits:
            set_of_digits.add(d)
        else:
            return None
        number //= 10  # number = number // 10
    return set_of_digits

            
#getting empty set and every new digit and not old digit besides zero to add at the back

for i in range(1, upper_bound):
    i_square = i * i
    digits_in_i_square = ok(i_square)
    if digits_in_i_square:
        for j in range(i + 1, upper_bound):
            j_square = j * j
            digits_in_i_square
            digits_in_i_square_and_j_square = ok(i_square, digits_in_i_square)
                
    


