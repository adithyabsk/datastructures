"""Unit tests for heap."""

import pytest


def test_basic():
    import random

    from datastructures import MaxHeap, MinHeap, PriorityQueue

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

    # priority queue requires that the data is unique
    data = random.sample(range(-1000, 1000), 100)
    pq = PriorityQueue(iterable=data, keys=keys)
    sorted_values = [pq.extract_root() for _ in range(pq.size())]
    ground_truth = [d for _, d in sorted(zip(keys, data))]

    assert sorted_values == list(ground_truth)


def test_empty():
    from datastructures import MaxHeap, MinHeap, PriorityQueue

    # test empty
    max_heap = MaxHeap()
    min_heap = MinHeap()
    pq = PriorityQueue()
    assert pytest.raises(ValueError, max_heap.get_root)
    assert pytest.raises(ValueError, max_heap.extract_root)
    assert pytest.raises(ValueError, min_heap.get_root)
    assert pytest.raises(ValueError, min_heap.extract_root)
    assert pytest.raises(ValueError, pq.get_root)
    assert pytest.raises(ValueError, pq.extract_root)


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
    from datastructures import MaxHeap, MinHeap, PriorityQueue

    max_heap = MaxHeap()
    data = list(range(10))
    max_heap.heapify(data, reversed(data))

    assert max_heap.size() == 10

    out = [max_heap.extract_root() for _ in range(max_heap.size())]

    assert data == out

    min_heap = MinHeap()
    min_heap.heapify(data, data)

    assert min_heap.size() == 10

    out = [min_heap.extract_root() for _ in range(min_heap.size())]

    assert data == out

    pq = PriorityQueue()
    pq.heapify(data, data)

    assert pq.size() == 10

    out = [pq.extract_root() for _ in range(pq.size())]

    assert data == out


def test_insert():
    from datastructures import MaxHeap, MinHeap, PriorityQueue

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

    pq = PriorityQueue()
    for i in data:
        pq.insert(i, i)
    out = [pq.extract_root() for _ in range(pq.size())]

    assert out == list(data)


def test_update_index_priority():
    from datastructures import MaxHeap, MinHeap, PriorityQueue

    data = list(range(10))

    max_heap = MaxHeap(reversed(data), data)
    # test both increase, decrease, set same priority of indices
    # also test get_root vs extract_root
    # set the value 0 to priority -1 (previously was 10, should go to the back)
    max_heap.update_index_priority(0, -1)
    assert max_heap.get_root() == 1
    max_heap.extract_root()
    # set the value 9 to priority 100 (previously was 0, should go to the front)
    max_heap.update_index_priority(max_heap.size() - 2, 100)
    assert max_heap.get_root() == 9
    max_heap.extract_root()
    # set the value of 2 to priority (previously was 7, should stay the same)
    max_heap.update_index_priority(0, 7)
    assert max_heap.extract_root() == 2

    min_heap = MinHeap(data, data)
    min_heap.update_index_priority(0, 100)
    assert min_heap.get_root() == 1
    min_heap.extract_root()
    # set the value 8 to priority -1 (previously was 8, should go to the front)
    # note, we nodes here since there is a sentinel node in the nodes array
    # which results in a size that is less than the actual node array
    min_heap.update_index_priority(len(min_heap.nodes) - 2, -1)
    assert min_heap.get_root() == 8
    min_heap.extract_root()
    # set the value of 2 to priority (previously was 2, should stay the same)
    min_heap.update_index_priority(0, 2)
    assert min_heap.extract_root() == 2

    # same notes as MinHeap
    pq = PriorityQueue(data, data)
    pq.update_index_priority(0, 100)
    assert pq.get_root() == 1
    pq.extract_root()
    pq.update_index_priority(len(pq.nodes) - 2, -1)
    assert pq.get_root() == 8
    pq.extract_root()
    pq.update_index_priority(0, 2)
    assert pq.extract_root() == 2


def test_non_unique():
    from datastructures import PriorityQueue
    from datastructures.heap import HeapItem

    keys = [0, 1]
    data = [1] * 2
    assert pytest.raises(ValueError, PriorityQueue, data, keys)

    pq = PriorityQueue()
    assert pytest.raises(ValueError, pq.heapify, data, keys)

    pq = PriorityQueue([0], [0])
    assert pytest.raises(ValueError, pq.insert, 1, 0)

    pq = PriorityQueue([0], [0])
    # should not raise
    pq.set_node(0, HeapItem(0, 0))
    assert pytest.raises(ValueError, pq.set_node, 1, HeapItem(1, 0))


def test_update_value_priority():
    from datastructures import PriorityQueue

    data = list(range(10))
    keys = list(range(-10, 0))
    pq = PriorityQueue(data, keys)
    # the below test both sift_down and sift_up
    # set value of 0 to priority 100 (lowest)
    pq.update_value_priority(0, 100)
    assert pq.extract_root() == 1
    # bring 0 back to the front of the line
    pq.update_value_priority(0, -100)
    assert pq.extract_root() == 0
    # no change in priority
    pq.update_value_priority(2, -8)
    assert pq.extract_root() == 2
