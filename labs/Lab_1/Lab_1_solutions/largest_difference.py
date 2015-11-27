# Generates a list of 10 random integers between -50 and 50, prints out the list,
# computes the maximum difference between 2 successive elements in the list, and prints it out.
#
# Written by Eric Martin for COMP9021

from random import randint

L = []
for i in range(10):
    L.append(randint(-50, 50))
print('The list is:' , L)
max_difference = -100
for i in range(9):
    difference = L[i + 1] - L[i]
    if difference > max_difference:
        max_difference = difference
print('The maximum difference between successive numbers in this list is:', max_difference)
