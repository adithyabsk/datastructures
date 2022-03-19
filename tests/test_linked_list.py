"""Linked lists tests."""

# Note: These tests are modified from the python standard library unit tests
#       for `collections.deque`
#       https://github.com/python/cpython/blob/main/Lib/test/test_deque.py


def test_basics():
    from datastructures import LinkedList as deque

    d = deque(range(-5125, -5000))
    d.__init__(range(200))
    for i in range(200, 400):
        d.append(i)
    for i in reversed(range(-200, 0)):
        d.appendleft(i)
    assert list(d) == list(range(-200, 400))
    assert len(d) == 600

    left = [d.popleft() for i in range(250)]
    assert left == list(range(-200, 50))
    assert list(d) == list(range(50, 400))

    right = [d.pop() for i in range(250)]
    right.reverse()
    assert right == list(range(150, 400))
    assert list(d) == list(range(50, 150))
