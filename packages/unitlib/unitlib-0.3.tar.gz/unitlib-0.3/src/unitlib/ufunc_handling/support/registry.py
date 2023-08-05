from typing import Dict, Iterable, Union, Callable

import numpy as np

from unitlib.core_objects.type_aliases import UnitlibObject
from .ufunc_args import UfuncArgs


UfuncOutput = Union[UnitlibObject, np.ndarray, bool]
UfuncHandler = Callable[[UfuncArgs], UfuncOutput]


ufunc_handlers: Dict[np.ufunc, UfuncHandler] = {}


def implements(ufuncs: Iterable[np.ufunc]):
    """ Decorator to register a function as handling specific NumPy ufuncs. """

    # Called at `implements(..)`-time.

    def decorator(ufunc_handler: UfuncHandler):
        # Called at `def ufunc_handler(..`-time.

        for ufunc in ufuncs:
            ufunc_handlers[ufunc] = ufunc_handler

        return ufunc_handler

    return decorator
