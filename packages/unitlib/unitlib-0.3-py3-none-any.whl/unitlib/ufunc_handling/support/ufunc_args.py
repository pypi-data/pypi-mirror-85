from dataclasses import dataclass
from typing import Tuple, Dict, Any

import numpy as np

from unitlib.core_objects.array import NonNumericDataException, Array
from unitlib.core_objects.type_aliases import UfuncInput
from unitlib.core_objects.util import as_array


@dataclass
class UfuncArgs:
    """ Arguments passed to an `Array.__array_ufunc__` call. """

    ufunc: np.ufunc
    method: str
    inputs: Tuple[UfuncInput, ...]
    kwargs: Dict[str, Any]

    @property
    def is_unary(self) -> bool:
        # cos, sign, abs, negative, …
        return len(self.inputs) == 1

    @property
    def is_binary(self) -> bool:
        # +, >, **, *=, …
        return len(self.inputs) == 2

    def parse_binary_inputs(self):
        try:
            left, right = self.inputs
            left_array = as_array(left)
            right_array = as_array(right)
            return BinaryUfuncInputs(left, right, left_array, right_array
                                     )
        except NonNumericDataException as exception:
            raise NonNumericDataException(
                f"Cannot perform `{self.ufunc}` operation with non-numeric data."
            ) from exception


@dataclass
class BinaryUfuncInputs:

    left_operand: UfuncInput
    right_operand: UfuncInput
    left_array: Array
    right_array: Array
