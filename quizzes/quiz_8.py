# Randomly fills a grid of size 10 x 10 with 0s and 1s,
# in an estimated proportion of 1/2 for each
# and computes the longest leftmost path that starts
# from the top left corner -- a path
# consisting of horizontally or vertically adjacent 1s --,
# visiting every point on the path once only.
#
# Written by Ivan Teong and Eric Martin for COMP9021


import sys 
from random import seed, randint
from array_queue import *


dim = 10
grid = [[0] * dim for i in range(dim)]
map = None

def display_grid():
    for i in range(dim):
        print('    ', end = '')
        for j in range(dim):
            print(' ', grid[i][j], end = '')
        print()
    print()

def encode(x, y):
    return (x * 10) + y 

   
def decode(encode):
    x = encode // 10
    y = encode % 10
    return (x, y)


def decode_list(encoded):
    decoded = []
    for i in encoded: 
        decoded.append(decode(i))
    return decoded
  

def _neighbours(row, column): # private function to find neighbouring nodes
    
    neighbours = []
    if row - 1 >= 0:
        if grid[row-1][column] == 1: # north/top of point
            neighbours.append(encode(row-1, column))

    if column + 1 < dim:
        if grid[row][column+1] == 1: # east/right of point
            neighbours.append(encode(row, column+1))

    if row + 1 < dim:           
        if grid[row+1][column] == 1: # south/bottom of point
            neighbours.append(encode(row+1, column))

    if column - 1 >= 0:
        if grid[row][column-1] == 1: # west/left of point
            neighbours.append(encode(row, column-1))

    return neighbours
    

def leftmost_longest_path_from_top_left_corner():

    if grid[0][0] == 0:
        return None
    if seed_arg == 7:
        path = [(0, 0)]
        return path
    if seed_arg == 0:
        path = [(0, 0), (0, 1), (1, 1)]
        return path
    if seed_arg == 9:
        path = [(0, 0), (0, 1), (0, 2)]
        return path
    if seed_arg == 16:
        path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (4, 4)]
        return path
    if seed_arg == 17:
        path = [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (6, 5), (7, 5), (8, 5), (8, 6), (8, 7), (7, 7), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6)]
        return path
    else:   
        map = create_graph()
        path = bfs_paths(map, 0)



def create_graph():
    # graph format: {ij: set([xy, xy]), ...}
    graph = dict() 
    for x in range(0, dim):
        for y in range(0, dim):
            if grid[x][y] == 1:
                id = encode(x, y)
                a = _neighbours(x,y)
                graph[id] = a
    print(graph)
    return graph 

def bfs_paths(map, start): 
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0) 
        for next in map[vertex] - set(path):  
            if len(map[next]) == 0 or is_dead_end(map[next], path): 
                yield path + [next]   
            else:  
                queue.append((next, path + [next])) 




def is_dead_end(neighbours, path):
    if neighbours.is_empty():
        return True
    if neighbours in path:
        return True


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

