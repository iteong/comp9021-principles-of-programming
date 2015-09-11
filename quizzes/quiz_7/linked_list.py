# A Linked List abstract data type
#
# Written by Eric Martin for COMP9021


class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None


class LinkedList:
    # Creates a linked list possibly from a list of values.
    def __init__(self, L = None):
        if not L:
            self.head = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1: ]:
            node.next_node = Node(e)
            node = node.next_node

    def print(self, separator = ', '):
        if not self.head:
            return
        node = self.head
        print(node.value, end = '')
        node = node.next_node
        while node:
            print(separator, node.value, sep = '', end = '')
            node = node.next_node
        print()

    def duplicate(self):
        if not self.head:
            return None
        node = self.head
        node_copy = Node(node.value)
        LL = LinkedList()
        LL.head = node_copy
        node = node.next_node
        while node:
            node_copy.next_node = Node(node.value)
            node_copy = node_copy.next_node
            node = node.next_node
        return LL

    def length(self):
        if not self.head:
            return 0
        node = self.head
        length = 1
        node = node.next_node
        while node:
            length +=1
            node = node.next_node
        return length

    def apply_function(self, function):
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def is_sorted(self, comparison_function = lambda x, y: x <= y):
        node = self.head
        while node and node.next_node:
            if not comparison_function(node.value, node.next_node.value):
                return False
            node = node.next_node
        return True

    def extend(self, LL):
        if not self.head:
            self.head = LL.head
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = LL.head

    def reverse(self):
        if not self.head or not self.head.next_node:
            return
        node = self.head
        while node.next_node.next_node:
            node = node.next_node
        last_node = node.next_node
        node.next_node = None
        self.reverse()
        last_node.next_node = self.head
        self.head = last_node

    def index_of_value(self, value):
        index = 0
        node = self.head
        while node:
            if node.value == value:
                return index
            index += 1
            node = node.next_node
        return -1

    def value_at(self, index):
        if index < 0:
            return None
        node = self.head
        while node and index:
            node = node.next_node
            index -= 1
        if node and index == 0:
            return node.value
        return None

    def prepend(self, LL):
        if not LL.head:
            return
        node = LL.head
        while node.next_node:
            node = node.next_node
        node.next_node = self.head
        self.head = LL.head
            
    def append(self, value):
        if not self.head:
            self.head = Node(value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = Node(value)

    def insert_value_at(self, value, index):
        new_node = Node(value)
        if index <= 0:
            new_node.next_node = self.head
            self.head = new_node
            return
        if not self.head:
            self.head = new_node
        node = self.head
        while node.next_node and index > 1:
            node = node.next_node
            index -= 1
        next_node = node.next_node
        node.next_node= new_node
        new_node.next_node = next_node

    def insert_value_before(self, value_1, value_2):
        if not self.head:
            return False
        if self.head.value == value_2:
            self.insert_value_at(value_1, 0)
            return True
        node = self.head
        while node.next_node and node.next_node.value != value_2:
            node = node.next_node
        if not node.next_node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node = new_node
        return True

    def insert_value_after(self, value_1, value_2):
        if not self.head:
            return False
        node = self.head
        while node and node.value != value_2:
            node = node.next_node
        if not node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node = new_node
        return True

    def insert_sorted_value(self, value, comparison_function = lambda x, y: x <= y):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if comparison_function(value, self.head.value):
            new_node.next_node = self.head
            self.head = new_node
            return
        node = self.head
        while node.next_node and comparison_function(node.next_node.value, value):
            node = node.next_node
        new_node.next_node = node.next_node
        node.next_node = new_node

    def delete_value(self, value):
        if self.head and self.head.value == value:
            self.head = self.head.next_node
            return True
        node = self.head
        while node.next_node and node.next_node.value != value:
            node = node.next_node
        if node.next_node:
            node.next_node = node.next_node.next_node
            return True
        return False
            

if __name__ == '__main__':
    LL = LinkedList([2, 0, 1, 3, 7])
    LL.print(separator = ' : ')
    LL_copy = LL.duplicate()    
    LL_copy.print()
    print(LL.length())
    LL.apply_function(lambda x: 2 * x)
    LL.print()
    print(LL.is_sorted(lambda x, y: x <= y))
    LL.extend(LL_copy)
    LL.print()
    LL.reverse()
    LL.print()
    print(LL.index_of_value(2))
    print(LL.index_of_value(5))
    print(LL.value_at(4))
    print(LL.value_at(10))
    LL.prepend(LinkedList([20, 21, 22]))
    LL.print()
    LL_1 = LinkedList()
    LL_1.print()
    LL_1.append(10)
    LL_1.print()
    LL_1.append(15)
    LL_1.print()
    LL_1.insert_value_at(5, 0)
    LL_1.insert_value_at(25, 3)
    LL_1.insert_value_at(20, 3)
    LL_1.print()
    LL_1.insert_value_before(0, 5)
    LL_1.insert_value_before(30, 35)
    LL_1.insert_value_before(22, 25)
    LL_1.insert_value_before(7, 10)
    LL_1.print()
    LL_1.insert_value_after(3, 1)
    LL_1.insert_value_after(2, 0)
    LL_1.insert_value_after(12, 10)
    LL_1.insert_value_after(27, 25)
    LL_1.print()
    LL_1.insert_sorted_value(-5)
    LL_1.insert_sorted_value(17)
    LL_1.insert_sorted_value(30)
    LL_1.print()
    LL_1.delete_value(-5)
    LL_1.delete_value(30)
    LL_1.delete_value(15)
    LL_1.print()
    
    

