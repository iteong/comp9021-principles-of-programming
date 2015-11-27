# Cryptarithm solver.
#
# Written by Eric Martin for COMP9021


def solve(cryptarithm):
    letters_starting_a_word = set()
    letters_not_starting_a_word = set()
    in_word = False
    for c in cryptarithm:
        if str.isalpha(c):
            if not in_word:
                letters_starting_a_word.add(c)
                in_word = True
            else:
                letters_not_starting_a_word.add(c)
        else:
            in_word = False
    letters_not_starting_a_word -= letters_starting_a_word
    all_letters_with_those_starting_a_word_last = ''.join(letters_not_starting_a_word) + ''.join(letters_starting_a_word)
    if len(all_letters_with_those_starting_a_word_last) > 10:
        print('There are more than 10 letters, this is not a valid cryptarithm.')
        return
    for possible_solution in generate_possible_solutions(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                                                         len(letters_starting_a_word), len(letters_not_starting_a_word)):
        equation = cryptarithm.translate(str.maketrans(all_letters_with_those_starting_a_word_last, possible_solution))
        try:
            if eval(equation): 
                print(equation)
        except ArithmeticError:
            pass
        except:
            print('Incorrect expression, this is not a valid cryptarithm.')
            return


# Permutes the last "length" members of L, using the last "size" members of L,
# the first of which is at index "start".
# Assumes that "length" is at most equal to "size" - 1
# (it could be equal to "size", but if "size" - 1 elements
# are determined, then the last one is determined too).
def permute(L, start, size, length):
    if length == 0:
        yield L
        if size > 1:
            # "Simulates" the permutation of the "size" first elements
            # by computing what would be the last permutation.
            if size % 2 or size == 2:
               L[start], L[start + size - 1] = L[start + size - 1], L[start]
            elif size == 4:
                L[start: start + 3], L[start + 3] = L[start + 1: start + 4], L[start]
            else:
                L[start: start + 2], L[start + 2: start + size - 2], L[start + size - 2], L[start + size - 1] = \
                         L[start + size - 3: start + size - 1], L[start + 1: start + size - 3], L[start + size - 1], L[start]
    else:
        size -= 1
        length -= 1
        for i in range(size):
            for L in permute(L, start, size, length):
                yield L
            if size % 2:
                L[start + i], L[start + size] = L[start + size], L[start + i]
            else:
                L[start], L[start + size] = L[start + size], L[start]
        for L in permute(L, start, size, length):
            yield L


# Generates all sequences of distinct digits of the form "sigma tau"
# with tau of length size1 and sigma of length size2,
# and with no occurrence of 0 in tau.
def generate_possible_solutions(L, size1, size2):
    adjusted_size2 = size2
    # Once nonzero digits have been allocated to all letters starting a word,
    # if all digits that remain have to be used for the letters not starting a word,
    # then there is no need to allocate the last one
    # once all others have been allocated.
    if size2 == 10 - size1:
        adjusted_size2 -= 1
    adjusted_size1 = size1
    # If all nonzero digits have to be used for the letters starting a word,
    # then there is no need to allocate the last one
    # once all others have been allocated.
    if size1 == 9:
        adjusted_size1 -= 1
    start = 10 - size1 - size2
    for L in permute(L, 1, 9, adjusted_size1):
        L1 = list(L)
        for L1 in permute(L1, 0, 10 - size1, adjusted_size2):
            yield ''.join(L1[start:])


def solve_cryptarithm_selection():
    for cryptarithm in ['SEND + MORE == MONEY',
                        'VIOLIN * 2 + VIOLA == TRIO + SONATA',
                        'SEND + A + TAD + MORE == MONEY',
                        'ZEROES + ONES == BINARY',
                        'DCLIZ + DLXVI == MCCXXV',
                        'COUPLE + COUPLE == QUARTET',
                        'FISH + N + CHIPS == SUPPER',
                        'SATURN + URANUS + NEPTUNE + PLUTO == PLANETS',
                        'EARTH + AIR + FIRE + WATER == NATURE',
                       ('AN + ACCELERATING + INFERENTIAL + ENGINEERING + TALE + ' +
                        'ELITE + GRANT + FEE + ET + CETERA == ARTIFICIAL + INTELLIGENCE'),
                        'TWO * TWO == SQUARE',
                        'HIP * HIP == HURRAY',
                        'PI * R ** 2 == AREA',
                        'NORTH / SOUTH == EAST / WEST',
                        'NAUGHT ** 2 == ZERO ** 3',
                        'I + THINK + IT + BE + THINE == INDEED',
                        'DO + YOU + FEEL == LUCKY',
                        'NOW + WE + KNOW + THE == TRUTH',
                        'SORRY + TO + BE + A + PARTY == POOPER',
                        'SORRY + TO + BUST + YOUR == BUBBLE',
                        'STEEL + BELTED == RADIALS',
                        'ABRA + CADABRA + ABRA + CADABRA == HOUDINI',
                        'I + GUESS + THE + TRUTH == HURTS',
                        'LETS + CUT + TO + THE == CHASE',
                        'THATS + THE + THEORY == ANYWAY',
                        '1/(2*X-Y) == 1']:
        print(cryptarithm)
        solve(cryptarithm)
        print()
