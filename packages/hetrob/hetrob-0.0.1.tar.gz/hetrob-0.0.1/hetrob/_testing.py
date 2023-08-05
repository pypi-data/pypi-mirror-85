"""
A module, which contains necessary utility for the testing of the project
"""
# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations

from typing import Tuple, Type
import random

from hetrob.util import JsonMixin, AbstractTerminationCondition
from hetrob.problem import AbstractProblem
from hetrob.solution import AbstractSolution
from hetrob.result import AlgorithmResult

class MockProblem(AbstractProblem):

    def __init__(self):
        AbstractProblem.__init__(self)
        JsonMixin.__init__(self)

    # IMPLEMENT "JsonMixin"
    # ---------------------

    def get_import(self) -> Tuple[str, str]:
        return 'hetrob._testing', 'MockProblem'

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> MockProblem:
        return cls()


class MockSolution(AbstractSolution):

    def __init__(self, problem: AbstractProblem):
        AbstractSolution.__init__(self)
        JsonMixin.__init__(self)

        self.problem = problem
        self.feasible = bool(random.randint(0, 1))

    # IMPLEMENT "AbstractSolution"
    # ----------------------------

    def evaluate(self) -> float:
        return random.randint(10, 1000)

    def is_feasible(self) -> bool:
        return self.feasible

    def get_penalty(self) -> float:
        if self.is_feasible():
            return 0
        else:
            return random.randint(10, 1000)

    @classmethod
    def construct(cls, problem: AbstractProblem) -> MockSolution:
        return cls(problem)

    # IMPLEMENT "JsonMixin"
    # ---------------------

    def get_import(self) -> Tuple[str, str]:
        return 'hetrob._testing', 'MockSolution'

    def to_dict(self) -> dict:
        return {
            'problem': self.problem
        }

    @classmethod
    def from_dict(cls, data: dict) -> MockSolution:
        return cls(data['problem'])


def solve_mock(solution_class: Type[AbstractSolution],
               problem: AbstractProblem,
               termination: AbstractTerminationCondition) -> AlgorithmResult:
    solution = solution_class.construct(problem)
    iterations = random.randint(10, 200)
    return AlgorithmResult(
        problem=problem,
        solution=solution,
        termination=termination,
        logbook={},
        fitness=solution.evaluate(),
        time=iterations * 10,
        iterations=iterations,
        feasible=solution.is_feasible()
    )
