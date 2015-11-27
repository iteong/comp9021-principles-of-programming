# A max or min priority queue abstract data type.
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10


# Max priority queue by default
class PriorityQueue():
    def __init__(self, capacity = MIN_CAPACITY, compare = lambda x, y: x > y):
        self._data = [None] * capacity
        self._length = 0
        self._compare = compare
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def top_priority(self):
        if not self._length:
            return None
        return self._data[1]

    def insert(self, element):
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = element
        self._bubble_up(self._length)

    def delete_top_priority(self):
        top_element = self._data[1]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        if MIN_CAPACITY * 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return top_element

    def _bubble_up(self, i):
        if i > 1 and self._compare(self._data[i], self._data[i // 2]):
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._compare(self._data[child + 1], self._data[child]):
            child += 1
        if child <= self._length:
            if self._compare(self._data[child], self._data[i]):
                self._data[child], self._data[i] = self._data[i], self._data[child]
                self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[ : self._length + 1]) + [None] * (new_size - self._length - 1)


class MaxPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        

class MinPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__(compare = lambda x, y: x < y)
        


        
if __name__ == '__main__':
    max_pq = MaxPriorityQueue()
    min_pq = MinPriorityQueue()
    L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
    for e in L:
        max_pq.insert(e)
        min_pq.insert(e)
    print(max_pq._data[ : max_pq._length + 1])
    print(min_pq._data[ : min_pq._length + 1])
    for i in range(len(L)):
        print(max_pq.delete_top_priority(), end = ' ')
    print()
    for i in range(len(L)):
        print(min_pq.delete_top_priority(), end = ' ')
    print()        
    
   
            
