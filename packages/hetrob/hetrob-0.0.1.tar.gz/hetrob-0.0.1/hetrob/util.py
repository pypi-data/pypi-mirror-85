"""
Module for general utility functions.
"""
# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations

from typing import List, Tuple, Any, Sequence, Optional
from abc import ABC, abstractmethod
import importlib
import math
import copy
import random
import json
import os

import numpy as np


# INTERFACES
# ==========

class HetrobJsonEncoder(json.JSONEncoder):
    """
    This is a subclass of `json.JSONEncoder`, which implements the custom behaviour to encode subclasses of
    the JsonMixin.
    """
    def default(self, obj):
        """
        This function is being called whenever the encoder finds an object, which is not one of the basic supported
        data types. Here we are implementing the custom behaviour by checking if this object is a child of the
        JsonMixin.

        :param obj:
        :return:
        """
        # In case the object is a subclass of the JsonMixin we can of course convert that into a dictionary using the
        # "get_dict" method.
        if isinstance(obj, JsonMixin):
            return obj.get_dict()
        # Now usually if an object enters the "default" method (=is not a basic data type) AND is not a child class of
        # of JsonMixin, the call would be passed to the super implementation of default, which in turn would raise an
        # exception for a custom class. But I would like to add the possibility, that if the class at least implements
        # the StringMixin, it's string representation would be used in it's place. This functionality will be
        # useful for cases where the actual object does not have to be loaded again, but is simply an information for
        # the user.
        elif isinstance(obj, StringMixin):
            return str(obj)

        return super(HetrobJsonEncoder, self).default(obj)


