from typing import Optional

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from ..backwards_compatibility import TYPE_CHECKING

if TYPE_CHECKING:
    from ._3_unit import Unit, DataUnit


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
        :param data:  Array-like.
        :param display_unit:  Units in which to display the data.
        :param name:  What the data represents (e.g. "Membrane potential").
        :param data_are_given_in_display_units:  If True, the given `data` is taken to
                    be expressed in `display_unit`s, and is converted to and stored
                    internally in `display_unit.data_unit`s. If False (default), `data`
                    is taken to be already expressed in `display_unit.data_unit`s, and
                    no conversion is done.
        """

        data_as_array = np.asarray(data)
        if not issubclass(data_as_array.dtype.type, np.number):
            raise TypeError(f'Input data must be numeric. Got "{repr(data_as_array)}"')

        if data_are_given_in_display_units:
            self.data = data_as_array * display_unit.scale
        else:
            self.data = data_as_array

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
        """ Called for `format(array)` and `f-strings containing {array}`. """
        if not format_spec:
            format_spec = ".4G"
        array_string = np.array2string(
            self.data_in_display_units,
            formatter={"float_kind": lambda x: format(x, format_spec)},
        )
        return f"{array_string} {self.display_unit}"

    #
    #
    # --------------------------------------------
    #

    # See "Writing custom array containers"[1] from the NumPy manual for info on the
    # below `__array_ufunc__` and `__array_function__` methods.
    #
    # # [1](https://numpy.org/doc/stable/user/basics.dispatch.html)

    # The base class `NDArrayOperatorsMixin` implements Python dunder methods like
    # `__mul__` and `__imul__`, so that we can use standard Python syntax like `*` and
    # `*=` with our `Array`s.
    #
    # `NDArrayOperatorsMixin` implements these by calling the
    # corresponding NumPy ufuncs [like `np.multiply`], which in turn defer to our
    # `__array_ufunc__` method.

    # Elementwise operations (+, >, cos, sign, ..)
    def __array_ufunc__(self, *args, **kwargs):
        # Delegate implementation to a separate module, to keep this file overview-able.
        from .ufunc import __array_ufunc__

        return __array_ufunc__(self, *args, **kwargs)

    # NumPy methods (mean, sum, linspace, ...)
    def __array_function__(self, func, _types, _args, _kwargs):
        raise NotImplementedError(
            f"`{self.__class__.__name__}` does not yet support being used "
            f"with function `{func.__name__}`. {self._DIY_help_text}"
        )

    _DIY_help_text = (  # Shown when a NumPy operation is not implemented yet for our Array.
        "You can get the bare numeric data (a plain NumPy array) "
        "via `array.data`, and work with it manually."
    )
