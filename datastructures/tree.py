"""Tree based data structures."""

# TODO: Update the expand and contract code to double the size of the node
#       array rather than incrementing it up to the required index size. i.e.
#       the size should go 2 --> 4 --> 8 and so on. It should also contract in
#       similar fashion.

sentinel = object()


class BinaryTree:
    def __init__(self):
        self.nodes = []

    def _validate_index(self, index):
        if index >= len(self.nodes) or index < 0:
            raise ValueError("index out of range")

    def get_node(self, index):
        self._validate_index(index)
        if self.nodes[index] == sentinel:
            raise ValueError("index is null")
        else:
            return self.nodes[index]

    def set_node(self, index, value):
        if index < 0:
            raise ValueError("index out of range")
        if index != 0:
            try:
                self.get_node(self.parent_index(index))
            except ValueError:
                raise ValueError("node does not have parent")
        self._check_extend_internal(index)
        self.nodes[index] = value

    def left(self, index):
        return self.get_node(self.left_index(index))

    def right(self, index):
        return self.get_node(self.right_index(index))

    def parent(self, index):
        return self.get_node(self.parent_index(index))

    def get_str_node(self, index):
        try:
            return str(self.get_node(index))
        except ValueError:
            return "(null)"

    def is_leaf(self, index):
        left_index = self.left_index(index)
        right_index = self.right_index(index)
        return not (
            (left_index < len(self.nodes) and self.nodes[left_index] != sentinel)
            or (right_index < len(self.nodes) and self.nodes[right_index] != sentinel)
        )

    def _check_extend_internal(self, index):
        if index >= len(self.nodes):
            extend_count = (index + 1) - len(self.nodes)
            self.nodes.extend([sentinel] * extend_count)

    def add_left(self, index, value):
        self._validate_index(index)
        self._check_extend_internal(index)
        self.nodes[self.left_index(index)] = value

    def add_right(self, index, value):
        self._validate_index(index)
        self._check_extend_internal(index)
        self.nodes[self.right_index(index)] = value

    def node_count(self):
        return len([n for n in self.nodes if n != sentinel])

    def swap(self, index1, index2):
        self.nodes[index1], self.nodes[index2] = self.nodes[index2], self.nodes[index1]

    def root(self):
        if len(self.nodes) >= 1:
            return self.nodes[0]
        else:
            raise ValueError("cannot return root of empty tree")

    def remove(self, index):
        if self.is_leaf(index):
            self.nodes[index] = sentinel
            self._cleanup()
        else:
            raise ValueError("cannot remove non-leaf node")

    def _cleanup(self):
        """Remove unnecessary length from the nodes array.

        This is the opposite of `_check_extend_internal`. It removes any
        sentinel nodes that no longer have a parent and aren't required as
        buffer to an existing node.
        """
        # intentionally exclude the 0th index
        for i in range(len(self.nodes) - 1, 0, -1):
            if self.nodes[i] == self.nodes[i - 1] == sentinel:
                del self.nodes[i]
            else:
                break
        if len(self.nodes) == 1 and self.root() == sentinel:
            del self.nodes[0]

    @staticmethod
    def parent_index(index):
        return (index - 1) // 2

    @staticmethod
    def left_index(index):
        return 2 * index + 1

    @staticmethod
    def right_index(index):
        return 2 * index + 2

    def node_exists(self, index):
        try:
            node = self.get_node(index)
            if node == sentinel:
                return False
        except ValueError:
            return False
        return True

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
            rslt += f"{self.get_str_node(index)}\n"
            if level >= 1:
                if is_left:
                    prepend += prepend_template
                else:
                    prepend += empty_template
            left_exists = self.node_exists(self.left_index(index))
            right_exists = self.node_exists(self.right_index(index))
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

    def __str__(self):
        if len(self.nodes) == 0:
            return "(empty)"
        else:
            return self._node_level_string(0)

    def __repr__(self):
        return f"BinaryTree({self.nodes})"
