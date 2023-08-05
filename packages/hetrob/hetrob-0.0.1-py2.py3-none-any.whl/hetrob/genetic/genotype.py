import random
import copy
from abc import ABC, abstractmethod, abstractclassmethod
from typing import List, Type, Any

from hetrob.util import two_point_insert, two_point_reverse, two_point_swap
from hetrob.util import random_indices, random_pop

# INTERFACES
# ==========


class ChromosomeInterface(ABC):

    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def decode(self) -> List[List[int]]:
        raise NotImplementedError()

    @abstractmethod
    def crossover(self, other):
        raise NotImplementedError()

    @abstractmethod
    def mutate(self):
        raise NotImplementedError()

    @classmethod
    def random(cls, problem):
        raise NotImplementedError()


class AbstractGenotype(ABC):

    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def decode(self) -> List[List[int]]:
        raise NotImplementedError()

    @abstractmethod
    def crossover(self, other):
        raise NotImplementedError()

    @abstractmethod
    def mutate(self):
        raise NotImplementedError()

    @abstractmethod
    def args(self) -> List[Any]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def random(cls, problem):
        raise NotImplementedError()


# HELPER FUNCTIONS
# ================


# SPECIFIC CHROMOSOME IMPLEMENTATIONS
# ===================================

class RoutesChromosome(ChromosomeInterface):

    def __init__(self, problem, routes):
        ChromosomeInterface.__init__(self, problem)

        self.routes = routes

    def decode(self) -> List[List[int]]:
      return self.routes

    @classmethod
    def random(cls, problem):
        amount = int(problem.N / problem.M)
        nodes = copy.deepcopy(problem.nodes)[:-1]
        random.shuffle(nodes)

        routes = []
        for vehicle in problem.vehicles:
            route = []
            for i in range(amount):
                route.append(nodes.pop(0))
            routes.append(route)

        return cls(problem, routes)


    def crossover(self, other):
        pass

    def mutate(self):
        pass


class EntezariMahootchiChromosome(AbstractGenotype):

    def __init__(self, problem, assignments: List[int], schedule: List[int]):
        AbstractGenotype.__init__(self, problem)

        self.assignments = assignments
        self.schedule = schedule

    # PUBLIC METHODS
    # --------------

    # ChromosomeInterface

    def decode(self) -> List[List[int]]:
        vehicles = self.problem.get_vehicles()
        # Initializing an empty list(route) for every vehicle
        routes = [[] for _ in vehicles]

        for index, node in enumerate(self.schedule):
            vehicle = self.assignments[node]
            routes[vehicle].append(node)

        return routes

    def crossover(self, other):
        assignments1, assignments2 = self.crossover_assignments(other)
        schedule1, schedule2 = self.crossover_schedule(other)

        return (
            self.__class__(self.problem, assignments1, schedule1),
            self.__class__(self.problem, assignments2, schedule2)
        )

    def crossover_assignments(self, other):
        mask = [random.randint(0, 1) for _ in self.assignments]

        assignments1 = copy.deepcopy(self.assignments)
        assignments2 = copy.deepcopy(other.assignments)

        for index, switch in enumerate(mask):
            if switch:
                assignments1[index], assignments2[index] = assignments2[index], assignments1[index]

        return assignments1, assignments2

    def crossover_schedule(self, other):
        schedule1 = copy.deepcopy(self.schedule)
        schedule2 = copy.deepcopy(other.schedule)

        index, = random_indices(schedule1, k=1)

        front1 = set(schedule1[:index])
        front2 = set(schedule2[:index])

        index1 = index
        for i, value in enumerate(schedule2):
            if value not in front1:
                schedule1[index1] = value
                index1 += 1

        index2 = index
        for j, value in enumerate(schedule1):
            if value not in front2:
                schedule2[index2] = value
                index2 += 1

        return schedule1, schedule2

    def mutate(self):
        assignments = self.mutate_assignments()
        schedule = self.mutate_schedule()

        result = self.__class__(self.problem, assignments, schedule)
        return result

    def mutate_assignments(self):
        assignments = copy.deepcopy(self.assignments)
        index, = random_indices(assignments, k=1)

        qualified_vehicles = self.problem.qualified_vehicles
        assignments[index] = random.choice(qualified_vehicles[index])
        return assignments

    def mutate_schedule(self):
        schedule = copy.deepcopy(self.schedule)
        operators = [
            two_point_reverse,
            two_point_swap,
            two_point_insert
        ]

        operator = random.choice(operators)
        schedule = operator(schedule)

        return schedule

    @classmethod
    def random(cls, problem):
        assignments = []
        for node, qualified in enumerate(problem.qualified_vehicles[1:]):
            vehicle = random.choice(qualified)
            assignments.append(vehicle)

        schedule = list(range(len(problem) - 1))
        random.shuffle(schedule)

        return cls(problem, assignments, schedule)


