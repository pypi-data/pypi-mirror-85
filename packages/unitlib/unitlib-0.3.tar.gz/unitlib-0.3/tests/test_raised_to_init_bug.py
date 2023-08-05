"""
Bug example (from `test_array_times_unit`):

        def _raised_to(self, power):    self = <UnitAtom "mV">, power = 1
    >       return PoweredUnitAtom(unit_atom=self, power=power)
    E       TypeError: __init__() got an unexpected keyword argument 'unit_atom'

Problem was that `PoweredUnitAtom.__new__` made a new `UnitAtom` and wrongly called
**UnitAtom's** `__init__` with PoweredUnitAtom's kwargs.

Fixed by not using a custom `PoweredUnitAtom.__new__`, but rather placing its logic in
`PoweredUnitAtom._raised_to` (which is inherited unmodified by `UnitAtom`).
"""

import numpy as np

from unitlib import Unit
from unitlib.core_objects.unit_internals import PoweredUnitAtom
from unitlib.prefixes import milli

volt = Unit.define("V")
mV = Unit.from_prefix(milli, volt)


def check(mV2: PoweredUnitAtom):
    assert mV2.name == "mV²"
    assert mV2.unit_atom == mV
    assert mV2.power == 2
    assert mV2.data_unit == volt ** 2
    assert mV2.scale == mV2.data == np.array(1e-6)
    assert mV2.data_in_display_units == mV2.dd == np.array(1)
    assert mV2.value == 1
    assert mV2.components == (mV2,)


def test_new_and_init():
    check(PoweredUnitAtom(unit_atom=mV, power=2))


def test_raised_to():
    check(mV._raised_to(power=2))


def test_raised_to_1():
    assert mV._raised_to(power=1) == mV
