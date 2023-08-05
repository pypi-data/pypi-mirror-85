# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, ClassVar, Tuple

from hetrob.util import JsonMixin
from hetrob.problem import AbstractProblem
from hetrob.solution import AbstractSolution

from hetrob.genetic.genotype import AbstractGenotype
from hetrob.genetic.phenotype import AbstractPhenotype


def generate_genetic_solution(genotype_class,
                              phenotype_class) -> Type[AbstractGeneticSolution]:

    class TempGeneticSolution(AbstractGeneticSolution):

        @classmethod
        def get_genotype_class(cls) -> Type[AbstractGenotype]:
            return genotype_class

        @classmethod
        def get_phenotype_class(cls) -> Type[AbstractPhenotype]:
            return phenotype_class

        def get_import(self) -> Tuple[str, str]:
            return '', ''

        def to_dict(self) -> dict:
            return {}

        def from_dict(cls, data: dict) -> JsonMixin:
            return cls()

    return TempGeneticSolution



class AbstractGeneticSolution(AbstractSolution):

    def __init__(self, problem: AbstractProblem, *args):
        AbstractSolution.__init__(self)
        self.problem = problem
        self.args = args

        self.genotype_class = self.get_genotype_class()
        self.phenotype_class = self.get_phenotype_class()

        self.genotype: AbstractGenotype = self.genotype_class(self.problem, *args)
        self.phenotype: AbstractPhenotype = self.phenotype_class(self.problem, self.genotype)

    def evaluate(self) -> float:
        value = self.phenotype.evaluate()
        self.phenotype.fitness.values = value,
        return value

    def is_feasible(self) -> bool:
        return self.phenotype.is_feasible()

    def get_penalty(self) -> float:
        return self.phenotype.get_penalty()

    @property
    def fitness(self):
        return self.phenotype.fitness

    @classmethod
    def from_genotype(cls, problem: AbstractProblem, genotype: AbstractGenotype):
        return cls(problem, *genotype.args())

    @classmethod
    def construct(cls, problem: AbstractProblem):
        genotype_class = cls.get_genotype_class()
        genotype = genotype_class.random(problem)
        return cls.from_genotype(problem, genotype)

    # TO BE IMPLEMENTED
    # -----------------

    @classmethod
    @abstractmethod
    def get_phenotype_class(cls) -> Type[AbstractPhenotype]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_genotype_class(cls) -> Type[AbstractGenotype]:
        raise NotImplementedError()

    # IMPLEMENT "JsonMixin"
    # ---------------------

    def to_dict(self) -> dict:
        return {
            'problem': self.problem,
            'args': self.args
        }

    @classmethod
    def from_dict(cls, data: dict) -> JsonMixin:
        return cls(data['problem'], *data['args'])
