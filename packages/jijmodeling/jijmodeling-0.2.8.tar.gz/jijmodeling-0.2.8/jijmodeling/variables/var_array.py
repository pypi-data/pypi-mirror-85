from typing import Union
from jijmodeling.variables.array import Array
from jijmodeling.variables.variable import Binary, DisNum, Placeholder, LogEncInteger

def BinaryArray(label: str, shape: Union[int, tuple, Placeholder])->Array:
    return Array(Binary(label), shape)

def PlaceholderArray(label: str, dim: int=None, shape: Union[int, tuple, Placeholder]=None)->Array:
    if shape is None and isinstance(dim, int):
        _shape = tuple(None for _ in range(dim))
        return Array(Placeholder(label), _shape)
    elif shape is not None:
        shape = (shape, ) if isinstance(shape, int) else shape
        return Array(Placeholder(label), shape)
    else:
        raise ValueError("Input shape or dim.")





def DisNumArray(label: str, shape, lower: float=0.0, upper: float=1.0, bits: int=3):
    return Array(DisNum(label, lower, upper, bits), shape)


def LogEncIntArray(label: str, shape, lower:int, upper: int):
    return Array(LogEncInteger(label, lower, upper), shape)