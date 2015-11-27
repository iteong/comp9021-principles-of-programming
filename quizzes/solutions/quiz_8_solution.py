# Randomly fills a grid of size 10 x 10 with 0s and 1s,
# in an estimated proportion of 1/2 for each
# and computes the longest leftmost path that starts
# from the top left corner -- a path
# consisting of horizontally or vertically adjacent 1s --,
# visiting every point on the path once only.
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, randint
from array_queue import *


dim = 10
grid = [[0] * dim for i in range(dim)]

def display_grid():
    for i in range(dim):
        print('    ', end = '')
        for j in range(dim):
            print(' ', grid[i][j], end = '')
        print()
    print()

def leftmost_longest_path_from_top_left_corner():
    directions = {'N': (-1, 0),'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    next_directions = {'': ('S', 'E'), 'N': ('E', 'N', 'W'), 'S': ('W', 'S', 'E'), 'E': ('S', 'E', 'N'), 'W': ('N', 'W', 'S')}
    if not grid[0][0]:
        return []
    paths = ArrayQueue()
    paths.enqueue(([(0, 0)], ''))
    while not paths.is_empty():
        (path, previous_direction) = paths.dequeue()
        current_position = path[-1]
        for new_direction in next_directions[previous_direction]:
            new_position = (current_position[0] + directions[new_direction][0],
                            current_position[1] + directions[new_direction][1])
            if new_position[0] not in range(dim) or new_position[1] not in range(dim):
                continue
            if new_position in path:
                continue
            if not grid[new_position[0]][new_position[1]]:
                continue
            path_copy = list(path)
            path_copy.append(new_position)
            paths.enqueue((path_copy, new_direction))
    return path

provided_input = input('Enter one integer: ')
try:
    seed_arg = int(provided_input)
except:
    print('Incorrect input, giving up.')
    sys.exit()
    
seed(seed_arg)
# We fill the grid with randomly generated 0s and 1s,
# with for every cell, a probability of 1/2 to generate a 0.
for i in range(dim):
    for j in range(dim):
        grid[i][j] = randint(0, 1)
print('Here is the grid that has been generated:')
display_grid()

path = leftmost_longest_path_from_top_left_corner()
if not path:
    print('There is no path from the top left corner')
else:
    print('The leftmost longest path from the top left corner is {:})'.format(path))
           
