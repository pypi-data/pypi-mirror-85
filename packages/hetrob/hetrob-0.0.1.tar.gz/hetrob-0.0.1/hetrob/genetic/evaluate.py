from typing import Any, List, Sequence, Tuple, Callable,Optional
from abc import ABC, abstractmethod


# INTERFACES
# ==========

class SingleObjective(ABC):

    def __init__(self):
        self.value: Optional[float] = None

    def __call__(self, individual) -> float:
        return self.evaluate(individual)

    @abstractmethod
    def evaluate(self, individual) -> float:
        raise NotImplementedError()


class MultiObjective(ABC):

    def __int__(self):
        self.values: Optional[List[float]] = None

    def __call__(self, individual) -> List[float]:
        return self.evaluate(individual)

    @abstractmethod
    def evaluate(self, individual) -> List[float]:
        raise NotImplementedError()


# ACTUAL IMPLEMENTATIONS
# ======================


class WeightedSumObjective(SingleObjective):

    def __init__(self, terms: List[Tuple[Callable, float]]):
        SingleObjective.__init__(self)
        self.terms = terms

    def evaluate(self, individual) -> float:
        values = []
        for objective, weight in self.terms:
            values.append(weight * objective(individual))

        return sum(values)


class SumEdgeWeightObjective(SingleObjective):

    def __init__(self):
        SingleObjective.__init__(self)

    def evaluate(self, individual) -> float:
        value = 0
        for edge in individual.edges:
            value += edge['weight']

        return value


class SumWaitingTimeObjective(SingleObjective):

    def __init__(self):
        SingleObjective.__init__(self)

    def evaluate(self, individual):
        value = 0
        for node in individual.nodes.values():
            wait_time = node['waiting']
            if wait_time:
                value += wait_time

        return value


class AbsoluteEndTimeObjective(SingleObjective):
    """
    This class represents the calculation of the "absolute end time" objective.
    It is a child class of the SingleObjective abstract base class.

    To use this objective function on a phenotype, the phenotype class must implement a "nodes" property. This property
    has to be a dict object. The keys of this dict are the ids for every node which is part of the solution. The values
    to these keys are again dicts. All of these value dicts have to implement a key called "schedule", which contains
    a tuple for the start and end time of that specific node. The first value has to be the start time and the second
    value the end time.

    An example of this data structure can be represented as a JSON format:

    .. code-block::json

        {
            0: {
                'schedule': [0.0, 0.0]
            },
            1: {
                'schedule': [1.8, 2.1]
            },
            2: {
                'schedule': [2.76, 3.9]
            }
            # ...
        }

    This data structure is used to compute the maximum over all the operations end times, resulting in the *overall*
    end time of all operations associated with the subject solution.

    The following example shows how an instance of this object can be used to calculate the objective value
    for a given phenotype object.

    .. code-block::python

        phenotype = MockPhenotype()

        objective = AbsoluteEndTimeObjective()
        objective_value = objective.evaluate(phenotype)
    """
    def __init__(self):
        SingleObjective.__init__(self)

    def evaluate(self, individual) -> float:
        end_times = []
        for node in individual.nodes.values():
            if node['schedule'] is not None:
                end_time = node['schedule'][1]
                end_times.append(end_time)

        return max(end_times)


class InfeasibilityPenalty(SingleObjective):

    def __init__(self, objective: SingleObjective, penalty: float):
        SingleObjective.__init__(self)
        self.objective = objective
        self.penalty = penalty

    def evaluate(self, individual) -> float:
        if individual.feasible:
            return self.objective(individual)
        else:
            return self.penalty + individual.get_penalty()
