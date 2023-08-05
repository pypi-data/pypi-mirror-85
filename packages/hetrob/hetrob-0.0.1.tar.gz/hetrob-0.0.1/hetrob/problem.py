"""
Module for problem formulation/modelling
"""
# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations

from typing import List, Dict, Tuple, Optional, TypeVar
from pprint import pprint

import numpy as np

from hetrob.pledge import HeterogeneousGraphPledge, WindowedPrecedencePledge, TimeWindowPledge
from hetrob.pledge import BasicGraphPledge, VehiclePledge
from hetrob.util import distance_3d, distance_2d, d2, JsonMixin


ProblemType = TypeVar('ProblemType')


# INTERFACES & ABSTRACT METHODS
# -----------------------------

"""
How could you mostly make the representation of the problem decoupled from the individual?
What simple atomic methods and attributes would an interface have to enforce?

BRAINSTORMING:
- get_weight(node1, node2, vehicle)
    So currently I am modelling the weight between two nodes explicitly as the distance between them. But this could
    be a much more abstract representation, which could be hidden behind this interface
- get_profit(node, vehicle)
    So this might be misleading, but the profit of a node in this case would be the opposite if a profit. Right now
    it has a duration, which is more of a cost


"""

class AbstractProblem(JsonMixin):

    def __init__(self):
        JsonMixin.__init__(self)


# PROBLEM REPRESENTATION ClASSES
# ------------------------------

class BasicProblem(BasicGraphPledge,
                   VehiclePledge,
                   AbstractProblem):

    def __init__(self, vehicle_count: int, coordinates: List[Tuple[float, float]], duration: float):
        AbstractProblem.__init__(self)
        BasicGraphPledge.__init__(self)
        VehiclePledge.__init__(self)

        self.vehicle_count = vehicle_count
        self.node_coordinates = coordinates
        self.duration = duration

        # COMPUTED ATTRIBUTES
        # Obviously there is one coordinate entry for every node that is supposed to be part of the problem in the
        # given list "node_coordinates" so it's length gives us the node count
        self.node_count = len(self.node_coordinates)
        # The id lists can simply be created as a list of ascending indices.
        self.vehicle_ids = list(range(self.vehicle_count))
        self.node_ids = list(range(self.node_count))

    # IMPLEMENT 'JsonMixin'
    # ---------------------
    # The AbstractProblem class demands an implementation of JsonMixin, because every problem instance has to be
    # savable and loadable from persistent files in JSON format

    def get_import(self) -> Tuple[str, str]:
        return 'hetrob.problem', 'BasicProblem'

    def to_dict(self) -> dict:
        return {
            'vehicle_count': self.vehicle_count,
            'coordinates': self.node_coordinates,
            'duration': self.duration
        }

    @classmethod
    def from_dict(cls, data: dict) -> BasicProblem:
        return cls(
            vehicle_count=data['vehicle_count'],
            coordinates=data['coordinates'],
            duration=data['duration']
        )

    # IMPLEMENT "NodePledge"
    # ----------------------

    def get_nodes(self):
        return self.node_ids

    def get_node_count(self):
        return self.node_count - 1

    # IMPLEMENT "VehiclePledge"
    # -------------------------

    def get_vehicles(self) -> List[int]:
        return self.vehicle_ids

    def get_vehicle_count(self) -> int:
        return self.vehicle_count

    # IMPLEMENT "BasicGraphPledge"
    # ----------------------------

    def get_node_cost(self, node: int) -> float:
        return self.duration

    def get_node_profit(self, node: int) -> float:
        return 1

    def get_edge_weight(self, node1: int, node2: int) -> float:
        return distance_2d(
            self.node_coordinates[node1],
            self.node_coordinates[node2]
        )


