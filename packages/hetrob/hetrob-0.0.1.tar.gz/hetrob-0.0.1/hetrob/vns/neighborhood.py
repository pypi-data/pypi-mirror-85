import random
import copy
from abc import ABC, abstractmethod
from typing import List

from hetrob.solution import AbstractSolution
from hetrob.util import random_indices


class AbstractNeighborhoodPool:

    @abstractmethod
    def apply(self, solution: AbstractSolution) -> AbstractSolution:
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()


class LasfargeasNeighborhoodPool:

    def __init__(self):
        self.neighborhoods = [
            self.route_swap,
            self.inter_swap,
            self.inter_insert,
            self.intra_insert,
            self.intra_swap,
        ]

        self.max_iterations = 500

    def apply(self, solution: AbstractSolution) -> AbstractSolution:
        new_solution = self.refine(self.shake(solution))
        if new_solution.evaluate() < solution.evaluate():
            return new_solution
        else:
            return solution

    def shake(self, solution):
        operator = random.choice(self.neighborhoods[:-1])
        return operator(solution)

    def refine(self, solution):
        operator = self.neighborhoods[-1]
        current_solution = solution
        for i in range(self.max_iterations):
            new_solution = operator(current_solution)
            if new_solution.evaluate() < current_solution.evaluate():
                current_solution = new_solution

        return current_solution

    def update(self):
        random.shuffle(self.neighborhoods)

    def intra_insert(self, solution):
        routes = self._get_routes(solution)
        index, = random_indices(routes, 1)
        if len(routes[index]) >= 2:
            i, j = random_indices(routes[index], 2, distinct=True)
            routes[index].insert(i, routes[index].pop(j))

        return self._create_solution(solution, routes)

    def inter_insert(self, solution):
        routes = self._get_routes(solution)
        i, j = random_indices(routes, 2, distinct=True)
        if len(routes[i]) >= 1 and len(routes[j]) >= 1:
            k, = random_indices(routes[i], 1)
            h, = random_indices(routes[j], 1)

            routes[i].insert(k, routes[j].pop(h))

        return self._create_solution(solution, routes)

    def intra_swap(self, solution):
        routes = self._get_routes(solution)
        index, = random_indices(routes, 1)
        if len(routes[index]) >= 2:
            i, j = random_indices(routes[index], 2, distinct=True)
            routes[index][i], routes[index][j] = routes[index][j], routes[index][i]

        return self._create_solution(solution, routes)

    def inter_swap(self, solution):
        routes = self._get_routes(solution)
        i, j = random_indices(routes, 2, distinct=True)
        if len(routes[i]) >= 1 and len(routes[j]) >= 1:
            k, = random_indices(routes[i], 1)
            h, = random_indices(routes[j], 1)

            routes[i][k], routes[j][h] = routes[j][h], routes[i][k]

        return self._create_solution(solution, routes)

    def route_swap(self, solution):
        routes = self._get_routes(solution)
        i, j = random_indices(routes, 2, distinct=True)
        routes[i], routes[j] = routes[j], routes[i]

        return self._create_solution(solution, routes)

    def _get_routes(self, solution) -> List[List[int]]:
        return copy.deepcopy(solution.genotype.routes)

    def _create_solution(self, solution, routes):
        return solution.__class__(solution.problem, routes)
