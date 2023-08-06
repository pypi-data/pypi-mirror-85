from functools import singledispatch
from jijmodeling.transpilers.calc_value import calc_value

from jijmodeling.variables.element import Element
from jijmodeling.expression.constraint import Constraint, Penalty
from jijmodeling.expression.expression import Operator
from numbers import Number
from typing import Dict, Union

from jijmodeling.variables.variable import Binary, DisNum, LogEncInteger, Placeholder
from jijmodeling.variables.array import ArraySizePlaceholder
from jijmodeling.variables.array import Tensor
from jijmodeling.expression.sum import Sum
from jijmodeling.transpilers.decode_from_sampleset import convert_to_int
from jijmodeling.transpilers.utils import _reshape_index, index_to_value
import numpy as np
import pyqubo as pyq


def to_pyqubo(term, placeholder:dict={}, fixed_variables: dict={}, index_values: dict={})->pyq.Base:

    cache = {}

    @singledispatch
    def _to_pyqubo(term, placeholder={}, fixed_variables={}, index_values={})->pyq.Base:
        # transpile to PyQUBO
        if isinstance(term, (Number, str)):
            return term
        raise TypeError("{} cannot convert to pyqubo object.".format(type(term)))

    @_to_pyqubo.register(Binary)
    def binary_to_pyqubo(term, fixed_variables={}, relabel:str=None, variables={}, **kwargs):
        if term.label in fixed_variables and not isinstance(fixed_variables[term.label], dict):
            return fixed_variables[term.label]
        else:
            # If _to_pyqubo is called as an element of Tensor, 
            # use relabel to add subscript information to label.
            # ex. relabel => 'x[1][0]'
            if term.label in variables:
                return variables[term.label]
            term_label = term.label if relabel is None else relabel
            return pyq.Binary(term_label)

    def index_from_str(ind_str: str):
        if ind_str is None:
            return []
        ind_int = [int(ind[:-1]) for ind in ind_str.split('[')[1:]]
        return ind_int

    @_to_pyqubo.register(DisNum)
    def disnum_to_pyqubo(term: DisNum, placeholder: dict, fixed_variables: dict, relabel: str=None, **kwargs):
        if term.label in fixed_variables and not isinstance(fixed_variables[term.label], dict):
            return fixed_variables[term.label]
        var_label = (term.label if relabel is None else relabel) + '[{}]'
        index_int = index_from_str(relabel)
        upper: int = convert_to_int(term.upper, placeholder=placeholder, indices=index_int)
        lower: int = convert_to_int(term.lower, placeholder=placeholder, indices=index_int)
        bits: int = convert_to_int(term.bits, placeholder=placeholder, indices=index_int)
        coeff = (upper - lower)/(2**bits - 1)
        return coeff * sum(2**i * pyq.Binary(var_label.format(i)) for i in range(bits)) + lower


    @_to_pyqubo.register(LogEncInteger)
    def logencint__to_pyqubo(term: LogEncInteger, placeholder, fixed_variables, relabel: str=None, **kwargs):
        if term.label in fixed_variables and not isinstance(fixed_variables[term.label], dict):
            return fixed_variables[term.label]
        var_label = (term.label if relabel is None else relabel)
        index_int = index_from_str(relabel)
        upper: int = convert_to_int(term.upper, placeholder=placeholder, indices=index_int)
        lower: int = convert_to_int(term.lower, placeholder=placeholder, indices=index_int)
        bits = int(np.log2(upper - lower)) + 1
        coeff = (upper - lower)/(2**bits - 1)
        array = pyq.Array.create(var_label, shape=bits, vartype='BINARY')
        return coeff * sum(2**i * array[i] for i in range(bits)) + lower

    @_to_pyqubo.register(Placeholder)
    def placeholder_to_pyqubo(term, placeholder, index_values: dict = {}, fixed_variables={}):
        if term.label in placeholder:
            return placeholder[term.label]
        else:
            return pyq.Placeholder(term.label)

    @_to_pyqubo.register(Element)
    def element_to_pyqubo(term, placeholder: dict, fixed_variables: dict, index_values: dict):
        if term.array_label is None:
            start, end = term.range
            se_to_pyq = lambda a: _to_pyqubo(a, placeholder=placeholder, index_values=index_values, fixed_variables=fixed_variables)
            data_set = np.arange(se_to_pyq(start), se_to_pyq(end))
        else:
            data_set = placeholder[term.array_label]
        return data_set[index_values[term.label]]

    @_to_pyqubo.register(ArraySizePlaceholder)
    def arraysizeplaceholder_to_pyqubo(term: ArraySizePlaceholder, placeholder: dict, index_values={}, fixed_variables={}):
        if term.array_label in placeholder:
            p_array = np.array(placeholder[term.array_label])
            return p_array.shape[term.dimension]
        else:
            raise ValueError("The placeholder must be set to list or np.ndarray if the size of the array is used.")


    @_to_pyqubo.register(Tensor)
    def tensor_to_pyqubo(
        term: Tensor, 
        index_values: dict, 
        placeholder:Dict[str, Union[Number, list, np.ndarray]]={}, 
        fixed_variables:Dict[str, Dict[tuple, Number]]={},
        variables={}):

        ind_value_list = [int(index_values[ind]) if isinstance(ind, str) else int(_to_pyqubo(ind, placeholder=placeholder, index_values=index_values, fixed_variables=fixed_variables))
                        for ind in term.indices]
        
        # If a fixed value is set, it is returned.
        if term.label in fixed_variables:
            if tuple(ind_value_list) in fixed_variables[term.label]:
                fixed_var: Union[dict, Number] = fixed_variables[term.label]
                if isinstance(fixed_var, dict):
                    return fixed_var[tuple(ind_value_list)]
                else:
                    raise TypeError("fixed variable's value type is dict")
        try:
            if term.label in placeholder:
                if isinstance(placeholder[term.label], (list, np.ndarray)):
                    return np.array(placeholder[term.label])[tuple(ind_value_list)]
        except IndexError as e:
            raise ValueError("{}.\nThe shape of '{}' is {}, but access indices are {}.".format(e, term.label, np.array(placeholder[term.label]).shape, ind_value_list))

        # make name of tensor element (ex. x[0][1])
        def generator(index):
            tensor_name = term.label + ''.join(['[{}]'.format(ind) for ind in index])
            return _to_pyqubo(term.variable, relabel=tensor_name, placeholder=placeholder, fixed_variables=fixed_variables, variables=variables)
        if term.label not in variables:
            shape = [_to_pyqubo(s, placeholder=placeholder, fixed_variables=fixed_variables) for s in term.shape]
            pyq_obj = pyq.Array._create_with_generator(shape=shape, generator=generator)
            variables[term.label] = pyq_obj
        else:
            pyq_obj = variables[term.label]
        return pyq_obj[tuple(ind_value_list)]


    @_to_pyqubo.register(Operator)
    def operator_to_pyqubo(term: Operator, placeholder: dict, fixed_variables: dict, index_values: dict):
        pyq_children = [_to_pyqubo(c, 
                                placeholder=placeholder, 
                                fixed_variables=fixed_variables, 
                                index_values=index_values) 
                        for c in term.children]
        return term.operation(pyq_children)


    def memorize(f):
        def memorized__to_pyqubo(term, placeholder: dict, fixed_variables: dict, index_values: dict):
            term_indices = [index_to_value(ind, placeholder, index_values) for ind in term.index_set]
            cache_hash = hash((hash(term), tuple(term_indices)))
            if cache_hash not in cache:
                # check index
                cache[cache_hash] = f(term, placeholder=placeholder, fixed_variables=fixed_variables, index_values=index_values)
            return cache[cache_hash]
        return memorized__to_pyqubo


    @_to_pyqubo.register(Sum)
    @memorize
    def sum_to_pyqubo(term: Sum, placeholder: dict, fixed_variables: dict, index_values: dict):
        # convert index set to list
        ind_value_list = _reshape_index(term.indices, index_values, placeholder)
        value = 0.0
        if term.condition is not None:
            for ind in ind_value_list:
                if calc_value(term.condition, {}, placeholder=placeholder, fixed_indices=ind):
                    value += _to_pyqubo(term.children[0], placeholder=placeholder, fixed_variables=fixed_variables, index_values=ind)
        else:
            for ind in ind_value_list:
                value += _to_pyqubo(term.children[0], placeholder=placeholder, fixed_variables=fixed_variables, index_values=ind)
            
        return value


    @_to_pyqubo.register(Constraint)
    def constraint__to_pyqubo(term: Constraint, placeholder: dict, fixed_variables: dict, index_values: dict):
        if term._penalty is None:
            return 0

        pena = _to_pyqubo(term.penalty, placeholder=placeholder, fixed_variables=fixed_variables, index_values=index_values)

        return pyq.Constraint(pena, term.label)

    @_to_pyqubo.register(Penalty)
    def penalty__to_pyqubo(term: Penalty, placeholder: dict, fixed_variables: dict, index_values: dict):
        pena_term = term.children[0]
        return _to_pyqubo(pena_term, placeholder=placeholder, fixed_variables=fixed_variables, index_values=index_values)


    return _to_pyqubo(term, placeholder=placeholder, fixed_variables=fixed_variables, index_values=index_values)