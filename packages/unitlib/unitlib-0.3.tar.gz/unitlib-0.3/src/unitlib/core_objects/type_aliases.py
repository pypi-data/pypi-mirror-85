from typing import Union, Tuple

from . import Array, Quantity, Unit
from ..type_aliases import NDArrayLike

UnitlibObject = Union[Array, Quantity, Unit]
UfuncInput = Union[UnitlibObject, NDArrayLike]
ArrayIndex = Union[int, Tuple[int, ...]]
ArraySlice = Union[Array, Quantity]
