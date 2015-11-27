# A Binary Tree abstract data type
#
# Written by Eric Martin for COMP9021


class BinaryTree:
    def __init__(self, value = None):
        self.value = value
        if self.value:
            self.left_node = BinaryTree()
            self.right_node = BinaryTree()
        else:
            self.left_node = None
            self.right_node = None

    def height(self):
        if not self.value:
            return 0
        return max(self._height(self.left_node), self._height(self.right_node))

    # Both an empty tree and a tree consisting of its root are of height 0.
    def _height(self, node):
        if node.value == None:
            return 0
        return 1 + max(self._height(node.left_node), self._height(node.right_node))

    # Number of values stored in tree.
    def size(self):
        if self.value == None:
            return 0
        return 1 + self.left_node.size() + self.right_node.size()

    def occurs_in_tree(self, value):
        if self.value == None:
            return False
        if self.value == value:
            return True
        return self.left_node.occurs_in_tree(value) or self.right_node.occurs_in_tree(value)

    # Binary search for value.
    def occurs_in_bst(self, value):
        if self.value == None:
            return False
        if self.value == value:
            return True
        if value < self.value:
            return self.left_node.occurs_in_bst(value)
        return self.right_node.occurs_in_bst(value)

    def is_bst(self):
        if self.value == None:
            return True
        node = self.left_node
        if node.value != None:
            while node.right_node.value != None:
                node = node.right_node
            if self.value <= node.value:
                return False
        node = self.right_node
        if node.value:
            while node.left_node.value != None:
                node = node.left_node
        if node.value != None and self.value >= node.value:
            return False
        return self.left_node.is_bst() and self.right_node.is_bst()

    # Inserts value in binary search and returns True in case value is not already in the tree.
    # Otherwise, returns False.
    def insert_in_bst(self, value):
        if self.value == None:
            self.value = value
            self.left_node = BinaryTree()
            self.right_node = BinaryTree()
            return True
        if self.value == value:
            return False
        if value < self.value:
            return self.left_node.insert_in_bst(value)
        return self.right_node.insert_in_bst(value)


    # Deletes value from binary search and returns True in case value is stored in the tree.
    # Otherwise, returns False.
    def delete_in_bst(self, value):
        return self._delete_in_bst(value, self, '')

    def _delete_in_bst(self, value, parent, link):
        if self.value == None:
            return False
        if value < self.value:
            return self.left_node._delete_in_bst(value, self, 'L')
        if value > self.value:
            return self.right_node._delete_in_bst(value, self, 'R')
        if self.left_node.value == None:
            new_tree = self.right_node
        elif self.right_node.value == None:
            new_tree = self.left_node
        elif self.left_node.right_node.value == None:
            new_tree = self.left_node
            new_tree.right_node = self.right_node
        else:
            # Looking for the node containing the largest value
            # smaller than the value to delete.
            # That node will be node_2 and its parent node_1
            node_1 = self.left_node
            node_2 = node_1.right_node
            while node_2.right_node.value != None:
                node_1 = node_2
                node_2 = node_2.right_node
            # The value stored in node_2 is meant to replace
            # the value to delete.
            # The replacement will only happen in case the value
            # being deleted is stored in the root; otherwise,
            # node_2 will be connected to the parent
            # of the node storing the value to delete.
            new_tree = node_2
            # Values larger than the value to delete
            # are larger than the replacing value.
            new_tree.right_node = self.right_node
            # Values between the value to delete
            # and the value stored in the parent P
            # of the node N storing that value 
            # are larger than the replacing value
            # and can be linked to P since N is going away.
            node_1.right_node = node_2.left_node
            # The replacing value is larger than
            # all other values stored on the left
            # of the node N containing the value to delete,
            # and can be linked to the node containing that value
            # since N is going. 
            new_tree.left_node = self.left_node      
        if link == '':
            self.value = new_tree.value
            self.left_node = new_tree.left_node
            self.right_node = new_tree.right_node
        elif link == 'L':
            parent.left_node = new_tree
        else:
            parent.right_node = new_tree
        return True
    
    def print_binary_tree(self):
        if self.value == None:
            return
        self._print_binary_tree(0, self.height())

    def _print_binary_tree(self, n, height):
        if n > height:
            return
        if self.value == None:
            print('\n' * (2 ** (height - n + 1) - 1), end = '')
        else:
            self.left_node._print_binary_tree(n + 1, height)
            print('\t' * n, self.value, sep = '')
            self.right_node._print_binary_tree(n + 1, height)
            
    def pre_order_traversal(self):
        if self.value == None:
            return []
        values = [self.value]
        values.extend(self.left_node.pre_order_traversal())
        values.extend(self.right_node.pre_order_traversal())
        return values

    def in_order_traversal(self):
        if self.value == None:
            return []
        values = self.left_node.in_order_traversal()
        values.append(self.value)
        values.extend(self.right_node.in_order_traversal())
        return values

    def post_order_traversal(self):
        if self.value == None:
            return []
        values = self.left_node.post_order_traversal()
        values.extend(self.right_node.post_order_traversal())
        values.append(self.value)
        return values
            

