"""
A module which contains all the different required fitness representations.
"""
from deap import base


class FitnessMin(base.Fitness):
    """
    A basic fitness representation, which simply aims to MINIMIZE a single objective...
    """

    weights = (-1.0,)
