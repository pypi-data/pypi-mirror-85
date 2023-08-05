from typing import Optional

import numpy as np

from .array import Array
from ..type_aliases import Scalar
from ..backwards_compatibility import TYPE_CHECKING

if TYPE_CHECKING:
    from .unit import Unit


class Quantity(Array):
    """
    A scalar number with a physical unit, such as `8 * mV`.

    In addition to `Array`'s functionality, it has a `value` property, which is
    `data_in_display_units` as a Python scalar (and not a 0-dimensional NumPy array).
    """

    def __init__(
        self,
        value: Scalar,
        display_unit: "Unit",
        name: Optional[str] = None,
        value_is_given_in_display_units: bool = True,
    ):
        """
        :param value:  A Python or NumPy scalar number.
        :param display_unit:  Units in which to display the value.
        :param name:  What the data represents (e.g. "Tissue resistance").
        :param value_is_given_in_display_units:  If True (default), the given `value` is
                    taken to be expressed in `display_unit`s, and is converted to and
                    stored internally in `display_unit.data_unit`s. If False, `value`
                    is taken to be already expressed in `display_unit.data_unit`s,
                    and no conversion is done.
        """
        if np.size(value) > 1:
            raise ValueError(
                f"`value` must not have more than one element. Got `{value}`."
            )
        # We implicitly allow not only scalars, but also any size-1 array, like
        # `array(3)`, `[3]`, `[[3]]`, etc.
        Array.__init__(
            self,
            value,
            display_unit,
            name,
            value_is_given_in_display_units,
        )

    @property
    def value(self):
        return self.data_in_display_units.item()

    _DIY_help_text = (
        "You can get the bare numeric value via `quantity.value` "
        "and work with it manually."
    )

    def __bool__(self):
        # Python implicit truth value testing (`if quantity:` or `if unit:`)
        # would check whether `__len__` is 0; but `__len__` is not defined
        # for 0-dimensional arrays. Hence, avoid that `__len__` check by defining
        # `__bool__` (which gets checked before `__len__`).
        return True
