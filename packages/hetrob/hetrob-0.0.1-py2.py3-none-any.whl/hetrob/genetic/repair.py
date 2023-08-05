import random
from abc import ABC, abstractmethod
from typing import List, Tuple

from hetrob.solution import AbstractSolution


# ABSTRACT BASE CLASSES
# =====================

class AbstractRepairSelect(ABC):

    @abstractmethod
    def __call__(self,
                 gen: int,
                 offspring: List[AbstractSolution]) -> Tuple[List[AbstractSolution], List[AbstractSolution]]:
        raise NotImplementedError()


class AbstractRepairCondition(ABC):

    @abstractmethod
    def __call__(self,
                 gen: int,
                 offspring: List[AbstractSolution]) -> bool:
        raise NotImplementedError()


# REPAIR CONDITIONS
# =================

class InfeasiblePercentageRepairCondition(AbstractRepairCondition):

    def __init__(self, percentage: float):
        self.percentage = percentage

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        infeasible_count = sum(1 for ind in offspring if not ind.is_feasible())
        infeasible_percentage = infeasible_count / len(offspring)

        return infeasible_percentage > self.percentage


class FeasibleCountRepairCondition(AbstractRepairCondition):

    def __init__(self, max_feasible: int):
        self.min_count = max_feasible

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        feasible_count = sum(1 for ind in offspring if ind.is_feasible())

        return feasible_count < self.min_count


# REPAIR SELECT OPERATORS
# =======================

class ConditionalRepairSelect(AbstractRepairSelect):

    def __init__(self,
                 condition: AbstractRepairCondition,
                 select: AbstractRepairSelect):
        self.condition = condition
        self.select = select

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        if self.condition(gen, offspring):
            return self.select(gen, offspring)
        else:
            return offspring, []


class WorstRepairSelect(AbstractRepairSelect):

    def __init__(self, k: int):
        self.k = k

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        offspring.sort(key=lambda ind: ind.evaluate())
        # offspring.sort(key= lambda ind: ind)

        return offspring[0:len(offspring) - self.k], offspring[len(offspring) - self.k:]


class BestRepairSelect(AbstractRepairSelect):

    def __init__(self, k: int):
        self.k = k

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        offspring.sort(key=lambda ind: ind.evaluate())
        offspring.reverse()
        # offspring.sort(key= lambda ind: ind)

        return offspring[0:len(offspring) - self.k], offspring[len(offspring) - self.k:]


class RandomRepairSelect(AbstractRepairSelect):

    def __init__(self, k: int):
        self.k = k

    def __call__(self, gen: int, offspring: List[AbstractSolution]):
        random.shuffle(offspring)
        return offspring[0:len(offspring) - self.k], offspring[len(offspring) - self.k:]

