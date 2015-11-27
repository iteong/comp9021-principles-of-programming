# A Deque abstract data type
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10

class ArrayDeque:
    def __init__(self, capacity = MIN_CAPACITY):
        self._data = [None] * capacity
        self._length = 0
        self._front = 1
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def peek_at_the_front(self):
        if self.is_empty():
            raise Exception('Empty deque')
        return self._data[self._front]

    def peek_at_the_back(self):
        if self.is_empty():
            raise Exception('Empty deque')
        return self._data[(self._front + self._length - 1) % len(self._data)]

    def add_at_the_front(self, datum):
        if self._length == len(self._data):
            self._resize(2 * len(self._data))
        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = datum
        self._length += 1

    def add_at_the_back(self, datum):
        if self._length == len(self._data):
            self._resize(2 * len(self._data))
        self._data[(self._front + self._length) % len(self._data)] = datum
        self._length += 1

    def remove_from_the_front(self):
        if self.is_empty():
            raise Exception('Empty deque')
        datum_at_the_front = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)        
        self._length -= 1
        if MIN_CAPACITY // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return datum_at_the_front

    def remove_from_the_back(self):
        if self.is_empty():
            raise Exception('Empty deque')
        index_at_the_back = (self._front + self._length - 1) % len(self._data)
        datum_at_the_back = self._data[index_at_the_back]
        self._data[index_at_the_back] = None
        self._length -= 1
        if MIN_CAPACITY // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return datum_at_the_back

    def _resize(self, new_size):
        end = self._front + new_size
        # No wrapping in original list,
        # and we are shrinking to a smaller list
        if end <= len(self._data):
            self._data = self._data[self._front : end]
        # Wrapping in original list,
        # and we are shrinking to a smaller list        
        elif new_size <= len(self._data):
            self._data = self._data[self._front : ] + self._data[ : end - len(self._data)]
        # We are expanding to a larger list
        else:
            self._data = self._data[self._front : ] + self._data[ : self._front] + [None] * (new_size - len(self._data))
        self._front = 0


if __name__ == '__main__':
    deque = ArrayDeque(3)
    deque.add_at_the_front(0)
    deque.add_at_the_back(1)
    deque.add_at_the_front(2)
    deque.add_at_the_back(3)
    deque.add_at_the_front(4)
    deque.add_at_the_back(5)
    print(deque.peek_at_the_front())      
    print(deque.peek_at_the_back())
    deque.remove_from_the_front()
    deque.remove_from_the_back()
    print(deque.peek_at_the_front())      
    print(deque.peek_at_the_back())
