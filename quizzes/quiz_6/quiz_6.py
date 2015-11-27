# Randomly fills a grid of size 10 x 10 with 0s and 1s
# and computes the number of paths that go from from a point (x1, y1)
# to a point (x2, y2) -- a path consisting of horizontally or
# vertically adjacent 1s --, visiting every point on the path once only.
#
# Written by Ivan Teong and Eric Martin for COMP9021


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
    count = 0

    if length == 0: # check at the beginning every time whether it has reached goal state
        if x1 == x2 and y1 == y2:
            return 1 # path is 1 when the values of original and goal positions the same
        else:
            return 0
    
    if y1 - 1 >= 0 and grid[x1][y1 - 1] == 1: # will only move if firstly, it is still within the grid
                                              # at the left side after minusing 1 and there is a 1 at left
                                              # there is no y1[-1] as it will be outside the grid
        grid[x1][y1] = 0 # set original position to 0 so it cannot move back to previous position
        count += number_of_paths_from_to_of_length(x1, y1 - 1, x2, y2, length - 1) # accumulates paths
        grid[x1][y1] = 1 # set original position to 1 after moved to new position
        
    if x1 + 1 <= 9 and grid[x1 + 1][y1] == 1: # will only move if firstly, it is still within the grid range
                                              # at the right side after adding 1 and there is a 1 below
        grid[x1][y1] = 0
        count += number_of_paths_from_to_of_length(x1 + 1, y1, x2, y2, length - 1)
        grid[x1][y1] = 1
        
    if y1 + 1 <= 9 and grid[x1][y1 + 1] == 1:
        grid[x1][y1] = 0
        count += number_of_paths_from_to_of_length(x1, y1 + 1, x2, y2, length - 1)
        grid[x1][y1] = 1
        
    if x1 - 1 >= 0 and grid[x1 - 1][y1] == 1:
        grid[x1][y1] = 0
        count += number_of_paths_from_to_of_length(x1 - 1, y1, x2, y2, length - 1)
        grid[x1][y1] = 1
        
    return count


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
           
