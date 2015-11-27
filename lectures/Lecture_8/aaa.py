class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None

class LinkedList:
    def __init__(self, data_list = []):
        if not data_list:
            self.head = None
            return # return then no need to put else for next line
        self.head = Node(data_list[0])
        node = self.head
        for e in data_list[1: ]:
            node.next_node = Node(e)
            node = node.next_node
##            new_node = Node(e)
##            node.next_node = new_node
##            node = new_node

    
    def length(self):
        if not self.head:
            return 0 # if head of list is nothing, return 0
        length = 1
        node = self.head
        while node.next_node:
            length += 1
            node = node.next_node
        return length

    def apply_function(self, function):
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def printer(self, separator = ', '):
        if not self.head:
            return
        node = self.head
        print(node.value, sep = '', end = '')
        node = node.next_node
        while node:
            print(separator, node.value, sep = '', end = '')
            node = node.next_node
        print()

    def reverse(self):
        if not self.head or not self.head.next_node:
            return # if list is empty or only 1 element, nothing to do
        node = self.head
        while node.next_node.next_node: # we can use next_node.next_node coz already taken care of list with 1 element
            node = node.next_node
        new_head = node.next_node
        node.next_node = None
        self.reverse()
        new_head.next_node = self.head
        self.head = new_head

    def is_sorted(self, comparison_function):
        if not self.head or not self.head.next_node:
            return True
        node = self.head
        while node.next_node:
            if not comparison_function(node.value, node.next_node.value):
                return False
            node = node.next_node
        return True
                
    def insert_value_before(self, value_1, value_2):
        if not self.head:
            return False
        if self.head.value == value_2:
            new_node = Node(value_1)
            new_node.next_node = self.head
            self.head = new_node
            return True
        node = self.head
        while node.next_node:
            if node.next_node.value == value_2:
                new_node = Node(value_1)
                new_node.next_node = node.next_node
                node.next_node = new_node
                return True
            node = node.next_node
        return False
        


        
