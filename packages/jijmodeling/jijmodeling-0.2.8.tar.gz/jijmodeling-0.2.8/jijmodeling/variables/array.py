from typing import Union
from jijmodeling.expression.expression import Expression, _latex_repr
from jijmodeling.variables.variable import Placeholder, Variable
from jijmodeling.expression.sum import Sum

class Tensor(Variable):
    """A class for making a Variable object subscriptable.

    Args:
        label (str): label of variable.
        variable (:class:`jijmodeling.Variable`): base variable object.
        shape (tuple/int): shape of variable.
        index_set (list[str/:class:`Expression`/int]): Index object list, which is unordered.
        indices (list[str/:class:`Element`/int]): List of ordered subscript elements

    Attributes:
        label (str): label of variable.
        variable (:class:`jijmodeling.Variable`): base variable object.
        shape (tuple): shape of variable.
        index_set (list[str/:class:`Expression`/int]): Index object list, which is unordered.
        indices (list[str/:class:`Element`/int]): List of ordered subscript elements
    """
    def __init__(self, label, variable, shape, index_set, indices):
        super().__init__(label)
        self.variable = variable
        self.shape = (shape, ) if isinstance(shape, int) else shape
        self.index_set = index_set
        self.indices = indices

    def _rdiv_validate(self, other):
        self.variable._rdiv_validate(other)

    def __repr__(self):
        index_str = ''
        for i in self.index_set:
            index_str += '[%s]' % i
        return self.label + index_str

    def __make_latex__(self):
        t_str = self.label
        t_str += "_{{{}}}".format(','.join([_latex_repr(ind, False) for ind in self.index_set]))
        return t_str


class ArraySizePlaceholder(Placeholder):
    def __init__(self, label:str, array_label: str, dimension: int):
        super().__init__(label)
        self.array_label = array_label
        self.dimension = dimension

    def __make_latex__(self):
        return "|" + self.array_label + "|_" + "{{{}}}".format(self.dimension + 1)


class Array:
    """Array object of Variable object.

    Args:
        variable (:class:`jijmodeling.Variable`): element object of Array.
        shape (tuple | int): shape of array.

    Attributes:
        variable (:class:`jijmodeling.Variable`): element object of Array.
        var_label (str): label of variable.
        dim (int): number of indices.
    """
    def __init__(self, variable: Variable, shape):
        self.variable: Variable = variable
        self.var_label: str = variable.label
        self._shape = shape if isinstance(shape, tuple) else (shape, )
        self.dim: int = len(self._shape)

    @property
    def shape(self):
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                array_size = ArraySizePlaceholder(
                                label=self.var_label + '_shape_%d' % i, 
                                array_label=self.var_label,
                                dimension=i
                            )
                shape.append(array_size)
            else:
                shape.append(s)
        return tuple(shape)

    def __getitem__(self, key)->Union[Tensor, Sum]:
        if not isinstance(key, tuple):
            key = (key, )

        if len(key) != self.dim:
            raise ValueError("{}'s dimension is {}.".format(self.var_label, self.dim))

        index_set = []
        indices = []
        summation_index = []
        for i, k in enumerate(list(key)):
            # for syntaxsugar x[:]
            # If a slice [:] is used for a key, 
            # it is syntax-sugar that represents Sum, 
            # and the index is automatically created and assigned.
            # i.e. x[:] => Sum({':x_0': n}, x[':x_0']) 
            # This created index is stored in summation_index as Sum will be added later.
            if isinstance(k, slice):
                index_set.append(':{}_{}'.format(self.var_label, i))
                indices.append(':{}_{}'.format(self.var_label, i))
                summation_index.append((i, index_set[i]))
            elif isinstance(k, (int, str)):
                index_set.append(k)
                indices.append(k)
            elif isinstance(k, Expression):
                # exstract Element class
                elements = set(extract_element_class(k))
                if len(elements) > 0 or len(k.index_set) > 0:
                    index_set += list(elements)
                    index_set += k.index_set
                else:
                    index_set.append(k)
                indices.append(k)

        term = Tensor(self.var_label, self.variable, self.shape, index_set=index_set, indices=indices)
        # for syntax-sugar x[:]
        for i, ind in summation_index:
            term = Sum({ind: self.shape[i]}, term)

        return term

    def __repr__(self) -> str:
        return self.var_label


def extract_element_class(term):
    from jijmodeling.variables.element import Element
    if isinstance(term, Element):
        return [term]
    elif isinstance(term, Expression):
        elements = []
        for child in term.children:
            elements += extract_element_class(child)
        for ind in term.index_set:
            if isinstance(ind, Element):
                elements.append(ind)
        return elements
    else:
        return []
    