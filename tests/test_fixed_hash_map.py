"""Tests for the FixedHashMap data structure."""

import pytest


@pytest.fixture
def fhm():
    from datastructures import FixedHashMap

    return FixedHashMap()


def test_init(fhm):
    assert "{}" == str(fhm)


def test_add_item(fhm):
    fhm["0"] = 1
    assert str(fhm) == "{'0': 1}"


def test_get_item(fhm):
    fhm["0"] = 1
    assert fhm["0"] == 1


def test_replace_item(fhm):
    fhm["0"] = 1
    fhm["0"] = 2
    assert fhm["0"] == 2


def test_repr(fhm):
    fhm["0"] = 1
    assert repr(fhm) == "FixedHashMap({'0': 1})"


def test_add_multiple_item(fhm):
    fhm["0"] = 1
    fhm["1"] = 2
    # note: we cannot just check the string representation because python
    #       hashing is only deterministic within a single run
    assert fhm["0"] == 1
    assert fhm["1"] == 2


def test_remove_item(fhm):
    fhm["0"] = 1
    del fhm["0"]
    assert str(fhm) == "{}"


def test_get_load(fhm):
    # note: default hash map size is 1000
    fhm["0"] = 1
    assert fhm.load() == 0.001


def test_get_keys(fhm):
    fhm["0"] = 1
    fhm["1"] = 2
    assert sorted(fhm.keys()) == ["0", "1"]


def test_non_existent_key(fhm):
    with pytest.raises(KeyError) as e:
        _ = fhm["0"]

    assert "could not find" in str(e)

    with pytest.raises(KeyError) as e2:
        del fhm["0"]

    assert "could not find" in str(e2)


def test_memory_error():
    from datastructures import FixedHashMap

    fhm = FixedHashMap(2)
    fhm[0] = 1
    fhm[1] = 2
    with pytest.raises(MemoryError) as e:
        fhm[2] = 3

    assert "the hash map is full" in str(e)


def test_unhashable_key(fhm):
    with pytest.raises(ValueError) as e:
        fhm[[1, 2, 3]] = 10

    assert "key must be hashable" in str(e)


def test_non_existent_key_full_hash_map():
    from datastructures import FixedHashMap

    fhm = FixedHashMap(2)
    fhm[0] = 1
    fhm[1] = 2

    with pytest.raises(KeyError) as e:
        _ = fhm[2]

    assert "could not find key" in str(e)
