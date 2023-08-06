from jijmodeling.expression.expression import Add, Expression
from jijmodeling.extracte_vars import extracte_variables
from jijmodeling.transpilers.calc_value import calc_value
from jijmodeling.expression.constraint import Constraint
from jijmodeling.transpilers.to_pyqubo import to_pyqubo
from jijmodeling.transpilers.to_pulp import to_pulp
from jijmodeling.transpilers.decode_from_sampleset import decode_from_dict
from jijmodeling.transpilers.shape_check import variables_validation
from typing import TypeVar, Generic, List, Dict
import dimod

Var = TypeVar('T')

class Problem(Generic[Var]):
    def __init__(self, problem_name: str) -> None:
        self.obj_vars = {}
        self.placeholders = {}
        self.name = problem_name
        self.model = 0
        self.cost = 0
        self.constraints = {}

        self._placeholder = None
        self._fixed_variables = None

    def var(self, variable: Var)->Var:
        return variable

    
    def __repr__(self) -> str:
        return '{}: {}'.format(self.name, self.model)


    def __add__(self, other):
        if self.model == 0:
            self.model = other
        else:
            self.model += other

        if isinstance(other, Add):
            for child in other.children:
                if isinstance(child, Constraint):
                    self.constraints[child.label] = child
                else:
                    self.cost = child if self.cost == 0 else self.cost + child
        elif isinstance(other, Constraint):
            self.constraints[other.label] = other
        else:
            self.cost = other if self.cost == 0 else self.cost + other

        return self


    def to_pyqubo(self, index: dict={}, placeholder: dict={}, fixed_variables: dict={}):
        variables = extracte_variables(self.model)
        variables_validation(placeholder, variables)
        self._placeholder = placeholder
        self._fixed_variables = fixed_variables
        return to_pyqubo(self.model, placeholder=placeholder, fixed_variables=fixed_variables, index_values=index)

 
    def decode(self, response: dimod.SampleSet, placeholder: dict=None, fixed_variables: dict=None)->List[Dict[str, dict]]:
        """decode dimod.SampleSet object.

        Validation check for constraint conditions and decode by meta info of each term classes.

        Args:
            response (dimod.SampleSet): response from dimod.Sampler or openjij's sampler

        Returns:
            List[Dict[str, dict]]: {'solution': decoded solution (dict), 'penalty': value of each penalty (dict), 'cost': cost value without penalty term (float).}
        """

        if self._placeholder is None and self._fixed_variables is None:
            if placeholder is None:
                raise TypeError("decode() missing 1 required argument: 'placeholder'")
            if fixed_variables is None:
                raise TypeError("decode() missing 1 required argument: 'fixed_variables'")

            self._placeholder = placeholder
            self._fixed_variables = fixed_variables


        decoded = []
        variables = extracte_variables(self.model)
        # decode variables
        for sample in response.samples():
            vars_value = {}
            for var in variables['obj_vars'].values():
                vars_value.update(decode_from_dict(var, sample=dict(sample), placeholder=self._placeholder))
            
            # replace fixed variables
            for label, fixed_val in self._fixed_variables.items():
                if isinstance(fixed_val, dict):
                    for key, value in fixed_val.items():
                        vars_value[label][key] = value
                else: # scalar case
                    vars_value[label] = fixed_val

            # calculate constraint penalies
            penalty = self.calc_penalty(vars_value)

            # calculate cost (with out penalty term)
            cost = self.calc_cost(vars_value)

            decoded.append(
                {
                    'solution': vars_value, 
                    'penalty': penalty,
                    'cost': cost
                 }
            )

        return decoded

    def calc_penalty(self, solution):
        penalties = {}
        for k, const in self.constraints.items():
            penalties[k] = calc_value(const, decoded_sol=solution, placeholder=self._placeholder)
            if const.condition == '==' and penalties[k] == const.constant:
                penalties[k] = 0.0
            elif const.condition == '<=' and penalties[k] <= const.constant:
                penalties[k] = 0.0
            else:
                penalties[k] -= const.constant
        return penalties

    def calc_cost(self, solution):
        return calc_value(self.cost, decoded_sol=solution, placeholder=self._placeholder)


    def from_serializable(self, serializable: dict):
        import jijmodeling
        className = serializable['class'].split('.')[1:]
        cls = getattr(jijmodeling, className)
        return cls.from_serializable(serializable)


    def to_pulp(self, placeholder: dict={}, fixed_variables: dict={}, sense: int=1):
        self._placeholder = placeholder
        self._fixed_variables = fixed_variables
        objective, constraints, vars = to_pulp(self.model, placeholder=placeholder, fixed_variables=fixed_variables)

        import pulp
        problem = pulp.LpProblem(sense=sense)
        problem += objective
        for cons in constraints:
            problem += cons
        return problem, vars


    def _repr_latex_(self):
        opt_model = "$$\\begin{align}"
        opt_model += "\\min~&" + (self.cost.__latex__() if isinstance(self.cost, Expression) else str(self.cost))
        def condition_str(cond):
            if cond == '==': return '='
            elif cond == '<=': return '\\leq'
            elif cond == '<': return '<'
            else: return cond

        if len(self.constraints) > 0:
            opt_model += "\\\ \\mathrm{s.t.}~"
            for cons, term in self.constraints.items():
                opt_model += "&" + term.__latex__() +  condition_str(term.condition) + str(term.constant) + "\\\ "
            opt_model = opt_model[:-3] 
            opt_model += "\end{align}$$"
        return opt_model