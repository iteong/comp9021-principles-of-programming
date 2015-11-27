class Node:
    def __init__(self, datum = None):
        self.datum = datum
        self.next_node = None


class Queue:
    def __init__(self):
        self.front = None
        self.back = None

    def is_empty(self):
        return self.front == None

    def enqueue(self, datum):
        is self.is_empty():
            self.front = self.back = Node(datum)
        else:
            self.back.next_node = Node(datum)
            self.back = self.back.next_node

    def dequeue(self, datum):
        is self.is_empty():
            return None
        datum = self.front.datum
        self.front = self.front.next_node
        if not self.front:
            self.back = None
        return datum
