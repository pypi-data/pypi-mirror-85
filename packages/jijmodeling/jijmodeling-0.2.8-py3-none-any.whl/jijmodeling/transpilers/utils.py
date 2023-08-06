
from jijmodeling.variables.element import Element
from jijmodeling.expression.expression import Expression, Operator
from typing import Tuple, List, Dict
from numbers import Number
from jijmodeling.variables.variable import Placeholder
from jijmodeling.variables.array import Array, ArraySizePlaceholder, Tensor
import numpy as np


def index_to_value(term, placeholder, indices):
    if isinstance(term, Operator):
        pyq_children = [index_to_value(c, 
                                placeholder=placeholder, 
                                indices=indices) 
                        for c in term.children]
        return term.operation(pyq_children)
    elif isinstance(term, Tensor) and isinstance(term.variable, Placeholder):
        ind_value_list = [int(indices[ind]) if isinstance(ind, str) else int(index_to_value(ind, placeholder, indices))
                      for ind in term.index_set]
        return np.array(placeholder[term.label])[tuple(ind_value_list)]
    elif isinstance(term, Element):
        return int(indices[term.label])
    elif isinstance(term, Expression):
        return to_value(term, placeholder, fixed_indices=indices)
    elif isinstance(term, int):
        return term
    elif isinstance(term, str):
        return indices[term]
    else:
        raise TypeError("The index's type should be Operator, Placeholder, Tensor or int.")


def _reshape_index(indices: dict, fixed_indices: dict, placeholder: dict)->List[Dict[str, int]]:
   # convert index set to list
    index_lists = {}
    for _index_label, V in indices.items():

        if isinstance(_index_label, Element):
            index_label = _index_label.label
        else:
            index_label = _index_label

        if isinstance(V, (list, np.ndarray)):
            # if like {'j > i': V} (V=[0,1,2,3] and i=1)
            # _satisfied_index_set retruns ('j', [2,3])
            index, index_set = _satisfied_index_set(index_label, V, fixed_indices)
        elif isinstance(V, (Number, Placeholder, Operator, Element)):
            V_length: int = to_value(V, placeholder=placeholder, fixed_indices=fixed_indices)
            if isinstance(int(V_length), int):
                index, index_set = _satisfied_index_set(index_label, np.arange(V_length), fixed_indices)
            else:
                raise TypeError("indices type is an integer. not {}".format(type(V_length)))
        elif isinstance(V, tuple):
            v0: int = to_value(V[0], placeholder=placeholder, fixed_indices=fixed_indices)
            v1: int = to_value(V[1], placeholder=placeholder, fixed_indices=fixed_indices)
            if isinstance(v0, int) and isinstance(v1, int):
                index, index_set = _satisfied_index_set(index_label, np.arange(v0, v1), fixed_indices)
            else:
                raise TypeError("When using tuple as a sum indices, the integer or placeholder which data type is an integer.")

        elif isinstance(V, Array) and isinstance(V.variable, Placeholder):
            v_set = placeholder[V.var_label]
            index, index_set = _satisfied_index_set(index_label, v_set, fixed_indices)
        elif isinstance(V, Expression):
            v_length = index_to_value(V, placeholder=placeholder, indices=fixed_indices)
            index, index_set = _satisfied_index_set(index_label, np.arange(v_length), fixed_indices)
        else:
            raise TypeError("index type should be list, Number, Placeholder or tuple, not {}".format(type(V)))
        index_lists[index] = index_set

    # reshape index_lists
    # ex. index_lists {'i': [0,1,2]}
    #     => ind_value_list [{'i': 0}, {'i': 1}, {'i': 2}]
    ind_value_list = []
    keys = list(index_lists.keys())
    num_indices = len(index_lists[keys[0]])
    for i in range(num_indices):
        ind_dict = {label: index_lists[label][i] for label in keys}
        ind_dict.update(fixed_indices)
        ind_value_list.append(ind_dict)
    return ind_value_list

def _satisfied_index_set(index_str: str, index_set: list, fixed_indices: dict)->Tuple[str, list]:
    """return index list satisfies condition

    Args:
        index_str (str): key string for summation index (ex. 'i', 'j > i')
        index_set (list): index value's list
        fixed_indices (dict): fixed index values to check condition for index (like 'j > i')

    Returns:
        Tuple[str, list]: modified index and index value list.
    """
    # When the key string of the index contains a conditional operation such as i < j, 
    # this function writes out the set that satisfies the condition.

    ind_chars = index_str.split(' ')
    if len(ind_chars) == 1:
        # index just represents index (has not condition like <)
        return index_str, index_set

    # ex. ind_chars = ('j', '<', 'i')
    index, operator, right_ind = ind_chars
    return index, [j for j in index_set 
                     if eval('{} {} {}'.format(j, operator, fixed_indices[right_ind]))]


def to_value(term, placeholder: dict, fixed_indices: dict):
    if isinstance(term, ArraySizePlaceholder):
        return np.array(placeholder[term.array_label]).shape[term.dimension]
    elif isinstance(term, Placeholder):
        return placeholder[term.label]
    elif isinstance(term, int):
        return term
    elif isinstance(term, (Operator, Tensor)):
        from jijmodeling.transpilers.calc_value import calc_value
        value: float = calc_value(term, {}, placeholder=placeholder, fixed_indices=fixed_indices)
        return int(value)
    elif isinstance(term, Element):
        return fixed_indices[term.label]
    else:
        raise TypeError('"{}" should be ArraySizePlaceholder or Placeholder or int.'.format(term.label))