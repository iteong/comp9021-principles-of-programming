# Written by Ivan Teong for COMP9021


from binary_tree import *
from math import log


class PriorityQueue(BinaryTree):
    def __init__(self):
        super().__init__()

    def insert(self, value, parent = None):
        if not parent: # remember self as parent
            parent = self
            
        if self.value == None:
            self.value = value
            self.left_node = PriorityQueue()
            self.right_node = PriorityQueue()
            self._bubble_up(parent)  # check if need to swap value: if parent > child, swap value so that parent < child
            return True
        
# Check any branch is full by seeing if n = 2**h - 1 is true; where n = tree size of branch and
# h = tree height of the branch, changed to height() + 1 = log(size() + 1, 2) for this program

        if self.left_node.size() == 0 and self.right_node.size() == 0: # if both nodes are empty, insert into left node
            self.left_node.insert(value, self) # self takes place of parent
            return False

        else: # if both nodes are not empty

            # if both left and right nodes are full and have the same tree size (same number of nodes on either side), insert into left node
            if self.left_node.height() + 1 == log(self.left_node.size() + 1, 2) and (self.right_node.height() + 1) == log(self.right_node.size() + 1, 2) and self.left_node.size() == self.right_node.size():
                self.left_node.insert(value, self)
                return False

            # if left node is not full, insert into left node
            if self.left_node.height() + 1 != log(self.left_node.size() + 1, 2):
                self.left_node.insert(value, self)
                return False

        self.right_node.insert(value, self)


    def _bubble_up(self, parent = None):
        if not parent or self.value > parent.value:
            return True
        self.value, parent.value = parent.value, self.value
                

