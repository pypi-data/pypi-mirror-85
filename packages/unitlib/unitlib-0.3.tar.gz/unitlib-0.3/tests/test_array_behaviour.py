import pytest

from unitlib import Unit
from unitlib.core_objects import IncompatibleUnitsError
from unitlib.prefixes import milli

volt = Unit.define("V")
mV = Unit.from_prefix(milli, volt)
siemens = Unit.define("S")


array_1D = [5, 3, 5.2] * mV


def test_len():
    assert len(array_1D) == 3


def test_getitem_1D():
    assert array_1D[1] == 3 * mV
    assert all(array_1D[:2] == [5, 3] * mV)


def test_setitem_1D():
    array = array_1D  # copy not yet implemented

    array[2] = 1 * volt
    assert all(array == [5, 3, 1000] * mV)

    array[:] = 3 * mV
    assert all(array == [3, 3, 3] * mV)

    array[::2] = 1 * volt
    assert all(array == [1000, 3, 1000] * mV)


def test_setitem_wrong_unit():
    with pytest.raises(IncompatibleUnitsError):
        array_1D[0] = 1 * siemens


def test_truthiness():
    assert array_1D
    assert 1 * mV
    if [] * mV:
        assert False
    else:
        assert True


array_2D = [
    [1, 2],
    [3, 4],
] * mV


def test_getitem_2D():
    assert array_2D[0, 1] == 2 * mV
    assert all(array_2D[:, 1] == [2, 4] * mV)


# noinspection PyUnresolvedReferences
#  ^ This is for `(__eq__).all()`. Remove when Array.pyi is there.
def test_setitem_2D():
    array = array_2D  # copy not yet implemented
    array[1, :] = 5 * mV
    assert (array == [[1, 2], [5, 5]] * mV).all()
