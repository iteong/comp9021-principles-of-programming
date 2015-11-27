# Generates a list of 10 random numbers between -19 and 19 included,
# and determines the two largest (distinct) strictly negative and
# the two smallest (distinct) strictly positive elements in the list.
#
# Writtten by Ivan Teong (z3386180) and Eric Martin for COMP9021


import sys
from random import seed, randint


nb_of_elements = 10

if len(sys.argv) != 2:
    print('Provide one and only only command line argument')
    sys.exit()
try:
    seed(int(sys.argv[1]))
except:
    print('The command line argument should be an integer.')
    sys.exit()

L = [None] * nb_of_elements
for i in range(nb_of_elements):
    L[i] = randint(-19, 19)
print('The generated list is:', L)

first_max_negative_element = None
second_max_negative_element = None
first_min_positive_element = None
second_min_positive_element = None

# Ivan's Code

if L:
    L.sort()
    last = L[-1]
    for i in range(len(L)-2, -1, -1):
        if last == L[i]:
            del L[i]
        else:
            last = L[i]
print('Sorted list without duplicates from most negative to most positive:', L)

def splitPosNonPos():
    posList=[]
    nonPosList=[]
    for z in L:
        if z > 0:
            posList.append(z)
        elif z < 0:
            nonPosList.append(z)

    return (posList, nonPosList)

posList, nonPosList = splitPosNonPos()

first_min_positive_element = posList[:1];
second_min_positive_element = posList[1:2]

first_max_negative_element = nonPosList[-1:];
second_max_negative_element = nonPosList[-2:-1]

# End of Ivan's Code

if not first_max_negative_element:
    print('There is no stricly negative integer.')
else:
    if not second_max_negative_element:
        print('There is only one strictly negative integer, {:}.'.format(first_max_negative_element))
    else:
        print('The largest and second largest strictly negative integers are ' +
              '{:} and {:}.'.format(first_max_negative_element, second_max_negative_element))
if not first_min_positive_element:
    print('There is no stricly positive integer.')
else:
    if not second_min_positive_element:
        print('There is only one strictly positive integer, {:}.'.format(first_min_positive_element))
    else:
        print('The smallest and second smallest strictly positive integers are ' +
              '{:} and {:}.'.format(first_min_positive_element, second_min_positive_element))
