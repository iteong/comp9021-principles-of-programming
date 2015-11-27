# Written by Eric Martin for COMP9021


from binary_tree import *
from math import log


class PriorityQueue(BinaryTree):
    def __init__(self):
        super().__init__()

    def insert(self, value):
        if self.value == None:
            self.value = value
            self.left_node = BinaryTree()
            self.right_node = BinaryTree()
            return
        new_node_nb = self.size() + 1
        level = int(log(new_node_nb, 2))
        nb_of_nodes_on_level = 2 ** level
        first_node_nb_on_level = nb_of_nodes_on_level
        node = self
        ancestor_nodes = [node]
        for i in range(level - 1):
            nb_of_nodes_on_level //= 2
            if new_node_nb < first_node_nb_on_level + nb_of_nodes_on_level:
                node = node.left_node
            else:
                first_node_nb_on_level += nb_of_nodes_on_level
                node = node.right_node
            ancestor_nodes.append(node)
        if new_node_nb == first_node_nb_on_level:
            node.left_node = BinaryTree(value)
            parent_node = node.left_node
        else:
            node.right_node = BinaryTree(value)
            parent_node = node.right_node
        while ancestor_nodes:
            child_node = parent_node
            parent_node = ancestor_nodes.pop()
            if child_node.value < parent_node.value:
                child_node.value, parent_node.value = parent_node.value, child_node.value

