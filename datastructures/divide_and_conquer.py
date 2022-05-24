"""Some divide and conquer algorithms."""

from collections import deque


def _is_sorted(iterable):
    return all(iterable[i] <= iterable[i + 1] for i in range(len(iterable) - 1))


def binary_search(iterable, checker_fn):
    """Find the first element where `checker_fn` is `True` in `iterable`

    Note: assumes that the elements are sorted such that checker_fn evaluates to
        `True` for all elements past some index (or no index) and `False` for
        all elements before some index (or no index). In the code this points
        are moved around using the `high` and `low` variables.

    A helpful way to think of the array is filled with ones and zeros, where
    one is `True` and zero is `False`. We can think of this boolean mask as a
    representation of the evaluations of the `checker_fn`. This makes it clear
    what index we are searching for.

            index:  0, 1, 2, 3, 4, 5, 6
    Example array: [0, 0, 0, 1, 1, 1, 1]

    In the above example, we are searching for index 3. It is also possible to
    have an array that is composed of all zeros or all ones. In the former case,
    we would return -1 signifying that no match was found. In the latter case,
    we would return 0 since that is the first element where `checker_fn`
    evaluates to `True`.

    """
    if not _is_sorted(iterable):
        raise ValueError("cannot binary search on unsorted iterable.")

    low = 0
    high = len(iterable)

    # we can use low != high since it is not possible for low > high
    while low != high:
        mid = (low + high) // 2
        if checker_fn(iterable[mid]):
            # if `checker_fn` returns `True` then `mid` must be
            high = mid
        else:
            low = mid + 1

    # the case where `checker_fn` never evaluates to `True` for any index
    if high == len(iterable):
        return -1

    return high


# https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme
def _partition(iterable, start, end, reverse=False):
    def cmp(x, y):
        return x >= y if reverse else x <= y

    # find the median and move it to the end of the current partition--
    # recommended by Sedgewick to prevent worst case performance when array is
    # sorted or reverse order sorted. The traditional implementation is to just
    # set the pivot to value at `end` without moving the median there.
    mid = (start + end) // 2
    # TODO: why does the median need to be moved to the end? I tried it where
    #       I just used the median value, but that seemed to not work in all
    #       cases
    if iterable[mid] < iterable[start]:
        iterable[start], iterable[mid] = iterable[mid], iterable[start]
    if iterable[end] < iterable[start]:
        iterable[start], iterable[end] = iterable[end], iterable[start]
    if iterable[mid] < iterable[start]:
        iterable[mid], iterable[start] = iterable[start], iterable[mid]
    # now the end has the median value
    pivot = iterable[end]

    # temporary pivot
    p_index = start

    for i in range(start, end):
        if cmp(iterable[i], pivot):
            # swap
            iterable[i], iterable[p_index] = iterable[p_index], iterable[i]
            p_index += 1

    iterable[p_index], iterable[end] = iterable[end], iterable[p_index]

    return p_index


def quicksort(iterable, start=0, end=None, reverse=False):
    """Sort a subsection of an iterable in place.

    Uses the `deque` since that standard implementation of quicksort uses
    recursion which can cause stack overflows. Instead, we use an explicit
    stack object.

    """
    if end is None:
        end = len(iterable) - 1

    if start >= end or start < 0:
        raise ValueError("start or end out of range")

    stack = deque([(start, end)])

    while stack:
        start, end = stack.pop()
        p_index = _partition(iterable, start, end, reverse=reverse)

        # add the two partitions to the queue to be sorted
        if p_index - 1 > start:
            stack.append((start, p_index - 1))
        if p_index + 1 < end:
            stack.append((p_index + 1, end))
