# Generates a list of 20 random integers between 0 and 99,
# prints out the list, computes the maximum element of the list,
# and prints it out.
#
# Written by Eric Martin for COMP9021

from random import randint

# Start with an empty list.
L = []
# Randomly generate 20 integers between 0 and 99, and
# add every new one to the end of the list.
for i in range(20):
    L.append(randint(0, 100))
print('The list is:' , L)
max_element = 0
for i in range(20):
    # If the (i+1)st element in the list, L[i], is greater than
    # the largest number seen before, then L[i] becomes the largest
    # element seen so far, recorded as max_element.
    if L[i] > max_element:
        max_element = L[i]
print('The maximum number in this list is:', max_element)
# Of course there is an easier way; as almost always, python just makes it too easy!
print('Again, the maximum number in this list is:', max(L))
