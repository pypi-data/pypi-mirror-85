from abc import ABC, abstractmethod

from hetrob.solution import AbstractSolution


class AnnealingSearchOperator(ABC):

    @abstractmethod
    def __call__(self, solution: AbstractSolution) -> AbstractSolution:
        raise NotImplementedError()

