# Takes as command line arguments:
# - a nonnegative integer max_element
# - a nonnegative integer encoded_set at most equal to 2 ** max_element - 1,
#   so a number which encodes a set S of numbers between 0 and max_element - 1, and
# - an integer rotation,
# and determines the number that encodes the set obtained from S by rotating all elements rotation
# times to the right or to the left, depending on whether rotation is positive or negative, respectively,
# with max_element - 1 becoming 0 when rotated to the right,
# and 0 becoming max_element - 1 when rotated to the left.
#
# Writtten by Eric Martin for COMP9021


import sys


two_to_the_power_20 = 1048576

def display_encoded_set(encoded_set):
    print('{', end = '')
    i = 0
    if encoded_set:
        while encoded_set % 2 == 0:
            encoded_set //= 2
            i += 1
        print(i, end = '')
        encoded_set //= 2
        i += 1
    while encoded_set:
        if encoded_set % 2:
            print(',', i, end = '')
        encoded_set //= 2
        i += 1
    print('}')

if len(sys.argv) != 4:
    print('Provide exactly three command line arguments')
    sys.exit()
try:
    max_element = int(sys.argv[1])
    if max_element < 0:
        raise Exception
except:
    print('The first command line argument should be a nonnegative integer.')
    sys.exit()
try:
    encoded_set = int(sys.argv[2])
    if encoded_set < 0 or encoded_set >= 2 ** max_element:
        raise Exception
except:
    print('The second command line argument should be an integer between 0 and 2**{:} - 1.'.format(max_element))
    sys.exit()
try:
    rotation = int(sys.argv[3])
except:
    print('The third command line argument should be an integer.')
    sys.exit()

print('The encoded set is: ', end = '')
display_encoded_set(encoded_set)

if roration:
    rotation %= max_element
rotated_encoded_set = encoded_set << rotation & 2 ** max_element - 1 | (encoded_set & 2 ** max_element - 1) >> max_element - rotation
    
print('The rotated encoded set is: ', end = '')
display_encoded_set(rotated_encoded_set)

    
