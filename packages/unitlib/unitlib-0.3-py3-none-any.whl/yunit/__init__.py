from .core_objects import Unit, Quantity, Array


try:
    import matplotlib
except ModuleNotFoundError:
    pass  # A matplotlib installation is not required.
else:
    # But if it is installed, allow it to plot yunit Arrays.
    from . import matplotlib_support
