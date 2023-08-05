import random
import copy
import time
from typing import Any, Type, Callable, Dict, List, Optional
from functools import partial
from pprint import pprint

import numpy as np

from deap import algorithms
from deap import base
from deap import tools

from hetrob.util import AbstractTerminationCondition
from hetrob.result import AlgorithmResult
from hetrob.genetic.solution import AbstractGeneticSolution
from hetrob.genetic.search import AbstractGeneticSearch

# CLASSES
# =======


class GeneticOperators:

    def __init__(self,
                 problem: Any,
                 genetic_solution_class: Type[AbstractGeneticSolution],
                 select_func: Callable = partial(tools.selTournament, tournsize=3)):
        self.problem = problem
        self.genetic_solution_class = genetic_solution_class
        self.select_func = select_func

    def select(self, individuals, k):
        return self.select_func(individuals, k)

    def generate(self):
        genotype_class = self.genetic_solution_class.get_genotype_class()
        genotype = genotype_class.random(self.problem)
        return self.genetic_solution_class.from_genotype(self.problem, genotype)

    def mutate(self, solution: AbstractGeneticSolution):
        mutated_genotype = solution.genotype.mutate()
        return self.genetic_solution_class.from_genotype(self.problem, mutated_genotype),

    def crossover(self, solution1: AbstractGeneticSolution, solution2: AbstractGeneticSolution):
        genotype1, genotype2 = solution2.genotype.crossover(solution1.genotype)
        child1 = self.genetic_solution_class.from_genotype(self.problem, genotype1)
        child2 = self.genetic_solution_class.from_genotype(self.problem, genotype2)

        return child1, child2

    def repair(self, solution: AbstractGeneticSolution):
        return solution

    def evaluate(self, solution: AbstractGeneticSolution):
        return solution.evaluate(),

    def feasible(self, solution: AbstractGeneticSolution):
        return solution.is_feasible()

    def penalized(self, solution: AbstractGeneticSolution):
        return solution.evaluate() + solution.get_penalty()


class MigrateNone:

    def __call__(self, population: List[Any], offspring: List[Any], gen: int) -> List[Any]:
        return offspring


class MigrateElite:

    def __init__(self, k: int):
        self.length = k

    def __call__(self, population: List[Any], offspring: List[Any], gen: int) -> List[Any]:
        population.sort(key=lambda ind: -ind.evaluate())

        result = offspring.copy()
        result.sort(key=lambda ind: -ind.evaluate())

        elite = population[len(population) - self.length:len(population)]
        result[0:self.length] = elite
        return result


class MigrateEliteProgression:

    def __init__(self, start: int, end: int, ngen: int):
        self.start = start
        self.end = end
        self.generations = ngen

        self.slope = (self.end - self.start) / self.generations

    def __call__(self, population: List[Any], offspring: List[Any], gen: int) -> List[Any]:
        length = self.length(gen)
        population.sort(key=lambda ind: ind.fitness)

        result = offspring.copy()
        result.sort(key=lambda ind: ind.fitness)

        result[0:length] = population[len(population) - length:len(population)]

        return result

    def length(self, gen):
        return int(self.start + self.start * self.slope * gen)


class ConstantParameterProgression:

    def __init__(self, value: float):
        self.value = value

    def __call__(self, gen):
        return self.value


class LinearParameterProgression:

    def __init__(self, start: float, end: float, ngen: int, cast: Type = float):
        self.start = start
        self.end = end
        self.generations = ngen + 1
        self.cast = cast

        self.slope = (end - start) / ngen

    def __call__(self, gen):
        value = self.start + self.start * self.slope * gen

        return self.cast(value)

# HELPER FUNCTIONS
# ================


def _setup_toolbox(genetic_operators: GeneticOperators) -> base.Toolbox:
    toolbox = base.Toolbox()

    toolbox.register('individual', genetic_operators.generate)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('evaluate', genetic_operators.evaluate)
    # toolbox.decorate('evaluate', tools.DeltaPenalty(genetic_operators.feasible, 0, genetic_operators.penalized))

    toolbox.register('select', genetic_operators.select)
    toolbox.register('mate', genetic_operators.crossover)
    toolbox.register('mutate', genetic_operators.mutate)

    return toolbox


def _setup_statistics(**additional_statistics):
    stats_fitness = tools.Statistics(lambda ind: ind.fitness.values)
    stats_fitness.register("avg", np.mean)
    stats_fitness.register("std", np.std)
    stats_fitness.register("min", np.min)
    stats_fitness.register("max", np.max)

    stats_general = tools.Statistics(lambda ind: ind)
    stats_general.register('feasible', _population_count_feasible)

    stats = tools.MultiStatistics(fitness=stats_fitness, general=stats_general, **additional_statistics)
    return stats


def _population_count_feasible(population):
    return sum([1 for ind in population if ind.is_feasible()])


def _var_and(population, toolbox, cxpb: Callable, mutpb: Callable, gen: int):
    offspring = [None] * len(population)

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb(gen):
            offspring[i - 1], offspring[i] = toolbox.mate(population[i - 1],
                                                          population[i])
        else:
            offspring[i - 1], offspring[i] = population[i - 1], population[i]
        del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb(gen):
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


# ACTUAL ALGORITHMS
# =================

