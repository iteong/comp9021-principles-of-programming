# Defines a class to manage a list of values with the following operations:
# - add a value in logarithmic time complexity;
# - delete the smallest value, delete the largest value in constant time complexity;
# - return the median in constant time complexity.
#
# Written by Eric Martin for COMP9021

from priority_queue import *

class Median:
    def __init__(self):
        # To store the first half of the values, the largest of which is of highest priority
        self.max_pq = MaxPriorityQueue()
        # To store the second half of the values, the smallest of which is of highest priority
        self.min_pq = MinPriorityQueue()

    def nb_of_elements(self):
        return len(self.max_pq) + len(self.min_pq)

    def median(self):
        if len(self.max_pq) > len(self.min_pq):
            return self.max_pq.top_priority()
        if len(self.min_pq) > len(self.max_pq):
            return self.min_pq.top_priority()
        return (self.max_pq.top_priority() + self.min_pq.top_priority()) / 2

    def insert(self, element):
        # Do not bother with two many cases in case we are adding the second element:
        # let it join the side with the first element and let rebalance() make sure
        # that both elements end up on the correct side.       
        if self.max_pq.top_priority() == None:
            self.min_pq.insert(element)
            self._rebalance()
        elif self.min_pq.top_priority() == None:
            self.max_pq.insert(element)
            self._rebalance()
        elif element < self.max_pq.top_priority():
            self.max_pq.insert(element)
            self._rebalance()
        elif element > self.min_pq.top_priority():
            self.min_pq.insert(element)
            self._rebalance()
        # In both cases, "element" is equal to the largest element from the first half
        # and to the smallest element from the second half, so it can join either side.
        # We chose a side so as to avoid rebalance.
        elif len(self.max_pq) <= len(self.min_pq):
            self.max_pq.insert(element)
        else:
            self.min_pq.insert(element)
            
    def _rebalance(self):
        if len(self.min_pq) > len(self.max_pq) + 1:
            self.max_pq.insert(self.min_pq.delete_top_priority())
        elif len(self.max_pq) > len(self.min_pq) + 1:
            self.min_pq.insert(self.max_pq.delete_top_priority())

if __name__ == '__main__':
    L = [2, 1, 7, 5, 4, 8, 0, 6, 3, 9]
    values = Median()
    for e in L:
        values.insert(e)
        print(values.median(), end = ' ')
    print()
        
