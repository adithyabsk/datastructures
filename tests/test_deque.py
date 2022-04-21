"""Linked lists tests."""

import pytest

# Note: These tests are modified from the python standard library unit tests
#       for `collections.deque`. They were also translated to use pytest instead
#       of the builtin unittest module.
#       https://github.com/python/cpython/blob/main/Lib/test/test_deque.py

BIG = 100_00


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
    from datastructures import Deque

    d = Deque(range(-5125, -5000))
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
    d2 = Deque()
    assert repr(d2) == "Deque([])"


def test_maxlen():
    from datastructures import Deque

    with pytest.raises(ValueError):
        Deque("abc", -1)

    with pytest.raises(ValueError):
        Deque("abc", -2)

    it = iter(range(10))
    d = Deque(it, maxlen=3)
    assert list(it) == []
    assert repr(d) == "Deque([7, 8, 9], maxlen=3)"
    assert list(d) == [7, 8, 9]
    assert d == Deque(range(10), 3)
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
    d = Deque(range(200), maxlen=10)
    d.append(d)
    assert repr(d)[-50:] == "195, 196, 197, 198, 199, Deque([...])], maxlen=10)"
    d = Deque(range(10), maxlen=None)
    assert repr(d) == "Deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])"


def test_maxlen_zero():
    from datastructures import Deque

    it = iter(range(100))
    Deque(it, maxlen=0)
    assert list(it) == []

    it = iter(range(100))
    d = Deque(maxlen=0)
    d.extend(it)
    assert list(it) == []

    it = iter(range(100))
    d = Deque(maxlen=0)
    d.extendleft(it)
    assert list(it) == []


def test_maxlen_attribute():
    from datastructures import Deque

    assert Deque().maxlen is None
    assert Deque("abc").maxlen is None
    assert Deque("abc", maxlen=4).maxlen == 4
    assert Deque("abc", maxlen=2).maxlen == 2
    assert Deque("abc", maxlen=0).maxlen == 0

    with pytest.raises(AttributeError):
        d = Deque("abc")
        d.maxlen = 10


def test_count():
    from datastructures import Deque

    for s in ("", "abracadabra", "simsalabim" * 500 + "abc"):
        s = list(s)
        d = Deque(s)
        for letter in "abcdefghijklmnopqrstuvwxyz":
            assert s.count(letter) == d.count(letter)

    with pytest.raises(TypeError):
        d.count()

    with pytest.raises(TypeError):
        d.count(1, 2)

    class BadCompareArithmetic:
        def __eq__(self, other):
            raise ArithmeticError

    d = Deque([1, 2, BadCompareArithmetic(), 3])
    with pytest.raises(ArithmeticError):
        d.count(2)

    d = Deque([1, 2, 3])
    with pytest.raises(ArithmeticError):
        d.count(BadCompareArithmetic())

    class MutatingCompare:
        def __eq__(self, other):
            self.d.pop()
            return True

    m = MutatingCompare()
    d = Deque([1, 2, 3, m, 4, 5])
    m.d = d
    with pytest.raises(RuntimeError):
        d.count(3)

    # block advance failed after rotation aligned elements on right side of block
    d = Deque([None] * 16)
    for _ in range(len(d)):
        d.rotate(-1)
    d.rotate(1)
    assert d.count(1) == 0
    assert d.count(None) == 16


def test_comparisons():
    from datastructures import Deque

    d = Deque("xabc")
    d.popleft()
    for e in [d, Deque("abc"), Deque("ab"), Deque(), list(d)]:
        assert (d == e) == (type(d) == type(e) and list(d) == list(e))
        assert (d != e) == (not (type(d) == type(e) and list(d) == list(e)))

    args = list(map(Deque, ("", "a", "b", "ab", "ba", "abc", "xba", "xabc", "cba")))
    for x in args:
        for y in args:
            assert (x == y) == (list(x) == list(y))
            assert (x != y) == (list(x) != list(y))
            assert (x < y) == (list(x) < list(y))
            assert (x <= y) == (list(x) <= list(y))
            assert (x > y) == (list(x) > list(y))
            assert (x >= y) == (list(x) >= list(y))

    # check raises
    a = Deque("abc")
    other = list("abc")
    assert pytest.raises(TypeError, a.__lt__, other)
    assert pytest.raises(TypeError, a.__le__, other)
    assert pytest.raises(TypeError, a.__gt__, other)
    assert pytest.raises(TypeError, a.__ge__, other)


