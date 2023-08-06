import sys
import openjij as oj
from jijmodeling.problem import Problem
from logging import INFO, getLogger, StreamHandler, Formatter
import time
import cpp_pyqubo
import numpy as np


logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('# %(message)s'))
logger.addHandler(handler)

class DecodedResult:
    def __init__(self, decoded: list, energies: list, timing: dict, info: dict, feed_dict={}) -> None:
        self.results = decoded
        self.timing = timing
        self.sampler_info = info
        self.energies = energies
        self.feed_dict = feed_dict

        self._analyzed = False
        self._feasibles = []
        self._lowest_cost = None
        self._costs = []
        self._penalties = {}

    def _analyzed_has_been_executed(self):
        if not self._analyzed:
            raise ValueError('Cannot get the value because `.analyze_results` method is not executed.')

    @property
    def feasibles(self):
        self._analyzed_has_been_executed()
        return self._feasibles
    
    @property
    def lowest_cost(self):
        self._analyzed_has_been_executed()
        return self._lowest_cost

    @property
    def costs(self):
        self._analyzed_has_been_executed()
        return self._costs

    @property
    def penalties(self):
        self._analyzed_has_been_executed()
        return self._penalties

    def analyze_results(self):
        if self._analyzed:
            return 
        self._analyzed = True

        feasible_solution = []
        lowest_cost = sys.float_info.max
        costs = []
        penalty = {key: [] for key in self.results[0]['penalty'].keys()}
        for sol in self.results:
            for key, pena in sol['penalty'].items():
                penalty[key].append(pena)
            costs.append(sol['cost'])
            pena_value = sum(pena for pena in sol['penalty'].values())
            if pena_value == 0.0:
                feasible_solution.append(sol)
                if sol['cost'] < lowest_cost:
                    lowest_cost = sol['cost']

        self._feasibles = feasible_solution
        self._lowest_cost = lowest_cost if lowest_cost < sys.float_info.max else None
        self._costs = costs
        self._penalties= penalty

    def __repr__(self) -> str:
        repr_str = "Store {} samples.".format(len(self.results))
        if not self._analyzed:
            repr_str += " `.analyze_results` has not been executed yet."
            return repr_str
        
        repr_str += "\n`.analyze_results` has been executed."
        repr_str += '\nThe number of feasible solutions: {}'.format(len(self.feasibles))
        repr_str += '\nThe lowest cost value: {:3e}'.format(self.lowest_cost)
        return repr_str


def solve_pyqubo(pyqubo_model: cpp_pyqubo.Model, problem: Problem, feed_dict={}, sampler=oj.SASampler(), sampler_args={}, decode_only_lowest=False, analyze_response=True, with_info=True):
    if with_info:
        logger.setLevel(INFO)
    logger.info('####################################################')
    logger.info('Infomation of the JijModeling `solve_pyqubo` method.')
    logger.info('Make Binary quadratic model from PyQUBO compiled object.')
    start = time.time()
    bqm = pyqubo_model.to_bqm(feed_dict=feed_dict)
    to_bqm_time = time.time() - start
    logger.info('\tThe execution time of `pyqubo_model.to_bqm` is {:.3e}[s]'.format(to_bqm_time))
    
    logger.info('Start sampling: `{}`'.format(sampler.__class__.__name__))
    start = time.time()
    response = sampler.sample(bqm, **sampler_args)
    exe_time = time.time() - start
    logger.info('\tTotal sampling time is {:.3e}[s]'.format(exe_time))
    logger.info('\tThe lowest energy: {:.3e}'.format(response.lowest().record[0][1]))
    

    logger.info('Start solution decoding')
    if decode_only_lowest:
        response = response.lowest()
        logger.info('\tdecode only lowest results.')
    start = time.time()
    decoded = problem.decode(response)
    decode_time = time.time() - start
    logger.info('\tThe decoding time is {:.3e}[s]'.format(decode_time))

    result = DecodedResult(
                decoded,
                energies=[r[1] for r in response.record],
                timing={
                    'pyqubo_to_bqm': to_bqm_time, 
                    'sampling': exe_time, 
                    'decode': decode_time}, 
                info=response.info,
                feed_dict=feed_dict
                )
    if analyze_response:
        result.analyze_results()
        logger.info('\tThe number of feasible solutions: {}'.format(len(result.feasibles)))
        if len(result.feasibles) > 0:
            logger.info('\tThe lowest cost value: {:3e}'.format(result.lowest_cost))
    else:
        logger.info('`DecodedResult.analyze_results` has not been executed yet.')
    logger.info('####################################################')


    return result



def solve_pulp(problem: Problem, placeholder: dict, fixed_variables: dict, solver=None, sense=1, with_info=False):
    import pulp
    pulp_model, variables = problem.to_pulp(placeholder=placeholder, fixed_variables=fixed_variables, sense=sense)
    if solver is None:
        status = pulp_model.solve(pulp.PULP_CBC_CMD(msg=1 if with_info else 0))
    else:
        status = pulp_model.solve(solver)


    npmat_value = np.frompyfunc(lambda v: v.value(), 1, 1)

    def decode_variable(v, label):
        if isinstance(v, np.ndarray):
            return npmat_value(v)
        else:
            value = v.value()
            if value is None:
                if label in fixed_variables:
                    return fixed_variables[label]
                else:
                    return np.nan
            return value

    start = time.time()
    decoded_result = {key: decode_variable(value, key)  for key, value in variables.items()}
    exe_time = time.time() - start


    cost = pulp_model.objective.value()
    result = DecodedResult([{'solution': decoded_result, 'cost': cost}], energies=[cost], timing={'exe_time': exe_time}, info={'status': pulp.LpStatus[status]})
    result._costs = [cost]
    result._feasibles = [decoded_result]
    result._lowest_cost = cost
    result._analyzed= True
    return result
    
