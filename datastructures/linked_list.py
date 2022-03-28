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

        def clear(self, unlink=False):
            if unlink:
                if self.parent is not None:
                    self.parent.child = self.child
                if self.child is not None:
                    self.child.parent = self.parent
            self.val = None
            self.parent = None
            self.child = None

        def __del__(self):
            self.clear(True)

        def __eq__(self, other):  # pragma: no cover
            return self.val == other.val

        def __repr__(self):  # pragma: no cover
            return f"LinkedList.Node({self})"

        def __str__(self):  # pragma: no cover
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
        # extract nodes in advance since iteration requires the next node
        nodes = [n for n in self._iter()]
        for node in nodes:
            # we are removing all nodes, so we don't need to unlink them
            node.clear(unlink=False)
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
            raise IndexError("pop from an empty LinkedList")
        node_val = self.tail.val
        if self.tail.parent is not None:
            self.tail = self.tail.parent
            self.tail.child = None
        else:
            self.tail = self.root = None
        self._total_items -= 1
        return node_val

    def popleft(self):
        self._check_not_iterating()
        if len(self) == 0:
            raise IndexError("pop from an empty LinkedList")
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
        # extract nodes in advance since iteration requires the next node
        nodes = [n for n in self._iter()]
        for node in nodes:
            node.child, node.parent = node.parent, node.child
        self.root, self.tail = self.tail, self.root

    def rotate(self, n=1):
        self._check_not_iterating()
        if self._total_items == 0:
            return
        elif n > 0:
            for _ in range(n):
                self.appendleft(self.pop())
        elif n < 0:
            for _ in range(-n):
                self.append(self.popleft())

    def _rectify_negative_index(self, idx):
        if idx < 0:
            idx = self._total_items + idx
        return idx

    def index(self, x, start=None, stop=None):
        if start is None:
            start = 0
        if stop is None:
            stop = self._total_items
        if not (start >= self._total_items or stop < -self._total_items):
            start = self._rectify_negative_index(start)
            stop = self._rectify_negative_index(stop)
            for idx, val in enumerate(self):
                if idx < start:
                    continue
                if idx >= stop:
                    break
                if val == x:
                    return idx
        raise ValueError(f"{x} is not in the LinkedList")

    def insert(self, i, x):
        if self.maxlen is not None and self._total_items >= self.maxlen:
            raise IndexError("LinkedList already at its maximum size")
        if i < -self._total_items:
            i = 0
        if i >= self._total_items:
            i = self._total_items
        i = self._rectify_negative_index(i)
        if i == 0:
            self.appendleft(x)
        elif i == self._total_items:
            self.append(x)
        else:
            parent_node = self._getnode(i - 1)
            # current node at i will become i+1
            child_node = self._getnode(i)
            new_node = self.Node(x)
            parent_node.append(new_node)
            new_node.append(child_node)
            self._total_items += 1

    def __len__(self):
        return self._total_items

    def _getnode(self, index):
        if index >= self._total_items or index < -self._total_items:
            raise IndexError("index out of range")
        index = self._rectify_negative_index(index)
        # we need this conditional so that we can optimally reach indices
        # on the other side of the doubly linked list without having to iterate
        # over the entire array
        iterate_forward = ((self._total_items - 1) // 2) - index >= 0
        if iterate_forward:
            for i, node in enumerate(self._iter()):
                if i == index:
                    return node
        else:
            for i, node in enumerate(self._iter(reverse=True)):
                if (self._total_items - 1 - i) == index:
                    return node

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError(f"sequence index must be integer, not '{type(index)}'")
        return self._getnode(index).val

    def __setitem__(self, index, value):
        node = self._getnode(index)
        node.val = value

    def __delitem__(self, index):
        # we use popleft and pop instead of the below code so we don't have to
        # manage head and tail
        if index == 0 or index == -self._total_items:
            self.popleft()
        elif index == self._total_items - 1 or index == -1:
            self.pop()
        else:
            node = self._getnode(index)
            # since we are removing only one node, we need to unlink it
            node.clear(unlink=True)
            self._total_items -= 1

    def _iter(self, reverse=False):
        # we need to use try/finally so that `__is_iterating` is set to False on
        # garbage collection of the generator. Otherwise, if we have an early
        # exit from the generator (e.g. a return), `__is_iterating` is not set
        # to False.
        try:
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
        finally:
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

    def __mul__(self, other):
        if isinstance(other, int):
            ret = LinkedList(maxlen=self.maxlen)
            if other <= 0:
                return ret
            else:
                tmp_self = list(self)
                for _ in range(other):
                    ret.extend(tmp_self)
            return ret
        else:
            raise TypeError(
                f"can't multiply sequence by non-int of type '{type(other)}'"
            )

    def __rmul__(self, first):
        return self * first

    def __imul__(self, other):
        if isinstance(other, int):
            if other <= 0:
                self.clear()
                return self
            else:
                tmp_self = list(self)
                for _ in range(other - 1):
                    self.extend(tmp_self)
                return self
        else:
            raise TypeError(
                f"can't multiply sequence by non-int of type '{type(other)}'"
            )

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
