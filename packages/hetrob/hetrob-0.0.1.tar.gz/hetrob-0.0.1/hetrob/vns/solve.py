import time
import copy
from typing import Any, Type, Optional

from deap import tools

from hetrob.problem import ProblemType
from hetrob.solution import AbstractSolution
from hetrob.util import AbstractTerminationCondition

from hetrob.vns.neighborhood import AbstractNeighborhoodPool


class VNSOperators:

    def __init__(self,
                 problem: ProblemType,
                 solution_class: Type[AbstractSolution],
                 neighborhoods: AbstractNeighborhoodPool):
        self.problem = problem
        self.solution_class = solution_class
        self.neighborhoods = neighborhoods

    def generate(self) -> AbstractSolution:
        return self.solution_class.construct(self.problem)

    def improve(self, solution: AbstractSolution):
        result = self.neighborhoods.apply(solution)
        self.neighborhoods.update()
        return result


def solve_vns(operators: VNSOperators,
              termination: AbstractTerminationCondition,
              initial: Optional[AbstractSolution] = None,
              hof_size: int = 1,
              verbose: bool = True):
    # Setting up logging
    logbook = tools.Logbook()
    logbook.header = ['iter', 'time', 'feasible', 'min']

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

        current_solution = operators.improve(current_solution)
        hof.update([current_solution])

        logbook.record(
            iter=index,
            time=computation_time,
            min=current_solution.evaluate(),
            feasible=current_solution.is_feasible()
        )

        if verbose:
            print(logbook.stream)

        # Updating the loop state
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
        'termination':      termination_condition,
        # Simulated Annealing specific optional returns
        'iterations':       index
    }
