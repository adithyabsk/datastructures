"""A doubly linked list."""

from functools import total_ordering

# when you're bored and have some time, finish these TODOs
# TODO: add support for arbitrary index popping to DRY the implemenation of
#       pop and popleft
# TODO: add support for copy and deepcopy
# TODO: add support for __add__
# TODO: add support for __mul__
# TODO: add support for __imul__

# Note: total ordering generates all the rich comparison operators given
#       `__eq__` and `__lt__`.
#       https://docs.python.org/3/library/functools.html#functools.total_ordering


@total_ordering
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
            if self.parent is not None:
                self.parent.child = self.child
            if self.child is not None:
                self.child.parent = self.parent
            self.clear()

        def __eq__(self, other):
            return self.val == other.val

        def __repr__(self):
            return f"LinkedList.Node({self})"

        def __str__(self):
            return str(self.val)

    def __init__(self, iterable=None, maxlen=None):
        if maxlen is not None and maxlen < 0:
            raise ValueError("maxlen must be > 0")
        if hasattr(self, "root"):
            # init is being called directly for the second time
            self.clear()
        self.root = None
        self.tail = None
        self._total_items = 0
        self._maxlen = maxlen
        self.__is_iterating = False
        if iterable is not None:
            self.extend(iterable)

    @property
    def maxlen(self):
        return self._maxlen

    def _check_not_iterating(self):
        if self.__is_iterating:
            raise RuntimeError("linked list mutated during iteration")

    def append(self, val):
        self._check_not_iterating()
        if self.maxlen is not None and self._total_items >= self.maxlen:
            if self.maxlen == 0:
                return
            else:
                self.popleft()
        if self.tail is None:
            self.root = self.tail = self.Node(val)
        else:
            node = self.Node(val)
            self.tail.append(node)
            self.tail = node
        self._total_items += 1

    def appendleft(self, val):
        self._check_not_iterating()
        if self.maxlen is not None and self._total_items >= self.maxlen:
            if self.maxlen == 0:
                return
            else:
                self.pop()
        if self.root is None:
            self.root = self.tail = self.Node(val)
        else:
            node = self.Node(val)
            self.root.appendleft(node)
            self.root = node
        self._total_items += 1

    def count(self, x):
        total = 0
        for item in self:
            if item == x:
                total += 1

        return total

    def clear(self):
        self._check_not_iterating()
        for node in self._iter():
            node.clear()
        self.root = self.tail = None
        self._total_items = 0

    def extend(self, iterable):
        # iterate over the data in advance in case iterable is self
        tmp_data = [i for i in iterable]
        for i in tmp_data:
            self.append(i)

    def extendleft(self, iterable):
        # iterate over the data in advance in case iterable is self
        tmp_data = [i for i in iterable]
        for i in tmp_data:
            self.appendleft(i)

    def pop(self):
        self._check_not_iterating()
        if len(self) == 0:
            raise ValueError("linked list is empty")
        node_val = self.tail.val
        if self.tail.parent is not None:
            self.tail = self.tail.parent
            self.tail.child = None
        else:
            self.tail = self.root = None
        self._total_items -= 1
        return node_val

    def popleft(self):
        if self.__is_iterating:
            raise RuntimeError("linked list mutated during iteration")
        if len(self) == 0:
            raise ValueError("linked list is empty")
        node_val = self.root.val
        if self.root.child is not None:
            self.root = self.root.child
            self.root.parent = None
        else:
            self.root = self.tail = None
        self._total_items -= 1
        return node_val

    def reverse(self):
        self._check_not_iterating()
        for node in self:
            node.child, node.parent = node.parent, node.child
        self.root, self.tail = self.tail, self.root

    def rotate(self, n=1):
        self._check_not_iterating()
        if n > 0:
            for _ in range(n):
                self.appendleft(self.pop())
        elif n < 0:
            for _ in range(-n):
                self.append(self.popleft())

    def __len__(self):
        return self._total_items

    def _getnode(self, index):
        if index >= self._total_items or index < -self._total_items:
            raise IndexError("index out of range")
        if index < 0:
            index = self._total_items + index
        # we need this conditional so that we can optimally reach indices
        # on the other side of the doubly linked list without having to iterate
        # over the entire array
        iterate_forward = ((self._total_items - 1) // 2) - index >= 0
        if iterate_forward:
            for i, node in enumerate(self._iter()):
                if i == index:
                    # Since we exit out of the generator early, (before
                    # StopIteration has been raised, we don't actually set the
                    # `__is_iterating` to false, so have to manually do it here
                    self.__is_iterating = False
                    return node
        else:
            for i, node in enumerate(self._iter(reverse=True)):
                if (self._total_items - 1 - i) == index:
                    self.__is_iterating = False
                    return node

    def __getitem__(self, index):
        return self._getnode(index).val

    def __setitem__(self, index, value):
        node = self._getnode(index)
        node.val = value

    def _iter(self, reverse=False):
        self.__is_iterating = True
        if not reverse:
            node = self.root
            while node is not None:
                yield node
                node = node.child
        else:
            node = self.tail
            while node is not None:
                yield node
                node = node.parent
        self.__is_iterating = False

    def __iter__(self):
        for n in self._iter():
            yield n.val

    def __reversed__(self):
        # we could just use the default implementation of reversed that uses
        # __len__ and __getitem__, but this is likely more optimal
        # TODO: validate the above assumption
        for node in self.iter(reverse=True):
            yield node.val

    def __eq__(self, other):
        if isinstance(other, LinkedList):
            return len(self) == len(other) and all(s == o for s, o in zip(self, other))
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, LinkedList):
            return len(self) < len(other) or (
                len(self) == len(other) and all(s < o for s, o in zip(self, other))
            )
        else:
            raise TypeError(
                f"supported between instances of '{type(self)}' and " f"'{type(other)}'"
            )

    def __add__(self, other):
        if isinstance(other, LinkedList):
            ret = LinkedList(self, maxlen=self.maxlen)
            ret.extend(other)
            return ret
        else:
            raise TypeError(
                f'can only concatenate deque (not "{type(other)}") to deque'
            )

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __str__(self):
        # CPython has some magic code to traverse the stack to check if an
        # object is self referential. We could replicate that functionality with
        # inspect, but that would make this function waaaay to complicated.
        # Instead, we just truncate any LinkedList that refers to another
        # LinkedList.
        # https://stackoverflow.com/a/15849554/3262054
        inner = ", ".join(
            str(n) if not isinstance(n, LinkedList) else "LinkedList([...])"
            for n in self
        )
        return f"[{inner}]"

    def __repr__(self):
        ret = f"LinkedList({self}"
        if self.maxlen is not None:
            ret += f", maxlen={self.maxlen}"
        ret += ")"
        return ret
