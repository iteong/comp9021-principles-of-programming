# Reads from a file named tree.txt, containing numbers expected to be organised as a tree,
# a number at a depth of N in the tree being preceded with N tabs in the file.
# The file can also contain any number of lines with nothing but blank lines.
# Uses the module general_tree.py to build the tree represented in the file
# (outputs an error message in case the representation is incorrect),
# and prints it out using the same representation as in the file.
#
# Written by Eric Martin for COMP9021


import sys
from general_tree import *


def generate_nonblank_lines(input_file):
    nonblank_lines = []
    for line in input_file:
        line = line.rstrip()
        if line:
            nonblank_lines.append(line)
    nonblank_lines.reverse()
    return nonblank_lines

def number_of_leading_tabs(line):
    count = 0
    while count < len(line) and line[count] == '\t':
        count += 1
    return count

def build_tree(input_file):
    lines = generate_nonblank_lines(input_file)
    if not lines or number_of_leading_tabs(lines[-1]):
        return None
    tree = _build_tree(lines, 0)
    if not tree or lines:
        return None
    return tree

def _build_tree(lines, level):
    line = lines.pop()
    try:
        value = int(line[level: ])
    except:
        return None
    tree = GeneralTree(value)   
    while lines:
        next_line_level = number_of_leading_tabs(lines[-1])
        if next_line_level > level + 1:
            return None
        if next_line_level == level + 1:
            tree.children.append(_build_tree(lines, level + 1))
        else:
            return tree
    return tree
                
def print_out(tree):
    _print_out(tree, 0)

def _print_out(tree, level):
    print('\t' * level, end = '')
    print(tree.value)
    for subtree in tree.children:
        _print_out(subtree, level + 1)
        
        
try:
    input_file = open('tree.txt', 'r')
except:
    print('Sorry, could not open file tree.txt.')
    sys.exit()
    
tree = build_tree(input_file)
if not tree:
    print('tree.txt does not contain the correct representation of a tree.')
    sys.exit()
print_out(tree)


