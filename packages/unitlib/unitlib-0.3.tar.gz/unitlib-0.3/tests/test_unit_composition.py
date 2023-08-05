from numpy import allclose as numeric_equals

from unitlib import Unit
from unitlib.core_objects.unit_internals import PoweredUnitAtom
from unitlib.prefixes import milli, nano


volt = Unit.define("V")
mV = Unit.from_prefix(milli, volt)
nV = Unit.from_prefix(nano, volt)

second = Unit.define("s")
ms = Unit.from_prefix(milli, second)
minute = Unit.define("min", data_unit=second, scale=60)

siemens = Unit.define("S")
nS = Unit.from_prefix(nano, siemens)


def test_mul():
    umu = volt * ms
    assert umu.data_unit == volt * second
    assert numeric_equals(umu.scale, 0.001)


def test_div():
    udu = mV / nS
    assert udu.data_unit == volt / siemens
    assert numeric_equals(udu.scale, 1e6)


def test_one_over():
    oou = 1 / mV
    assert isinstance(oou, PoweredUnitAtom)
    assert oou.power == -1
    assert oou.data_unit == 1 / volt
    assert numeric_equals(oou.scale, 1e3)
    assert oou == mV ** -1


def test_power():
    up = mV ** 3
    assert isinstance(up, PoweredUnitAtom)
    assert up.power == 3
    assert up.data_unit == volt ** 3
    assert up.name == "mV³"
    assert numeric_equals(up.scale, 1e-9)


def test_compound():
    umudu = nV * nS / mV
    udumu = nV * (nS / mV)
    assert umudu.data_unit == udumu.data_unit == volt * siemens / volt == siemens
    assert numeric_equals(umudu.scale, udumu.scale)
    assert numeric_equals(umudu.scale, 1e-15)
    assert umudu.name == udumu.name == "nV·nS·mV⁻¹"
