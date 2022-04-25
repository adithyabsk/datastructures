"""Unit tests for heap."""

import pytest


def test_basic():
    import random

    from datastructures import MaxHeap, MinHeap

    data = [random.randrange(-100, 100) for _ in range(100)]
    # keys need to be unique otherwise, the ground truth output could end up
    # in a different order when the key is the same
    keys = random.sample(range(-1000, 1000), 100)

    max_heap = MaxHeap(iterable=data, keys=keys)
    sorted_values = [max_heap.extract_root() for _ in range(max_heap.size())]
    ground_truth = [d for _, d in sorted(zip(keys, data))]

    assert sorted_values == list(reversed(ground_truth))

    min_heap = MinHeap(iterable=data, keys=keys)
    sorted_values = [min_heap.extract_root() for _ in range(min_heap.size())]
    ground_truth = [d for _, d in sorted(zip(keys, data))]

    assert sorted_values == list(ground_truth)


def test_empty():
    from datastructures import MaxHeap, MinHeap

    # test empty
    max_heap = MaxHeap()
    min_heap = MinHeap()
    assert pytest.raises(ValueError, max_heap.get_root)
    assert pytest.raises(ValueError, max_heap.extract_root)
    assert pytest.raises(ValueError, min_heap.get_root)
    assert pytest.raises(ValueError, min_heap.extract_root)


def test_heapsort():
    import random

    from datastructures import heapsort

    data = [random.randrange(-100, 100) for _ in range(100)]

    out_forward = heapsort(data)
    ground_truth_forward = sorted(data)
    assert out_forward == ground_truth_forward

    out_reverse = heapsort(data, reverse=True)
    ground_truth_reverse = sorted(data, reverse=True)
    assert out_reverse == ground_truth_reverse


def test_heapify():
    from datastructures import MaxHeap, MinHeap

    max_heap = MaxHeap()
    data = list(range(10))
    max_heap.heapify(reversed(data), data)

    assert max_heap.size() == 10

    out = [max_heap.extract_root() for _ in range(max_heap.size())]

    assert data == out

    min_heap = MinHeap()
    min_heap.heapify(data, data)

    assert min_heap.size() == 10

    out = [min_heap.extract_root() for _ in range(min_heap.size())]

    assert data == out


def test_insert():
    from datastructures import MaxHeap, MinHeap

    max_heap = MaxHeap()
    data = list(range(10))
    for i in data:
        max_heap.insert(i, i)
    out = [max_heap.extract_root() for _ in range(max_heap.size())]

    assert out == list(reversed(data))

    min_heap = MinHeap()
    for i in data:
        min_heap.insert(i, i)
    out = [min_heap.extract_root() for _ in range(min_heap.size())]

    assert out == list(data)


def test_update_priority():
    from datastructures import MaxHeap, MinHeap

    data = list(range(10))

    max_heap = MaxHeap(reversed(data), data)
    # test both increase, decrease, set same priority of indices
    # also test get_root vs extract_root
    # set the value 0 to priority -1 (previously was 10, should go to the back)
    max_heap.update_priority(0, -1)
    assert max_heap.get_root() == 1
    max_heap.extract_root()
    # set the value 9 to priority 100 (previously was 0, should go to the front)
    max_heap.update_priority(max_heap.size() - 2, 100)
    assert max_heap.get_root() == 9
    max_heap.extract_root()
    # set the value of 2 to priority (previously was 7, should stay the same)
    max_heap.update_priority(0, 7)
    assert max_heap.extract_root() == 2

    min_heap = MinHeap(data, data)
    min_heap.update_priority(0, 100)
    assert min_heap.get_root() == 1
    min_heap.extract_root()
    # set the value 8 to priority -1 (previously was 8, should go to the front)
    # note, we nodes here since there is a sentinel node in the nodes array
    # which results in a size that is less than the actual node array
    min_heap.update_priority(len(min_heap.nodes) - 2, -1)
    assert min_heap.get_root() == 8
    min_heap.extract_root()
    # set the value of 2 to priority (previously was 2, should stay the same)
    min_heap.update_priority(0, 2)
    assert min_heap.extract_root() == 2
