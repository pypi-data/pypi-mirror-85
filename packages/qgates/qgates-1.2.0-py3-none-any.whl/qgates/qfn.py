"""qgates.qfn

Contains helper functions for working with
quantum gates.
"""

from typing import Union, Iterable

from functools import reduce as _reduce
from operator import matmul as _matmul

import numpy as np

from . import states
from . import gates

__version__ = "1.0.3"


def tens(a: Union[int,float,list,np.ndarray],*b: Union[int,float,list,np.ndarray]) -> np.ndarray:
    """
    Computes the tensor product of
    two (or more) vectors/matrices.

    :param a: Start value for tensor product
    :param b: One or more other values for tensor product
    """
    return _reduce(np.kron,b,a)

def matmul(a: np.ndarray,*b: np.ndarray) -> np.ndarray:
    """
    Performs matrix multiplication between
    two or more

    :param a: Start value for matrix multiplication
    :param b: One or more other values for tensor product
    """
    return _reduce(_matmul,b,a)

def state(arr: Union[int,Iterable]) -> np.ndarray:
    """Creates a state vector
    from either an iterable of
    1s and 0s (or from an int that
    will be converted to a state
    vector based on its binary
    representation.

    :param arr: Int or iterable for creating state vector
    """
    if isinstance(arr,int):
        arr = [int(b) for b in bin(arr)[2:]]
    s = states.QB1 if arr[0] else states.QB0
    for n in arr[1:]:
        if n == 0:
            s = tens(s,states.QB0)
        else:
            s = tens(s,states.QB1)
    return s


def conjugate(v: Union[complex,list,np.ndarray],*args,**kwargs) -> Union[complex,np.ndarray]:
    """
    Returns the complex conjugate of v.

    :param v: number, vector, or matrix to conjugate
    """
    return np.conjugate(v,*args,**kwargs)
