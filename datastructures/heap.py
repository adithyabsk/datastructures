"""min and max heap."""

from abc import ABCMeta, abstractmethod
from collections import namedtuple

from datastructures.tree import BinaryTree

HeapItem = namedtuple("HeapItem", ["key", "value"])


def heapsort(iterable, reverse=False):
    # convert iterable to list in case it is a consumable iterable, and pass the
    # data as both key and value
    data = list(iterable)
    if reverse:
        heap = MaxHeap(data, data)
    else:
        heap = MinHeap(data, data)
    return [heap.extract_root() for _ in range(heap.size())]


class BaseHeap(BinaryTree, metaclass=ABCMeta):
    def __init__(self, iterable=None, keys=None):
        super().__init__()
        if keys is not None and iterable is not None:
            self.heapify(iterable, keys)

    def get_root(self):
        return self.root().value

    def extract_root(self):
        if self.node_count() < 1:
            raise ValueError("heap underflow")
        _max = self.root().value
        if self.node_count() == 1:
            self.remove(0)
        else:
            # the reason we can use node count to find the last index is
            # because when we fill the tree, we make sure to full pack the
            # binary tree structure. i.e. we don't just fill the left branch,
            # for example. This makes sure that the binary heap is an *almost
            # complete* binary tree.
            self.swap(0, self.node_count() - 1)
            self.remove(self.node_count() - 1)
            self._sift_down(0)

        return _max

    def insert(self, key, value):
        new_node_idx = self.node_count()
        self.set_node(new_node_idx, HeapItem(key, value))
        self._sift_up(new_node_idx)

    def heapify(self, iterable, keys):
        # we perform this algorithm instead of repeated inserts since repeated
        # inserts have a worst case time complexity of O(N log(N)) vs O(N) for
        # "heapify" which does a bottom up approach
        self.nodes = [HeapItem(key, value) for key, value in zip(keys, iterable)]
        last_node_idx = self.node_count() - 1
        parent_idx = self.parent_index(last_node_idx)
        for index in reversed(range(0, parent_idx + 1)):
            self._sift_down(index)

    def size(self):
        return self.node_count()

    def update_index_priority(self, index, key):
        curr_node = self.get_node(index)
        # we don't update value2idx because that is handled through calls to
        # set_node
        if key < curr_node.key:
            self._decrease_key(index, key)
        elif key > curr_node.key:
            self._increase_key(index, key)
        # else no update required

    @abstractmethod
    def _sift_down(self, index):  # pragma: no cover
        """Correct the placement of node at index.

        For example, in a max heap this node may be less than it's children
        which violates the max heap property. The max heap property requires
        that all parent nodes are greater than or equal to their children.

        """
        pass

    @abstractmethod
    def _sift_up(self, index):  # pragma: no cover
        """Bubble nodes upwards until it satisfies the heap property."""
        pass

    @abstractmethod
    def _increase_key(self, index, key):  # pragma: no cover
        """Change the key of the node at index to a larger value."""
        pass

    @abstractmethod
    def _decrease_key(self, index, key):  # pragma: no cover
        """Change the key of the node at index to a smaller value."""
        pass

    def __len__(self):
        return self.size()


class MaxHeap(BaseHeap):
    """Implement a max heap.

    Note the root will always have the largest key.

    In `_sift_down` we find the largest. In `sift_up` we swap if the parent is
    smaller than the child. In `_increase_key` we call `sift_up` since the new
    key may be larger than the parent.And, in `_decrease_key`, we call
    `sift_down` for the opposite reason.

    """

    def _sift_down(self, index):
        left_index = self.left_index(index)
        right_index = self.right_index(index)
        tree_size = self.node_count()
        # compare the priority of parent node, left node, and right node and
        # determine which has the highest priority
        if (
            left_index < tree_size
            and self.get_node(left_index).key > self.get_node(index).key
        ):
            largest = left_index
        else:
            largest = index
        if (
            right_index < tree_size
            and self.get_node(right_index).key > self.get_node(largest).key
        ):
            largest = right_index
        if largest != index:
            self.swap(index, largest)
            self._sift_down(largest)

    def _sift_up(self, index):
        while index > 0 and self.parent(index).key < self.get_node(index).key:
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)

    def _increase_key(self, index, key):
        curr_node = self.get_node(index)
        if key < curr_node.key:  # pragma: no cover
            raise ValueError("new key is smaller than current key")
        self.set_node(index, HeapItem(key, curr_node.value))
        self._sift_up(index)

    def _decrease_key(self, index, key):
        curr_node = self.get_node(index)
        if key > curr_node.key:  # pragma: no cover
            raise ValueError("new key is greater than current key")
        self.set_node(index, HeapItem(key, curr_node.value))
        self._sift_down(index)


