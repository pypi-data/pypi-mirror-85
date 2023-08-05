"""
A module for utility functions and data structures for the genetic sub-package
"""
from typing import List, Tuple, Any, Callable

import numpy as np

from hetrob.pledge import Pledge, HeterogeneousGraphPledge, WindowedPrecedencePledge


# UTILITY FUNCTIONS
# -----------------


def iterate_path(route: List[int]):
    return zip(route, np.roll(route, -1))


# DATA STRUCTURES
# ---------------


class StatefulQueue:

    def __init__(self, element_id: Callable = lambda x: x):
        self.get_id = element_id

        self.elements = []
        self.state = []

    def add(self, element: Any):
        self.elements.append(element)

        element_id = self.get_id(element)
        self.state.append(element_id)

    def pop(self) -> Any:
        element = self.elements.pop(0)
        self.state.pop(0)

        return element

    def empty(self) -> bool:
        return len(self.elements) == 0

    def __hash__(self):
        return hash(str(sorted(self.state)))

    def __len__(self):
        return len(self.elements)
