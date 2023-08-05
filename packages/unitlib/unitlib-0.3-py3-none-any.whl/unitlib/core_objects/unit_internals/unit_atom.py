from .powered_unit_atom import PoweredUnitAtom, PoweredDataUnitAtom
from ..unit import DataUnit


class UnitAtom(PoweredUnitAtom):
    """
    Eg "volt" or "mV";
    as contrasted with "mV²" (a `PoweredUnitAtom`) or "N·mV²" (a `CompoundUnit`).

    Defining attributes:
        - name: str
        - data_unit: DataUnitAtom
        - scale: float
    """

    def __init__(self, name: str, data_unit: "DataUnitAtom", scale: float):
        PoweredUnitAtom.__init__(self, unit_atom=self, power=1)
        self._name = name
        self._data_unit = data_unit
        self._scale = scale
        # These three attributes cannot be set directly (e.g. using `self.name = name`);
        # this would yield an `AttributeError`. This is because they are *properties* in
        # the parent class. Properties can only be overriden by new properties. Hence
        # the annoying verbosity of dummy variables and trivial property getters. (And
        # no, using `self.name = property(..)` or `self.__dict__["name"] = ..` also
        # doesn't work :) ).

    @property
    def name(self):
        return self._name

    @property
    def data_unit(self):
        return self._data_unit

    @property
    def scale(self):
        return self._scale

    def __hash__(self):
        return hash((self.name, self.data_unit, self.scale))


class DataUnitAtom(DataUnit, UnitAtom):
    def __init__(self, name: str):
        UnitAtom.__init__(self, name, self.data_unit, self.scale)
        #   `data_unit` and `scale` are provided by `DataUnit`.

    def __hash__(self):
        return hash(self.name)


dimensionless = DataUnitAtom("<dimensionless>")
#   We give this one a real name (instead of just the empty string) to make debugging
#   easier.
