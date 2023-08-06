from abc import ABCMeta, abstractmethod
from typing import Any, Dict
import inspect
import numpy as np
import pyqubo
from jijmodeling.expression.from_serializable import from_serializable, _cls_serializable_validation

class Expression(metaclass=ABCMeta):
    """All component of JijModeling objects inheritance this class.
    This class provide computation rules and each component.

    Args:
        children (list): children objects list. list of :class:`Expression`, int or float.
    
    Attributes:
        children (list): children objects list. list of :class:`Expression`, int or float.
        index_set (list[str/:class:`Expression`/int]): Index object list, which is unordered.
    """

    remove_element = []

    def __init__(self, children: list):
        self.children = []
        for c in children:
            if not isinstance(c, Expression) and c in self.remove_element:
                continue
            self.children.append(c)

        # Collect the un-summarized indices of each child.
        self.index_set = []
        for child in self.children:
            if isinstance(child, Expression):
                self.index_set += child.index_set
        self.index_set = list(set(self.index_set))
        self._latex_label = None


    def set_latex_label(self, label: str):
        """Change LaTeX representation

        Args:
            label (str): Modified LaTeX representation

        Example:
            By default, the LaTeX representation is determined by the child object, 
            but the LaTeX representation will be overwritten if set by this method.

            >>> from jijmodeling import Binary
            >>> x, y = Binary('x'), Binary('y')
            >>> term = x + y
            >>> term._repr_latex_()
            '$x + y$'
            >>> term.set_latex_label('t')
            >>> term._repr_latex()
            '$t$'
        """
        self._latex_label = label

    def _repr_latex_(self):
        return "${}$".format(self.__latex__())

    def __make_latex__(self):
        return self.__repr__()
    
    def __latex__(self):
        if self._latex_label is None:
            return self.__make_latex__()
        else:
            return self._latex_label

    def __add__(self, other):
        # TODO: check type of other
        return Add([self, other])

    def __radd__(self, other):
        return self.__add__(other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __rsub__(self, other):
        return Add([other, -1*self])

    def __lsub__(self, other):
        return Add([self, -1*other])

    def __mul__(self, other):
        return Mul([self, other])
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __lmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Div([self, other])

    def __rtruediv__(self, other):
        return Div([other, self])

    def __pow__(self, other):
        return Power([self, other])

    def __rpow__(self, other):
        return Power([other, self])

    def __mod__(self, other):
        return Mod([self, other])

    def __hash__(self) -> int:
        if len(self.children) > 0:
            hashs = [hash(c) for c in self.children]
            repr_str = str(self)
            return hash((repr_str, tuple(hashs)))
        else:
            raise ValueError('Expression objects that do not have children are not hashable.')

    def __lt__(self, other):
        from jijmodeling.expression.condition import LessThan
        return LessThan([self, other])

    def __le__(self, other):
        from jijmodeling.expression.condition import LessThanEqual
        return LessThanEqual([self, other])

    # TODO: If you overwrite the equivalence, 
    #       the in operator will behave unexpectedly, 
    #       and it will affect many places, so the test will not pass, 
    #       so we will not implement it once.
    # def __eq__(self, other):
    #     from jijmodeling.expression.condition import Equal
    #     return Equal([self, other])
    # def __ne__(self, other):
    #     from jijmodeling.expression.condition import NotEqual
    #     return NotEqual([self, other])

    def __gt__(self, other):
        from jijmodeling.expression.condition import GreaterThan
        return GreaterThan([self, other])
    
    def __ge__(self, other):
        from jijmodeling.expression.condition import GreaterThanEqual
        return GreaterThanEqual([self, other])

    def to_serializable(self)->dict:
        """Convert to serializable object (dict)

        Returns:
            dict: serializable object
        """

        def express_to_ser(s):
            if 'to_serializable' in dir(s):
                return s.to_serializable()
            elif isinstance(s, (list, tuple)):
                return {
                    'iteratable': 'list' if isinstance(s, list) else 'tuple',
                    'value': [express_to_ser(t) for t in s],
                }
            elif isinstance(s, dict):
                return {k: express_to_ser(v) for k,v in s.items()}
            else:
                return s
        serializable = {
            'class': self.__class__.__module__ + '.' + self.__class__.__name__,
            'attributes': {k: express_to_ser(v) for k, v in vars(self).items()}
        }
        return serializable

    def to_pyqubo(self, placeholder={}, fixed_variables: Dict[tuple, int]={}, index_values={})->pyqubo.Base:
        """Convert to PyQUBO object

        Args:
            placeholder (dict, optional): A dictionary that contains the values that correspond to each placeholder object. Defaults to {}.
            fixed_variables (dict[tuple, int], optional): A dictionary that stores variables to be fixed. Defaults to {}.
            index_values (dict, optional): Value of each index. Defaults to {}.

        Returns:
            :class:`pyqubo.Base`: Converted PyQUBO object.

        Example:
            >>> from jijmodeling import Binary, Placeholder
            >>> x, y = Binary('x'), Binary('y')
            >>> d = Placeholder('d')
            >>> t = d*x*(y+1)
            >>> t.to_pyqubo({'d': 3}, {'y': 1})
            Binary(x)*Num(3.000000)*Num(2.000000)
            >>> import pyqubo as pyq
            >>> x_p = pyq.Binary('x')
            >>> x_p * 3 * (1+1) == t.to_pyqubo({'d': 3}, {'y': 1})
            True
        """
        # type check
        _ph = {k: np.array(v) if isinstance(v, list) else v for k, v in placeholder.items()}
        from jijmodeling.transpilers.to_pyqubo import to_pyqubo
        return to_pyqubo(self, placeholder=_ph, fixed_variables=fixed_variables, index_values=index_values)

    @classmethod
    def from_serializable(cls, serializable: dict):
        """Create Expression object from serializable object (dict)

        Args:
            serializable (dict): serializable object which is created by `.to_serializable`

        Returns:
            :class:`jijmodeling.expression.expression.Expression`: Expression object
        """
        _cls_serializable_validation(serializable, cls)
        init_args = inspect.getfullargspec(cls.__init__).args
        init_args_values = {arg: from_serializable(serializable['attributes'][arg]) for arg in init_args if arg != 'self'}
        return cls(**init_args_values)

class Operator(Expression, metaclass=ABCMeta):
    @abstractmethod
    def operation(self, objects:list)->Any:
        pass
        

class Add(Operator):

    remove_element = [0]

    def __add__(self, other):
        if isinstance(other, Add) and other._latex_label is None and self._latex_label is None:
            self.children += other.children
        elif isinstance(other, Expression) and (other._latex_label is not None or self._latex_label is not None):
            return Add([self, other])
        else:
            self.children.append(other)
        return self

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            str_repr += t.__repr__() + ' + '
        return str_repr[:-3]

    def __make_latex__(self):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Mul):
                latex_str = _latex_repr(t)
                if latex_str[0] == '-':
                    str_repr = str_repr[:-3]
                str_repr += _latex_repr(t) + ' + '
            elif isinstance(t, Expression):
                str_repr += _latex_repr(t) + ' + '
            else:
                if t < 0:
                    str_repr = str_repr[:-3]
                str_repr += str(t) + ' + '

        return str_repr[:-3]

    def operation(self, objects:list):
        return sum(objects)


