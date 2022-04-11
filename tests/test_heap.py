"""Unit tests for heap."""


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
