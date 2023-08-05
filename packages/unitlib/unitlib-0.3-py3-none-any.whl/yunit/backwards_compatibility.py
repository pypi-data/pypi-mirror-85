"""
Support Python 3.6 and 3.7
"""

import sys
from typing import Iterable

import numpy as np


if sys.version_info >= (3, 8):
    from typing import Protocol, Literal, TYPE_CHECKING
    from math import prod

else:
    # Backports of new objects from `typing`.
    from typing_extensions import Protocol, Literal, TYPE_CHECKING

    def prod(numbers: Iterable[float]) -> float:
        return np.prod(numbers).item()


# Trick to make PyCharm IDE:
#  - Not complain about unused imports
#  - In other modules, suggest importing these objects from this module instead of from
#    their original packages.
Protocol, Literal, TYPE_CHECKING = Protocol, Literal, TYPE_CHECKING
prod = prod

# `TYPE_CHECKING` is `False` at runtime, but `True` for the IDE (PyCharm eg). This means
# that we can put import statements that would cause circular import errors within an
# `if TYPE_CHECKING` block, and avoid such errors, while still having the IDE resolve
# type annotations.
# See [PEP 563](https://www.python.org/dev/peps/pep-0563/#runtime-annotation-resolution-and-type-checking).
