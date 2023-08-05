"""
Comparison
----------

Examples:
  - mV >= volt
  - 0.7 volt == 800 volt
  - [5 5] volt != [5 5] mV
  - 5 volt == [5 5 6] volt
"""

import numpy as np

from unitlib.core_objects import Unit, IncompatibleUnitsError
from unitlib.core_objects.array import NonNumericDataException
from .support import implements, UfuncOutput, UfuncArgs

equality_comparators = (
    np.equal,
    np.not_equal,
)

ordering_comparators = (
    np.greater,
    np.greater_equal,
    np.less,
    np.less_equal,
)


@implements(equality_comparators + ordering_comparators)
def compare(ufunc_args: UfuncArgs) -> UfuncOutput:

    try:
        inputs = ufunc_args.parse_binary_inputs()
    except NonNumericDataException as exception:
        # One of the operands is e.g. `None`, as in `8 mV == None`.
        if ufunc_args.ufunc in equality_comparators:
            if ufunc_args.ufunc == np.equal:
                return False
            elif ufunc_args.ufunc == np.not_equal:
                return True
        else:
            raise exception

    # volt == mV
    if isinstance(inputs.left_array, Unit) and isinstance(inputs.right_array, Unit):
        if ufunc_args.ufunc == np.equal:
            return hash(inputs.left_array) == hash(inputs.right_array)
        elif ufunc_args.ufunc == np.not_equal:
            return not (inputs.left_array == inputs.right_array)

    # 8 mV > 9 newton
    elif (
        ufunc_args.ufunc in ordering_comparators
        and inputs.left_array.data_unit != inputs.right_array.data_unit
    ):
        raise IncompatibleUnitsError(
            f"Ordering comparator '{ufunc_args.ufunc.__name__}' cannot be used between "
            f'incompatible Units "{inputs.left_array.display_unit}" '
            f'and "{inputs.right_array.display_unit}".'
        )

    #  - [80 200] mV > 0.1 volt       -> [False True]
    #  - mV > μV                      -> True  (`.data` = `.scale` of mV is larger)
    #  - [8 3] newton == [8 3] volt   -> [False, False]
    else:
        data_comparison_result = ufunc_args.ufunc(
            inputs.left_array.data,
            inputs.right_array.data,
            **ufunc_args.kwargs,
        )
        unit_comparison_result = (
            inputs.left_array.data_unit == inputs.right_array.data_unit
        )
        return np.logical_and(data_comparison_result, unit_comparison_result)
        # Note that there are no in-place versions of comparator dunders (i.e. __lt__
        # etc). They wouldn't make sense anyway: the type changes from `unitlib.Array` to
        # `np.ndarray`.
