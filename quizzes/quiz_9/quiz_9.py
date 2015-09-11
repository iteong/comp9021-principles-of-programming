# Randomly generates a binary search tree with values from 0 up to 9,
# and displays it growing south (changing the perspective of left and right...).
#
# Written by Ivan Teong and Eric Martin for COMP9021


import sys
from random import seed, choice
from binary_tree import *

def print_tree_without_causing_torticollis(tree):
    height = tree.height()
    for d in range(1, height + 2): # height + 2 coz it goes to left child then root, so want them to transverse down to no child when at leaf node (last row)
        _printGivenLevel(tree, d, height, True) # start with first left
        print()

# Level Order Tree Traversal: http://www.geeksforgeeks.org/level-order-tree-traversal/

def _printGivenLevel(tree, level, h, left):
    space = ' ' * (2 * ((2**h) - 1) + 1) # + 1 for the value directly above (the root)

    if left: # if node is left most is True
        space = ' ' * ((2**h) - 1)

    if tree == None:
        if level >= 1:
            print(space,' ', sep='', end = '')
            # seeding tree shape from leftmost node with spaces
            if level > 1 and left == True:
                print(' ' * (level-1), sep='', end = '')
        return

    if level == 1 and tree.value != None:
        print(space, tree.value, sep = '', end = '')
    # replace empty child node with empty string
    if level == 1 and tree.value == None:
        tree.value = ' '
        print(space, tree.value, sep = '', end = '')
    elif level > 1:
        _printGivenLevel(tree.left_node, level-1, h-1, left) # most left node
        _printGivenLevel(tree.right_node, level-1, h-1, False)
        
        
provided_input = input('Enter two integers, the second one nonnegative and at most equal to 10: ')
provided_input = provided_input.split()
if len(provided_input) != 2:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    seed_arg = int(provided_input[0])
    nb_of_nodes = int(provided_input[1])
    if nb_of_nodes < 0 or nb_of_nodes > 10:
        raise ValueError
except:
    print('Incorrect input, giving up.')
    sys.exit()

seed(seed_arg)
data_pool = list(range(nb_of_nodes))
tree = BinaryTree()
for i in range(nb_of_nodes):
    datum = choice(data_pool)
    tree.insert_in_bst(datum)
    data_pool.remove(datum)
print('Brought to you by quiz 9 for the comfort of your neck:')
print_tree_without_causing_torticollis(tree)
           
    
