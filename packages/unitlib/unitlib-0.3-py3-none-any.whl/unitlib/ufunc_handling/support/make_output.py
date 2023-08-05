from typing import Optional

import numpy as np

from unitlib.core_objects import Unit, dimensionless
from unitlib.core_objects.util import create_Array_or_Quantity
from .registry import UfuncOutput
from .ufunc_args import UfuncArgs, BinaryUfuncInputs


def make_ufunc_output(
    new_display_unit: Unit,
    numpy_ufunc_output: np.ndarray,
) -> UfuncOutput:
    """ Select/create output object of correct type """
    if new_display_unit == dimensionless:
        return numpy_ufunc_output
    else:
        return create_Array_or_Quantity(numpy_ufunc_output, new_display_unit)


def make_binary_ufunc_output(
    ufunc_args: UfuncArgs,
    inputs: BinaryUfuncInputs,
    new_display_unit: Unit,
    left_numpy_ufunc_arg: Optional[np.ndarray] = None,
    right_numpy_ufunc_arg: Optional[np.ndarray] = None,
) -> UfuncOutput:

    is_in_place = ufunc_args.kwargs.get("out") is (inputs.left_operand,)
    #      Whether this __array_ufunc__ call is an in-place operation such as
    #      `array *= 2`. See `numpy.lib.mixins._inplace_binary_method`, which added
    #      the "out" kwarg (as `out=(self,)`).

    if is_in_place:
        ufunc_args.kwargs.update(out=inputs.left_operand.data)

    if left_numpy_ufunc_arg is None:
        left_numpy_ufunc_arg = inputs.left_array.data
    if right_numpy_ufunc_arg is None:
        right_numpy_ufunc_arg = inputs.right_array.data

    numpy_ufunc_output = ufunc_args.ufunc(
        left_numpy_ufunc_arg, right_numpy_ufunc_arg, **ufunc_args.kwargs
    )

    if is_in_place:
        inputs.left_operand.display_unit = new_display_unit
        return inputs.left_operand
    else:
        return make_ufunc_output(new_display_unit, numpy_ufunc_output)
