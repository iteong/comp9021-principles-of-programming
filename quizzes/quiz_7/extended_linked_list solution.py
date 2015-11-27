# Written by Eric Martin for COMP9021

from linked_list import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        node = self.head
        length = 1
        index_of_smallest_value = 0
        smallest_value = node.value
        while node.next_node:
            node = node.next_node
            if node.value < smallest_value:
                smallest_value = node.value
                index_of_smallest_value = length
            length += 1
        # We link the last node to the first one and create a loop.
        node.next_node = self.head
        index_of_to_be_second_node = (index_of_smallest_value - 1) % length
        node = self.head
        while index_of_to_be_second_node:
            node = node.next_node
            index_of_to_be_second_node -= 1
        previous_node = node
        current_node = self.head = previous_node.next_node
        nb_of_iterations = (length - 1) // 2
        while nb_of_iterations:
            next_previous_node = current_node.next_node
            current_node.next_node = previous_node
            current_node = next_previous_node.next_node
            previous_node.next_node = current_node
            previous_node = next_previous_node
            nb_of_iterations -= 1
        current_node.next_node = previous_node
        previous_node.next_node = None
    
    
    
