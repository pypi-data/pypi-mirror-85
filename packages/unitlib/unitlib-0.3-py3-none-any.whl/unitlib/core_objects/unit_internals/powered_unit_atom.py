from .compound_unit import CompoundUnit
from ..unit import DataUnit
from ...backwards_compatibility import TYPE_CHECKING

if TYPE_CHECKING:
    from .unit_atom import UnitAtom, DataUnitAtom, dimensionless


class PoweredUnitAtom(CompoundUnit):
    """
    Eg "mm²"; as contrasted with "mm" (a `UnitAtom`) or "N/mm²" (a `CompoundUnit`).

    Defining attributes:
        - unit_atom: UnitAtom
        - power: int
    """

    def __init__(self, unit_atom: "UnitAtom", power: int):
        CompoundUnit.__init__(self, components=(self,))
        self.unit_atom = unit_atom
        self.power = power

    @property
    def name(self):
        return f"{self.unit_atom.name}{self._power_as_superscript}"

    @property
    def data_unit(self):
        return self.unit_atom.data_unit ** self.power

    @property
    def scale(self):
        return self.unit_atom.scale ** self.power

    def __hash__(self):
        return hash((self.unit_atom, self.power))

    # (mV⁻³)**2
    def _raised_to(self, power: int):
        new_power = self.power * power
        if new_power == 0:
            return dimensionless
        elif new_power == 1:
            return self.unit_atom
        else:
            if isinstance(self, DataUnit):
                PoweredClass = PoweredDataUnitAtom
            else:
                PoweredClass = PoweredUnitAtom
            return PoweredClass(self.unit_atom, new_power)

    @property
    def _power_as_superscript(self) -> str:
        # Transform eg the int `-87` to the string `"⁻⁸⁷"`.
        superscript_chars = "⁰¹²³⁴⁵⁶⁷⁸⁹"
        digits = str(abs(self.power))
        output_chars = [superscript_chars[int(digit)] for digit in digits]
        if self.power < 0:
            output_chars.insert(0, "⁻")
        return "".join(output_chars)


class PoweredDataUnitAtom(DataUnit, PoweredUnitAtom):
    def __init__(self, unit_atom: "DataUnitAtom", power: int):
        PoweredUnitAtom.__init__(self, unit_atom, power)
