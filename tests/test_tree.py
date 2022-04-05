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
