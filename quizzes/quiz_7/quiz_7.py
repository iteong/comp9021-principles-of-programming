# Generates a linked list of an even length of 4 or more, determined by user input,
# and reorders the list so that it starts with the first occurrence
# of the smallest element and repeatively moves backwards by one step and forward
# by three steps, wrapping around when needed.

import sys
from random import seed, randrange
from linked_list import *
from extended_linked_list import ExtendedLinkedList

provided_input = input('Enter 2 integers: ')
provided_input = provided_input.split()
if len(provided_input) != 2:
    print('Incorrect input, giving up.')
    sys.exit()
seed(int(provided_input[0]))
# An even number at least equal to 4
length = (abs(int(provided_input[1])) + 2) * 2

L = [0] * length
for i in range(length):
    L[i] = randrange(100)

LL = ExtendedLinkedList(L)
LL.print()
LL.rearrange()
LL.print()
    

