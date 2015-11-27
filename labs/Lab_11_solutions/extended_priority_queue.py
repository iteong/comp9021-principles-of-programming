# A max priority queue abstract data type to insert pairs of the form (datum, priority).
# If a pair is inserted with a datum that already occurs in the priority queue, then
# the priority is (possibly) changed to the (possibly) new value.
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10


class PriorityQueue():
    def __init__(self, capacity = MIN_CAPACITY):
        self._data = [None] * capacity
        self._length = 0
        self._locations = {}
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def insert(self, element):
        datum = element[0]
        priority = element[1]
        if datum in self._locations:
            self._change_priority(datum, priority)
            return
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = [datum, priority]
        self._locations[datum] = self._length
        self._bubble_up(self._length)

    def delete(self):
        top_datum = self._data[1][0]
        del self._locations[top_datum]        
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        if MIN_CAPACITY <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return top_datum

    def _change_priority(self, datum, priority):
        i = self._locations[datum]
        if priority > self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_up(i)
        elif priority < self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_down(i)
            self._bubble_up(i)
        
    def _bubble_up(self, i):
        if i > 1 and self._data[i][1] > self._data[i // 2][1]:
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._locations[self._data[i // 2][0]] = i // 2
            self._locations[self._data[i][0]] = i
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._data[child + 1][1] > self._data[child][1]:
            child += 1
        if child <= self._length and self._data[child][1] > self._data[i][1]:
            self._data[child], self._data[i] = self._data[i], self._data[child]
            self._locations[self._data[child][0]] = child
            self._locations[self._data[i][0]] = i
            self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[ : self._length + 1]) + [None] * (new_size - self._length - 1)
        

if __name__ == '__main__':
    pq = PriorityQueue()
    L = [('A', 13), ('B', 13), ('C', 4), ('D', 15), ('E', 9), ('F', 4), ('G', 5), ('H', 14),
         ('A', 4), ('B', 11), ('C', 15), ('D', 2), ('E', 17),
         ('A', 8), ('B', 14), ('C',12), ('D', 9), ('E', 5),
         ('A', 6), ('B', 16)]
    for e in L:
        pq.insert(e)
    for i in range(8):
        print(pq.delete(), end = ' ')
    print()
    print(pq.is_empty())
    
   
            
