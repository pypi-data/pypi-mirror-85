from abc import ABC, abstractmethod
from typing import Callable

import numpy as np


class DynamicTemperatureProgression(ABC):

    @abstractmethod
    def get(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def update(self, fitness: float):
        raise NotImplementedError()


class ExponentialTemperatureProgression(DynamicTemperatureProgression):

    def __init__(self, initial: float, alpha: float, limit: float = 10):
        self.alpha = alpha
        self.initial = initial
        self.temperature = initial
        self.limit = limit

    def get(self) -> float:
        return max(self.temperature, self.limit)

    def update(self, fitness: float):
        self.temperature *= self.alpha


class AutomaticReheatingProgression(DynamicTemperatureProgression):

    def __init__(self,
                 initial: float,
                 alpha: float,
                 reheat: Callable = lambda p: np.std(p[-10:]) < 10,
                 heat: float = 100,
                 limit: float = 1):
        self.initial = initial
        self.alpha = alpha
        self.reheat = reheat
        self.heat = heat
        self.limit = limit

        self.temperature = initial
        self.fitnesses = []

    def get(self) -> float:
        return max(self.temperature, self.limit)

    def update(self, fitness: float):
        self.fitnesses.append(fitness)
        if self.reheat(self.fitnesses):
            self.temperature = self.heat
        else:
            self.temperature *= self.alpha
