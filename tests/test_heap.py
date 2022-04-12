"""Unit tests for heap."""

import pytest


def test_basic():
    import random

    from datastructures import MaxHeap

    data = [random.randrange(-100, 100) for _ in range(100)]
    # keys need to be unique otherwise, the ground truth output could end up
    # in a different order when the key is the same
    keys = random.sample(range(-1000, 1000), 100)

    mh = MaxHeap(iterable=data, keys=keys)
    sorted_values = [mh.extract_max() for _ in range(mh.size())]
    ground_truth = [d for _, d in sorted(zip(keys, data))]

    assert sorted_values == list(reversed(ground_truth))


def test_empty():
    from datastructures import MaxHeap

    # test empty
    mh = MaxHeap()
    assert pytest.raises(ValueError, mh.get_max)
    assert pytest.raises(ValueError, mh.extract_max)


def test_heapsort():
    import random

    from datastructures import heapsort

    data = [random.randrange(-100, 100) for _ in range(100)]
    out = heapsort(data)
    ground_truth = sorted(data, reverse=True)

    assert out == ground_truth


def test_heapify():
    from datastructures import MaxHeap

    mh = MaxHeap()
    data = list(range(10))
    mh.heapify(reversed(data), data)

    assert mh.size() == 10

    out = [mh.extract_max() for _ in range(mh.size())]

    assert data == out


def test_insert():
    from datastructures import MaxHeap

    mh = MaxHeap()
    data = list(range(10))
    for i in data:
        mh.insert(i, i)
    out = [mh.extract_max() for _ in range(mh.size())]

    assert out == list(reversed(data))


def test_update_priority():
    from datastructures import MaxHeap

    data = list(range(10))
    mh = MaxHeap(reversed(data), data)

    # test both increase, decrease, set same priority of indices
    # also test get_max vs extract_max
    # set the value 0 to priority -1 (previously was 10, should go to the back)
    mh.update_priority(0, -1)
    assert mh.get_max() == 1
    mh.extract_max()
    # set the value 9 to priority 100 (previously was 0, should go to the front)
    mh.update_priority(mh.size() - 2, 100)
    assert mh.get_max() == 9
    mh.extract_max()
    # set the value of 2 to priority (previously was 7, should stay the same)
    mh.update_priority(0, 7)
    assert mh.extract_max() == 2
