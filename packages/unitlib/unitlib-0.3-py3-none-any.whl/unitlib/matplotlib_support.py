import matplotlib.units as mpl_custom_classes
import numpy as np
from matplotlib.axis import Axis

import unitlib


# The matplotlib module of interest is called `units`; but really it is used to allow
# arbitrary classes to be plotted -- nothing unit specific. That's why we aliased it to
# `mpl_custom_types`.


class ArrayPlotInterface(mpl_custom_classes.ConversionInterface):
    @staticmethod
    def convert(obj: unitlib.Array, unit: unitlib.Unit, axis: Axis) -> np.ndarray:
        """
        `unit` argument is specified by the user via the (not well-documented) options
        `xaxis.set_units()` or `plot(..., xunits=...)`. When these are not set, this
        class's `default_units` is used.
        """
        return obj.data_in_display_units

    @staticmethod
    def default_units(obj: unitlib.Array, axis: Axis) -> unitlib.Unit:
        return obj.display_unit

    @staticmethod
    def axisinfo(unit: unitlib.Unit, axis: Axis) -> mpl_custom_classes.AxisInfo:
        return mpl_custom_classes.AxisInfo(label=unit.name)


mpl_custom_classes.registry[unitlib.Array] = ArrayPlotInterface()
