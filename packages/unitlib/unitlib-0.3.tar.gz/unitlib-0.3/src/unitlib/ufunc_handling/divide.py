"""
Division
--------

Examples:
  - 8 mV / 3 mV
  - 8 mV / mV
  - mV / second
  - [8 3] mV / 6 second
  - 8 / second
"""

import numpy as np

from unitlib.core_objects import Unit
from .support import UfuncOutput, implements, UfuncArgs


@implements([np.divide])  # np.divide == np.true_divide
def divide(ufunc_args: UfuncArgs) -> UfuncOutput:

    inputs = ufunc_args.parse_binary_inputs()

    # Allow `1 / mV` as a special case to create a pure Unit (`mV⁻¹`), and not a
    # Quantity with value = 1.
    if (
        isinstance(inputs.left_operand, int)
        and inputs.left_operand == 1
        and isinstance(inputs.right_array, Unit)
    ):
        return inputs.right_array ** -1

    else:
        return inputs.left_array * (inputs.right_array ** -1)
