from jijmodeling.variables.var_array import LogEncIntArray
from jijmodeling.variables.array import Tensor
from jijmodeling.expression.sum import Sum
from jijmodeling.expression.constraint import Constraint
from jijmodeling.expression.expression import Expression, Operator
from jijmodeling.variables.array import ArraySizePlaceholder
from jijmodeling.variables.variable import Binary, DisNum, LogEncInteger, Placeholder
from jijmodeling.transpilers.utils import _reshape_index
from functools import singledispatch
import numpy as np

def to_pulp(term: Expression, placeholder: dict, fixed_variables: dict):
    import pulp

    constraints = []
    variables = {}

    @singledispatch
    def jij_to_pulp(term, **kwargs):
        return term

    def variable_to_pulp(term, var_func, relabel):
        if term.label in fixed_variables and not isinstance(fixed_variables[term.label], dict):
            return fixed_variables[term.label]
        elif term.label in variables:
            return variables[term.label]
        elif relabel is not None:
            return var_func(relabel)
        else:
            # If to_pyqubo is called as an element of Tensor, 
            # use relabel to add subscript information to label.
            # ex. relabel => 'x[1][0]'
            term_label = term.label if relabel is None else relabel
            var_obj = var_func(term_label)
            variables[term_label] = var_obj
            return var_obj

    @jij_to_pulp.register(Binary)
    def binary_to_pulp(term: Binary, relabel: str=None, index_values={}):
        var_func = lambda label: pulp.LpVariable(label, cat=pulp.LpBinary)
        return variable_to_pulp(term, var_func, relabel)

    @jij_to_pulp.register(DisNum)
    def disnum_to_pulp(term: DisNum, relabel: str = None, index_values={}):
        var_func = lambda label: pulp.LpVariable(label, lowBound=term.lower, upBound=term.upper)
        return variable_to_pulp(term, var_func, relabel)

    @jij_to_pulp.register(LogEncInteger)
    def logencint_to_pulp(term: LogEncInteger, relabel: str = None, index_values={}):
        var_func = lambda label: pulp.LpVariable(label, lowBound=term.lower, upBound=term.upper, cat='Integer')
        return variable_to_pulp(term, var_func, relabel)

    @jij_to_pulp.register(Placeholder)
    def placeholder_to_pulp(term, index_values: dict = {}):
        return placeholder[term.label]

    @jij_to_pulp.register(Tensor)
    def tensor_to_pulp(term: Tensor, index_values: dict):
        ind_value_list = [index_values[ind] if isinstance(ind, str) else jij_to_pulp(ind, index_values=index_values) 
                      for ind in term.index_set]
        # If a fixed value is set, it is returned.
        if term.label in fixed_variables:
            if tuple(ind_value_list) in fixed_variables[term.label]:
                fixed_var = fixed_variables[term.label]
                if isinstance(fixed_var, dict):
                    return fixed_var[tuple(ind_value_list)]
                else:
                    raise TypeError("fixed variable's value type is dict")
        if term.label in placeholder:
            if isinstance(placeholder[term.label], (list, np.ndarray)):
                return np.array(placeholder[term.label])[tuple(ind_value_list)]

        if term.label in variables:
            return variables[term.label][tuple(ind_value_list)]
        else:
            shape = [jij_to_pulp(s) for s in term.shape]
            def make_array(array, indices):
                if len(indices) == len(shape) -1:
                    name = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
                    return [jij_to_pulp(term.variable, relabel=name + '[{}]'.format(i)) for i in range(shape[-1])]
                else:
                    for s in range(shape[len(indices)]):
                        array.append(make_array([], indices + [s]))
                    return array
            variables[term.label] = np.array(make_array([], []))

        vars = variables[term.label][tuple(ind_value_list)]
        return vars

    @jij_to_pulp.register(ArraySizePlaceholder)
    def arraysizeplaceholder_to_pyqubo(term: ArraySizePlaceholder, index_values={}):
        if term.array_label in placeholder:
            p_array = np.array(placeholder[term.array_label])
            return p_array.shape[term.dimension]
        else:
            raise ValueError("The placeholder must be set to list or np.ndarray if the size of the array is used.")


    @jij_to_pulp.register(Sum)
    def sum_to_pulp(term: Sum, index_values: dict):
        # convert index set to list
        ind_value_list = _reshape_index(term.indices, index_values, placeholder)
        return sum(jij_to_pulp(term.children[0], index_values=ind) for ind in ind_value_list)

    @jij_to_pulp.register(Operator)
    def operator_to_pulp(term: Operator, index_values: dict={}):
        pyq_children = [jij_to_pulp(c, index_values=index_values) 
                        for c in term.children]
        return term.operation(pyq_children)



    @jij_to_pulp.register(Constraint)
    def constraint_to_pulp(term: Constraint, index_values: dict={}):
        if term.with_penalty and term.with_mul:
            # In this case, penalty term's shape is "multiplier" * "constraint-term"
            # So, we have to extracte only "constraint-term"
            child = term.children[0].children[0].children[1]
        else:
            child = term.children[0]
        constraint_term = jij_to_pulp(child, index_values=index_values)
        right_hand_side = jij_to_pulp(term.constant, index_values=index_values)
        if term.condition == '==':
            constraints.append(constraint_term == right_hand_side)
        elif term.condition == '<=':
            constraints.append(constraint_term <= right_hand_side)
        elif term.condition == '<':
            constraints.append(constraint_term <= right_hand_side)

        return 0


    objective = jij_to_pulp(term, index_values={})
    return objective, constraints, variables


    
    




    