if __name__ == '__main__':
    print('Testing empty tree:')
    t = BinaryTree()
    print(t.height())
    print(t.size())
    print(t.is_bst())
    print(t.occurs_in_tree(0))
    print(t.occurs_in_bst(0))
    t.print_binary_tree()
    print(t.pre_order_traversal())
    print(t.in_order_traversal())
    print(t.post_order_traversal())
            
    print('\nTesting 1 node tree:')
    t = BinaryTree(1)
    print(t.height())
    print(t.size())
    print(t.is_bst())
    print(t.occurs_in_tree(0))
    print(t.occurs_in_bst(0))
    print(t.occurs_in_tree(1))
    print(t.occurs_in_bst(1))
    t.print_binary_tree()
    print(t.pre_order_traversal())
    print(t.in_order_traversal())
    print(t.post_order_traversal())

    print('\nTesting a tree storing 1, 2, 3, 4, 5 and 6 twice:')
    t = BinaryTree(3)
    t_1 = BinaryTree(2)
    t_2 = BinaryTree(5)
    t_3 = BinaryTree(1)
    t_4 = BinaryTree(4)
    t_5 = BinaryTree(6)
    t_6 = BinaryTree(6)
    t.left_node = t_1
    t.right_node = t_2
    t_1.left_node = t_3
    t_2.left_node = t_4
    t_2.right_node = t_5
    t_4.right_node = t_6
    print(t.height())
    print(t.size())
    print(t.is_bst())
    print(t.occurs_in_tree(0))
    print(t.occurs_in_tree(1))
    t.print_binary_tree()
    print(t.pre_order_traversal())
    print(t.in_order_traversal())
    print(t.post_order_traversal())
    
    print('\nTesting a binary tree:')
    t = BinaryTree()
    t.insert_in_bst(4)
    t.print_binary_tree()
    t.insert_in_bst(2)
    t.print_binary_tree()
    t.insert_in_bst(1)
    t.print_binary_tree()
    t.insert_in_bst(5)
    t.print_binary_tree()
    t.insert_in_bst(3)
    t.print_binary_tree()
    t.insert_in_bst(6)
    t.print_binary_tree()
    t.insert_in_bst(7)
    t.print_binary_tree()
    print(t.is_bst())
    print(t.occurs_in_tree(3))
    print(t.occurs_in_bst(3))
    print(t.occurs_in_tree(8))
    print(t.occurs_in_bst(8))
    print(t.pre_order_traversal())
    print(t.in_order_traversal())
    print(t.post_order_traversal())
    t.delete_in_bst(5)
    t.print_binary_tree()
    t.delete_in_bst(7)
    t.print_binary_tree()
    t.delete_in_bst(2)
    t.print_binary_tree()
    t.delete_in_bst(4)
    t.print_binary_tree()
    t.delete_in_bst(1)
    t.print_binary_tree()
    t.delete_in_bst(6)
    t.print_binary_tree()
    t.delete_in_bst(3)
    t.print_binary_tree()
    