class Mul(Operator):
    def __mul__(self, other):
        if isinstance(other, Mul):
            self.children += other.children
        else:
            self.children.append(other)
        return self

    def __repr__(self):
        return self.__str_repr__('__repr__')

    def __make_latex__(self):
        latex_str = ""
        coeffs = 1.0
        for child in self.children:
            if isinstance(child, Expression):
                latex_str += _latex_repr(child)
            else:
                coeffs *= child
        if coeffs == -1.0:
            latex_str = '-' + latex_str
        elif coeffs != 1.0:
            latex_str = str(coeffs) + latex_str
        return latex_str

    def __str_repr__(self, func_name):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Add) and len(t.children) > 1:
                str_repr += '({})'.format(eval('t.{}()'.format(func_name)))
            elif isinstance(t, (int, float)):
                str_repr += '{}'.format(str(t))
            else:
                str_repr += t.__repr__()
        return str_repr

    def operation(self, objects: list):
        term = 1
        for obj in objects:
            term *= obj
        return term

class Div(Operator):
    def __init__(self, children: list):
        # TODO: raise error when divide zero
        # self.children = [numerator, denominator]
        super().__init__(children)

    def __repr__(self):
        return self.__str_repr__('__repr__')

    def __make_latex__(self):

        # The parentheses don't look good in fractions, so I'll remove them.
        latex0 = _latex_repr(self.children[0], with_brakets=False)
        latex1 = _latex_repr(self.children[1], with_brakets=False)
        return "\\frac{{ {} }}{{ {} }}".format(latex0, latex1)

    def __str_repr__(self, func_name):
        str_repr = ""
        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '({})'.format(eval("t.{}()".format(func_name)))
            if isinstance(t, (int, float)):
                return '{}'.format(str(t))
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '/' + get_str(self.children[1])
        return str_repr

    def operation(self, objects):
        return objects[0]/objects[1]

class Power(Operator):
    @property
    def base(self):
        return self.children[0]

    @property
    def exponent(self):
        return self.children[1]

    def operation(self, objects: list):
        return objects[0]**objects[1] 

    def __repr__(self) -> str:
        return str(self.base) + '^' + str(self.exponent)

    def __make_latex__(self):
        from jijmodeling.expression.sum import Sum
        base_str = _latex_repr(self.base, forced_brakets=isinstance(self.base, Sum))
        exp_str = _latex_repr(self.exponent)
        return base_str + '^' + exp_str


class Mod(Operator):
    def __repr__(self):
        str_repr = ""
        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '(%s)' % t.__repr__()
            if isinstance(t, (int, float)):
                return '{}'.format(t.__repr__())
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '%' + get_str(self.children[1])
        return str_repr

    def __make_latex__(self):
        str_repr = ""
        str_repr = _latex_repr(self.children[0]) 
        str_repr += '\\bmod ' + _latex_repr(self.children[1])
        return str_repr

    def operation(self, objects: list) -> Any:
        return objects[0]%objects[1]


def _latex_repr(term, with_brakets=True, forced_brakets=False):

    if isinstance(term, Expression) and term._latex_label is not None:
        with_brakets = False


    if (isinstance(term, Operator) and with_brakets) or forced_brakets:
        from jijmodeling.expression.mathfuncs import Log, Absolute
        if isinstance(term, (Log, Absolute, Mul, Div)) and not forced_brakets:
            return term.__latex__()
        bra, ket = '\left(', '\\right)'
        return bra + term.__latex__() + ket
    elif isinstance(term, Expression):
        exp_str =  term.__latex__()
        if exp_str[0] == ':':
            return 'i_{{' + exp_str[1:] + '}}'
        return exp_str
    else:
        exp_str = str(term)
        if exp_str[0] == ':':
            return 'i_{{' + exp_str[1:] + '}}'
        return exp_str
