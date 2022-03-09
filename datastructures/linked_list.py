"""A doubly linked list."""

# when you're bored and have some time, finish these TODOs
# TODO: add support for copy and deepcopy
# TODO: add support for __add__
# TODO: add support for __mul__
# TODO: add support for __imul__


class LinkedList:
    """A pure python implementation of collections.deque"""

    class Node:
        def __init__(self, val):
            self.val = val
            self.parent = None
            self.child = None

        def append(self, node: "LinkedList.Node"):
            node.parent = self
            self.child = node

        def appendleft(self, node: "LinkedList.Node"):
            node.child = self
            self.parent = node

        def clear(self):
            self.val = None
            self.parent = None
            self.child = None

        def __del__(self):
            self.parent.child = self.child
            self.child.parent = self.parent
            self.clear()

    def __init__(self):
        self.root = None
        self.tail = None
        self.count = 0

    def append(self, val):
        if self.tail is None:
            self.root = self.tail = self.Node(val)
        else:
            node = self.Node(val)
            self.tail.append(node)
            self.tail = node
        self.count += 1

    def appendleft(self, val):
        if self.root is None:
            self.root = self.tail = self.Node(val)
        else:
            node = self.Node(val)
            self.root.appendleft(node)
            self.root = node
        self.count += 1

    def clear(self):
        for node in self:
            node.clear()
        self.root = self.tail = None
        self.count = 0

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    def extendleft(self, iterable):
        for i in iterable:
            self.appendleft(i)

    def pop(self):
        if self.tail is None:
            raise ValueError("linked list is empty")
        node_val = self.tail.val
        if self.tail.parent is not None:
            self.tail = self.tail.parent
        else:
            self.tail = self.root = None
        self.count -= 1
        return node_val

    def popleft(self):
        if self.root is None:
            raise ValueError("linked list is empty")
        node_val = self.root.val
        if self.root.child is not None:
            self.root = self.root.child
        else:
            self.root = self.tail = None
        self.count -= 1
        return node_val

    def reverse(self):
        for node in self:
            node.child, node.parent = node.parent, node.child
        self.root, self.tail = self.tail, self.root

    def rotate(self, n=1):
        if n > 0:
            for _ in range(n):
                self.appendleft(self.pop())
        elif n < 0:
            for _ in range(-n):
                self.append(self.popleft())

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        if index >= self.count:
            raise IndexError("index out of range")
        # we need this conditional so that we can optimally reach indices
        # on the other side of the doubly linked list without having to iterate
        # over the entire array
        # TODO: scrutinize this conditional for an off by one error
        iterate_forward = ((self.count - 1) // 2) - index >= 0
        if iterate_forward:
            for i, node in enumerate(self):
                if i == index:
                    return node.val
        else:
            # TODO: scrutinize this iterator for an off by one error
            for i, node in enumerate(reversed(self)):
                if (self.count - 1 - i) == index:
                    return node.val

    def __iter__(self):
        node = self.root
        while node is not None:
            val = node.val
            node = node.child
            yield val

    def __reversed__(self):
        # we could just use the default implementation of reversed that uses
        # __len__ and __getitem__, but this is likely more optimal
        # TODO: validate the above assumption
        node = self.tail
        while node is not None:
            val = node.val
            node = node.parent
            yield val
