"""
Exponentiation
--------------

Examples:
  - mV ** 2
  - (8 mV) ** 2
  - ([3 8 1] mV) ** 2
  - (8 mV) ** [[2]]      (This becomes [[64]] mV²).
But not:
  - mV ** (8 mV)
  - mV ** [3, 8]         (Would yield a list with different unit per element).
  - mV ** (1/2)
"""

import numpy as np

from unitlib.core_objects import Unit, dimensionless
from .support import make_binary_ufunc_output, implements, UfuncOutput, UfuncArgs


@implements([np.power])
def power(ufunc_args: UfuncArgs) -> UfuncOutput:

    inputs = ufunc_args.parse_binary_inputs()

    if inputs.right_array.data_unit is not dimensionless:
        raise ValueError(
            "Cannot raise to powers with a unit "
            f'(power "{inputs.right_operand}" is not dimensionless).'
        )

    if inputs.right_array.data.size != 1:
        raise ValueError(
            f"Can only raise to scalar powers "
            f'(power "{inputs.right_operand}" does not have size 1).'
        )
        # An sequence with different units per element is not supported by unitlib.

    if not issubclass(inputs.right_array.data.dtype.type, np.integer):
        raise NotImplementedError(
            f"Can not yet raise to non-integer powers "
            f'(power "{inputs.right_operand}" '
            f'has non-integer dtype "{inputs.right_array.data.dtype}").'
        )

    power = inputs.right_array.data.item()
    new_display_unit = inputs.left_array.display_unit._raised_to(power)

    # Unit to a power remains a pure Unit (`mV ** 2`)
    if isinstance(inputs.left_array, Unit):
        return new_display_unit

    else:
        if power < 0 and issubclass(inputs.left_array.data.dtype.type, np.integer):
            # NumPy doesn't allow exponentiating integers to negative powers.
            # (Because it changes the data type to no longer be integer,
            # presumably). We -- just like plain Python -- do allow it however.
            left_numpy_ufunc_arg = inputs.left_array.data.astype(float)
        else:
            left_numpy_ufunc_arg = inputs.left_array.data

        return make_binary_ufunc_output(
            ufunc_args, inputs, new_display_unit, left_numpy_ufunc_arg
        )
