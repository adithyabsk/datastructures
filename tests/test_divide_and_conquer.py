"""Divide and Conquer Unit Tests"""

SEED = 42


def test_binary_search_find_num():
    import random

    from datastructures import binary_search

    random.seed(SEED)

    def find_num(target):
        return lambda x: x >= target

    data = [random.randrange(-100, 100) for _ in range(100)]

    target1 = 53
    data.append(target1)
    data.sort()
    idx1 = data.index(target1)

    assert binary_search(data, find_num(target1)) == idx1

    target2 = 72
    data.append(target2)
    data.sort()
    idx2 = data.index(target2)

    assert binary_search(data, find_num(target2)) == idx2


def test_binary_search_last_zero():
    import random

    from datastructures import binary_search

    random.seed(SEED)

    def find_last_element_less_than_zero(x):
        return x > 0

    # note if there are duplicate numbers then this method will find the last
    # element such that the above condition holds

    data = [random.randrange(-100, 100) for _ in range(100)]
    target_num = 0
    data.append(target_num)
    data.sort()

    # if there are duplicates, we need to find the last one
    # https://stackoverflow.com/a/6890255/3262054
    ground_truth_idx = len(data) - 1 - data[::-1].index(target_num)

    assert (
        binary_search(data, find_last_element_less_than_zero) - 1
    ) == ground_truth_idx
