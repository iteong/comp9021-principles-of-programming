# A Queue abstract data type
#
# Written by Eric Martin for COMP9021


MIN_CAPACITY = 10

class ArrayQueue:
    def __init__(self, capacity = MIN_CAPACITY):
        self._data = [None] * capacity
        self._length = 0
        self._front = 0
        
    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def peek_at_the_front(self):
        if self.is_empty():
            raise Exception('Empty queue')
        return self._data[self._front]

    def peek_at_the_back(self):
        if self.is_empty():
            raise Exception('Empty queue')
        return self._data[(self._front + self._length - 1) % len(self._data)]

    def enqueue(self, datum):
        if self._length == len(self._data):
            self._resize(2 * len(self._data))
        self._data[(self._front + self._length) % len(self._data)] = datum
        self._length += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception('Empty queue')
        datum_at_the_front = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)        
        self._length -= 1
        if MIN_CAPACITY // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return datum_at_the_front

    def _resize(self, new_size):
        end = self._front + new_size
        if end <= len(self._data):
            self._data = self._data[self._front : end]
        elif new_size <= len(self._data):
            self._data = self._data[self._front : ] + self._data[ : end - len(self._data)]
        else:
            self._data = self._data[self._front : ] + self._data[ : self._front] + [None] * (new_size - len(self._data))
        self._front = 0
        
