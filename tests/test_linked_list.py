"""Linked lists tests."""

import pytest

# Note: These tests are modified from the python standard library unit tests
#       for `collections.deque`. They were also translated to use pytest instead
#       of the builtin unittest module.
#       https://github.com/python/cpython/blob/main/Lib/test/test_deque.py


def test_basics():
    from datastructures import LinkedList

    d = LinkedList(range(-5125, -5000))
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

    # test empty repr
    d2 = LinkedList()
    assert repr(d2) == "LinkedList([])"


def test_maxlen():
    from datastructures import LinkedList

    with pytest.raises(ValueError):
        LinkedList("abc", -1)

    with pytest.raises(ValueError):
        LinkedList("abc", -2)

    it = iter(range(10))
    d = LinkedList(it, maxlen=3)
    assert list(it) == []
    assert repr(d) == "LinkedList([7, 8, 9], maxlen=3)"
    assert list(d) == [7, 8, 9]
    assert d == LinkedList(range(10), 3)
    d.append(10)
    assert list(d) == [8, 9, 10]
    d.appendleft(7)
    assert list(d) == [7, 8, 9]
    d.extend([10, 11])
    assert list(d) == [9, 10, 11]
    d.extendleft([8, 7])
    assert list(d) == [7, 8, 9]

    # this is a mind bending test, basically, if the node we are adding is the
    # object itself, then we should concatenate the output to just [...]
    # otherwise we end up in a recursive loop
    d = LinkedList(range(200), maxlen=10)
    d.append(d)
    assert repr(d)[-50:] == "196, 197, 198, 199, LinkedList([...])], maxlen=10)"
    d = LinkedList(range(10), maxlen=None)
    assert repr(d) == "LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])"


def test_maxlen_zero():
    from datastructures import LinkedList

    it = iter(range(100))
    LinkedList(it, maxlen=0)
    assert list(it) == []

    it = iter(range(100))
    d = LinkedList(maxlen=0)
    d.extend(it)
    assert list(it) == []

    it = iter(range(100))
    d = LinkedList(maxlen=0)
    d.extendleft(it)
    assert list(it) == []


def test_maxlen_attribute():
    from datastructures import LinkedList

    assert LinkedList().maxlen is None
    assert LinkedList("abc").maxlen is None
    assert LinkedList("abc", maxlen=4).maxlen == 4
    assert LinkedList("abc", maxlen=2).maxlen == 2
    assert LinkedList("abc", maxlen=0).maxlen == 0

    with pytest.raises(AttributeError):
        d = LinkedList("abc")
        d.maxlen = 10


def test_count():
    from datastructures import LinkedList

    for s in ("", "abracadabra", "simsalabim" * 500 + "abc"):
        s = list(s)
        d = LinkedList(s)
        for letter in "abcdefghijklmnopqrstuvwxyz":
            assert s.count(letter) == d.count(letter)

    with pytest.raises(TypeError):
        d.count()

    with pytest.raises(TypeError):
        d.count(1, 2)

    class BadCompare:
        def __eq__(self, other):
            raise ArithmeticError

    d = LinkedList([1, 2, BadCompare(), 3])
    with pytest.raises(ArithmeticError):
        d.count(2)

    d = LinkedList([1, 2, 3])
    with pytest.raises(ArithmeticError):
        d.count(BadCompare())

    class MutatingCompare:
        def __eq__(self, other):
            self.d.pop()
            return True

    m = MutatingCompare()
    d = LinkedList([1, 2, 3, m, 4, 5])
    m.d = d
    with pytest.raises(RuntimeError):
        d.count(3)

    # block advance failed after rotation aligned elements on right side of block
    d = LinkedList([None] * 16)
    for _ in range(len(d)):
        d.rotate(-1)
    d.rotate(1)
    assert d.count(1) == 0
    assert d.count(None) == 16


def test_comparisons():
    from datastructures import LinkedList

    d = LinkedList("xabc")
    d.popleft()
    for e in [d, LinkedList("abc"), LinkedList("ab"), LinkedList(), list(d)]:
        assert (d == e) == (type(d) == type(e) and list(d) == list(e))
        assert (d != e) == (not (type(d) == type(e) and list(d) == list(e)))

    args = map(LinkedList, ("", "a", "b", "ab", "ba", "abc", "xba", "xabc", "cba"))
    for x in args:
        for y in args:
            assert (x == y) == (list(x) == list(y))
            assert (x != y) == (list(x) != list(y))
            assert (x < y) == (list(x) < list(y))
            assert (x <= y) == (list(x) <= list(y))
            assert (x > y) == (list(x) > list(y))
            assert (x >= y) == (list(x) >= list(y))
