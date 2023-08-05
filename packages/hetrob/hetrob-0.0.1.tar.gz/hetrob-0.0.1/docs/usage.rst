=====
Usage
=====

The basic use case of this library is intended to be the solving of problems concerning multi-robot coordination
and vehicle routing. A vehicle routing problem is a combinatorial problem, which is often encountered with physical
distribution process. The problem can be stated like this: There is usually a set of spacially distributed tasks
which have to be processed. Additionally there is a fleet of vehicles, where each vehicle is able to process one such
task at a time. The additional rules are, that every task *has to* be processed exactly once. This presents a
fundamental optimization process, where the optimal routes of the vehicles between the different tasks has to be
found.

An example for such a problem would be from the delivery industry. Say every task represents a package which has to
be delivered and the vehicles are delivery trucks. A company is now interested to find such a route which minimizes
the total needed time and the costs for truck fuel.

This library is now concerned with the previously described optimization problem. This generally involves the
generation of a solution for a specific problem.

Simple optimization with a genetic algorithm
--------------------------------------------

The following example contains the code to run the optimization of a basic vehicle routing problem instance using a
simple genetic algorithm. The code will be explained in more detail right after.

Before going into the code, here is a short description of which kind of vehicle routing problem will be considered
in this example: It is a very basic homogeneous vehicle routing problem with no additional constraints. There is a set
of tasks which have to be completed. Each of these tasks will be represented as two dimensional coordinates. Thus the
travel distance between two nodes will be symmetrical and equal to the euclidean distance between their coordinates.
Every node will have the same duration to be completed. The travel speed of every vehicle is implicitly assumed to be
one unit of distance per unit of time. A fix amount of vehicles is available to visit the nodes. For this problem the
default objective function of "absolute end time" is assumed. This will be the maximum end time over every last visit
of any vehicle.

.. code-block::python

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
        pprint(algorithm_result.to_dict())

The following steps are involved in this example program:

1. Every specific problem configuration is represented by a problem object in this library. These objects are created
   by using special problem classes. Every problem class has to be child class of `hetrob.problem.AbstractProblem`. In
   this case 2 vehicles are used for the problem and 4 tasks are being defined by their coordinate tuples. Note that the
   first coordinate tuple represents the location of the depot, from which all the vehicles start.
2. This second step mainly defines the inner workings of the genetic algorithm, which will be used to solve the problem.
   The genetic algorithm requires a class of the type `hetrob.genetic.solution.AbstractGeneticSolution` to work properly.
   In this case the function `generate_genetic_solution` dynamically creates a new class of this type. A genetic
   solution consists of two parts: The genotype and the phenotype. Each of those are again represented by classes. The
   genotype class is responsable of wrapping the basic representation of an individual solution. This representation of
   an individual is an important concept within genetic algorithms. On this genotypic representation, the variation
   operators of mutation and crossover are defined. The phenotype class mainly handles the evaluation of the quality of
   of a solution. It accepts a genotype representation and decodes all the important features from it. These features
   are for example whether the solution is feasible or not, or the float objective value which indicates the quality
   of the solution.
3. The `GeneticOperators` class is simply used to wrap the information for a single run of the genetic algorithm. It
   needs information about the specific problem instance which is to be solved, as well as the solution class (which
   defines the specifics of the actual operators to be used).
   The function `solve_ga` is the one actually executing the algorithm. It obviously needs the genetic operators object.
   It wraps information about the problem instance to be solved as well as the operators which actually make up the GA.
   Additionally the function accepts hyper parameters, which control the behaviour of the algorithm. In this case this
   includes the chances of mutation/crossover to be applied and the population size. The termination condition is
   controlled by `Termination` classes. In this case the algorithm will stop after 100 generations (=iterations of the
   evolutionary loop).
4. The result of this function will be an object of the type `hetrob.result.AlgorithmResult`. This object will contain
   the final solution as well as some meta information about the execution process. This includes the time, amount of
   iterations, final fitness value, log output etc. This object can be converted to a dictionary to view the results.
   Note that the library additionally contains functionality for visualizing the actual solution, but this will be
   explained with a different topic.


Changing the select operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One part of the evolutionary loop is the "select" operator. It defines the rules by which the individuals from a
population are selected as parents of the next population.

This operator is not tied to the genotype representation of a