def test_contains():
    from datastructures import Deque

    n = 200

    d = Deque(range(n))
    for i in range(n):
        assert i in d
    assert (n + 1) not in d

    # Test detection of mutation during iteration
    d = Deque(range(n))
    d[n // 2] = MutateCmp(d, False)
    with pytest.raises(RuntimeError):
        n in d  # noqa: B015

    # Test detection of comparison exceptions
    d = Deque(range(n))
    d[n // 2] = BadCmp()
    with pytest.raises(RuntimeError):
        n in d  # noqa: B015


def test_contains_count_stop_crashes():
    from datastructures import Deque

    class A:
        def __eq__(self, other):
            d.clear()
            return NotImplemented

    d = Deque([A(), A()])
    with pytest.raises(RuntimeError):
        _ = 3 in d
    d = Deque([A(), A()])
    with pytest.raises(RuntimeError):
        _ = d.count(3)


def test_extend():
    from datastructures import Deque

    d = Deque("a")
    with pytest.raises(TypeError):
        d.extend(1)
    d.extend("bcd")
    assert list(d) == list("abcd")
    d.extend(d)
    assert list(d) == list("abcdabcd")


def test_add():
    from datastructures import Deque

    d = Deque()
    e = Deque("abc")
    f = Deque("def")
    assert d + d == Deque()
    assert e + f == Deque("abcdef")
    assert e + e == Deque("abcabc")
    assert e + d == Deque("abc")
    assert d + e == Deque("abc")
    assert d + d == Deque()
    assert e + d == Deque("abc")
    assert d + e == Deque("abc")

    g = Deque("abcdef", maxlen=4)
    h = Deque("gh")
    assert g + h == Deque("efgh")

    with pytest.raises(TypeError):
        Deque("abc") + "def"


def test_iadd():
    from datastructures import Deque

    d = Deque("a")
    d += "bcd"
    assert list(d) == list("abcd")
    d += d
    assert list(d) == list("abcdabcd")


def test_extendleft():
    from datastructures import Deque

    def fail():
        raise SyntaxError

    d = Deque("a")
    with pytest.raises(TypeError):
        d.extendleft(1)
    d.extendleft("bcd")
    assert list(d) == list(reversed("abcd"))
    d.extendleft(d)
    assert list(d) == list("abcddcba")
    d = Deque()
    d.extendleft(range(1000))
    assert list(d) == list(reversed(range(1000)))
    with pytest.raises(SyntaxError):
        d.extendleft(fail())


def test_getitem():
    import random

    from datastructures import Deque

    random.seed(0)

    n = 200
    d = Deque(range(n))
    cmp_list = list(range(n))
    for i in range(n):
        d.popleft()
        cmp_list.pop(0)
        if random.random() < 0.5:
            d.append(i)
            cmp_list.append(i)
        for j in range(1 - len(cmp_list), len(cmp_list)):
            assert d[j] == cmp_list[j]

    d = Deque("superman")
    assert d[0] == "s"
    assert d[-1] == "n"

    d = Deque()
    assert pytest.raises(IndexError, d.__getitem__, 0)
    assert pytest.raises(IndexError, d.__getitem__, -1)

    other = 1.5
    assert pytest.raises(TypeError, d.__getitem__, other)


def test_index():
    from datastructures import Deque

    for n in 1, 2, 30, 40, 200:
        d = Deque(range(n))
        for i in range(n):
            assert d.index(i) == i

        with pytest.raises(ValueError):
            d.index(n + 1)

        # Test detection of mutation during iteration
        d = Deque(range(n))
        d[n // 2] = MutateCmp(d, False)
        with pytest.raises(RuntimeError):
            d.index(n)

        # Test detection of comparison exceptions
        d = Deque(range(n))
        d[n // 2] = BadCmp()
        with pytest.raises(RuntimeError):
            d.index(n)

    # Test start and stop arguments behavior matches list.index()
    elements = "ABCDEFGHI"
    non_element = "Z"
    d = Deque(elements * 2)
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
    d = Deque(range(0, 10000, 10))
    for _ in range(100):
        i = d.index(8500, 700)
        assert d[i] == 8500
        # Repeat test with a different internal offset
        d.rotate()


def test_index_bug_24913():
    from datastructures import Deque

    d = Deque("A" * 3)
    with pytest.raises(ValueError):
        d.index("Hello world", 0, 4)


def test_insert():
    from datastructures import Deque

    # Test to make sure insert behaves like lists
    elements = "ABCDEFGHI"
    for i in range(-5 - len(elements) * 2, 5 + len(elements) * 2):
        d = Deque("ABCDEFGHI")
        s = list("ABCDEFGHI")
        d.insert(i, "Z")
        s.insert(i, "Z")
        assert list(d) == s


def test_insert_bug_26194():
    from datastructures import Deque

    data = "ABC"
    d = Deque(data, maxlen=len(data))
    with pytest.raises(IndexError):
        d.insert(2, None)

    elements = "ABCDEFGHI"
    for i in range(-len(elements), len(elements)):
        d = Deque(elements, maxlen=len(elements) + 1)
        d.insert(i, "Z")
        if i >= 0:
            assert d[i] == "Z"
        else:
            assert d[i - 1] == "Z"


def test_imul():
    from datastructures import Deque

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = Deque()
        d *= n
        assert d == Deque()
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = Deque("a")
        d *= n
        assert d == Deque("a" * n)
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 499, 500, 501, 1000):
        d = Deque("a", 500)
        d *= n
        assert d == Deque("a" * min(n, 500))
        assert d.maxlen == 500

    for n in (-10, -1, 0, 1, 2, 10, 1000):
        d = Deque("abcdef")
        d *= n
        assert d == Deque("abcdef" * n)
        assert d.maxlen is None

    for n in (-10, -1, 0, 1, 2, 10, 499, 500, 501, 1000):
        d = Deque("abcdef", 500)
        d *= n
        assert d == Deque(("abcdef" * n)[-500:])
        assert d.maxlen == 500

    d = Deque()
    other = 1.5
    assert pytest.raises(TypeError, d.__imul__, other)


def test_mul():
    from datastructures import Deque

    d = Deque("abc")
    assert d * -5 == Deque()
    assert d * 0 == Deque()
    assert d * 1 == Deque("abc")
    assert d * 2 == Deque("abcabc")
    assert d * 3 == Deque("abcabcabc")
    assert d * 1 is not d

    assert Deque() * 0 == Deque()
    assert Deque() * 1 == Deque()
    assert Deque() * 5 == Deque()

    assert -5 * d == Deque()
    assert 0 * d == Deque()
    assert 1 * d == Deque("abc")
    assert 2 * d == Deque("abcabc")
    assert 3 * d == Deque("abcabcabc")

    d = Deque("abc", maxlen=5)
    assert d * -5 == Deque()
    assert d * 0 == Deque()
    assert d * 1 == Deque("abc")
    assert d * 2 == Deque("bcabc")
    assert d * 30 == Deque("bcabc")

    d = Deque()
    other = 1.5
    assert pytest.raises(TypeError, d.__mul__, other)


def test_setitem():
    from datastructures import Deque

    n = 200
    d = Deque(range(n))
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

    from datastructures import Deque

    n = 500  # O(n**2) test, don't make this too big
    d = Deque(range(n))
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

    from datastructures import Deque

    n = 500  # O(n**2) test, don't make this too big
    data = [random.random() for _ in range(n)]
    for i in range(n):
        d = Deque(data[:i])
        r = d.reverse()
        assert list(d) == list(reversed(data[:i]))
        assert r is None
        d.reverse()
        assert list(d) == data[:i]
    with pytest.raises(TypeError):
        # Arity is zero
        d.reverse(1)


def test_rotate():
    from datastructures import Deque

    s = tuple("abcde")
    n = len(s)

    d = Deque(s)
    d.rotate(1)  # verify rot(1)
    assert "".join(d) == "eabcd"

    d = Deque(s)
    d.rotate(-1)  # verify rot(-1)
    assert "".join(d) == "bcdea"
    d.rotate()  # check default to 1
    assert tuple(d) == s

    for i in range(n * 3):
        d = Deque(s)
        e = Deque(d)
        d.rotate(i)  # check vs. rot(1) n times
        for _ in range(i):
            e.rotate(1)
        assert tuple(d) == tuple(e)
        d.rotate(-i)  # check that it works in reverse
        assert tuple(d) == s
        e.rotate(n - i)  # check that it wraps forward
        assert tuple(e) == s

    for i in range(n * 3):
        d = Deque(s)
        e = Deque(d)
        d.rotate(-i)
        for _ in range(i):
            e.rotate(-1)  # check vs. rot(-1) n times
        assert tuple(d) == tuple(e)
        d.rotate(i)  # check that it works in reverse
        assert tuple(d) == s
        e.rotate(i - n)  # check that it wraps backaround
        assert tuple(e) == s

    d = Deque(s)
    e = Deque(s)
    e.rotate(BIG + 17)  # verify on long series of rotates
    dr = d.rotate
    for _ in range(BIG + 17):
        dr()
    assert tuple(d) == tuple(e)

    with pytest.raises(TypeError):
        # Wrong arg type
        d.rotate("x")
    with pytest.raises(TypeError):
        d.rotate(1, 10)

    d = Deque()
    d.rotate()  # rotate an empty deque
    assert d == Deque()


def test_len():
    from datastructures import Deque

    d = Deque("ab")
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
    from datastructures import Deque

    d = Deque()
    with pytest.raises(IndexError):
        d.pop()

    with pytest.raises(IndexError):
        d.popleft()


def test_clear():
    from datastructures import Deque

    d = Deque(range(100))
    assert len(d) == 100
    d.clear()
    assert len(d) == 0
    assert list(d) == []
    # clear an empty deque
    d.clear()
    assert list(d) == []


def test_remove():
    from datastructures import Deque

    d = Deque("abcdefghcij")
    d.remove("c")
    assert d == Deque("abdefghcij")
    d.remove("c")
    assert d == Deque("abdefghij")
    with pytest.raises(ValueError):
        d.remove("c")
    assert d == Deque("abdefghij")

    # Handle comparison errors
    d = Deque(["a", "b", BadCmp(), "c"])
    e = Deque(d)
    with pytest.raises(RuntimeError):
        d.remove("c")
    for x, y in zip(d, e):
        # verify that original order and values are retained.
        assert x is y

    # Handle evil mutator
    for match in (True, False):
        d = Deque(["ab"])
        d.extend([MutateCmp(d, match), "c"])
        # changed to RuntimeError for consistency (original test checked for an
        # IndexError)
        with pytest.raises(RuntimeError):
            d.remove("c")
        assert d == Deque()


def test_repr():
    from datastructures import Deque

    d = Deque(range(200))
    e = eval(repr(d))
    assert list(d) == list(e)
    d.append(d)
    assert repr(d)[-40:] == " 195, 196, 197, 198, 199, Deque([...])])"


def test_init():
    from datastructures import Deque

    with pytest.raises(TypeError):
        Deque("abc", 2, 3)
    with pytest.raises(TypeError):
        Deque(1)


def test_hash():
    from datastructures import Deque

    with pytest.raises(TypeError):
        hash(Deque("abc"))


def test_long_steadystate_queue_popleft():
    from datastructures import Deque

    for size in (0, 1, 2, 100, 1000):
        d = Deque(range(size))
        append, pop = d.append, d.popleft
        for i in range(size, BIG):
            append(i)
            x = pop()
            if x != i - size:
                assert x == i - size
        assert list(d) == list(range(BIG - size, BIG))


def test_long_steadystate_queue_popright():
    from datastructures import Deque

    for size in (0, 1, 2, 100, 1000):
        d = Deque(reversed(range(size)))
        append, pop = d.appendleft, d.pop
        for i in range(size, BIG):
            append(i)
            x = pop()
            if x != i - size:
                assert x == i - size
        assert list(reversed(list(d))) == list(range(BIG - size, BIG))


def test_big_queue_popleft():
    from datastructures import Deque

    d = Deque()
    append, pop = d.append, d.popleft
    for i in range(BIG):
        append(i)
    for i in range(BIG):
        x = pop()
        if x != i:
            assert x == i


def test_big_queue_popright():
    from datastructures import Deque

    d = Deque()
    append, pop = d.appendleft, d.pop
    for i in range(BIG):
        append(i)
    for i in range(BIG):
        x = pop()
        if x != i:
            assert x == i


def test_big_stack_right():
    from datastructures import Deque

    d = Deque()
    append, pop = d.append, d.pop
    for i in range(BIG):
        append(i)
    for i in reversed(range(BIG)):
        x = pop()
        if x != i:
            assert x == i
    assert len(d) == 0


def test_big_stack_left():
    from datastructures import Deque

    d = Deque()
    append, pop = d.appendleft, d.popleft
    for i in range(BIG):
        append(i)
    for i in reversed(range(BIG)):
        x = pop()
        if x != i:
            assert x == i
    assert len(d) == 0


def test_roundtrip_iter_init():
    from datastructures import Deque

    d = Deque(range(200))
    e = Deque(d)
    assert id(d) != id(e)
    assert list(d) == list(e)


def test_pickle():
    import pickle

    from datastructures import Deque

    for d in Deque(range(200)), Deque(range(200), 100):
        for i in range(pickle.HIGHEST_PROTOCOL + 1):
            s = pickle.dumps(d, i)
            e = pickle.loads(s)
            assert id(e) != id(d)
            assert list(e) == list(d)
            assert e.maxlen == d.maxlen


def test_pickle_recursive():
    import pickle

    from datastructures import Deque

    for d in Deque("abc"), Deque("abc", 3):
        d.append(d)
        for i in range(pickle.HIGHEST_PROTOCOL + 1):
            e = pickle.loads(pickle.dumps(d, i))
            assert id(e) != id(d)
            assert id(e[-1]) == id(e)
            assert e.maxlen == d.maxlen


def test_iterator_pickle():
    import pickle

    from datastructures import Deque

    orig = Deque(range(200))
    data = [i * 1.01 for i in orig]
    for proto in range(pickle.HIGHEST_PROTOCOL + 1):
        # initial iterator
        itorg = iter(orig)
        dump = pickle.dumps((itorg, orig), proto)
        it, d = pickle.loads(dump)
        for i, x in enumerate(data):
            d[i] = x
        assert type(it) == type(itorg)
        assert list(it) == data

        # running iterator
        next(itorg)
        dump = pickle.dumps((itorg, orig), proto)
        it, d = pickle.loads(dump)
        for i, x in enumerate(data):
            d[i] = x
        assert type(it) == type(itorg)
        assert list(it) == data[1:]

        # empty iterator
        for _ in range(1, len(data)):
            next(itorg)
        dump = pickle.dumps((itorg, orig), proto)
        it, d = pickle.loads(dump)
        for i, x in enumerate(data):
            d[i] = x
        assert type(it) == type(itorg)
        assert list(it) == []

        # exhausted iterator
        with pytest.raises(StopIteration):
            next(itorg)
        dump = pickle.dumps((itorg, orig), proto)
        it, d = pickle.loads(dump)
        for i, x in enumerate(data):
            d[i] = x
        assert type(it) == type(itorg)
        assert list(it) == []


def test_deepcopy():
    import copy

    from datastructures import Deque

    mut = [10]
    d = Deque([mut])
    e = copy.deepcopy(d)
    assert list(d) == list(e)
    mut[0] = 11
    assert id(d) != id(e)
    assert list(d) != list(e)


def test_copy():
    import copy
    import random

    from datastructures import Deque

    mut = [10]
    d = Deque([mut])
    e = copy.copy(d)
    assert list(d) == list(e)
    mut[0] = 11
    assert id(d) != id(e)
    assert list(d) == list(e)

    for i in range(5):
        for maxlen in range(-1, 6):
            s = [random.random() for j in range(i)]
            d = Deque(s) if maxlen == -1 else Deque(s, maxlen)
            e = d.copy()

            assert d == e
            assert d.maxlen == e.maxlen
            assert all(x is y for x, y in zip(d, e))


def test_copy_method():
    from datastructures import Deque

    mut = [10]
    d = Deque([mut])
    e = d.copy()
    assert list(d) == list(e)
    mut[0] = 11
    assert id(d) != id(e)
    assert list(d) == list(e)


def test_reversed():
    from datastructures import Deque

    for s in ("abcd", range(2000)):
        assert list(reversed(Deque(s))) == list(reversed(s))


# I chose to skip this test since it tests internal implementation details
# rather than functionality. This test checks if you can create a new linked
# list iterator using the internal iterator class and passing it an existing
# linked list. That was not how I chose to implement my iterator since it
# handles both forward and revese iterations.
def test_reversed_new():
    pass


def test_gc_doesnt_blowup():
    import gc

    from datastructures import Deque

    # This used to assert-fail in deque_traverse() under a debug
    # build, or run wild with a NULL pointer in a release build.
    d = Deque()
    for _ in range(100):
        d.append(1)
        gc.collect()


def test_container_iterator():
    import gc
    import weakref

    from datastructures import Deque

    # Bug #3680: tp_traverse was not implemented for deque iterator objects
    class C:
        pass

    for i in range(2):
        obj = C()
        ref = weakref.ref(obj)
        if i == 0:
            container = Deque([obj, 1])
        else:
            container = reversed(Deque([obj, 1]))
        obj.x = iter(container)
        del obj, container
        gc.collect()
        assert ref() is None