def solve_ga(genetic_operators: GeneticOperators,
             termination: AbstractTerminationCondition,
             mutpb: float = 0.2,
             cxpb: float = 0.2,
             pop_size: int = 200,
             hof_size: int = 1,
             initials: List[AbstractGeneticSolution] = [],
             verbose: bool = True,
             additional_statistics: Dict[str, tools.Statistics] = {},
             **kwargs) -> AlgorithmResult:
    start_time = time.time()
    toolbox = _setup_toolbox(genetic_operators)

    stats = _setup_statistics(**additional_statistics)

    termination_condition = copy.deepcopy(termination)

    population = toolbox.population(pop_size - len(initials)) + initials
    hof = tools.HallOfFame(hof_size)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'time', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    hof.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(population), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    computation_time = 0
    gen = 1
    while not bool(termination_condition):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = _var_and(offspring, toolbox, lambda g: cxpb, lambda g: mutpb, gen)

        # Replace the current population by the offspring
        population[:] = offspring

        # Evaluate the individuals with an invalid fitness
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        hof.update(population)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(population), time=computation_time, **record)
        if verbose:
            print(logbook.stream)

        computation_time = time.time() - start_time
        gen += 1
        termination_condition.update(gen, computation_time, hof[0].evaluate())

    return AlgorithmResult(
        problem=genetic_operators.problem,
        solution=hof[0],
        fitness=hof[0].evaluate(),
        feasible=hof[0].is_feasible(),
        logbook=logbook,
        time=computation_time,
        termination=termination_condition,
        iterations=gen,
    )


def solve_ga_progression(genetic_operators: GeneticOperators,
                         migrate: Callable,
                         mutpb: Callable,
                         cxpb: Callable,
                         termination: AbstractTerminationCondition,
                         pop_size: int = 200,
                         hof_size: int = 1,
                         verbose: bool = True,
                         additional_statistics: Dict[str, tools.Statistics] = {},
                         repair_select: Optional[Callable] = None,
                         **kwargs) -> Dict[str, Any]:
    start_time = time.time()
    toolbox = _setup_toolbox(genetic_operators)

    stats = _setup_statistics(**additional_statistics)

    termination_condition = copy.deepcopy(termination)

    population = toolbox.population(pop_size)
    hof = tools.HallOfFame(hof_size)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'time', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hof.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    computation_time = 0
    gen = 1
    while not bool(termination_condition):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = _var_and(offspring, toolbox, cxpb, mutpb, gen)

        # Apply optional repair operator
        if repair_select is not None:
            unchanged, damaged = repair_select(gen, offspring)
            repaired = [genetic_operators.repair(ind) for ind in damaged]
            offspring = unchanged + repaired

        # Migrate some of the individuals from the old population to the new population
        offspring = migrate(population, offspring, gen)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        hof.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), time=computation_time, **record)
        if verbose:
            print(logbook.stream)

        computation_time = time.time() - start_time
        gen += 1
        termination_condition.update(gen, computation_time, hof[0].evaluate())

    return {
        # Expected returns
        'problem':              genetic_operators.problem,
        'solution':             hof[0],
        'fitness':              hof[0].evaluate(),
        'logbook':              logbook,
        'time':                 computation_time,
        'termination':          termination_condition,
        # Genetic algorithm specific optional return
        'generations':          gen
    }


def solve_ga_hybrid(genetic_operators: GeneticOperators,
                    migrate: Callable,
                    mutpb: Callable,
                    cxpb: Callable,
                    termination: AbstractTerminationCondition,
                    genetic_search: AbstractGeneticSearch,
                    pop_size: int = 200,
                    hof_size: int = 1,
                    initials: Optional[List[AbstractGeneticSolution]] = [],
                    verbose: bool = True,
                    additional_statistics: Dict[str, tools.Statistics] = {},
                    **kwargs) -> AlgorithmResult:
    start_time = time.time()
    toolbox = _setup_toolbox(genetic_operators)

    stats = _setup_statistics(**additional_statistics)

    termination_condition = copy.deepcopy(termination)

    population = toolbox.population(pop_size - len(initials)) + initials
    hof = tools.HallOfFame(hof_size)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'time', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    fitnesses = toolbox.map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    hof.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(population), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    computation_time = 0
    gen = 1
    while not bool(termination_condition):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = _var_and(offspring, toolbox, cxpb, mutpb, gen)

        # Apply local search to some individuals of the generation
        keep, modify = genetic_search.select(offspring)
        modified = [genetic_search.improve(ind) for ind in modify]
        offspring = keep + modified

        # Migrate some of the individuals from the old population to the new population
        offspring = migrate(population, offspring, gen)

        # Replace the current population by the offspring
        population[:] = offspring

        # Evaluate the individuals with an invalid fitness
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        hof.update(population)

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(population), time=computation_time, **record)
        if verbose:
            print(logbook.stream)

        computation_time = time.time() - start_time
        gen += 1
        termination_condition.update(gen, computation_time, hof[0].evaluate())

    result = AlgorithmResult(
        problem=genetic_operators.problem,
        solution=hof[0],
        fitness=hof[0].evaluate(),
        feasible=hof[0].is_feasible(),
        logbook=logbook,
        time=computation_time,
        termination=termination_condition,
        iterations=gen,
    )

    return result
