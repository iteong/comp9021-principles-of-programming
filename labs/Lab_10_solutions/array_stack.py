# A Stack abstract data type
#
# Written by Eric Martin for COMP9021


class ArrayStack:
    def __init__(self):
        self._data = []
        
    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def peek(self):
        if self.is_empty():
            raise Exception('Empty stack')
        return self._data[-1]

    def push(self, datum):
        self._data.append(datum)

    def pop(self):
        if self.is_empty():
            raise Exception('Empty stack')
        return self._data.pop()
        
