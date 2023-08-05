import math
import random
from functools import partial
from abc import ABC, abstractmethod
from typing import Callable


def exponential_acceptance(current, new, temp: float):
    current_fitness = current.evaluate()
    new_fitness = new.evaluate()
    return new_fitness < current_fitness or math.exp(- (new_fitness - current_fitness) / temp) > random.random()


class ImprovementStrategy(ABC):

    @abstractmethod
    def __call__(self, search, solution, temp):
        raise NotImplementedError()


class FirstImprovement(ImprovementStrategy):

    def __init__(self, max_iter: int = 100, accept: Callable = exponential_acceptance):
        self.max_iter = max_iter
        self.accept = accept

    def __call__(self, search, solution, temp):

        index = 0
        current_solution = solution
        while index < self.max_iter:
            current_solution = search(solution)

            if self.accept(solution, current_solution, temp):
                return current_solution

            index += 1

        return solution


class PooledImprovement(ImprovementStrategy):

    def __init__(self,
                 k: int = 100,
                 accept: Callable = exponential_acceptance,
                 choose: Callable = random.choice,
                 max_iter: int = 1000):
        self.pool_size = k
        self.accept = accept
        self.choose = choose
        self.max_iter = max_iter

    def __call__(self, search, solution, temp):
        pool = []
        index = 0
        while index < self.max_iter:
            current_solution = search(solution)

            if self.accept(solution, current_solution, temp):
                pool.append(current_solution)

            index += 1

        return solution if len(pool) == 0 else self.choose(pool)
