from jijmodeling.variables.variable import Placeholder
from jijmodeling.expression.expression import Expression, Mul, _latex_repr
from jijmodeling.expression.from_serializable import from_serializable


class Penalty(Expression):
    def __init__(self, label:str, term, with_multiplier:bool=True):
        self.label = label
        self.penalty_term = term
        self.with_multiplier = with_multiplier
        if with_multiplier:
            # multiple placeholder (for the Lagrange multiplier)
            pl_mul = Placeholder(self.label)
            pl_mul.set_latex_label('\\lambda_{{\\mathrm{{{}}}}}'.format(self.label))
            child_term = Mul([pl_mul, term])
        else:
            child_term = term
        super().__init__([child_term])

    @classmethod
    def from_serializable(cls, serializable: dict):
        label = from_serializable(serializable['attributes']['label'])
        term = from_serializable(serializable['attributes']['children'])[0]
        with_multiplier = from_serializable(serializable['attributes']['with_multiplier'])
        return cls(label, term, with_multiplier)

    def __latex__(self):
        return _latex_repr(self.children[0], with_brakets=False)
        


class Constraint(Expression):
    def __init__(self, label: str, term, condition='==', constant=0, with_penalty: bool=True, with_mul: bool=True):
        self.label = label
        self.with_penalty = with_penalty
        self.with_mul = with_mul
        if with_penalty:
            penalty = Penalty(label, term, with_multiplier=with_mul)
            self._penalty = penalty
            super().__init__([penalty])
        else:
            self._penalty = None
            super().__init__([term])

        if not condition in ['==', '<=', '<']:
            raise ValueError('condition only support ==, <= or <')

        self.condition = condition
        self.constant = constant

    @property
    def penalty(self):
        return self._penalty


    @classmethod
    def from_serializable(cls, serializable: dict):
        label = from_serializable(serializable['attributes']['label'])
        term = from_serializable(serializable['attributes']['children'])[0]
        condition = from_serializable(serializable['attributes']['condition'])
        constant = from_serializable(serializable['attributes']['constant'])
        with_penalty = from_serializable(serializable['attributes']['with_penalty'])
        with_mul = from_serializable(serializable['attributes']['with_mul'])
        return cls(label, term, condition=condition, constant=constant, with_penalty=with_penalty, with_mul=with_mul)

    def __latex__(self):
        return _latex_repr(self.children[0])
