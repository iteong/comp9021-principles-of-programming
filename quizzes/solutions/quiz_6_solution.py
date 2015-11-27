# Randomly fills a grid of size 10 x 10 with 0s and 1s
# and computes the number of paths that go from from a point (x1, y1)
# to a point (x2, y2) -- a path consisting of horizontally or
# vertically adjacent 1s --, visiting every point on the path once only.

# Written by Eric Martin for COMP9021


import sys
from random import seed, randint


dim = 10
grid = [[0] * dim for i in range(dim)]

def display_grid():
    for i in range(dim):
        print('    ', end = '')
        for j in range(dim):
            print(' ', grid[i][j], end = '')
        print()
    print()

def number_of_paths_from_to_of_length(x1, y1, x2, y2, length):
    if x1 < 0 or x1 >= dim or y1 < 0 or y1 >= dim or not grid[x1][y1]:
        return 0
    if length == 0:
        if x1 == x2 and y1 == y2:
            return 1
        return 0
    grid[x1][y1] = 0
    nb_of_paths = number_of_paths_from_to_of_length(x1 + 1, y1, x2, y2, length - 1) + \
        number_of_paths_from_to_of_length(x1 - 1, y1, x2, y2, length - 1) + \
        number_of_paths_from_to_of_length(x1, y1 - 1, x2, y2, length - 1) + \
        number_of_paths_from_to_of_length(x1, y1 + 1, x2, y2, length - 1)
    grid[x1][y1] = 1
    return nb_of_paths

provided_input = input('Enter 7 integers,\n'
                       '  the second and third ones being nonnegative,\n'
                       '  the last 4 beeing between 0 and 9: ')
provided_input = provided_input.split()
if len(provided_input) != 7:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    (seed_arg, density, length, x1, y1, x2, y2) = (int(i) for i in provided_input)
    if density < 0 or length < 0:
        raise ValueError
    if {x1, y1, x2, y2} - set(range(dim)):
        raise ValueError        
except:
    print('Incorrect input, giving up.')
    sys.exit()

seed(seed_arg)
# We fill the grid with randomly generated 0s and 1s,
# with for every cell, a probability of 1/(density + 1) to generate a 0.
for i in range(dim):
    for j in range(dim):
        grid[i][j] = int(randint(0, density) != 0)
print('Here is the grid that has been generated:')
display_grid()

nb_of_paths = number_of_paths_from_to_of_length(x1, y1, x2, y2, length)
if nb_of_paths:
    print('Number of paths of length {:} that connect ({:}, {:}) to ({:}, {:}): {:}'.format(length, x1, y1, x2, y2, nb_of_paths))
else:
    print('No path of length {:} connects ({:}, {:}) to ({:}, {:})'.format(length, x1, y1, x2, y2))        
