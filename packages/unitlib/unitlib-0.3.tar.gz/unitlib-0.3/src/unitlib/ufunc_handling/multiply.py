"""
Multiplication
--------------

Examples:
  - mV * newton
  - 8 mV * 3
  - 8 mV * (mV ** -1)
"""

import numpy as np

from unitlib.core_objects import Unit
from unitlib.core_objects.unit_internals import CompoundUnit
from .support import make_binary_ufunc_output, UfuncOutput, implements, UfuncArgs


@implements([np.multiply])
def multiply(ufunc_args: UfuncArgs) -> UfuncOutput:

    inputs = ufunc_args.parse_binary_inputs()

    new_display_unit = CompoundUnit.squeeze(
        [
            inputs.left_array.display_unit,
            inputs.right_array.display_unit,
        ]
    )

    # Unit * Unit remains pure Unit.
    if isinstance(inputs.left_array, Unit) and isinstance(inputs.right_array, Unit):
        return new_display_unit

    else:
        return make_binary_ufunc_output(ufunc_args, inputs, new_display_unit)
