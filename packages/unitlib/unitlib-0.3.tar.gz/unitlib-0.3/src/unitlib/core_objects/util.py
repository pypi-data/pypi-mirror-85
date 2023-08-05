from typing import Union, Optional

import numpy as np

from . import Array, Quantity, Unit, dimensionless
from .type_aliases import UnitlibObject
from ..type_aliases import NDArrayLike


def as_array(x: Union[NDArrayLike, UnitlibObject]) -> UnitlibObject:
    if isinstance(x, Array):
        return x
    else:  # `x` is purely numeric (scalar or array-like).
        #  # Eg. the right operand in `(8 mV) * 2`.
        return Array(x, dimensionless)


def create_Array_or_Quantity(
    data: np.ndarray,
    display_unit: Unit,
    name: Optional[str] = None,
) -> Union[Array, Quantity]:
    """ `data` is assumed to be in data units. """
    if data.size == 1:
        return Quantity(
            data,
            display_unit,
            name,
            value_is_given_in_display_units=False,
        )
    else:
        return Array(
            data,
            display_unit,
            name,
            data_are_given_in_display_units=False,
        )
