"""Tree based data structures."""

from collections import deque

# TODO: Use custom deque implementation

# TODO: Update the expand and contract code to double the size of the node
#       array rather than incrementing it up to the required index size. i.e.
#       the size should go 2 --> 4 --> 8 and so on. It should also contract in
#       similar fashion.


class BinaryTree:
    """Binary Tree data structure that stores nodes linearly in an array.

    The tree automatically resizes as it grows and shrinks.

    """

    _sentinel = object()

    def __init__(self, root=None):
        self.nodes = []
        if root is not None:
            self.nodes.append(root)

    def get_node(self, index):
        self._validate_index(index)
        if self.nodes[index] == self._sentinel:
            raise ValueError("index is null")
        else:
            return self.nodes[index]

    def set_node(self, index, value):
        if index != 0:
            # note we can set indices past the current length of `self.nodes`
            # as long as they have a parent--so we do not use `_validate_index`
            if index < 0:
                raise ValueError("index is negative")
            try:
                self.get_node(self.parent_index(index))
            except ValueError:
                raise ValueError("node does not have parent")
            self._check_extend_internal(index)
            self.nodes[index] = value
        else:
            self.set_root(value)

    def left(self, index):
        return self.get_node(self.left_index(index))

    def right(self, index):
        return self.get_node(self.right_index(index))

    def set_root(self, value):
        self._check_extend_internal(0)
        self.nodes[0] = value

    def parent(self, index):
        return self.get_node(self.parent_index(index))

    def is_leaf(self, index):
        left_index = self.left_index(index)
        right_index = self.right_index(index)
        return not (
            (left_index < len(self.nodes) and self.nodes[left_index] != self._sentinel)
            or (
                right_index < len(self.nodes)
                and self.nodes[right_index] != self._sentinel
            )
        )

    def add_left(self, index, value):
        if not self.node_exists(index):
            raise ValueError("either node does not exist or index out of bounds")
        new_idx = self.left_index(index)
        self._check_extend_internal(new_idx)
        self.nodes[new_idx] = value

    def add_right(self, index, value):
        if not self.node_exists(index):
            raise ValueError("either node does not exist or index out of bounds")
        new_idx = self.right_index(index)
        self._check_extend_internal(new_idx)
        self.nodes[new_idx] = value

    def node_count(self):
        return len([n for n in self.nodes if n != self._sentinel])

    def swap(self, index1, index2):
        if not (self.node_exists(index1) and self.node_exists(index2)):
            raise ValueError("both nodes must exist to swap")
        self.nodes[index1], self.nodes[index2] = self.nodes[index2], self.nodes[index1]

    def root(self):
        if len(self.nodes) >= 1:
            return self.nodes[0]
        else:
            raise ValueError("cannot return root of empty tree")

    def remove(self, index):
        self._validate_index(index)
        if self.is_leaf(index):
            self.nodes[index] = self._sentinel
            self._cleanup()
        else:
            raise ValueError("cannot remove non-leaf node")

    def node_exists(self, index):
        try:
            # note that sentinel checking is covered in get_node
            self.get_node(index)
        except ValueError:
            return False
        return True

    def breadth_first_traversal(self):
        queue = deque()
        if self.node_count() == 0:
            return
        explored = {0}
        queue.append(0)
        while len(queue) > 0:
            idx = queue.popleft()
            yield idx, self.nodes[idx]
            left_idx = self.left_index(idx)
            right_idx = self.right_index(idx)
            if not self._null_index(left_idx) and left_idx not in explored:
                explored.add(left_idx)
                queue.append(left_idx)
            if not self._null_index(right_idx) and right_idx not in explored:
                explored.add(right_idx)
                queue.append(right_idx)

    def depth_first_traversal(self):
        stack = deque()
        if self.node_count() == 0:
            return
        explored = {0}
        stack.append(0)
        while len(stack) > 0:
            idx = stack.pop()
            yield idx, self.nodes[idx]
            left_idx = self.left_index(idx)
            right_idx = self.right_index(idx)
            if not self._null_index(right_idx) and right_idx not in explored:
                explored.add(right_idx)
                stack.append(right_idx)
            if not self._null_index(left_idx) and left_idx not in explored:
                explored.add(left_idx)
                stack.append(left_idx)

    def breadth_first_search(self, target):
        for i, node in self.breadth_first_traversal():
            if node == target:
                return i
        return -1

    def depth_first_search(self, target):
        for i, node in self.depth_first_traversal():
            if node == target:
                return i
        return -1

    @staticmethod
    def parent_index(index):
        return (index - 1) // 2

    @staticmethod
    def left_index(index):
        return 2 * index + 1

    @staticmethod
    def right_index(index):
        return 2 * index + 2

    def _validate_index(self, index):
        if index >= len(self.nodes) or index < 0:
            raise ValueError("index out of range of tree nodes")

    def _null_index(self, index):
        if index >= len(self.nodes) or index < 0 or self.nodes[index] == self._sentinel:
            return True
        return False

    def _check_extend_internal(self, index):
        if index >= len(self.nodes):
            extend_count = (index + 1) - len(self.nodes)
            self.nodes.extend([self._sentinel] * extend_count)

    def _node_level_string(
        self, index, level=0, prepend="", is_left=True, is_only=False
    ):
        l_template = "├── "
        r_template = "└── "
        l_only_template = "└•─ "
        r_only_template = "└°─ "
        prepend_template = "│   "
        empty_template = "    "
        rslt = prepend
        if index != 0:
            if is_only:
                if is_left:
                    rslt += l_only_template
                else:
                    rslt += r_only_template
            else:
                if is_left:
                    rslt += l_template
                else:
                    rslt += r_template
        if self.node_exists(index):
            rslt += f"{self.get_node(index)}\n"
            left_exists = self.node_exists(self.left_index(index))
            right_exists = self.node_exists(self.right_index(index))
            if level >= 1:
                # is left and not only child
                if is_left and not (left_exists and not right_exists):
                    prepend += prepend_template
                else:
                    prepend += empty_template
            rslt += self._node_level_string(
                self.left_index(index),
                level + 1,
                prepend,
                is_left=True,
                is_only=(left_exists and not right_exists),
            )
            rslt += self._node_level_string(
                self.right_index(index),
                level + 1,
                prepend,
                is_left=False,
                is_only=(not left_exists and right_exists),
            )
        else:
            return ""

        return rslt

    def _cleanup(self):
        """Remove unnecessary length from the nodes array.

        This is the opposite of `_check_extend_internal`. It removes any
        sentinel nodes that no longer have a parent and aren't required as
        buffer to an existing node.
        """
        # intentionally exclude the 0th index
        for i in range(len(self.nodes) - 1, 0, -1):
            if self.nodes[i] == self.nodes[i - 1] == self._sentinel:
                del self.nodes[i]
            else:
                break
        if len(self.nodes) == 1 and self.root() == self._sentinel:
            del self.nodes[0]

    def __str__(self):
        if len(self.nodes) == 0:
            return "(empty)"
        else:
            return self._node_level_string(0)

    def __repr__(self):
        return f"BinaryTree({self.nodes})"
