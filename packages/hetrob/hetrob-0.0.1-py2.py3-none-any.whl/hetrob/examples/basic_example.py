from pprint import pprint

from hetrob.problem import BasicProblem
from hetrob.util import MaxIterTermination

from hetrob.genetic.solution import generate_genetic_solution
from hetrob.genetic.genotype import RoutesGenotype
from hetrob.genetic.phenotype import BasicPhenotype
from hetrob.genetic.solve import solve_ga, GeneticOperators


if __name__ == '__main__':
    # 1. LOAD ACTUAL PROBLEM INSTANCE
    problem = BasicProblem(
        vehicle_count=2,
        coordinates=[
            (10, 10),
            (15, 16),
            (23, 89),
            (9, 0),
            (15, 34)
        ],
        duration=10
    )

    # 2. DEFINE THE WAY A GENETIC SOLUTION LOOKS LIKE
    GeneticSolution = generate_genetic_solution(RoutesGenotype, BasicPhenotype)

    # 3. USE ALGORITHM TO SOLVE THE PROBLEM
    genetic_operators = GeneticOperators(
        problem=problem,
        genetic_solution_class=GeneticSolution
    )

    algorithm_result = solve_ga(
        genetic_operators=genetic_operators,
        termination=MaxIterTermination(100),
        mutpb=0.8,
        cxpb=0.6,
        pop_size=100,
        verbose=True
    )

    # 4. VIEW THE RESULTS
    pprint(algorithm_result)

