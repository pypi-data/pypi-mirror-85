import time
import copy
from typing import Type, Any, TypeVar, Optional
from pprint import pprint

import numpy as np
from deap import tools

from hetrob.util import AbstractTerminationCondition
from hetrob.problem import ProblemType
from hetrob.solution import AbstractSolution

from hetrob.annealing.temperature import DynamicTemperatureProgression
from hetrob.annealing.improvement import ImprovementStrategy
from hetrob.annealing.search import AnnealingSearchOperator


class AnnealingOperators:

    def __init__(self,
                 problem: ProblemType,
                 solution: Type[AbstractSolution],
                 search: AnnealingSearchOperator,
                 improvement: ImprovementStrategy):
        self.problem = problem
        self.solution = solution
        self.search = search
        self.improvement = improvement

    def generate(self):
        return self.solution.construct(self.problem)

    def improve(self, solution: AbstractSolution, temp: float):
        return self.improvement(self.search, solution, temp)


def solve_sa(operators: AnnealingOperators,
             temperature: DynamicTemperatureProgression,
             termination: AbstractTerminationCondition,
             initial: Optional[AbstractSolution] = None,
             hof_size: int = 1,
             verbose: bool = True):

    # Setting up logging
    logbook = tools.Logbook()
    logbook.header = ['iter', 'time', 'temp', 'feasible', 'min']

    hof = tools.HallOfFame(hof_size)

    termination_condition = copy.deepcopy(termination)

    # Initial solution
    # if an initial solution is provided as an argument, the this solution is chosen. Otherwise a random solution will
    # be generated.
    current_solution: AbstractSolution = initial if initial is not None else operators.generate()

    start_time = time.time()
    computation_time = 0
    index = 0

    while not bool(termination_condition):
        current_temperature = temperature.get()

        current_solution = operators.improve(current_solution, current_temperature)
        hof.update([current_solution])

        logbook.record(
            iter=index,
            time=computation_time,
            temp=current_temperature,
            min=current_solution.evaluate(),
            feasible=current_solution.is_feasible()
        )

        if verbose:
            print(logbook.stream)

        # Updating the loop state
        temperature.update(current_solution.evaluate())
        computation_time = time.time() - start_time
        index += 1
        termination_condition.update(index, computation_time, hof[0].evaluate())

    return {
        # Expected returns
        'problem':          operators.problem,
        'solution':         hof[0],
        'fitness':          hof[0].evaluate(),
        'logbook':          logbook,
        'time':             computation_time,
        'termination':      termination,
        # Simulated Annealing specific optional returns
        'iterations':       index
    }
