"""min and max heap."""

from collections import namedtuple

from datastructures.tree import BinaryTree

HeapItem = namedtuple("HeapItem", ["key", "value"])


# TODO: implement heapsort using the MaxHeap data structure.
def heapsort(iterable):
    pass


# TODO: Refactor this so that MaxHeap is a child class of BinaryTree. This may
#       work better than simply calling `self.tree` everywhere


class MaxHeap:
    def __init__(self):
        self.tree = BinaryTree()

    def heapify(self, index):
        """Correct the placement of node at index.

        This node may be less than it's children which violates the max heap
        property. The max heap property requires that all parent nodes are
        greater than or equal to their children.

        """
        left_index = self.tree.left_index(index)
        right_index = self.tree.right_index(index)
        tree_size = self.tree.node_count()
        # compare the priority of parent node, left node, and right node and
        # determine which has the highest priority
        if (
            left_index < tree_size
            and self.tree.get_node(left_index).key > self.tree.get_node(index).key
        ):
            largest = left_index
        else:
            largest = index
        if (
            right_index < tree_size
            and self.tree.get_node(right_index).key > self.tree.get_node(largest).key
        ):
            largest = right_index
        if largest != index:
            self.tree.swap(index, largest)
            self.heapify(largest)

    def _build_max_heap(self, iterable, priorities):
        for _, _ in zip(iterable, priorities):
            pass

    def get_max(self):
        return self.tree.root().value

    def extract_max(self):
        if self.tree.node_count() < 1:
            raise ValueError("heap underflow")
        _max = self.tree.root().value
        if self.tree.node_count() == 1:
            self.tree.remove(0)
        else:
            # the reason we can use node count to find the last index is
            # because when we fill the tree, we make sure to full pack the
            # binary tree structure. i.e. we don't just fill the left branch,
            # for example
            self.tree.swap(0, self.tree.node_count() - 1)
            self.tree.remove(self.tree.node_count() - 1)
            self.heapify(0)

        return _max

    def increase_key(self, index, key):
        curr_node = self.tree.get_node(index)
        if key < curr_node.key:
            raise ValueError("new key is smaller than current key")
        self.tree.set_node(index, HeapItem(key, curr_node.value))
        while index > 0 and self.tree.parent(index).key < self.tree.get_node(index).key:
            self.tree.swap(index, self.tree.parent_index(index))
            index = self.tree.parent_index(index)

    def insert(self, key, value):
        new_node_idx = self.tree.node_count()
        self.tree.set_node(new_node_idx, HeapItem(float("-inf"), value))
        self.increase_key(new_node_idx, key)

    def size(self):
        return self.tree.node_count()


if __name__ == "__main__":
    values = [(i, i) for i in range(100)]
    mh = MaxHeap()
    for idx, val in values:
        mh.insert(idx, val)
    print(mh.tree)
    sorted_values = [mh.extract_max() for _ in range(mh.size())]
    print(sorted_values)
