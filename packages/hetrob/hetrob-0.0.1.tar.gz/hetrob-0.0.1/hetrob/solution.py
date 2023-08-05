# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List

from hetrob.problem import AbstractProblem
from hetrob.util import JsonMixin


# ABSTRACT BASE CLASSES
# =====================

class AbstractSolution(JsonMixin, ABC):
    """
    This class represents the base class for any solution representation.

    At the very least any solution has to implement the following functionality as methods

    - **evaluate**: This is an instance method, which has to return a numeric metric for the "cost" of a solution.
    - **is_feasible**: This is an instance method, which has to return whether the solution configuration of that very
      instance is feasible or not.
    - **get_penalty**: This ties in with the concept of feasibility. This method can be used to generate an additional
      penalty if a solution is not feasible. This function should generally return 0 if the solution is feasible and
      a value bigger than zero for an infeasible solution. There are however no restrictions on the specific function
      which calculates this value.
    - **construct**: This is a class method, which is supposed to implement some sort of procedure, which constructs
      a solution from scratch. Note, that the created solution does NOT have to feasible and the construction process
      should also not be entirely deterministic, since this method is often used to create the initial solutions for
      population based procedures.
    """
    def __init__(self):
        JsonMixin.__init__(self)

    @abstractmethod
    def evaluate(self) -> float:
        """
        Supposed to return the calculated cost value for this solution

        :return: The cost value for this solution
        :rtype: float
        """
        raise NotImplementedError()

    @abstractmethod
    def is_feasible(self) -> bool:
        """
        Supposed to return whether or not this solution is feasible

        :return: Whether or not the solution is feasible
        :rtype: bool
        """
        raise NotImplementedError()

    @abstractmethod
    def get_penalty(self) -> float:
        """
        Supposed to return a penalty value in the case the solution is feasible. This penalty value will then be
        added to the cost to form "the actual cost".

        .. note::

            If the solution is feasible, this method should return 0. If it is not it should return a non 0 value

        :return: The feasibility penalty.
        :rtype: float
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def construct(cls, problem: AbstractProblem) -> AbstractSolution:
        """
        This method is supposed to construct a solution from scratch and return this solution.

        :param problem: The problem on which the solution should be based.
        :type problem: AbstractProblem

        :return: The constructed solution
        :rtype: AbstractSolution
        """
        raise NotImplementedError()


# INTERFACE CLASSES
# =================

class SolutionRoutesInterface:

    def get_routes(self) -> List[List[Any]]:
        raise NotImplementedError()

    def get_full_routes(self) -> List[List[Any]]:
        raise NotImplementedError()


class SolutionGraphMixin:

    def get_nodes(self) -> dict:
        raise NotImplementedError()

    def get_edges(self) -> List[dict]:
        raise NotImplementedError()


# MIXIN CLASSES
# =============

