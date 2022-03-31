"""A doubly linked list implementation of a deque."""
from functools import total_ordering

# TODO: add support for arbitrary index popping and appending to DRY the
#       implementation of pop, popleft, append, and appendleft

# Note: total ordering generates all the rich comparison operators given
#       `__eq__` and `__lt__`.
#       https://docs.python.org/3/library/functools.html#functools.total_ordering


@total_ordering
class Deque:
    """A pure python implementation of collections.deque"""

    class _Node:
        def __init__(self, val):
            self.val = val
            self.parent = None
            self.child = None

        def append(self, node: "Deque._Node"):
            node.parent = self
            self.child = node

        def appendleft(self, node: "Deque._Node"):
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
            return f"Deque._Node({self})"

        def __str__(self):  # pragma: no cover
            return str(self.val)

    # We need this separate iterator class so that we can pickle the iterator
    class _Iterator:
        def __init__(self, start, node=False, reverse=False) -> None:
            self.current = start
            self.reverse = reverse
            self.node = node

        def __iter__(self):
            return self

        def _update(self):
            if self.reverse:
                self.current = self.current.parent
            else:
                self.current = self.current.child

        def __next__(self):
            if self.current is None:
                raise StopIteration
            else:
                node = self.current
                self._update()
                return node if self.node else node.val

    def __init__(self, iterable=None, maxlen=None):
        if maxlen is not None and maxlen < 0:
            raise ValueError("maxlen must be > 0")
        if hasattr(self, "head"):
            # init is being called directly for the second time
            self.clear()
        self.head = None
        self.tail = None
        self._total_items = 0
        self._maxlen = maxlen
        self.__is_iterating = False
        self.__state = 0  # moves whenever indices are changed
        if iterable is not None:
            self.extend(iterable)

    @property
    def maxlen(self):
        return self._maxlen

    def _check_not_mutated(self, start_state):
        if self.__state != start_state:
            raise RuntimeError("linked list mutated during iteration")

    def append(self, val):
        if self.maxlen is not None and self._total_items >= self.maxlen:
            if self.maxlen == 0:
                return
            else:
                self.popleft()
        if self.tail is None:
            self.head = self.tail = self._Node(val)
        else:
            node = self._Node(val)
            self.tail.append(node)
            self.tail = node
        self._total_items += 1
        self.__state += 1

    def appendleft(self, val):
        if self.maxlen is not None and self._total_items >= self.maxlen:
            if self.maxlen == 0:
                return
            else:
                self.pop()
        if self.head is None:
            self.head = self.tail = self._Node(val)
        else:
            node = self._Node(val)
            self.head.appendleft(node)
            self.head = node
        self._total_items += 1
        self.__state += 1

    def count(self, x):
        total = 0
        start_state = self.__state
        for item in self:
            if item == x:
                total += 1
            self._check_not_mutated(start_state)

        return total

    def copy(self):
        return Deque(self, maxlen=self.maxlen)

    def clear(self):
        # extract nodes in advance since iteration requires the next node
        nodes = [n for n in self._Iterator(self.head, node=True)]

        for node in nodes:
            # we are removing all nodes, so we don't need to unlink them
            node.clear(unlink=False)

        self.head = self.tail = None
        self._total_items = 0
        self.__state += 1

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
        if len(self) == 0:
            raise IndexError("pop from an empty Deque")
        node_val = self.tail.val
        if self.tail.parent is not None:
            self.tail = self.tail.parent
            self.tail.child = None
        else:
            self.tail = self.head = None
        self._total_items -= 1
        self.__state += 1
        return node_val

    def popleft(self):
        if len(self) == 0:
            raise IndexError("pop from an empty Deque")
        node_val = self.head.val
        if self.head.child is not None:
            self.head = self.head.child
            self.head.parent = None
        else:
            self.head = self.tail = None
        self._total_items -= 1
        self.__state += 1
        return node_val

    def reverse(self):
        # extract nodes in advance since iteration requires the next node
        nodes = [n for n in self._Iterator(self.head, node=True)]
        for node in nodes:
            node.child, node.parent = node.parent, node.child
        self.head, self.tail = self.tail, self.head

    def remove(self, value):
        start_state = self.__state
        for i, v in enumerate(self):
            if v == value:
                self._check_not_mutated(start_state)
                del self[i]
                break
            else:
                self._check_not_mutated(start_state)
        else:
            raise ValueError(f"{value} not in deque")

    def rotate(self, n=1):
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
            start_state = self.__state
            for idx, val in enumerate(self):
                # we need to do the checks in each of the if statements in case
                # the mutation happens in an overloaded comparison function
                if idx < start:
                    self._check_not_mutated(start_state)
                    continue
                elif idx >= stop:
                    self._check_not_mutated(start_state)
                    break
                elif val == x:
                    self._check_not_mutated(start_state)
                    return idx
                self._check_not_mutated(start_state)
        raise ValueError(f"{x} is not in the Deque")

    def insert(self, i, x):
        if self.maxlen is not None and self._total_items >= self.maxlen:
            raise IndexError("Deque already at its maximum size")
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
            new_node = self._Node(x)
            parent_node.append(new_node)
            new_node.append(child_node)
            self._total_items += 1
            self.__state += 1

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
            start_state = self.__state
            for i, node in enumerate(self._Iterator(self.head, node=True)):
                self._check_not_mutated(start_state)
                if i == index:
                    return node
        else:
            start_state = self.__state
            for i, node in enumerate(
                self._Iterator(self.tail, node=True, reverse=True)
            ):
                self._check_not_mutated(start_state)
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
            self.__state += 1

    def __contains__(self, item):
        start_state = self.__state
        for val in self:
            if val == item:
                return True
            self._check_not_mutated(start_state)
        else:
            return False

    def __iter__(self):
        return self._Iterator(self.head)

    def __reversed__(self):
        # we could just use the default implementation of reversed that uses
        # __len__ and __getitem__, but this is likely more optimal
        # TODO: validate the above assumption
        return self._Iterator(self.tail, reverse=True)

    def __eq__(self, other):
        if isinstance(other, Deque):
            return len(self) == len(other) and all(s == o for s, o in zip(self, other))
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Deque):
            return len(self) < len(other) or (
                len(self) == len(other) and all(s < o for s, o in zip(self, other))
            )
        else:
            raise TypeError(
                f"supported between instances of '{type(self)}' and " f"'{type(other)}'"
            )

    def __add__(self, other):
        if isinstance(other, Deque):
            ret = Deque(self, maxlen=self.maxlen)
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
            ret = Deque(maxlen=self.maxlen)
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
        # Instead, we just truncate any Deque that refers to another
        # Deque.
        # https://stackoverflow.com/a/15849554/3262054
        inner = ", ".join(
            str(n) if not isinstance(n, Deque) else "Deque([...])"
            for n in self
        )
        return f"[{inner}]"

    def __repr__(self):
        ret = f"Deque({self}"
        if self.maxlen is not None:
            ret += f", maxlen={self.maxlen}"
        ret += ")"
        return ret