class OrderedHeterogeneousSkillTimeConstraintProblem(AbstractProblem):
                                                     # HeterogeneousGraphPledge,
                                                     # TimeWindowPledge,
                                                     # WindowedPrecedencePledge):
    """
    The name of this class `HeterogeneousSkillTimeConstraintProblem` contains three relevant terms, which define the
    degree of detail, which is considered in this model of the problem:
    - Ordered:                  This refers to the fact, that task orders (also called precedence constraints) are
                                considered here.
    - HeterogeneousSkill:       This means, that the main aspect of heterogeneity considered here is the aspect of
                                different skills or capabilities between the agents. Agents only have a subset of
                                all elementary skills and tasks require some of these skills to be completed.
    - TimeConstraint:           Refers to the fact that timing constraints are considered. This included mainly two
                                types of constraints: "time windows" and "windowed precedences"
    """

    # VISUALIZATION RELATED VALUES
    # ----------------------------

    plot_default_color = 'black'
    plot_depot_marker = 's'
    plot_node_marker = 'o'

    # THE CONSTRUCTOR
    # ---------------

    def __init__(self,
                 vehicles: List[Tuple[float, List[int]]],
                 coordinates: List[Tuple[float, float, float]],
                 durations: List[float],
                 time_windows: List[Optional[Tuple[float, float]]],
                 requirements: List[List[int]],
                 precedences: List[List[Tuple[int, Optional[float], Optional[float], bool]]],
                 # Additional parameters
                 ndigits: int = 3):
        """
        The constructor.

        Describes how a problem instance can be generated from a set of parameters, which describe the problem.
        These parameters, which completely describe the problem in the required modelling detail are:
        let N be the amount of tasks to be complete and M be the amount of vehicles available.
        (This means that it is in total N + 1 nodes that have to be defined; Including the DEPOT)

        - vehicles:                 The list of vehicles, which are available for the mission planning. This is a list,
                                    where each element represents one vehicle. Each element is a tuple of two values
                                    The first value being a float for the speed of a vehicle and the second value
                                    being a list of integers, where each integer is the ID of a skill, which the
                                    corresponding vehicle possesses.
        - coordinates:              The list of the 3D coordinates of each of the tasks with the length (N+1). Each
                                    element in the list is a tuple of 3 float values, each representing the x, y and z
                                    coordinates respectively.
        - durations:                A list of length (N+1). Each element is the float value, which defines the time
                                    duration, which is needed to complete the task, which is represented by that
                                    corresponding element
        - time_windows:             A list of length (N+1). Each element represents the time window for the
                                    corresponding task. The elements are tuples, which contain two float values. The
                                    first value is the earliest possible starting time for the task and the second
                                    value the latest possible starting time.
        - requirements:             A list of length (N+1): Each element represents the skill requirement for the
                                    corresponding task. This skill requirement is expressed as a single integer value,
                                    where the integer is the ID of the skill, which has the same assignment as in the
                                    vehicles list
        - precedences:              A list of length (N+1): Each element represents all the possible precedences of a
                                    task. That is more specifically all the other tasks upon which a task depends upon.
                                    All of these preceding tasks have to be completed in order to start the work on the
                                    the dependent task. Each element of this list is another list in turn which
                                    contains all the precedences. This list may also be empty, which defines the case
                                    that a task does not have any dependencies. In the case, that the list is not
                                    empty it will contain tuples with three elements. The first being an integer and
                                    the other two floats. The integer defines the ID of the task which is meant to go
                                    before the current one. The first float defines the minimum time to pass between
                                    the end of the preceding and the start of the current task, the second float value
                                    is the maximum time to pass in between.

        THE DEPOT
        A node on the depot: It is implicitly assumed that the first node defined in all the relevant lists is always
        describing the depot. An example would be that the first coordinate in the "coordinates" list is assumed to be
        the coordinates of the depot.

        :param vehicles:
        :param coordinates:
        :param durations:
        :param time_windows:
        :param requirements:
        :param precedences:
        :param ndigits:
        """
        # MAIN PROPERTIES
        # These properties are the ones, which completely describe a problem instance. They are directly passed to the
        # constructor.
        self.vehicles = vehicles
        self.coordinates = coordinates
        self.durations = durations
        self.time_windows = time_windows
        self.requirements = requirements
        self.precedences = precedences

        # The following attributes are additional configurations, which do not represent the problem itself, but are
        # used to set certain behaviour of the problem class.
        self.ndigits = ndigits

        # COMPUTED PROPERTIES
        # All of the following fields are in some way derived from the main parameters, which fully describe the
        # problem, but they define certain data or data structures, which are beneficial for the representation of
        # the problem. Which could for example mean, that they are just better for certain calculations further down
        # the line etc.

        # The length value defines the amount of all nodes which make up the problem, which also includes the depot.
        # N however only defines the amount of actual tasks to be completed and M the amount of available vehicles.
        self.length = len(self.coordinates)
        self.N = self.length - 1
        self.M = len(self.vehicles)
        # This is a 2d numpy vector (matrix) which defines the travel distances(!) between all the task nodes
        self.distances = self._create_distance_matrix(self.coordinates)
        # The following are helper lists. The nodes list is simply a list, which contains the ids of all the vehicles
        # in increasing order and the skills variable is a set of all existing skill ids
        self.nodes = list(range(self.length))
        self.vehicle_ids = list(range(self.M))
        self.skills = self._create_skills_set(self.vehicles)
        # The following list will contain a list for every node in the problem and each of those lists will contain
        # the ID's of all the vehicles, which are qualified to execute this task based on their possessed skills.
        # The pre-computation of this data structure will also be used in further algorithms
        self.qualified_vehicles = self._create_qualified_vehicles_list(self.vehicles, self.requirements)

    # PUBLIC METHODS
    # --------------

    def get_vehicle_speed(self, vehicle: int) -> float:
        """
        Returns the speed of the given vehicle identifies by its ID

        :param vehicle:
        :return:
        """
        return self.vehicles[vehicle][0]

    # PLEDGE NodePledge

    def get_nodes(self):
        return self.nodes

    # PLEDGE FleetPledge

    def get_vehicles(self):
        return list(range(self.M))

    # PLEDGE HeterogeneousGraphPledge

    def get_edge_weight(self, node1: int, node2: int, vehicle: int) -> float:
        """
        Returns the weight of a an edge in the representation between the given node1 and node2 if traversed using
        the given vehicle.

        :param node1:
        :param node2:
        :param vehicle:
        :return:
        """
        speed = self.get_vehicle_speed(vehicle)
        distance = self.distances[node1][node2]
        return distance / speed

    def get_node_cost(self, node: int, vehicle: int) -> float:
        """
        Returns the cost of a node when visited with a given vehicle.
        In the case of this specific representation the cost is not dependent on the vehicle, it is a constant time
        duration only dependent on the node.

        :param node:
        :param vehicle:
        :return:
        """
        return self.durations[node]

    def get_node_profit(self, node: int, vehicle: int) -> float:
        """
        Returns 0, as this problem model does not include node profits

        :param node:
        :param vehicle:
        :return:
        """
        return 0

    # PLEDGE TimeWindowPledge

    def get_time_window(self, node: int, vehicle: int) -> Tuple[float, float]:
        return self.time_windows[node]

    # PLEDGE WindowedPrecedencePledge

    def precedes(self, node1: int, node2: int) -> bool:
        return node1 in [node for node, _, _, _ in self.precedences[node2]]

    def precedes_same(self, node1: int, node2: int) -> bool:
        return True in [same for node, _, _, same in self.precedences[node2] if node == node1]

    def get_precedence_window(self, node1: int, node2: int) -> Tuple[float, float]:
        for node, start, end in self.precedences[node2]:
            if node == node1:
                return start, end

        raise ValueError('node {} does not precede node {}! Not time window found'.format(node1, node2))

    def get_precedences(self) -> List[List[Tuple[int, float, float]]]:
        return self.precedences

    # IMPLEMENT "JsonMixin"
    # ---------------------

    def get_import(self) -> Tuple[str, str]:
        return 'hetrob.problem', 'OrderedHeterogeneousSkillTimeConstraintProblem'

    def to_dict(self) -> dict:
        nodes = {}
        for node_id, coords, duration, requires, time_window, precedes in zip(self.nodes,
                                                                              self.coordinates,
                                                                              self.durations,
                                                                              self.requirements,
                                                                              self.time_windows,
                                                                              self.precedences):
            nodes[str(node_id)] = {
                'coords': coords,
                'duration': duration,
                'precedes': precedes,
                'requires': requires,
                'tw': time_window
            }

        vehicles = {}
        for vehicle_id, (speed, skills) in zip(self.vehicle_ids, self.vehicles):
            vehicles[vehicle_id] = {
                'speed': speed,
                'skills': skills
            }

        return {
            'nodes': nodes,
            'vehicles': vehicles
        }


    @classmethod
    def from_dict(cls, data: dict) -> OrderedHeterogeneousSkillTimeConstraintProblem:
        return cls.from_dicts(data['vehicles'], data['nodes'])

    # PROTECTED METHODS
    # -----------------

    @classmethod
    def _create_distance_matrix(cls, coordinates: List[Tuple[float, float, float]]) -> np.ndarray:
        """
        Given the list of coordinates of the task nodes, this function creates a matrix, where each element is the
        distance between the pair of nodes given by the row and column index.

        :param coordinates:
        :return:
        """
        length = len(coordinates)
        # Initialize the matrix
        distances = np.zeros(shape=(length, length), dtype=np.float64)

        # Populate the matrix with the pairwise distances of all possible combinations of tasks
        for node1, coords1 in enumerate(coordinates):
            for node2, coords2 in enumerate(coordinates):
                distance = distance_3d(coords1, coords2)
                distances[node1][node2] = distance

        return distances

    @classmethod
    def _create_skills_set(cls, vehicles: List[Tuple[float, List[int]]]):
        """
        Given the list, which specifies the vehicles, this function will return a set, that contains the ids of all
        the elementary skills, that are represented by the vehicles.

        :param vehicles:
        :return:
        """
        skill_set = set()
        for speed, skills in vehicles:
            for skill in skills:
                skill_set.add(skill)

        return skill_set

    @classmethod
    def _create_qualified_vehicles_list(cls,
                                        vehicles: List[Tuple[float, List[int]]],
                                        requirements: List[List[int]]) -> List[List[int]]:
        """
        Given the specification of the available vehicles and the requirements of each task, this function will create
        a list, which assigns a list to each node of the problem. That list will contain the vehicle ID's of every
        vehicle, which is theoretically qualified to execute that task.

        :param vehicles:
        :param requirements:
        :return:
        """
        # Initializing for every node an empty list of qualified vehicles
        qualified_vehicles = [[] for _ in requirements]

        # for every node we iterate through every vehicle and check if that vehicle has the skills to complete the task
        # and if it does we append the vehicle ID to the list of qualified vehicles for that node.
        for node, requirements in enumerate(requirements):
            for vehicle, (speed, skills) in enumerate(vehicles):
                for requirement in requirements:
                    if requirement in skills:
                        qualified_vehicles[node].append(vehicle)

        return qualified_vehicles

    # MAGIC METHODS
    # -------------

    def __len__(self):
        return self.length

    # CLASS METHODS
    # -------------

    @classmethod
    def from_dicts(cls, vehicles: Dict[str, dict], nodes: Dict[str, dict]):
        # Creating a dict, whose keys are the string names of skills and the values the integer ID's
        # To do this we iterate the list of the vehicles and gather all the unique skill names which are possessed
        # by any of the vehicles and then convert this set into a dict.
        skill_name_set = set()
        for vehicle_name, vehicle_data in vehicles.items():
            skills = vehicle_data['skills']
            for skill in skills:
                skill_name_set.add(skill)

        skill_name_id_map = dict((name, index) for index, name in enumerate(skill_name_set))
        # print('\nSKILL NAME TO ID MAPPING:')

        # Creating a map, whose keys are the string names of the nodes and the values their integer ID's
        node_name_id_map = {}
        for node_id, (node_name, node_data) in enumerate(nodes.items()):
            node_name_id_map[node_name] = node_id

        # print('\nNODE NAME TO ID MAPPING:')
        # pprint(node_name_id_map)

        # Constructing the vehicle list. The problem object requires a list of vehicles, where each vehicle is
        # represented by a tuple of the format (speed: float, skills: List[int])
        vehicle_list = []
        for vehicle_name, vehicle_data in vehicles.items():
            skills = [skill_name_id_map[name] for name in vehicle_data['skills']]
            vehicle = (vehicle_data['speed'], skills)
            vehicle_list.append(vehicle)

        # Initializing all the lists, which are needed to represent various node properties
        coordinates = []
        durations = []
        requirements = []
        precedences = []
        time_windows = []

        # print('\nNODE DETAILS:')
        for node_id, (node_name, node_data) in enumerate(nodes.items()):
            # node coordinates, time windows and task durations are directly defined in the nodes dict as they are also
            # required for the Problem constructor. These can be simply added to the corresponding lists
            coordinates.append(node_data['coords'])
            durations.append(node_data['duration'])
            time_windows.append(node_data['tw'])

            # Requirements are defines using the string names if the requirements. What we actually need is integer ID's
            # so for the requirements we have to preprocess them by running the names though the previously created
            # mapping
            requires = [skill_name_id_map[name] for name in node_data['requires']]
            requirements.append(requires)

            # Precedence relationships between nodes are defined using the string names of the nodes. In this case we
            # also have to replace the string names with the integer ID's using the mapping
            precedes = [(node_name_id_map[str(name)], start, end, same) for name, start, end, same in node_data['precedes']]
            precedences.append(precedes)

            message_split = [
                'NODE {} ({}): '.format(node_name, node_id),
                '  coordinates (x y z): {} {} {}'.format(*node_data['coords']),
                '  duration: {}'.format(node_data['duration']),
                '  time window: {} - {}'.format(*node_data['tw'])
            ]
            # print('\n'.join(message_split))

        return cls(
            vehicle_list,
            coordinates,
            durations,
            time_windows,
            requirements,
            precedences
        )


