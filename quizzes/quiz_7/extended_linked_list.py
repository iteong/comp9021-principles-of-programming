# Written by Ivan Teong for COMP9021

from linked_list import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):

        result = LinkedList() # new

        mini = self.head.value # set mini variable as first value
        
        index = 0
        counter = 0 # counter to count which element
        node = self.head # refers node to self.head
        while node:
            if node.value < mini: # compare node value with mini,
                mini = node.value # if smaller, set index = counter,
                index = counter # index only activates when find smaller value
            counter += 1 # every time you move to next node, add 1 to counter
            node = node.next_node # move to next node

        for i in range(self.length()//2):
            if not result.head: # if nothing in head, append first value mini
                result.append(self.value_at(index))
                
            index = (index - 1) % self.length() # go back 1, modulus to wrap
            result.append(self.value_at(index)) # around end

            if not result.length() >= self.length(): # if length of new result
                index = (index + 3) % self.length() # exceeds old, then
                result.append(self.value_at(index)) # stop this action
            
        self.head = result.head # replaces old with new

        