class EntezariMahootchiGenotype(AbstractGenotype):

    def __init__(self, problem, assignments: List[int], schedule: List[int]):
        AbstractGenotype.__init__(self, problem)

        self.assignments = assignments
        self.schedule = schedule

    # PUBLIC METHODS
    # --------------

    # AbstractGenotype

    def decode(self) -> List[List[int]]:
        vehicles = self.problem.get_vehicles()
        # Initializing an empty list(route) for every vehicle
        routes = [[] for _ in vehicles]

        for index, node in enumerate(self.schedule):
            vehicle = self.assignments[node]
            routes[vehicle].append(node)

        return routes

    @classmethod
    def encode(cls, problem, routes: List[List[int]]):

        nodes = set()
        for route in routes:
            for node_id in route:
                nodes.add(node_id)

        schedule = []
        assignments = [0 for _ in nodes]

        for vehicle_id, route in enumerate(routes):
            for node_id in route:
                assignments[node_id - 1] = vehicle_id
                schedule.append(node_id - 1)

        return cls(problem, assignments, schedule)

    def crossover(self, other):
        assignments1, assignments2 = self.crossover_assignments(other)
        schedule1, schedule2 = self.crossover_schedule(other)

        return (
            self.__class__(self.problem, assignments1, schedule1),
            self.__class__(self.problem, assignments2, schedule2)
        )

    def crossover_assignments(self, other):
        mask = [random.randint(0, 1) for _ in self.assignments]

        assignments1 = copy.deepcopy(self.assignments)
        assignments2 = copy.deepcopy(other.assignments)

        for index, switch in enumerate(mask):
            if switch:
                assignments1[index], assignments2[index] = assignments2[index], assignments1[index]

        return assignments1, assignments2

    def crossover_schedule(self, other):
        schedule1 = copy.deepcopy(self.schedule)
        schedule2 = copy.deepcopy(other.schedule)

        index, = random_indices(schedule1, k=1)

        front1 = set(schedule1[:index])
        front2 = set(schedule2[:index])

        index1 = index
        for i, value in enumerate(schedule2):
            if value not in front1:
                schedule1[index1] = value
                index1 += 1

        index2 = index
        for j, value in enumerate(schedule1):
            if value not in front2:
                schedule2[index2] = value
                index2 += 1

        return schedule1, schedule2

    def mutate(self):
        assignments = self.mutate_assignments()
        schedule = self.mutate_schedule()

        result = self.__class__(self.problem, assignments, schedule)
        return result

    def mutate_assignments(self):
        assignments = copy.deepcopy(self.assignments)
        index, = random_indices(assignments, k=1)

        qualified_vehicles = self.problem.qualified_vehicles
        assignments[index] = random.choice(qualified_vehicles[index + 1])
        return assignments

    def mutate_schedule(self):
        schedule = copy.deepcopy(self.schedule)
        operators = [
            two_point_reverse,
            two_point_swap,
            two_point_insert
        ]

        operator = random.choice(operators)
        schedule = operator(schedule)

        return schedule

    def args(self):
        return [
            self.assignments,
            self.schedule
        ]

    @classmethod
    def random(cls, problem):
        assignments = []
        for node, qualified in enumerate(problem.qualified_vehicles[1:]):
            vehicle = random.choice(qualified)
            assignments.append(vehicle)

        schedule = list(range(len(problem) - 1))
        random.shuffle(schedule)

        return cls(problem, assignments, schedule)


class RoutesGenotype(AbstractGenotype):

    def __init__(self, problem, routes: List[List[int]]):
        AbstractGenotype.__init__(self, problem)

        self.routes = routes

    def decode(self) -> List[List[int]]:
        return self.routes

    def mutate(self):
        routes = copy.deepcopy(self.routes)
        i, j = random_indices(routes, 2)
        if len(routes[i]) != 0 and len(routes[j]) != 0:
            k, = random_indices(routes[i], 1)
            h, = random_indices(routes[j], 1)
            routes[i][k], routes[j][h] = routes[j][h], routes[i][k]

        return self.__class__(self.problem, routes)

    def crossover(self, other):
        routes1 = copy.deepcopy(self.routes)
        routes2 = copy.deepcopy(other.routes)

        return (
            self.__class__(self.problem, routes1),
            self.__class__(self.problem, routes2)
        )

    def args(self) -> List[Any]:
        return [
            self.routes
        ]

    @classmethod
    def random(cls, problem):
        routes = [[] for _ in problem.get_vehicles()]
        nodes = list(range(problem.get_node_count()))

        index = 0
        while len(nodes) != 0:
            routes[index].append(random_pop(nodes))
            index = 0 if index == len(routes) - 1 else index + 1

        return cls(problem, routes)
