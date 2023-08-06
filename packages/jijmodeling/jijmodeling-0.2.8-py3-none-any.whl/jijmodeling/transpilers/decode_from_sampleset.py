"""
In this module, we provide functions to decode solutions 
from dimod.SampleSet and openjij.Response 
into a form that can be easily analyzed.

Ex.
When jijmodeling generates a `Tensor` object to create a QUBO, 
a key is assigned to it in the form of "x[0][1]", 
but it is difficult to parse the solution with a dictionary type 
whose key is this string.
So the function decodes the key of Tensor Variables created 
by the object are returned as `numpy.ndarray`, 
and variables defined as integers such as `LogEncInt` are encoded as integers.
"""

from jijmodeling.variables.array import Tensor, Array, ArraySizePlaceholder
from typing import Union, Tuple
from functools import singledispatch
from jijmodeling.variables.variable import Binary, DisNum, LogEncInteger, Placeholder, Variable
from numbers import Number
import numpy as np

DATA_LIST = (np.ndarray, list)

@singledispatch
def decode_from_dict(term: Union[Variable, Tensor], sample: dict, placeholder={})->dict:
    if not isinstance(term, (Variable, Tensor)):
        raise TypeError("{} cannot convert to number.".format(type(term)))
    
    if isinstance(term, Placeholder):
        raise TypeError("decode_from_dict do not support Placeholder.")


@decode_from_dict.register(Binary)
def decode_binary(term: Binary, sample: dict, indices=[], placeholder={}, fixed_variables={})->dict:
    label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    if term.label in fixed_variables:
        if isinstance(fixed_variables[term.label], Number):
            return {term.label: fixed_variables[term.label]}
        elif isinstance(fixed_variables[term.label], DATA_LIST):
            # binary 'x' is an element of tensor object.
            # ex. fixed_variables => {'x': {(0, 1): 1}}
            return {term.label: fixed_variables[term.label][tuple(indices)]}
        else:
            return {term.label: np.nan}
    elif label in sample:
        return {term.label: sample[label]}
    
    # TODO: raise warning
    return {term.label: np.nan}


@decode_from_dict.register(LogEncInteger)
def decode_logencint_from_dict(term: LogEncInteger, sample: dict, indices=[], placeholder={}, fixed_variables={}):
    upper: int = convert_to_int(term.upper, placeholder=placeholder, indices=indices)
    lower: int = convert_to_int(term.lower, placeholder=placeholder, indices=indices)
    bits = int(np.log2(upper - lower))+1
    label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    value = 0.0
    for bit in range(bits):
        var_indices = label +'[{}]'.format(bit)
        if var_indices not in sample:
            value = np.nan
            break
        value += 2**bit * sample[var_indices]
    if value is np.nan:
        return {term.label: np.nan}
    value = int(value + lower)
    return {term.label: value}



@decode_from_dict.register(DisNum)
def decode_DisNum_from_dict(term: DisNum, sample: dict, indices=[], placeholder={}, fixed_variables={}):
    upper: int = convert_to_int(term.upper, placeholder=placeholder, indices=indices)
    lower: int = convert_to_int(term.lower, placeholder=placeholder, indices=indices)
    bits: int = convert_to_int(term.bits, placeholder=placeholder, indices=indices)
    label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    value = 0.0
    for bit in range(bits):
        var_indices = label +'[{}]'.format(bit)
        value += 2**bit * sample[var_indices]
    coeff = (upper - lower)/(2**bits-1)
    value = coeff * value + lower
    return {term.label: value}


@decode_from_dict.register(Tensor)
def decode_tensor(term: Tensor, sample: dict, placeholder={}):
    # shape is converted to an `int` object.
    shape: Tuple[int, ...] = tuple([convert_to_int(s, placeholder) for s in term.shape])

    array_value = np.full(shape, np.nan, dtype=np.float)
    # Based on the `self.shape`, we recursively call `set_value`
    # and add the decoded value to the `array_value`.
    def set_value(fixed_indice: list):
        if len(fixed_indice) == len(shape):
            # When the number of `fixed_indices` equals dimension of the array,
            # i.e. len(shape), the elements of the array can finally be accessed.
            # The result of accessing and decoding the elements is stored in `array_value`.
            indices_str = str(fixed_indice).replace(',', '][').replace(' ', '')
            decoded_value = decode_from_dict(term.variable, sample, placeholder=placeholder, indices=fixed_indice)
            array_value[tuple(fixed_indice)] = decoded_value[term.variable.label]
        else:
            # When `len(fixed_indices) < len(shape)`,
            # the values of all indices to access elements
            # have not yet been determinded.
            # Next, we will determined the value of the next dimension's
            # due to move on to the next recursive step.
            fixed_num = len(fixed_indice)
            for i in range(shape[fixed_num]):
                new_fixed = fixed_indice + [i]
                set_value(new_fixed)
    set_value([])
    return {term.variable.label: array_value}


@decode_from_dict.register(Array)
def decode_array(term: Array, sample: dict, placeholder={}):
    return decode_tensor(term, sample=sample, placeholder=placeholder)


def convert_to_int(obj, placeholder={}, indices=None)->int:
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, ArraySizePlaceholder):
        return np.array(placeholder[obj.array_label]).shape[obj.dimension]
    elif isinstance(obj, Array):
        return np.array(placeholder[obj.var_label])[tuple(indices)]
    elif isinstance(obj, Placeholder):
        return placeholder[obj.label]
    else:
        raise TypeError('summation index type is int or ArraySizePlaceholder or Placeholder.')


