# From general trees to binary trees.
#
# Written by Eric Martin for COMP9021

from binary_tree import *

class GeneralTree:
    def __init__(self, value = None):
        self.value = value
        self.children = []

    def set_children(self, children):
        if self.value == None:
            return
        self.children = children

    def leftmost_child_right_sibbling_equivalent(self):
        if self.value == None:
            return BinaryTree()        
        tree = BinaryTree(self.value)
        if self.children:
            tree.left_node = self.children[0].leftmost_child_right_sibbling_equivalent()
            current_subtree = tree.left_node
            for child in self.children[1: ]:
                current_subtree.right_node = child.leftmost_child_right_sibbling_equivalent()
                current_subtree = current_subtree.right_node
        return tree

if __name__ == '__main__':
    t_1 = GeneralTree(1)                
    t_2 = GeneralTree(2)                
    t_3 = GeneralTree(3)                
    t_4 = GeneralTree(4)                
    t_5 = GeneralTree(5)                
    t_6 = GeneralTree(6)                
    t_7 = GeneralTree(7)                
    t_8 = GeneralTree(8)
    t_2.set_children([t_5, t_6])
    t_3.set_children([t_7, t_8])
    t_1.set_children([t_2, t_3, t_4])
    t = t_1.leftmost_child_right_sibbling_equivalent()
    t.print_binary_tree()
                
        

    
        
