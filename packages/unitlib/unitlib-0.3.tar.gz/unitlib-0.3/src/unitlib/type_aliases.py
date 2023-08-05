from numbers import Number
from typing import Sequence, Union

import numpy as np

from .backwards_compatibility import Protocol


scalar_types = (Number, np.number)
Scalar = Union[scalar_types]


#
#
# NumPy 1.20 provides an `NDArrayLike` type out of the box; but that version isn't
# released at the time of writing (25 Aug 2020).
# So we recreate it manually here (following [https://github.com/numpy/numpy/blob/master/numpy/typing/_array_like.py]).


class ProvidesConversionToArray(Protocol):
    def __array__(self, *args) -> np.ndarray:
        ...


NDArrayLike = Union[Sequence, ProvidesConversionToArray, Scalar]
