from abc import ABC, abstractproperty, abstractmethod
from numbers import Number
from typing import Optional

import numpy as np

from ._2_quantity import Quantity
from ..backwards_compatibility import TYPE_CHECKING
from ..prefixes import Prefix

if TYPE_CHECKING:
    from .unit_internals import UnitAtom, DataUnitAtom


class Unit(Quantity, ABC):
    """
    A physical unit. For example, "farad", "μm²", or "mV/nS".

    Units can be:
     - raised to a power (`meter**2`);
     - composed with other units (`newton * meter`);
     - applied to numeric data (`8 * farad`, `[3,5] * mV`);

    This abstract base class (`ABC`) defines the interface and functionality common to
    all `Unit` subclasses:
        - `DataUnit`
        - `UnitAtom`
        - `DataUnitAtom`
        - `PoweredUnitAtom`
        - `PoweredDataUnitAtom`
        - `CompoundUnit`
        - `CompoundDataUnit`.
    """

    #
    #
    # ---------------
    # Core properties

    @abstractproperty
    def name(self) -> str:
        """
        How this unit is displayed textually (eg. in print statements or in axis labels
        of data plots). Examples: "min", "mV".
        """
        ...  # For subclasses to implement.

    @abstractproperty
    def scale(self) -> Number:
        """
        Factor with which numeric data annotated with this unit is multiplied before
        being stored in memory.

        For example, if this `unit` is "mV" (with a `data_unit` of "volt") and its
        `scale` is 1E-3, the numeric data underlying the expression `8 * mV` will
        be stored as `0.008` in memory.
        """
        ...  # For subclasses to implement.

    @abstractproperty
    def data_unit(self) -> "DataUnit":
        """
        A scalar multiple or submultiple of this `unit`.

        Numeric data annotated with this `unit` is stored in `data_unit`s in memory.
        See `scale`.

        One `unit` equals "`scale`" of its `data_unit`s.
        E.g. 1 minute = 60 seconds.
        """
        ...  # For subclasses to implement.

    #
    #
    # --------------------------------
    # Behave as a proper Python object

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}">'

    def __format__(self, format_spec: str = "") -> str:
        return str(self)

    @abstractmethod
    def __hash__(self) -> int:
        """ Used for unit (in)equality checks. """
        ...  # For subclasses to implement.

    #
    #
    # -------------------
    # Unit exponentiation

    @abstractmethod
    def _raised_to(self, power: int) -> "Unit":
        ...  # For subclasses to implement.

    #
    #
    # -----------------
    # Unit creation API

    @staticmethod
    def define(
        name: str,
        data_unit: Optional["DataUnitAtom"] = None,
        scale: Optional[float] = 1,
    ):
        from .unit_internals import UnitAtom, DataUnitAtom

        if data_unit:
            return UnitAtom(name, data_unit, scale)
        else:
            return DataUnitAtom(name)

    @staticmethod
    def from_prefix(prefix: Prefix, data_unit: "DataUnitAtom") -> "UnitAtom":
        from .unit_internals import UnitAtom

        return UnitAtom(
            name=f"{prefix.symbol}{data_unit.name}",
            data_unit=data_unit,
            scale=prefix.factor,
        )

    #
    #
    # -------------------------------------------
    # Substitutability with `Quantity` base class

    @property
    def data(self):
        return np.array(self.scale)

    @property
    def display_unit(self):
        return self

    _DIY_help_text = (
        "If you're working with yunit Arrays or Quantities, you can get their "
        "bare numeric values (plain NumPy arrays or Python scalars) "
        "via `array.data` or `quantity.value`, and work with them manually."
    )


class DataUnit(Unit, ABC):
    """
    A `Unit` in which numeric data is stored in memory.

    See the `Unit.data_unit` property.
    """

    @property
    def data_unit(self):
        return self

    @property
    def scale(self):
        return 1
