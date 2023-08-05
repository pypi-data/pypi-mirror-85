"""
Addition & subtraction
----------------------

Examples:
  - 800 mV - 23 mV
  - 800 mV + [3 8 2] volt
  - 800 mV + 1 volt
But not:
  - 800 mV + newton
  - 800 mV + volt

Note that order of operands doesn't matter for unit checks.
(It does for numeric subtraction itself ofc).
"""

import numpy as np

from unitlib.core_objects import Unit, IncompatibleUnitsError
from .support import make_binary_ufunc_output, UfuncOutput, implements, UfuncArgs


@implements([np.add, np.subtract])
def add_subtract(ufunc_args: UfuncArgs) -> UfuncOutput:

    inputs = ufunc_args.parse_binary_inputs()
    op_name = ufunc_args.ufunc.__name__

    # 800 mV + volt
    if isinstance(inputs.left_array, Unit) or isinstance(inputs.right_array, Unit):
        # Can't add (to) or subtract (from) a bare unit. We _could_ add or subtract bare
        # units (if they're compatible), by interpreting the `Unit` as a `Quantity` with
        # value = 1. But that's probably not what the user intended.
        if isinstance(inputs.left_array, Unit):
            if ufunc_args.ufunc == np.add:  # add to a Unit
                preposition = "to "
            else:  # subtract from a Unit
                preposition = "from "
        else:  # add/subtract a Unit
            preposition = ""

        raise ValueError(
            f"Cannot {op_name} {preposition}a bare unit. "
            f'Operands were "{inputs.left_array}" and "{inputs.right_array}".'
        )

    # 800 mV + 1 newton
    if inputs.left_array.data_unit != inputs.right_array.data_unit:
        raise IncompatibleUnitsError(
            f"Cannot {op_name} incompatible units "
            f'"{inputs.left_array.display_unit}" '
            f'and "{inputs.right_array.display_unit}".'
        )

    # For e.g. "800 mV + 1 volt", choose the largest unit as new unit (i.e. volt).
    if inputs.left_array.display_unit > inputs.right_array.display_unit:
        new_display_unit = inputs.left_array.display_unit
    else:
        new_display_unit = inputs.right_array.display_unit

    return make_binary_ufunc_output(ufunc_args, inputs, new_display_unit)
