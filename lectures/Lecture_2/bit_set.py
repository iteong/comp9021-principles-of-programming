# Encoding the set of (distinct) nonnegative integers {n_1, ..., n_k}
# as 2^{n_1} + ... + 2^{n_k}, provides:
# - a function to display a set encoded by a given nonnegative integer,
# - a function to encode a given set of nonnegative integers,
# - a function to check if a given nonnegative integer is a member of a set
#   encoded by a given nonnegative integer,
# - a function to compute the cardinality of a set encoded by a given nonnegative integer.
#
# Written by Eric Martin for COMP9021


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

def encoded_set(set_of_nonnegative_integers):
    encoding = 0
    for i in set_of_nonnegative_integers:
        encoding += 1 << i
    return encoding

def is_in_encoded_set(nonnegative_integer, encoded_set):
    return 1 << nonnegative_integer & encoded_set != 0

def cardinality(encoded_set):
    nb_of_elements = 0
    while encoded_set:
        if encoded_set % 2:
            nb_of_elements += 1
        encoded_set //= 2
    return nb_of_elements


if __name__ == '__main__':
    display_encoded_set(76)
    print(encoded_set({2, 3, 6}))
    print('3 is in {2, 3, 6}:', is_in_encoded_set(3, 76))
    print('7 is in {2, 3, 6}:', is_in_encoded_set(7, 76))
    print('Cardinality of {2, 3, 6}:', cardinality(76))
    