class MinHeap(BaseHeap):
    """Implement a min heap.

    Note the root will always have the smallest key.

    In `_sift_down` we find the smallest instead of the largest. In `sift_up`
    we swap if the parent is larger than the child. In `_increase_key` we
    call `sift_down`. And, in `_decrease_key`, we call `sift_up`.

    """

    def _sift_down(self, index):
        left_index = self.left_index(index)
        right_index = self.right_index(index)
        tree_size = self.node_count()
        # compare the priority of parent node, left node, and right node and
        # determine which has the highest priority
        if (
            left_index < tree_size
            and self.get_node(left_index).key < self.get_node(index).key
        ):
            smallest = left_index
        else:
            smallest = index
        if (
            right_index < tree_size
            and self.get_node(right_index).key < self.get_node(smallest).key
        ):
            smallest = right_index
        if smallest != index:
            self.swap(index, smallest)
            self._sift_down(smallest)

    def _sift_up(self, index):
        while index > 0 and self.parent(index).key > self.get_node(index).key:
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)

    def _increase_key(self, index, key):
        curr_node = self.get_node(index)
        if key < curr_node.key:  # pragma: no cover
            raise ValueError("new key is smaller than current key")
        self.set_node(index, HeapItem(key, curr_node.value))
        self._sift_down(index)

    def _decrease_key(self, index, key):
        curr_node = self.get_node(index)
        if key > curr_node.key:  # pragma: no cover
            raise ValueError("new key is greater than current key")
        self.set_node(index, HeapItem(key, curr_node.value))
        self._sift_up(index)


class PriorityQueue(MinHeap):
    """A priority queue based on MinHeap.

    Lower key values indicate higher priority. Implements a way to lookup items
    and their priorities by value. This means that each item in the priority
    queue must be unique. This results in the ability to change the priority of
    any item in O(log n) runtime.

    """

    def __init__(self, iterable=None, keys=None):
        self.value2idx = {}
        super().__init__(iterable, keys)

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, iterable):
        # this hook is useful so that value2idx is specified any time we
        # manually set `nodes` as in `heapify`
        for i, heap_item in enumerate(iterable):
            self._check_unique(heap_item.value)
            self.value2idx[heap_item.value] = i
        self._nodes = iterable

    def swap(self, index1, index2):
        # handle updating the key/index look up table before actually swapping
        # the nodes
        self.value2idx[self.nodes[index1].value] = index2
        self.value2idx[self.nodes[index2].value] = index1
        super().swap(index1, index2)

    def remove(self, index):
        del self.value2idx[self.nodes[index].value]
        super().remove(index)

    def set_node(self, index, heap_item):
        try:
            # delete the old val/index mapping
            del self.value2idx[self.nodes[index].value]
        except IndexError:
            # if it is a new index then skip
            pass
        self._check_unique(heap_item.value)
        self.value2idx[heap_item.value] = index
        super().set_node(index, heap_item)

    def update_value_priority(self, value, key):
        # this is required for dijkstra's
        if value in self.value2idx:
            index = self.value2idx[value]
            old_key = self.nodes[index].key
            # we don't update value2idx because that is handled through calls to
            # set_node
            if key < old_key:
                self._decrease_key(index, key)
            elif key > old_key:
                self._increase_key(index, key)
        else:
            raise ValueError(f"{value} not found in tree location lookup table")

    def insert(self, key, value):
        self._check_unique(value)
        super().insert(key, value)

    def _check_unique(self, value):
        if value in self.value2idx:
            raise ValueError("all items must be unique in the priority queue")
