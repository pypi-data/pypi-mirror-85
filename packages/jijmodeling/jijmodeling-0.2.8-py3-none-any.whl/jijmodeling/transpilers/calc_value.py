from functools import singledispatch

from numpy.lib.function_base import place

from jijmodeling.variables.element import Element

from jijmodeling.expression.expression import Operator
from jijmodeling.expression.constraint import Constraint, Penalty
from jijmodeling.variables.array import ArraySizePlaceholder, Tensor
from jijmodeling.variables.variable import Binary, Placeholder, Variable
from jijmodeling.expression.sum import Sum
from jijmodeling.transpilers.utils import _reshape_index
from typing import Dict
import numpy as np
import math


def calc_value(term, decoded_sol: dict, placeholder: dict={}, fixed_indices: dict={}):
    return _calc_value(term, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)

@singledispatch
def _calc_value(term, decoded_sol: dict, placeholder={}, **kwargs)->float:
    if isinstance(term, (int, float)):
        return term
    if isinstance(term, Variable):
        if term.label in decoded_sol:
            return decoded_sol[term.label]
        elif term.label in placeholder:
            return decoded_sol[placeholder]
        else:
            raise ValueError('{} is not found in solution and placeholder'.format(term.label))
    else:
        raise TypeError('calc_value do not support {}'.format(type(term)))


@_calc_value.register(Operator)
def calc_operator_value(term: Operator, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    child_values = [calc_value(child, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices) for child in term.children]
    term_value: float = term.operation(child_values)
    return term_value


@_calc_value.register(Binary)
def calc_binary_value(term: Binary, decoded_sol: dict, placeholder={}, **kwargs)->float:
    if term.label in decoded_sol:
        return decoded_sol[term.label]
    else:
        # TODO: add warning
        return 0

@_calc_value.register(Placeholder)
def calc_placeholder_value(term: Placeholder, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    return placeholder[term.label]

@_calc_value.register(ArraySizePlaceholder)
def calc_placeholder_value(term: ArraySizePlaceholder, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    array = placeholder[term.array_label]
    return array.shape[term.dimension]


@_calc_value.register(Element)
def calc_element_value(term: Element, decoded_sol: dict, placeholder={}, fixed_indices={}):
    return fixed_indices[term.label]


@_calc_value.register(Tensor)
def calc_tensor_value(term: Tensor, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    sol: Dict[tuple, float] = {}
    if term.label in decoded_sol:
        sol = decoded_sol[term.label]
    elif term.label in placeholder:
        sol = placeholder[term.label]
    else:
        ValueError('"{}" is not found in placehoder and solution.'.format(term.label))
    
    def to_index(obj):
        if isinstance(obj, str):
            return fixed_indices[obj]
        else:
            return calc_value(obj, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
    index_label = [int(to_index(label)) for label in term.indices]

    try:
        value = np.array(sol)[tuple(index_label)]
    except IndexError as e:
        raise ValueError("{}.\nThe shape of '{}' is {}, but access indices are {}.".format(e, term.label, np.array(sol).shape, index_label))

    if value is np.nan:
        return 0
    return value


@_calc_value.register(Sum)
def calc_sum_value(term: Sum, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    # Sum の calc_valueを書く
    # Sumのcalc_valueはいったん普通に要素に対してやるが、TODOでnumpyの演算をうまく使うようにメモしておく
    sum_index = _reshape_index(term.indices, fixed_indices=fixed_indices, placeholder=placeholder)
    term_value:float = 0.0
    if term.condition is not None:
        for child in term.children:
            for ind in sum_index:
                sum_cond = calc_value(term.condition, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
                if sum_cond:
                    child_val: float = calc_value(child, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
                    term_value += child_val if not math.isnan(child_val) else 0.0
    else:
        for child in term.children:
            for ind in sum_index:
                child_val: float = calc_value(child, decoded_sol=decoded_sol, placeholder=placeholder, fixed_indices=ind)
                term_value += child_val if not math.isnan(child_val) else 0.0
    return term_value



@_calc_value.register(Constraint)
def calc_constraint_value(term: Constraint, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    penalty_value = calc_value(term.children[0], decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
    if term.condition == '==' and penalty_value == term.constant:
        return 0.0
    elif term.condition == '<=' and penalty_value <= term.constant:
        return 0.0
    elif term.condition == '<' and penalty_value < term.constant:
        return 0.0
    else:
        return penalty_value - term.constant


@_calc_value.register(Penalty)
def calc_penalty_value(term: Penalty, decoded_sol: dict, placeholder={}, fixed_indices={})->float:
    return calc_value(term.penalty_term, decoded_sol, placeholder=placeholder, fixed_indices=fixed_indices)
