"""min and max heap."""

from collections import namedtuple

from datastructures.tree import BinaryTree

HeapItem = namedtuple("HeapItem", ["key", "value"])


def heapsort(iterable, reverse=True):
    if not reverse:
        raise NotImplementedError
    # convert iterable to list in case it is a consumable iterable, and pass the
    # data as both key and value
    data = list(iterable)
    mh = MaxHeap(data, data)
    return [mh.extract_max() for _ in range(mh.size())]


class MaxHeap(BinaryTree):
    def __init__(self, iterable=None, keys=None):
        super().__init__()
        if keys is not None and iterable is not None:
            self.heapify(keys, iterable)

    def get_max(self):
        return self.root().value

    def extract_max(self):
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

    def heapify(self, keys, iterable):
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

    def update_priority(self, index, key):
        curr_node = self.get_node(index)
        if key < curr_node.key:
            self._decrease_key(index, key)
        elif key > curr_node.key:
            self._increase_key(index, key)
        else:
            # no update required
            pass

    def _sift_down(self, index):
        """Correct the placement of node at index.

        This node may be less than it's children which violates the max heap
        property. The max heap property requires that all parent nodes are
        greater than or equal to their children.

        """
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
        """Bubble nodes upwards until it satisfies the heap property."""
        while index > 0 and self.parent(index).key < self.get_node(index).key:
            self.swap(index, self.parent_index(index))
            index = self.parent_index(index)

    def _increase_key(self, index, key):
        """Bubble nodes upwards until it satisfies the heap property."""
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
