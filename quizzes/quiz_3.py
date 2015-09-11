# Prompts the user for a word and a nonnegative integer d and outputs the list of
# all subwords of the word of depth d.
#
# Written by Ivan Teong and Eric Martin for COMP9021

import sys


def extract_subwords(word, depth):
    word = ''.join(word.split())
    list_of_tokens = []
    token = ''
    count_of_nonclosed_opening_parentheses = 0
    for c in word:
        if c == ',':
            if count_of_nonclosed_opening_parentheses == depth:
                list_of_tokens.append(token)
                token = ''
            else:
                if count_of_nonclosed_opening_parentheses >= depth:
                    token += ','
        elif c == '(':
            if count_of_nonclosed_opening_parentheses >= depth:
                token += '('
            count_of_nonclosed_opening_parentheses += 1
        elif c == ')':
            if count_of_nonclosed_opening_parentheses == depth:
                list_of_tokens.append(token)
                token = ''
            count_of_nonclosed_opening_parentheses -= 1
            if count_of_nonclosed_opening_parentheses >= depth:
                token += ')'
        else:
            if count_of_nonclosed_opening_parentheses >= depth:
                token += c
    if depth == 0:
        list_of_tokens.append(token)
    return list_of_tokens


word = input('Enter a word: ')
try:
    depth = int(input('Enter a nonnegative integer: '))
    if depth < 0:
        raise Exception
except:
    print('Incorrect input, giving up.')
    sys.exit()


print('The subwords of "{:}" of depth {:} are:\n    {:}'.format(word, depth, extract_subwords(word, depth)))
