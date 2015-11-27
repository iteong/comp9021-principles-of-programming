# Randomly generates a binary search tree with values from 0 up to 9,
# and displays it growing south (changing the perspective of left and right...).
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, choice
from binary_tree import *

def print_tree_without_causing_torticollis(tree):
    if tree.value == None:
        return
    height = tree.height()
    for n in range(height + 1):
        print_row(tree, 0, n, height)
        print()


def print_row(tree, i, n, height):
    if i == n:
        if tree == None or tree.value == None:
            print(' ' * (2 ** (height - n + 1) - 1), end = '')
        else:
            print(' ' * (2 ** (height - n) - 1), end = '')
            print(tree.value, end = '')
            print(' ' * (2 ** (height - n) - 1), end = '')
    else:
        if tree == None:
            print_row(None, i + 1, n, height)
            print(' ', end = '')
            print_row(None, i + 1, n, height)
        else:
            print_row(tree.left_node, i + 1, n, height)
            print(' ', end = '')
            print_row(tree.right_node, i + 1, n, height)        
        

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
