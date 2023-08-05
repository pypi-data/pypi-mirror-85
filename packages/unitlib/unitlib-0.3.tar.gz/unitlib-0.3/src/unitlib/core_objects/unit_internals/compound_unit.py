from collections import defaultdict
from itertools import chain
from typing import Iterable, Dict, Tuple

from ..unit import DataUnit, Unit
from ...backwards_compatibility import prod, TYPE_CHECKING

if TYPE_CHECKING:
    from .powered_unit_atom import PoweredUnitAtom, PoweredDataUnitAtom


class CompoundUnit(Unit):
    """
    A multiplicative combination of `PoweredUnitAtom`s.
    Eg "mV²·μm·nS⁻¹".

    Defining attribute:
        components: Tuple[PoweredUnitAtom, ...]
    """

    def __init__(self, components: Tuple["PoweredUnitAtom", ...]):
        self.components = components

    @classmethod
    def squeeze(cls, units: Iterable["CompoundUnit"]) -> Unit:

        from .unit_atom import UnitAtom, dimensionless

        flattened_units = chain(*(unit.components for unit in units))

        # Aggregate all `PoweredUnitAtom`s that have the same `unit_atom`, and sum their
        # powers. Throw away dimensionless components and components with a combined
        # power of zero.
        combined_powers: Dict[UnitAtom, int] = defaultdict(lambda: 0)
        for unit in flattened_units:
            combined_powers[unit.unit_atom] += unit.power

        squeezed_units = tuple(
            unit_atom._raised_to(combined_power)
            for unit_atom, combined_power in combined_powers.items()
            if unit_atom != dimensionless and combined_power != 0
        )

        if len(squeezed_units) == 0:
            return dimensionless

        elif len(squeezed_units) == 1:
            return squeezed_units[0]

        else:
            return cls(squeezed_units)
            #   `cls` can be `CompoundUnit` or `CompoundDataUnit`.

    @property
    def name(self):
        return "·".join([component.name for component in self.components])

    @property
    def data_unit(self) -> "CompoundDataUnit":
        return CompoundDataUnit.squeeze(
            [component.data_unit for component in self.components]
        )

    @property
    def scale(self) -> float:
        return prod([component.scale for component in self.components])

    def __hash__(self):
        return hash(self.components)

    def _raised_to(self, power: int):
        return self.squeeze([component ** power for component in self.components])


class CompoundDataUnit(DataUnit, CompoundUnit):
    def __init__(self, units: Tuple["PoweredDataUnitAtom", ...]):
        CompoundUnit.__init__(self, units)
