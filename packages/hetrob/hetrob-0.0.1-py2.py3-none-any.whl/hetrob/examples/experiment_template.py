import tempfile

from hetrob._testing import solve_mock, MockSolution, MockProblem
from hetrob.data import load_data_set_map
from hetrob.util import MaxTimeTermination
from hetrob.result import InstanceBatching, NoResultBatching

# ========================= #
#    REQUIRED CONSTANTS     #
# ========================= #
# These constants, which are defined here are absolutely required for this file to properly function. Their names
# should NOT be altered and they should be assigned valid values!

# This path defines the destination for the folder, which will contain the persistent representation of the experiments
# results. These files include for example the log file with the console output, a json file with the statistics of
# the experiment as well as multiple files with the raw result data from each individual execution of the algorithms
PATH = '/home/jonas/Desktop/select_operators'


# This defines the amount of times each algorithm is executed on EACH instance. This feature exists, because the
# results of an experiment may be more stable if they are averaged over multiple attempts.
REPETITIONS = 10

# This variable will have to be a dictionary, where the keys are the human-readable names of the instances which are
# supposed to be run for EACH algorithm. The values of the dict are supposed to be the absolute paths of where the
# JSON files of these instances are saved.
# The string key names used in this dict will also be the names of the keys used in the raw data files and the +
# statistics file for example.
# The "load_data_set_path" loads exactly such a dict, which was constructed from a predefined "data set". A data set is
# a collection of multiple problem instances, which a grouped by some criterion.
INSTANCES = load_data_set_map('HSVRSP_VARIABLE_SIZE_100')

# This variable is important for how the results of the experiment will be saved into persistent files. Just for a
# quick mentioning: With big experiments, the amount of result data can get so big, that it (a) produces really big
# files and (b) could cause a RAM overflow since they are stored in memory until they are saved.
# That is why it is important to split the data into smaller batches. Passing different classes to this variable will
# change at which layer these batches are implemented.
BATCHING = InstanceBatching
# BATCHING = NoResultBatching

# ======================== #
#    UTILITY CONSTANTS     #
# ======================== #
# These constants are not being called whenever this file is being executed. They are merely defined out of
# convenience for usage within the algorithms section below. If you choose not to use these values in the form of a
# global variable, they can be removed IF their usages below are replaced properly.

VERBOSE = True
INFEASIBILITY_PENALTY = 8000
TERMINATION_CONDITION = MaxTimeTermination(300)
PROBLEM_CLASS = MockProblem

# ================= #
#    CUSTOM CODE    #
# ================= #
# Use this section to define custom code needed for the experiment. This custom code could be custom "solve" callables
# or custom Solution and Problem representation as well as individual operators for existing algorithms etc.


# ================= #
#    ALGORITHMS     #
# ================= #
# This section is the most important one! The ALGORITHM dict defines the specifics of which algorithm is exected in
# what way (meaning with which meta parameters). Each additional algorithm which is supposed to be executed has to be
# represented by a new entry within the top level dictionary.
# The string key used to describe the algorithm wil also be the name which will be use as a key in the raw data files +
# and the statistics file.


ALGORITHMS = {
    'Algo1': {
        # The "solve" attribute has to give a callable object, which actually executes the algorithm.
        # Quick reminder: Each algorithm execution has to return an AlgorithmResult instance.
        'solve':            solve_mock,
        # Now these following fields solve the matter of how to pass parameters to this function. First of all:
        # Parameters will only be passed in the format of keyword arguments. So the keys of these dicts are the names
        # of the parameters the function expects.
        # Now there is the concept of the "static" and "dynamic" arguments. The static arguments are all those which do
        # not change despite which instance is currently being executed. The dynamic ones do change with each instance
        # The dynamic kwargs dict is created in-time and can use the specific problem instance which is executed at that
        # point as a dynamic argument...
        'static_kwargs':    {
            'solution_class':       MockSolution,
            'termination':          TERMINATION_CONDITION
        },
        'dynamic_kwargs':  lambda problem: {
            'problem':              problem
        }
    }
}


