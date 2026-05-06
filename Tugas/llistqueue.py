class _QueueNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class Queue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def isEmpty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def enqueue(self, item):
        node = _QueueNode(item)
        if self.isEmpty():
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def dequeue(self):
        assert not self.isEmpty(), "Cannot dequeue from empty queue"
        item = self._head.item
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return item

    def peek(self):
        assert not self.isEmpty()
        return self._head.item
