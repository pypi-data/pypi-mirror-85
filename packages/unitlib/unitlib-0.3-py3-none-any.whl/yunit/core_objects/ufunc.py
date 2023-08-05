"""
Implementation of `Array.__array_ufunc__`.

This handles all Python math syntax (*, *=, **, <, %, …)
as well as all NumPy elementwise functions (`cos`, `sign`, `abs`, …),
for both Arrays, Quantities, and Units.
"""

from typing import Union, Tuple, Optional

import numpy as np

from . import Array, Unit, dimensionless, Quantity
from .unit_internals import CompoundUnit
from ..type_aliases import NDArrayLike

equality_comparators = (np.equal, np.not_equal)
ordering_comparators = (
    np.greater,
    np.greater_equal,
    np.less,
    np.less_equal,
)
comparators = equality_comparators + ordering_comparators

numeric_methods = (
    np.add,
    np.subtract,
    np.multiply,
    np.divide,  # == np.true_divide
    np.power,
)  # There's more in `NDArrayOperatorsMixin`

supported_ufuncs = comparators + numeric_methods


YunitObject = Union[Array, Quantity, Unit]


def __array_ufunc__(
    self: YunitObject,
    ufunc: np.ufunc,
    method: str,
    *inputs: Tuple[Union[YunitObject, NDArrayLike], ...],
    **ufunc_kwargs,
) -> Union[YunitObject, np.ndarray, bool]:

    # Docs for __array_ufunc__:
    # https://numpy.org/doc/stable/reference/arrays.classes.html#numpy.class.__array_ufunc__

    #
    #
    # -------------------
    # Check function type

    if method != "__call__":  # method = "reduce", "accumulate", ...
        raise NotImplementedError(
            f'yunit objects do not yet support "{method}" ufuncs. '
            + self._DIY_help_text
        )

    if ufunc not in supported_ufuncs:
        raise NotImplementedError(
            f"yunit objects do not yet support the `{ufunc.__name__}` operation. "
            + self._DIY_help_text
        )

    #
    #
    # -------------
    # Parse `inputs`

    # - For unary operators (cos, sign, abs, …), `len(inputs)` is 1.
    # - For binary operators (+, >, **, …), it is 2.
    # - For 'normal' operations (`8 mV * 3`, i.e. `__mul__`) and in-place operations
    #   (`8 mV *= 3`, i.e. `__imul__`), `inputs[0] == self`
    # - For reflected operations (`3 * 8 mV`, i.e. `__rmul__`), `inputs[1] == self`.

    left_operand, right_operand = inputs

    def as_array(operand: Union[NDArrayLike, YunitObject]) -> YunitObject:
        if not isinstance(operand, Array):
            # `operand` is purely numeric (scalar or array-like). Eg. the right operand
            # in `(8 mV) * 2`.
            operand = Array(operand, dimensionless)
        return operand

    left_array, right_array = map(as_array, inputs)
    left_array: Array  # Helping PyCharm's type inference
    right_array: Array

    def make_output(
        new_display_unit: Unit,
        left_numpy_ufunc_arg: Optional[np.ndarray] = None,
        right_numpy_ufunc_arg: Optional[np.ndarray] = None,
    ) -> Union[np.ndarray, Array, Quantity]:

        #
        #
        # Process numeric data
        # --------------------

        is_in_place = ufunc_kwargs.get("out") is self
        #      Whether this __array_ufunc__ call is an in-place operation such as
        #      `array *= 2`. See `numpy.lib.mixins._inplace_binary_method`, which added
        #      the `out=self` kwarg.
        if is_in_place:
            ufunc_kwargs.update(out=self.data)

        if left_numpy_ufunc_arg is None:
            left_numpy_ufunc_arg = left_array.data
        if right_numpy_ufunc_arg is None:
            right_numpy_ufunc_arg = right_array.data

        ufunc_data_output: np.ndarray = ufunc(
            left_numpy_ufunc_arg, right_numpy_ufunc_arg, **ufunc_kwargs
        )

        #
        #
        # Select/create output object of correct type
        # ------------------------------------------

        if is_in_place:
            self.display_unit = new_display_unit
            return self

        elif new_display_unit == dimensionless:
            return ufunc_data_output

        elif ufunc_data_output.size == 1:
            return Quantity(
                ufunc_data_output,
                new_display_unit,
                name=None,
                value_is_given_in_display_units=False,
            )

        else:
            return Array(
                ufunc_data_output,
                new_display_unit,
                name=None,
                data_are_given_in_display_units=False,
            )

    #
    #
    # Exponentiation
    # --------------
    #
    # Examples:
    #   - mV ** 2
    #   - (8 mV) ** 2
    #   - ([3 8 1] mV) ** 2
    #   - (8 mV) ** [[2]]      (This becomes [[64]] mV²).
    # But not:
    #   - mV ** (8 mV)
    #   - mV ** [3, 8]         (Would yield a list with different unit per element).
    #   - mV ** (1/2)
    if (
        ufunc == np.power
        and right_array.data_unit == dimensionless
        and right_array.data.size == 1
        and issubclass(right_array.data.dtype.type, np.integer)
    ):
        power = right_array.data.item()
        new_display_unit = left_array.display_unit._raised_to(power)
        if isinstance(left_array, Unit):
            return new_display_unit
        else:
            if power < 0 and issubclass(left_array.data.dtype.type, np.integer):
                # NumPy doesn't allow exponentiating integers to negative powers
                # (Because it changes the data type to no longer be integer,
                # presumably). We (just like plain Python) do allow it however.
                left_numpy_ufunc_arg = float(left_array.data)
            else:
                left_numpy_ufunc_arg = left_array.data
            return make_output(new_display_unit, left_numpy_ufunc_arg)

    #
    #
    # Addition & subtraction
    # ----------------------
    #
    # Examples:
    #   - 800 mV - 23 mV
    #   - 800 mV + [3 8 2] volt
    #   - 800 mV + 1 volt
    # But not:
    #   - 800 mV + newton
    #   - 800 mV + volt
    #
    # Note that order of operands doesn't matter for unit checks.
    # (It does for the number subtraction itself ofc).
    #
    elif np.ufunc in (np.add, np.subtract):

        if isinstance(left_array, Unit) or isinstance(right_array, Unit):
            if isinstance(left_array, Unit):
                if ufunc == np.add:  # add to a Unit
                    preposition = "to "
                else:  # subtract from a Unit
                    preposition = "from "
            else:  # add/subtract a Unit
                preposition = ""
            raise UnitError(
                f"Cannot {ufunc.__name__} {preposition}a bare unit. "
                f'Operands were "{left_array}" and "{right_array}".'
            )

            # We _could_ add or subtract bare units (if they're compatible), by
            # interpreting the `Unit` as a `Quantity` with value = 1. But that's
            # probably not what the user intended.

        if left_array.data_unit != right_array.data_unit:
            raise UnitError(
                f"Cannot {ufunc.__name__} incompatible units "
                f'"{left_array.display_unit}" and "{right_array.display_unit}".'
            )

        if left_array.display_unit > right_array.display_unit:
            new_display_unit = left_array.display_unit
        else:
            new_display_unit = right_array.display_unit

        return make_output(new_display_unit)

    elif np.ufunc == np.negative:
        breakpoint()

    #
    #
    # Comparison
    # ----------
    #
    # Examples:
    #   - mV >= volt
    #   - 0.7 volt == 800 volt
    #   - [5 5] volt != [5 5] mV
    #   - 5 volt == [5 5 6] volt
    elif ufunc in comparators:

        # volt == mV
        if isinstance(left_array, Unit) and isinstance(right_array, Unit):
            if ufunc == np.equal:
                return hash(left_array) == hash(right_array)
            elif ufunc == np.not_equal:
                return not (left_array == right_array)

        # 8 mV > 9 newton
        elif (
            ufunc in ordering_comparators
            and left_array.data_unit != right_array.data_unit
        ):
            raise UnitError(
                f"Ordering comparator '{ufunc.__name__}' cannot be used between "
                f'incompatible Units "{left_array.display_unit}" '
                f'and "{right_array.display_unit}".'
            )

        #  - [80 200] mV > 0.1 volt   (becomes `[False True]`)
        #  - mV > μV                  (.data = .scale of the first is indeed larger)
        else:
            data_comparison_result = ufunc(
                left_array.data,
                right_array.data,
                **ufunc_kwargs,
            )
            unit_comparison_result = left_array.data_unit == right_array.data_unit
            return np.logical_and(data_comparison_result, unit_comparison_result)
            # Note that there are no in-place versions of comparator dunders (i.e. __lt__
            # etc). They wouldn't make sense anyway: the type changes from `yunit.Array` to
            # `np.ndarray`.

    #
    #
    # Division
    # --------
    #
    # Examples:
    #   - 8 mV / 3 mV
    #   - 8 mV / mV
    #   - mV / second
    #   - [8 3] mV / 6 second
    #   - 8 / second
    elif ufunc == np.divide:

        # Allow `1 / mV` as a special case to create a pure Unit (`mV⁻¹`), and not a
        # Quantity with value = 1.
        if (
            isinstance(left_operand, int)
            and left_operand == 1  # This and the first condition could be shortened to
            #                        `left_operand is 1`. But: __Explicit is better than
            #                        implicit__.
            and isinstance(right_array, Unit)
        ):
            return right_array ** -1

        else:
            return left_array * (right_array ** -1)

    #
    #
    # Multiplication
    # --------------
    #
    # Examples:
    #   - mV * newton
    #   - 8 mV * 3
    #   - 8 mV * (mV ** -1)
    elif ufunc == np.multiply:

        new_display_unit = CompoundUnit.squeeze(
            [left_array.display_unit, right_array.display_unit]
        )
        if isinstance(left_array, Unit) and isinstance(right_array, Unit):
            return new_display_unit
        else:
            return make_output(new_display_unit)

    else:
        ...


class UnitError(Exception):
    """
    Raised when an operation with incompatible units is attempted
    (eg `8 volt + 2 newton`).
    """
