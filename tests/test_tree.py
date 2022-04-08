"""Test the tree data structure."""

import pytest


def test_empty_tree():
    from datastructures import BinaryTree

    bt = BinaryTree()

    assert pytest.raises(ValueError, bt.root)
    assert pytest.raises(ValueError, bt.remove, 0)
    assert pytest.raises(ValueError, bt.get_node, 0)
    assert pytest.raises(ValueError, bt.add_left, 0, 0)
    assert pytest.raises(ValueError, bt.add_right, 0, 0)
    assert pytest.raises(ValueError, bt.parent, 0)
    assert pytest.raises(ValueError, bt.left, 0)
    assert pytest.raises(ValueError, bt.right, 0)
    assert str(bt) == "(empty)"

    bt2 = BinaryTree(10)
    assert bt2.root() == 10


def test_get_set_node():
    from datastructures import BinaryTree

    bt = BinaryTree()
    input_data = list(range(-100, -90))
    bt.nodes = input_data

    # test that the data matches the initialized data
    assert bt.get_node(0) == bt.root()
    for node, comp in zip(map(bt.get_node, range(10)), input_data):
        assert node == comp

    new_data = reversed(input_data)
    for i, val in enumerate(new_data):
        bt.set_node(i, val)

    # test that the internal data matches the newly set data
    assert bt.get_node(0) == bt.root()
    for node, comp in zip(map(bt.get_node, range(10)), new_data):
        assert node == comp


def test_node_relationships():
    from datastructures import BinaryTree

    bt = BinaryTree()
    bt.nodes = list(range(10))

    assert bt.left(0) == 1
    assert bt.right(0) == 2
    assert bt.left(1) == 3
    assert bt.right(1) == 4
    assert bt.parent(1) == 0
    assert bt.parent(2) == 0
    assert pytest.raises(ValueError, bt.parent, 0)


def test_add_nodes_and_count():
    from datastructures import BinaryTree

    bt = BinaryTree(-1)

    for i in range(10):
        bt.add_left(i, i + 1)
        bt.add_right(i, i + 2)
    assert bt.left(0) == 1
    assert bt.right(0) == 2
    assert bt.node_count() == 21


def test_print_and_repr():
    from datastructures import BinaryTree

    bt = BinaryTree()
    input_data = list(range(-100, -90))
    bt.nodes = input_data
    template = """-100
├── -99
│   ├── -97
│   │   ├── -93
│   │   └── -92
│   └── -96
│       └•─ -91
└── -98
    ├── -95
    └── -94
"""
    template2 = "BinaryTree([-100, -99, -98, -97, -96, -95, -94, -93, -92, -91])"
    assert str(bt) == template
    assert repr(bt) == template2


def test_lopsided_tree():
    from datastructures import BinaryTree

    bt = BinaryTree()
    bt.set_root(-1)
    prev_left = 0
    for _ in range(5):
        bt.add_left(prev_left, prev_left)
        prev_left = bt.left_index(prev_left)

    # try setting node without parent
    assert pytest.raises(ValueError, bt.set_node, 5, 0)
    # try checking node that is a sentinel
    assert not bt.node_exists(5)

    template = """-1
└•─ 0
    └•─ 1
        └•─ 3
            └•─ 7
                └•─ 15
"""

    assert bt.node_count() == 6
    assert len(bt.nodes) == 32
    assert str(bt) == template

    bt2 = BinaryTree()
    bt2.set_root(-1)
    prev_right = 0
    for _ in range(5):
        bt2.add_right(prev_right, prev_right)
        prev_right = bt.right_index(prev_right)

    template2 = """-1
└°─ 0
    └°─ 2
        └°─ 6
            └°─ 14
                └°─ 30
"""

    assert bt.node_count() == 6
    assert len(bt.nodes) == 32
    assert str(bt2) == template2


def test_is_leaf():
    from datastructures import BinaryTree

    bt = BinaryTree()
    bt.nodes = list(range(10))
    assert all(not bt.is_leaf(n) for n in range(5))
    assert all(bt.is_leaf(n) for n in range(5, 10))


def test_swap():
    from datastructures import BinaryTree

    bt = BinaryTree()
    assert pytest.raises(ValueError, bt.swap, 0, 1)
    bt.nodes = list(range(10))
    bt.swap(0, 9)
    assert bt.root() == 9
    assert bt.get_node(9) == 0


def test_remove():
    from datastructures import BinaryTree

    bt = BinaryTree()
    bt.nodes = list(range(10))
    for i in range(5):
        assert pytest.raises(ValueError, bt.remove, i)
    for i in reversed(range(5, 10)):
        bt.remove(i)

    assert bt.node_count() == 5

    for i in reversed(range(0, 5)):
        bt.remove(i)

    assert bt.node_count() == 0
