from typing import Optional, Tuple

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from ..backwards_compatibility import TYPE_CHECKING

if TYPE_CHECKING:
    from .unit import Unit, DataUnit
    from .type_aliases import UfuncInput, ArrayIndex, ArraySlice


class Array(NDArrayOperatorsMixin):
    """
    A NumPy array with a physical unit.

    This class is a wrapper around a NumPy `ndarray` (the `data` attribute), augmented
    with a `Unit` (`display_unit`) and an optional descriptive string (`name`).

    The `display_unit` is only used when interfacting with the user; that is: at Array
    creation time, and when printing or plotting the Array. Internally, the data is
    stored -- and calculations with the data are done -- in `data_unit`s.

    `data_unit` is a scalar multiple or submultiple of `display_unit`. (You can access
    it through this Array's `data_unit` property, or equivalently, via
    `display_unit.data_unit`). We could for example have a "mV" display unit with a
    "volt" data unit. All arrays containing voltage data -- whether their `display_unit`
    is "mV", "μV", or "kV" -- would have their data stored in volts. (Floating point
    number representation makes this possible even for very large or small multipliers,
    like eg attoseconds).

    The advantage of this is that you can push the `data` of different Arrays through a
    pipeline of speed-optimized functions (like Numba JIT-compiled functions) without
    the overhead of unit checking and unit conversions. Because all data is in the same
    relative unit system, there will be no order-of-magnitude unit errors.

    You thus get the best of both worlds:
    - The convenience of units when inputing and displaying your data.
    - The processing speed of raw NumPy arrays and Numba JIT-compiled functions.
    """

    #
    #
    # ---------------
    # Core properties

    data: np.ndarray
    display_unit: "Unit"
    name: Optional[str]

    @property
    def data_unit(self) -> "DataUnit":
        return self.display_unit.data_unit

    @property
    def data_in_display_units(self) -> np.ndarray:
        return self.data / self.display_unit.scale

    # Shorthand
    dd: np.ndarray = data_in_display_units

    #
    #
    # --------------
    # Initialisation

    def __init__(
        self,
        data,
        display_unit: "Unit",
        name: Optional[str] = None,
        data_are_given_in_display_units: bool = False,
    ):
        """
        :param data:  Numeric array-like.
        :param display_unit:  Units in which to display the data.
        :param name:  What the data represents (e.g. "Membrane potential").
        :param data_are_given_in_display_units:  If True, the given `data` is taken to
                    be expressed in `display_unit`s, and is converted to and stored
                    internally in `display_unit.data_unit`s. If False (default), `data`
                    is taken to be already expressed in `display_unit.data_unit`s, and
                    no conversion is done.
        """

        numpy_data = np.asarray(data)

        if not issubclass(numpy_data.dtype.type, np.number):
            raise NonNumericDataException(
                f"Can only create a `unitlib.Array` with numeric data. "
                f'Instead got "{repr(numpy_data)}".'
            )

        if data_are_given_in_display_units:
            self.data = numpy_data * display_unit.scale
        else:
            self.data = numpy_data

        self.display_unit = display_unit
        self.name = name

    #
    #
    # -------------------
    # Text representation

    def __str__(self):
        return format(self)

    __repr__ = __str__

    def __format__(self, format_spec: str = "") -> str:
        """ Called for `format(array)` and `f"String interpolation with {array}"`. """
        if not format_spec:
            format_spec = ".4G"
        array_string = np.array2string(
            self.data_in_display_units,
            formatter={"float_kind": lambda x: format(x, format_spec)},
        )
        return f"{array_string} {self.display_unit}"

    #
    #
    # ----------
    # Arithmetic

    # See "Writing custom array containers"[1] from the NumPy manual for info on the
    # below `__array_ufunc__` and `__array_function__` methods.
    #
    # # [1](https://numpy.org/doc/stable/user/basics.dispatch.html)

    # The base class `NDArrayOperatorsMixin` implements Python dunder methods like
    # `__mul__` and `__imul__`, so that we can use standard Python syntax like `*` and
    # `*=` with our `Array`s.
    #
    # `NDArrayOperatorsMixin` implements these by calling the corresponding NumPy ufunc
    # (like `np.multiply`), which in turn defer to our `__array_ufunc__` method.

    # Elementwise operations (+, >, cos, sign, ..)
    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: str,
        *inputs: Tuple["UfuncInput", ...],
        **kwargs,
    ):
        from ..ufunc_handling import ufunc_handlers, UfuncArgs

        # Docs for __array_ufunc__:
        # https://numpy.org/doc/stable/reference/arrays.classes.html#numpy.class.__array_ufunc__

        if method != "__call__":  # method = "reduce", "accumulate", ...
            raise NotImplementedError(
                f'Unitlib objects do not yet support "{method}" ufuncs. '
                + self._DIY_help_text
            )

        handler = ufunc_handlers.get(ufunc)

        if not handler:
            raise NotImplementedError(
                f"Unitlib objects do not yet support the `{ufunc.__name__}` operation. "
                + self._DIY_help_text
            )

        args = UfuncArgs(ufunc, method, inputs, kwargs)
        output = handler(args)
        return output

    # NumPy methods (mean, sum, linspace, ...)
    def __array_function__(self, func, _types, _args, _kwargs):
        raise NotImplementedError(
            f"Unitlib objects do not yet support being used with function"
            f"`{func.__name__}`. {self._DIY_help_text}"
        )

    _DIY_help_text = (  # Shown when a NumPy operation is not implemented yet for our Array.
        "You can get the bare numeric data (a plain NumPy array) "
        "via `array.data`, and work with it manually."
    )

    #
    #
    # ---------------
    # Array behaviour

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: "ArrayIndex") -> "ArraySlice":
        from .util import create_Array_or_Quantity

        data_slice: np.ndarray = self.data[index]
        output = create_Array_or_Quantity(data_slice, self.display_unit, self.name)
        return output

    def __setitem__(self, index: "ArrayIndex", value: "ArraySlice"):
        from .unit import Unit, IncompatibleUnitsError
        from .util import as_array

        if isinstance(value, Unit):
            raise ValueError(
                f"Cannot set Array element to a bare Unit "
                f'(assigned value was "{value}").'
            )

        try:
            value_as_array = as_array(value)

        except NonNumericDataException as exception:
            raise NonNumericDataException(
                "Can only assign numeric data to Array."
            ) from exception

        if value_as_array.data_unit != self.data_unit:
            raise IncompatibleUnitsError(
                f'Units are incompatible between Array "{self}"'
                f'and assigned value "{value_as_array}".'
            )

        self.data[index] = value_as_array.data

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.data.shape

    @property
    def ndim(self) -> int:
        return self.data.ndim


class NonNumericDataException(TypeError):
    pass
