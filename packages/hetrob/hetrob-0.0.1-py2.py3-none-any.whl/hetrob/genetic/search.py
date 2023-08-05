import random
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple, Optional
from collections import deque

import numpy as np

from hetrob.solution import AbstractSolution


class AbstractGeneticSearch(ABC):

    @abstractmethod
    def select(self, pop: List[AbstractSolution]) -> Tuple[List[AbstractSolution], List[AbstractSolution]]:
        raise NotImplementedError()

    @abstractmethod
    def improve(self, solution: AbstractSolution) -> AbstractSolution:
        raise NotImplementedError()


class ModularGeneticSearch(AbstractGeneticSearch):

    def __init__(self,
                 selection: Callable,
                 improvement: Callable):
        self.selection = selection
        self.improvement = improvement

    def select(self, pop: List[AbstractSolution]) -> Tuple[List[AbstractSolution], List[AbstractSolution]]:
        return self.selection(pop)

    def improve(self, solution: AbstractSolution) -> AbstractSolution:
        return self.improvement(solution)


class NoGeneticSearch(AbstractGeneticSearch):

    def select(self, pop: List[AbstractSolution]) -> Tuple[List[AbstractSolution], List[AbstractSolution]]:
        return pop, []

    def improve(self, solution: AbstractSolution) -> AbstractSolution:
        return solution


class RandomSelect:

    def __init__(self, k: int):
        self.k = k

    def __call__(self, pop):
        pop_size = len(pop)
        random.shuffle(pop)
        return pop[0:pop_size - self.k], pop[pop_size - self.k:]


class BestSelect:

    def __init__(self, k: int):
        self.k = k

    def __call__(self, pop):
        pop_size = len(pop)
        pop.sort(key=lambda ind: -ind.evaluate())

        return pop[0:pop_size - self.k], pop[pop_size - self.k:]


class StaticVariableNeighborhoodImprovement:

    def __init__(self, neighborhoods: List[Callable], max_iterations: int):
        self.neighborhoods = neighborhoods
        self.max_iterations = max_iterations

        self.max_index = len(self.neighborhoods) - 1
        self.index = 0

    def __call__(self, solution: AbstractSolution) -> AbstractSolution:
        neighborhood = self.neighborhoods[self.index]
        for i in range(self.max_iterations):
            new_solution = neighborhood(solution)
            if new_solution.evaluate() < solution.evaluate():
                self.update()
                return new_solution

        self.update()
        return solution

    def update(self):
        if self.index == self.max_index:
            self.index = 0
        else:
            self.index += 1


class AdaptiveVariableNeighborhoodImprovement:

    def __init__(self,
                 neighborhoods: List[Callable],
                 max_iterations: int,
                 memory_size: 200,
                 map_weight: Callable = lambda w: w,
                 initial_weights: Optional[List[float]] = None):
        self.neighborhoods = neighborhoods
        self.max_iterations = max_iterations
        self.memory_size = memory_size
        self.map_weight = map_weight

        self.memory = [deque(maxlen=self.memory_size)] * len(self.neighborhoods)
        self.weights = initial_weights if initial_weights is not None else [5000] * len(self.neighborhoods)
        self.indices = list(range(len(self.neighborhoods)))

    def __call__(self, solution: AbstractSolution) -> AbstractSolution:
        index, = random.choices(self.indices, weights=map(self.map_weight, self.weights))
        neighborhood = self.neighborhoods[index]

        result = solution
        iterations = 1
        for i in range(self.max_iterations):
            new_solution = neighborhood(solution)
            if new_solution.evaluate() < solution.evaluate():
                result = new_solution
                break
            iterations += 1

        # Updating the weight of this operator
        improvement = solution.evaluate() - result.evaluate()
        self.memory[index].append(improvement)
        weight = np.mean(self.memory[index])
        self.weights[index] = weight if weight != 0 else 0.1

        return result
