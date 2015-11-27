# Prompts the user for a word and a nonnegative integer d and outputs the list of
# all subwords of the word of depth d.
#
# Written by Eric Martin for COMP9021

import sys


def extract_subwords(word, depth):
    if not depth:
        return [word]
    subwords = []
    subword = ''
    count_of_non_closed_opening_parentheses = 0
    for c in word:
        if c == ' ' or c == '\t':
            continue
        elif c == ',':
            if count_of_non_closed_opening_parentheses == depth:
                subwords.append(word)
                word = ''
            else:
                word += ','
        elif c == '(':
            count_of_non_closed_opening_parentheses += 1
            if count_of_non_closed_opening_parentheses == depth:
                word = ''
            elif count_of_non_closed_opening_parentheses > depth:
                word += c
        elif c == ')':
            if count_of_non_closed_opening_parentheses == depth:
                subwords.append(word)
            elif count_of_non_closed_opening_parentheses > depth:
                word += c
            count_of_non_closed_opening_parentheses -= 1
        else:
            word += c
    return subwords



word = input('Enter a word: ')
try:
    depth = int(input('Enter a nonnegative integer: '))
    if depth < 0:
        raise Exception
except:
    print('Incorrect input, giving up.')
    sys.exit()


print('The subwords of "{:}" of depth {:} are:\n    {:}'.format(word, depth, extract_subwords(word, depth)))