class HetrobJsonDecoder(json.JSONDecoder):
    """
    This is a subclass of `json.JSONDecoder`, which implements the custom behaviour to decode the subclasses of
    the JsonMixin
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """
        This method will be called on every object within the JSON tree during the decoding process. This is where the
        custom decoding for JsonMixin is implemented.

        :param obj:
        :return:
        """
        # Every JsonMixin object must have the key '_import' as part of it's dictionary representation. On the contrary
        # this means that every dict which does not have this key is just another "normal" object, which will not be
        # further processed.
        if '_import' not in obj:
            return obj

        # The '_import' key contains a value which is a list of two items. The first item being the module name for a
        # dynamic import and the second item being the string class name of the class from which the dict was
        # originally created. These values are being unpacked and used to load this class dynamically.
        module_name, class_name = obj['_import']
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)

        # Since this class must be a subclass of JsonMixin, we simply call the "from_dict" method to recreate the
        # original object
        obj = cls.from_dict(obj)

        return obj


class JsonMixin(object):
    """
    This is a mixin which adds the possibility to convert an object from and to a JSON string.
    """

    def __init__(self):
        pass

    def get_dict(self) -> dict:
        """
        This method will return the dict representation of the object.

        **DESIGN CHOICES**

        Seeing this method, you might be wondering why it even exists if there is an abstract method "to_dict", which
        the user has to implement. To explain this I will have to go into the details of how this class works: To
        implement the custom JSON behaviour in python a custom Encoder and Decoder class has to be written, which will
        then have to be used in the "loads" and "dumps" functions of the json module. The decoder specifically needs to
        know the module and class name from where the data originally came from, to be able to dynamically import this
        class and call its "from_dict" method. This data for the dynamic import will always be saved within the field
        "_import" of the dict. But remembering to manually add this field "_import" within the "to_dict" method should
        not be the responsibility of the user. Instead it is explicitly implemented via the "get_import" method.

        So the "to_dict" method is only supposed to implement the serialization of the content of the class. The
        "get_import" method will explicitly prompt the user to define the import information and this method "get_dict"
        will call the get import method to add the field "_import" to the dict. This method "get_dict" will also be
        called within the decoder...

        :return: A dictionary, which contains all the information about the object as primitive datatypes.
        :rtype: dict
        """
        data = self.to_dict()
        data.update({'_import': self.get_import()})
        return data

    # TO BE IMPLEMENTED
    # -----------------

    def to_dict(self) -> dict:
        """
        Supposed to return the contents of an object as a dictionary consisting only of primitve datatypes.

        Has to be implemented by a child class

        :return: A dict with the objects attribute values
        :rtype: dict
        """
        raise NotImplementedError()

    def get_import(self) -> Tuple[str, str]:
        """
        Supposed to return a tuple, which defines the dynamic import information for the class of this object.

        Has to be implemented by the child class.

        The first value of the tuple is supposed to be the module, from which the class originally came. It's string
        format has to be exactly the same as if the module would have been imported in python normally.
        The second value of the tuple is supposed to be the string class name of this class.

        .. code-block:: python

            # Example implementation for "get_import"
            def get_import():
                return "hetrob.genetic.phenotype", "AbstractPhenotype"

        :return: The tuple
        :rtype: Tuple[str, str]
        """
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, data: dict) -> JsonMixin:
        """
        This method is supposed to reconstruct a object given the attributes in dict format.

        Has to be implemented by child class.

        :param data: The data, which has previously been created by the "from_dict" method
        :type data: dict

        :return: An object of this class
        """
        raise NotImplementedError()


class StringMixin(object):
    """
    This is a mixin which enables the possibility to convert an object to a string using the built-in "str()" function.
    """
    def __str__(self) -> str:
        """
        Gets called on application of built in "str" method. Returns the string representation of the object

        :return: string representation of object
        """
        return self.to_string()

    def __hash__(self) -> int:
        """
        Gets called on application of built in "hash" method. Returns the hash of the string representation of the
        object.

        :return: hash of the object
        """
        return hash(self.to_string())

    # TO BE IMPLEMENTED
    # -----------------

    def to_string(self) -> str:
        """
        This method is supposed to return a *descriptive* string for the object, which contains the type(=class name)
        as well as the values for the most important attributes of the object.

        :return: The string representation of the object#
        :rtype: string
        """
        raise NotImplementedError()


# UTILITY FUNCTIONS
# =================


def dump_json(obj: object, indent: Optional[int] = 4):
    """
    Converts an object, which only consists of basic data types and objects that implement JsonMixin into a json string

    :param obj: The object to be converted into a string
    :type obj: object

    :return: The string JSON representation of the object
    """
    return json.dumps(
        obj,
        indent=indent,
        sort_keys=False,
        cls=HetrobJsonEncoder
    )


def load_json(string: str):
    """
    Converts a JSON string back into its original representation.

    :param string: The json string which contains the information about the data
    :type string: str

    :return: The original object
    """
    return json.loads(
        string,
        cls=HetrobJsonDecoder
    )

# GRAPH/ROUTING UTILITIES
# =======================

def two_point_swap(_items: List[Any], inplace=False):
    items = _items if inplace else copy.deepcopy(_items)
    i, j = random_indices(items, k=2)

    items[i], items[j] = items[j], items[i]
    return items


def two_point_insert(_items: List[Any], inplace=False):
    items = _items if inplace else copy.deepcopy(_items)
    i, j = random_indices(items, k=2)

    items.insert(i + 1, items.pop(j))
    return items


def two_point_reverse(_items: List[Any], inplace=False):
    items = _items if inplace else copy.deepcopy(_items)
    i, j = sorted(random_indices(items, k=2))

    items[i:j] = reversed(items[i:j])
    return items


def iterate_paths(route: List[int]):
    result = zip(route, np.roll(route, -1))
    return result


def routes_add_depot(routes: List[List[int]], depot_node: int = 0) -> List[List[int]]:
    full_routes = []

    for route in routes:
        full_route = route.copy()
        full_route.insert(0, depot_node)
        full_routes.append(full_route)

    return full_routes


# MATHEMATICAL UTILITIES
# ======================

def d2(coords: Any,
       dimensions: Tuple[int, int] = (0, 1)) -> Tuple[float, float]:
    """
    Turns three dimensional coordinates into two dimensional ones.

    :param coords:
    :param dimensions:      A tuple, which defines the indices of which dimensions to use for the dimensionality
                            reduction. default are 0 and 1, which is the x and y coordinate.
    :return:
    """
    a = coords[dimensions[0]]
    b = coords[dimensions[1]]
    return a, b


def distance_2d(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> float:
    """
    Calculates the distance between two 2-dimensional coordinates.

    :param coords1:
    :param coords2:
    :return:
    """
    dx = abs(coords2[0] - coords1[0])
    dy = abs(coords2[1] - coords1[1])

    return math.sqrt(dx ** 2 + dy ** 2)


def distance_3d(coords1: Tuple[float, float, float], coords2: Tuple[float, float, float]) -> float:
    """
    Calculates the distance between two 3-dimensional coordinates.

    :param coords1:
    :param coords2:
    :return:
    """
    dx = abs(coords2[0] - coords1[0])
    dy = abs(coords2[1] - coords1[1])
    dz = abs(coords2[2] - coords1[2])

    return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


# STRING UTILITIES
# ================

def to_snake_case(name: str) -> str:
    letters = []
    for i, c in enumerate(name):
        if c.isupper() and i != 0:
            letters.append('_')
        letters.append(c.lower())

    return ''.join(letters)


# RANDOM UTILITIES
# ================


def random_pop(seq: List[Any]):
    index = random.randint(0, len(seq) - 1)
    return seq.pop(index)


def random_indices(seq: Sequence[Any], k: int, distinct=True):
    indices = list(range(len(seq)))

    choices = set(random.choices(indices, k=k))
    while distinct and len(choices) != k:
        choices = set(random.choices(indices, k=k))

    return choices


def pick_random_colors(k: int,
                       pool: List[str] = ['red', 'blue', 'green', 'purple', 'yellow', 'black', 'orange'],
                       allow_duplicates: bool = False) -> List[str]:
    population = list(pool)
    # So of course we are going to use the "random.choices" function to pick the random colors.
    # The base problem is that this basically does not rule out that the same item is being picked twice.
    # In case we do not want duplicates we are just going to repeat the picking process until all the items
    # are distinct. We ensure this by working with a set here. A set cannot contain duplicates by default. so
    # in case of a duplicate the size of the set will be smaller than the k "originally asked for"
    colors = set(random.choices(population, k=k))
    while not allow_duplicates and len(colors) != k:
        colors = set(random.choices(population, k=k))

    return list(colors)


# ALGORITHM UTILITIES
# ===================

class AbstractTerminationCondition(StringMixin, ABC):

    @abstractmethod
    def update(self, iteration: int, computation_time: float, fitness: float):
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> bool:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        return self.get()

    def __and__(self, other):
        return AndTermination(self, other)

    def __or__(self, other):
        return OrTermination(self, other)


class OrTermination(AbstractTerminationCondition):

    def __init__(self, *conditions):
        self.conditions: Sequence[AbstractTerminationCondition] = conditions

    def update(self, iteration: int, computation_time: float, fitness: float):
        for condition in self.conditions:
            condition.update(iteration, computation_time, fitness)

    def get(self):
        for condition in self.conditions:
            if bool(condition) is True:
                return True
        return False

    # IMPLEMENT "StringMixin"
    # -----------------------

    def to_string(self) -> str:
        substrings = [str(condition) for condition in self.conditions]
        string = "OrTermination({})".format('\n   '.join(substrings))
        return string


class AndTermination(AbstractTerminationCondition):

    def __init__(self, *conditions):
        self.conditions: Sequence[AbstractTerminationCondition] = conditions

    def update(self, iteration: int, computation_time: float, fitness: float):
        for condition in self.conditions:
            condition.update(iteration, computation_time, fitness)

    def get(self) -> bool:
        for condition in self.conditions:
            if bool(condition) is False:
                return False
        return True

    # IMPLEMENT "StringMixin"
    # -----------------------

    def to_string(self) -> str:
        substrings = [str(condition) for condition in self.conditions]
        string = "AndTermination({})".format('\n   '.join(substrings))
        return string


class MaxTimeTermination(AbstractTerminationCondition):

    def __init__(self, limit: float):
        self.limit = limit

        self.computation_time = 0

    def update(self, iteration: int, computation_time: float, fitness: float):
        self.computation_time = computation_time

    def get(self) -> bool:
        return self.computation_time > self.limit

    # IMPLEMENT "StringMixin"
    # -----------------------

    def to_string(self) -> str:
        return "MaxTimeTermination(time_limit={})".format(self.limit)


class MaxIterTermination(AbstractTerminationCondition):

    def __init__(self, niter: int):
        self.niter = niter
        self.index = 0

    def update(self, iteration: int, computation_time: float, fitness: float):
        self.index = iteration

    def get(self) -> bool:
        return self.index > self.niter

    # IMPLEMENT "StringMixin"
    # -----------------------

    def to_string(self) -> str:
        return "MaxIterTermination(iteration_limit={})".format(self.niter)


# FILE SYSTEM UTILITIES
# =====================

def create_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path, 0o777)
