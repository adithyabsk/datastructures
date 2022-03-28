"""Linked lists tests."""

import pytest

# Note: These tests are modified from the python standard library unit tests
#       for `collections.deque`. They were also translated to use pytest instead
#       of the builtin unittest module.
#       https://github.com/python/cpython/blob/main/Lib/test/test_deque.py


class MutateCmp:
    def __init__(self, deque, result):
        self.deque = deque
        self.result = result

    def __eq__(self, other):
        self.deque.clear()
        return self.result


class BadCmp:
    def __eq__(self, other):
        raise RuntimeError


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

    class BadCompareArithmetic:
        def __eq__(self, other):
            raise ArithmeticError

    d = LinkedList([1, 2, BadCompareArithmetic(), 3])
    with pytest.raises(ArithmeticError):
        d.count(2)

    d = LinkedList([1, 2, 3])
    with pytest.raises(ArithmeticError):
        d.count(BadCompareArithmetic())

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


def test_contains():
    from datastructures import LinkedList

    n = 200

    d = LinkedList(range(n))
    for i in range(n):
        assert i in d
    assert (n + 1) not in d

    # Test detection of mutation during iteration
    d = LinkedList(range(n))
    d[n // 2] = MutateCmp(d, False)
    with pytest.raises(RuntimeError):
        n in d  # noqa: B015

    # Test detection of comparison exceptions
    d = LinkedList(range(n))
    d[n // 2] = BadCmp()
    with pytest.raises(RuntimeError):
        n in d  # noqa: B015


def test_contains_count_stop_crashes():
    from datastructures import LinkedList

    class A:
        def __eq__(self, other):
            d.clear()
            return NotImplemented

    d = LinkedList([A(), A()])
    with pytest.raises(RuntimeError):
        _ = 3 in d
    d = LinkedList([A(), A()])
    with pytest.raises(RuntimeError):
        _ = d.count(3)


def test_extend():
    from datastructures import LinkedList

    d = LinkedList("a")
    with pytest.raises(TypeError):
        d.extend(1)
    d.extend("bcd")
    assert list(d) == list("abcd")
    d.extend(d)
    assert list(d) == list("abcdabcd")


def test_add():
    from datastructures import LinkedList

    d = LinkedList()
    e = LinkedList("abc")
    f = LinkedList("def")
    assert d + d == LinkedList()
    assert e + f == LinkedList("abcdef")
    assert e + e == LinkedList("abcabc")
    assert e + d == LinkedList("abc")
    assert d + e == LinkedList("abc")
    assert d + d == LinkedList()
    assert e + d == LinkedList("abc")
    assert d + e == LinkedList("abc")

    g = LinkedList("abcdef", maxlen=4)
    h = LinkedList("gh")
    assert g + h == LinkedList("efgh")

    with pytest.raises(TypeError):
        LinkedList("abc") + "def"


def test_iadd():
    from datastructures import LinkedList

    d = LinkedList("a")
    d += "bcd"
    assert list(d) == list("abcd")
    d += d
    assert list(d) == list("abcdabcd")


def test_extendleft():
    from datastructures import LinkedList

    def fail():
        raise SyntaxError

    d = LinkedList("a")
    with pytest.raises(TypeError):
        d.extendleft(1)
    d.extendleft("bcd")
    assert list(d) == list(reversed("abcd"))
    d.extendleft(d)
    assert list(d) == list("abcddcba")
    d = LinkedList()
    d.extendleft(range(1000))
    assert list(d) == list(reversed(range(1000)))
    with pytest.raises(SyntaxError):
        d.extendleft(fail())


def test_getitem():
    import random

    from datastructures import LinkedList

    random.seed(0)

    n = 200
    d = LinkedList(range(n))
    cmp_list = list(range(n))
    for i in range(n):
        d.popleft()
        cmp_list.pop(0)
        if random.random() < 0.5:
            d.append(i)
            cmp_list.append(i)
        for j in range(1 - len(cmp_list), len(cmp_list)):
            assert d[j] == cmp_list[j]

    d = LinkedList("superman")
    assert d[0] == "s"
    assert d[-1] == "n"
    d = LinkedList()
    with pytest.raises(IndexError):
        d.__getitem__(0)
    with pytest.raises(IndexError):
        d.__getitem__(-1)


def test_index():
    from datastructures import LinkedList

    for n in 1, 2, 30, 40, 200:
        d = LinkedList(range(n))
        for i in range(n):
            assert d.index(i) == i

        with pytest.raises(ValueError):
            d.index(n + 1)

        # Test detection of mutation during iteration
        d = LinkedList(range(n))
        d[n // 2] = MutateCmp(d, False)
        with pytest.raises(RuntimeError):
            d.index(n)

        # Test detection of comparison exceptions
        d = LinkedList(range(n))
        d[n // 2] = BadCmp()
        with pytest.raises(RuntimeError):
            d.index(n)

    # Test start and stop arguments behavior matches list.index()
    elements = "ABCDEFGHI"
    non_element = "Z"
    d = LinkedList(elements * 2)
    s = list(elements * 2)
    for start in range(-5 - len(s) * 2, 5 + len(s) * 2):
        for stop in range(-5 - len(s) * 2, 5 + len(s) * 2):
            for element in elements + non_element:
                try:
                    target = s.index(element, start, stop)
                except ValueError:
                    with pytest.raises(ValueError):
                        d.index(element, start, stop)
                else:
                    assert d.index(element, start, stop) == target

    # Test large start argument
    d = LinkedList(range(0, 10000, 10))
    for _ in range(100):
        i = d.index(8500, 700)
        assert d[i] == 8500
        # Repeat test with a different internal offset
        d.rotate()


def test_index_bug_24913():
    from datastructures import LinkedList

    d = LinkedList("A" * 3)
    with pytest.raises(ValueError):
        d.index("Hello world", 0, 4)


def test_insert():
    from datastructures import LinkedList

    # Test to make sure insert behaves like lists
    elements = "ABCDEFGHI"
    for i in range(-5 - len(elements) * 2, 5 + len(elements) * 2):
        d = LinkedList("ABCDEFGHI")
        s = list("ABCDEFGHI")
        d.insert(i, "Z")
        s.insert(i, "Z")
        assert list(d) == s


def test_insert_bug_26194():
    from datastructures import LinkedList

    data = "ABC"
    d = LinkedList(data, maxlen=len(data))
    with pytest.raises(IndexError):
        d.insert(2, None)

    elements = "ABCDEFGHI"
    for i in range(-len(elements), len(elements)):
        d = LinkedList(elements, maxlen=len(elements) + 1)
        d.insert(i, "Z")
        if i >= 0:
            assert d[i] == "Z"
        else:
            assert d[i - 1] == "Z"


def test_imul():
    from datastructures import LinkedList

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = LinkedList()
        d *= n
        assert d == LinkedList()
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = LinkedList("a")
        d *= n
        assert d == LinkedList("a" * n)
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 499, 500, 501, 1000):
        d = LinkedList("a", 500)
        d *= n
        assert d == LinkedList("a" * min(n, 500))
        assert d.maxlen == 500

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = LinkedList("abcdef")
        d *= n
        assert d == LinkedList("abcdef" * n)
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 499, 500, 501, 1000):
        d = LinkedList("abcdef", 500)
        d *= n
        assert d == LinkedList(("abcdef" * n)[-500:])
        assert d.maxlen == 500


def test_mul():
    from datastructures import LinkedList

    d = LinkedList("abc")
    assert d * -5 == LinkedList()
    assert d * 0 == LinkedList()
    assert d * 1 == LinkedList("abc")
    assert d * 2 == LinkedList("abcabc")
    assert d * 3 == LinkedList("abcabcabc")
    assert d * 1 is not d

    assert LinkedList() * 0 == LinkedList()
    assert LinkedList() * 1 == LinkedList()
    assert LinkedList() * 5 == LinkedList()

    assert -5 * d == LinkedList()
    assert 0 * d == LinkedList()
    assert 1 * d == LinkedList("abc")
    assert 2 * d == LinkedList("abcabc")
    assert 3 * d == LinkedList("abcabcabc")

    d = LinkedList("abc", maxlen=5)
    assert d * -5 == LinkedList()
    assert d * 0 == LinkedList()
    assert d * 1 == LinkedList("abc")
    assert d * 2 == LinkedList("bcabc")
    assert d * 30 == LinkedList("bcabc")


def test_setitem():
    from datastructures import LinkedList

    n = 200
    d = LinkedList(range(n))
    for i in range(n):
        d[i] = 10 * i
    assert list(d) == [10 * i for i in range(n)]
    _list = list(d)
    for i in range(1 - n, 0, -1):
        d[i] = 7 * i
        _list[i] = 7 * i
    assert list(d) == _list


def test_delitem():
    import random

    from datastructures import LinkedList

    n = 500  # O(n**2) test, don't make this too big
    d = LinkedList(range(n))
    with pytest.raises(IndexError):
        d.__delitem__(-n - 1)
    with pytest.raises(IndexError):
        d.__delitem__(n)
    for i in range(n):
        assert len(d) == n - i
        j = random.randrange(-len(d), len(d))
        val = d[j]
        assert val in d
        del d[j]
        assert val not in d
    assert len(d) == 0


def test_reverse():
    import random

    from datastructures import LinkedList

    n = 500  # O(n**2) test, don't make this too big
    data = [random.random() for _ in range(n)]
    for i in range(n):
        d = LinkedList(data[:i])
        r = d.reverse()
        assert list(d) == list(reversed(data[:i]))
        assert r is None
        d.reverse()
        assert list(d) == data[:i]
    with pytest.raises(TypeError):
        # Arity is zero
        d.reverse(1)


def test_rotate():
    from datastructures import LinkedList

    s = tuple("abcde")
    n = len(s)

    d = LinkedList(s)
    d.rotate(1)  # verify rot(1)
    assert "".join(d) == "eabcd"

    d = LinkedList(s)
    d.rotate(-1)  # verify rot(-1)
    assert "".join(d) == "bcdea"
    d.rotate()  # check default to 1
    assert tuple(d) == s

    for i in range(n * 3):
        d = LinkedList(s)
        e = LinkedList(d)
        d.rotate(i)  # check vs. rot(1) n times
        for _ in range(i):
            e.rotate(1)
        assert tuple(d) == tuple(e)
        d.rotate(-i)  # check that it works in reverse
        assert tuple(d) == s
        e.rotate(n - i)  # check that it wraps forward
        assert tuple(e) == s

    for i in range(n * 3):
        d = LinkedList(s)
        e = LinkedList(d)
        d.rotate(-i)
        for _ in range(i):
            e.rotate(-1)  # check vs. rot(-1) n times
        assert tuple(d) == tuple(e)
        d.rotate(i)  # check that it works in reverse
        assert tuple(d) == s
        e.rotate(i - n)  # check that it wraps backaround
        assert tuple(e) == s

    d = LinkedList(s)
    e = LinkedList(s)
    e.rotate(100_000 + 17)  # verify on long series of rotates
    dr = d.rotate
    for _ in range(100_000 + 17):
        dr()
    assert tuple(d) == tuple(e)

    with pytest.raises(TypeError):
        # Wrong arg type
        d.rotate("x")
    with pytest.raises(TypeError):
        d.rotate(1, 10)

    d = LinkedList()
    d.rotate()  # rotate an empty deque
    assert d == LinkedList()


def test_len():
    from datastructures import LinkedList

    d = LinkedList("ab")
    assert len(d) == 2
    d.popleft()
    assert len(d) == 1
    d.pop()
    assert len(d) == 0
    with pytest.raises(IndexError):
        d.pop()
    assert len(d) == 0
    d.append("c")
    assert len(d) == 1
    d.appendleft("d")
    assert len(d) == 2
    d.clear()
    assert len(d) == 0


def test_underflow():
    from datastructures import LinkedList

    d = LinkedList()
    with pytest.raises(IndexError):
        d.pop()

    with pytest.raises(IndexError):
        d.popleft()


def test_clear():
    from datastructures import LinkedList

    d = LinkedList(range(100))
    assert len(d) == 100
    d.clear()
    assert len(d) == 0
    assert list(d) == []
    # clear an empty deque
    d.clear()
    assert list(d) == []
