# Cryptarithm solver.
#
# Essentially written by Raymond Hettinger as part of ActiveState Code Recipes


from re import findall
from itertools import permutations


def solve(cryptarithm):
    words = findall('[A-Za-z]+', cryptarithm)
    all_letters = set(''.join(words))
    if len(all_letters) > 10:
        print('There are more than 10 letters, this is not a valid cryptarithm.')
        return
    letters_starting_a_word = set(w[0] for w in words)
    all_letters_with_those_starting_a_word_first = ''.join(letters_starting_a_word) + ''.join(all_letters - letters_starting_a_word)
    number_of_letters_starting_a_word = len(letters_starting_a_word)
    for possible_solution in permutations('0123456789', len(all_letters)):
        if '0' not in possible_solution[:number_of_letters_starting_a_word]:
            equation = cryptarithm.translate(str.maketrans(all_letters_with_those_starting_a_word_first, ''.join(possible_solution)))
            try:
                if eval(equation):
                    print(equation)
            except ArithmeticError:
                pass
            except:
                print('Incorrect expression, this is not a valid cryptarithm.')
                return


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
