import random
import uuid
import copy
import math
from pprint import pprint
from abc import ABC, abstractmethod
from typing import Sequence, Any, Type, Tuple, List, Optional
from collections import defaultdict, deque

from hetrob.util import random_pop, random_indices

# CONSTANTS
# =========

START_OF_TIME = 0
END_OF_TIME = 1000000000000000


# HELPERS
# =======

class AbstractLimiter(ABC):

    @abstractmethod
    def limit_reached(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def update(self, generator, value):
        raise NotImplementedError()

    def __bool__(self):
        return self.limit_reached()


class AbstractGenerate(ABC):

    def __init__(self, limiter: AbstractLimiter):
        self.limiter = limiter

    @abstractmethod
    def get(self) -> Any:
        raise NotImplementedError()

    def update(self, value):
        self.limiter.update(self, value)

    def __iter__(self):
        return self

    def __next__(self):
        if bool(self.limiter):
            raise StopIteration()

        value = self.get()
        return value


# LIMITERS
# ========

class SelfLimiter(AbstractLimiter):

    def __init__(self):
        self.flag = False

    def set(self):
        self.flag = True

    def limit_reached(self) -> bool:
        return self.flag

    def update(self, generator, value):
        pass


class NoLimit(AbstractLimiter):

    def limit_reached(self) -> bool:
        return False

    def update(self, generator, value):
        pass


class CountLimit(AbstractLimiter):

    def __init__(self, count: int):
        self.count = count
        self.index = 0

    def limit_reached(self) -> bool:
        return self.index >= self.count

    def update(self, generator, value):
        self.index += 1


# GENERATORS
# ==========

class MethodAsGenerate(AbstractGenerate):

    def __init__(self, method, limiter=NoLimit()):
        AbstractGenerate.__init__(self, limiter=limiter)
        self.method = method

    def __call__(self):
        return self.method()

    def get(self):
        return self.method()


class GenerateValueConstant(AbstractGenerate):

    def __init__(self, value: Any, limiter=NoLimit()):
        AbstractGenerate.__init__(self, limiter)
        self.value = value

    def get(self):
        self.update(self.value)
        return self.value


class GenerateValueRandomInteger(AbstractGenerate):

    def __init__(self, lower_limit: int, upper_limit: int, limiter=NoLimit()):
        AbstractGenerate.__init__(self, limiter)
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def get(self):
        value = random.randint(self.lower_limit, self.upper_limit)
        self.update(value)

        return value


class GenerateValueRandomChoice(AbstractGenerate):

    def __init__(self, limiter: AbstractLimiter, choices: Sequence):
        AbstractGenerate.__init__(self, limiter)
        self.choices = choices

    def get(self) -> Any:
        choice = random.choice(self.choices)
        self.update(choice)
        return choice


class GenerateValueRandomPop(AbstractGenerate):

    def __init__(self, limiter: AbstractLimiter, choices: List, reset_after: Optional[int] = None):
        AbstractGenerate.__init__(self, limiter)
        self.choices = choices

        self.reset_after = reset_after if reset_after is not None else len(choices)

        self.current_choices = copy.deepcopy(self.choices)
        self.index = 0

    def get(self) -> Any:
        if self.index >= self.reset_after:
            self.current_choices = copy.deepcopy(self.choices)

        random.shuffle(self.current_choices)
        choice = self.current_choices.pop(0)

        self.update(choice)
        self.index += 1

        return choice


class GenerateRandomSublist(AbstractGenerate):

    def __init__(self, limiter: AbstractLimiter, choices: Sequence, length: int):
        AbstractGenerate.__init__(self, limiter)

        self.choices = choices
        self.length = length

    def get(self):
        sublist = random.sample(self.choices, k=self.length)
        self.update(sublist)
        return sublist


class GenerateCoordinates(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_x: AbstractGenerate,
                 generate_y: AbstractGenerate,
                 generate_z: AbstractGenerate):
        AbstractGenerate.__init__(self, limiter)
        self.generate_x = generate_x
        self.generate_y = generate_y
        self.generate_z = generate_z

    def get(self):
        coordinates = (
            next(self.generate_x),
            next(self.generate_y),
            next(self.generate_z)
        )
        self.update(coordinates)

        return coordinates


class GenerateCoordinatesUniformAround(AbstractGenerate):

    def __init__(self,
                 center: Tuple[float, float, float],
                 x_distance: float = 20,
                 y_distance: float = 20,
                 z_distance: float = 0,
                 limiter: AbstractLimiter = NoLimit()):
        AbstractGenerate.__init__(self, limiter)
        self.center = center
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.z_distance = z_distance

    def get(self) -> Any:
        coordinates = (
            random.randint(self.center[0] - self.x_distance, self.center[0] + self.x_distance),
            random.randint(self.center[1] - self.y_distance, self.center[1] + self.y_distance),
            random.randint(self.center[2] - self.z_distance, self.center[2] + self.z_distance)
        )
        self.update(coordinates)
        return coordinates


class GenerateStandardNodes(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_coordinates: AbstractGenerate,
                 generate_duration: AbstractGenerate,
                 generate_requirements: AbstractGenerate,
                 generate_time_window: AbstractGenerate):
        AbstractGenerate.__init__(self, limiter)
        self.generate_coordinates = generate_coordinates
        self.generate_duration = generate_duration
        self.generate_requirements = generate_requirements
        self.generate_time_window = generate_time_window

        self.index = 0

    def get(self):
        node = {
            'coords':       next(self.generate_coordinates),
            'duration':     next(self.generate_duration),
            'requires':     next(self.generate_requirements),
            'tw':           next(self.generate_time_window),
            'precedes':     []
        }
        name = str(uuid.uuid4())

        value = (name, node)
        self.update(value)

        return value


class GenerateCooperativeNodes(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_coordinates: AbstractGenerate,
                 generate_duration: AbstractGenerate,
                 generate_requirements: AbstractGenerate,
                 generate_cooperation_size: AbstractGenerate):
        AbstractGenerate.__init__(self, limiter)
        self.generate_coordinates = generate_coordinates
        self.generate_duration = generate_duration
        self.generate_requirements = generate_requirements
        self.generate_cooperation_size = generate_cooperation_size

        self.current_node = []

    def get(self):
        if len(self.current_node) == 0:
            # Creating the cooperation size
            cooperation_size = next(self.generate_cooperation_size)
            coords = next(self.generate_coordinates)

            prev_name = ""
            for i in range(cooperation_size):
                duration = next(self.generate_duration)
                precedes = [] if i == 0 else [(prev_name, -duration, -duration, False)]
                node = {
                    'coords':           coords,
                    'duration':         duration,
                    'requires':         next(self.generate_requirements),
                    'tw':               (START_OF_TIME, END_OF_TIME),
                    'precedes':         precedes
                }
                name = str(uuid.uuid4())
                prev_name = name

                self.current_node.append((name, node))

        value = self.current_node.pop(0)

        if len(self.current_node) == 0:
            self.update(value)

        return value


class GenerateBiasedTree(AbstractGenerate):

    CHILD = "child"
    SIBLING = "sibling"

    NODE = defaultdict(lambda: {
        'name': '',
        'parent': None,
        'children': []
    })

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_node_count: AbstractGenerate,
                 child_weight: float,
                 sibling_weight: float):
        AbstractGenerate.__init__(self, limiter)
        self.generate_node_count = generate_node_count
        self.child_weight = child_weight
        self.sibling_weight = sibling_weight

        self.choices = [self.CHILD, self.SIBLING]
        self.weights = [self.child_weight, self.sibling_weight]

    def get(self) -> Any:
        tree = copy.deepcopy(self.NODE)

        nodes_left = max(next(self.generate_node_count), 2) - 1

        parent = 'root'
        for i in range(nodes_left):
            name = str(i)
            node_type, = random.choices(self.choices, self.weights, k=1)

            tree[name]['name'] = name
            tree[name]['parent'] = parent

            tree[parent]['children'].append(name)

            if node_type == self.CHILD:
                parent = name

        self.update(tree)
        return dict(tree)


class GeneratePrecedenceNodes(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_tree: AbstractGenerate,
                 generate_coordinates: AbstractGenerate,
                 generate_duration: AbstractGenerate,
                 generate_requirements: AbstractGenerate,
                 generate_precedence_window: AbstractGenerate,
                 generate_next_coordinates_class: Type[AbstractGenerate]):
        AbstractGenerate.__init__(self, limiter)
        self.generate_tree = generate_tree
        self.generate_coordinates = generate_coordinates
        self.generate_duration = generate_duration
        self.generate_requirements = generate_requirements
        self.generate_precedence_window = generate_precedence_window
        self.generate_next_coordinates_class = generate_next_coordinates_class

        self.current_tree = {}

        self.generator = self.next_node()

    def get(self):
        try:
            value = next(self.generator)
        except StopIteration:
            self.generator = self.next_node()
            value = next(self.generator)

        self.update(value)

        return value

    def next_node(self):
        # Generating a new tree, if the current one has been completed
        if len(self.current_tree) == 0:
            self.current_tree = next(self.generate_tree)

        name = str(uuid.uuid4())
        parent = {
            'coords': next(self.generate_coordinates),
            'duration': next(self.generate_duration),
            'requires': next(self.generate_requirements),
            'tw': (START_OF_TIME, END_OF_TIME),
            'precedes': []
        }
        yield name, parent
        # Iterating the precedence tree with breadth first search (BFS)
        stack = deque([('root', parent)])
        while len(stack) != 0:
            name, parent = stack.popleft()
            generate_coords = self.generate_next_coordinates_class(parent['coords'])

            for child in self.current_tree[name]['children']:
                name = str(uuid.uuid4())
                node = {
                    'coords': next(generate_coords),
                    'duration': next(self.generate_duration),
                    'requires': next(self.generate_requirements),
                    'tw': (START_OF_TIME, END_OF_TIME),
                    'precedes': []
                }

                # Telling the parent, that it is a precedence of these child nodes
                parent['precedes'].append((name, *next(self.generate_precedence_window), False))
                yield name, node

                # Adding the new child node to the stack
                stack.append((child, node))


class GenerateVehicles(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_speed: AbstractGenerate,
                 generate_skills: AbstractGenerate):
        AbstractGenerate.__init__(self, limiter)
        self.generate_speed = generate_speed
        self.generate_skills = generate_skills

    def get(self) -> Any:
        vehicle = {
            'speed':        next(self.generate_speed),
            'skills':       next(self.generate_skills)
        }
        self.update(vehicle)

        return vehicle


class GenerateRandomSplit(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 sequence: List,
                 k: int,
                 margin: int):
        AbstractGenerate.__init__(self, limiter)
        self.sequence = copy.deepcopy(sequence)
        self.k = k
        self.margin = margin

        self.length = len(self.sequence)
        self.parts = []
        self.sizes = []
        self._init()

    def _init(self):
        if self.k == 1:
            self.parts.append(self.sequence)
            return

        k = self.k if self.length % self.k == 0 else self.k - 1
        average = math.floor(self.length / self.k)
        for i in range(k):
            self.sizes.append(average)

        remaining = self.length - (average * k)
        if remaining != 0:
            self.sizes.append(remaining)

        for i in range(random.randint(len(self.sizes), len(self.sizes) * 2)):
            # Choose two sizes and move a element between them if the margin allows it
            i, j = random_indices(self.sizes, 2, distinct=True)
            if (self.sizes[i] - 1) > (average - self.margin) and (self.sizes[j] + 1) < (average + self.margin):
                self.sizes[i] -= 1
                self.sizes[j] += 1

        for size in self.sizes:
            part = []
            for i in range(size):
                part.append(random_pop(self.sequence))
            self.parts.append(part)

    def get(self):
        parts = self.parts.pop()
        self.update(parts)
        return parts


class GenerateOverlappingSublists(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 base: List[Any],
                 k: int,
                 min_representations: int,
                 max_representations: int):
        AbstractGenerate.__init__(self, limiter)
        self.base = base
        self.k = k
        self.min = min_representations
        self.max = max_representations

        self.amounts = defaultdict(int)
        self.sublists = []
        self._init()

    def _init(self):
        for item in self.base:
            self.amounts[item] = random.randint(
                min(self.k, self.min),
                min(self.k, self.max)
            )
        self.amounts = dict(self.amounts)

        sublists = defaultdict(list)
        for item, amount in self.amounts.items():
            indices = random_indices(range(self.k), k=amount, distinct=True)
            for index in indices:
                sublists[index].append(item)

        # Fixing it for the case that some vehicles have not been assigned any skills
        for index in range(self.k):
            if len(sublists[index]) < self.min:
                while len(sublists[index]) < self.min:
                    sublists[index].append(random.choice(self.base))

        self.sublists = list(sublists.values())

    def get(self):
        sublist = self.sublists.pop()
        self.update(sublist)
        return sublist


class GenerateOverlappingExhaustiveSublists(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 base: List[Any],
                 k: int,
                 add_chance: float,
                 min_representations: int = 1,
                 min_length: int = 2):
        AbstractGenerate.__init__(self, limiter)
        self.base = base
        self.k = k
        self.add_chance = add_chance
        self.min_representations = min_representations
        self.min_length = min_length

        self.sublists = [[] for _ in range(k)]

        self._init()

    def _init(self):
        self.satisfy_min_representations()
        self.satisfy_min_length()
        self.apply_chance()

    def get(self):
        sublist = self.sublists.pop()
        self.update(sublist)
        return sublist

    def apply_chance(self):
        for sublist in self.sublists:
            while len(sublist) < len(self.base) and random.random() < self.add_chance:
                value = self.random_exclusive_value(sublist)
                sublist.append(value)

    def satisfy_min_representations(self):
        # After this method we can be sure that every element of the base list is represented the minimum
        # amount of times...
        for value in self.base:
            for i in range(self.min_representations):
                sublist_index = self.random_sublist_index()
                self.sublists[sublist_index].append(value)

    def satisfy_min_length(self):
        # After this method we can make sure that every sublist has at least the minimum length
        for sublist in self.sublists:
            while len(sublist) < self.min_length:
                value = self.random_exclusive_value(sublist)
                sublist.append(value)

    def random_sublist_index(self):
        return random.randint(0, self.k - 1)

    def random_exclusive_value(self, sublist: List[Any]):
        value = random.choice(self.base)
        while value in sublist:
            value = random.choice(self.base)

        return value


class GenerateSum(AbstractGenerate):

    def __init__(self,
                 limiter: AbstractLimiter,
                 generate_list: AbstractGenerate):
        AbstractGenerate.__init__(self, limiter)
        self.generate_list = generate_list

    def get(self):
        _list = next(self.generate_list)
        _sum = sum(_list)
        self.update(_list)
        return _sum


class HeterogeneitySeeding:

    def __init__(self,
                 skill_count: int,
                 generate_node_count: AbstractGenerate,
                 generate_duration: AbstractGenerate,
                 generate_vehicles: AbstractGenerate):
        self.skill_count = skill_count
        self.generator_node_count = generate_node_count
        self.generator_duration = generate_duration
        self.generator_vehicles = generate_vehicles

        self.skills = {}
        self.vehicles = defaultdict(list)
        self._init()
        self._decorate()
        pprint(self.skills)
        pprint(self.vehicles)

        self.vehicle_index = 0

    def _init(self):
        for index in range(self.skill_count):
            node_count = next(self.generator_node_count)
            duration = next(self.generator_duration)
            vehicles = next(self.generator_vehicles)

            self.skills[index] = {
                'index':                    index,
                'durations_remaining':      node_count,
                'requirements_remaining':   node_count,
                'duration':                 duration,
                'vehicles':                 vehicles
            }

        for index, skill in self.skills.items():
            for vehicle_index in skill['vehicles']:
                self.vehicles[vehicle_index].append(index)

        self.vehicles = dict(self.vehicles)

    def _decorate(self):
        self.generate_duration = MethodAsGenerate(self.generate_duration)
        self.generate_requirements = MethodAsGenerate(self.generate_requirements)
        self.generate_skills = MethodAsGenerate(self.generate_skills)

    def generate_duration(self):
        valid_indices = [index for index, skill in self.skills.items() if skill['durations_remaining'] != 0]
        index = random.choice(valid_indices)
        self.skills[index]['durations_remaining'] -= 1
        return self.skills[index]['duration']

    def generate_requirements(self):
        valid_indices = [index for index, skill in self.skills.items() if skill['requirements_remaining'] != 0]
        index = random.choice(valid_indices)
        self.skills[index]['requirements_remaining'] -= 1
        return [self.skills[index]['index']]

    def generate_skills(self):
        vehicle_skills = self.vehicles[self.vehicle_index]
        self.vehicle_index += 1
        return vehicle_skills


if __name__ == '__main__':
    generate_sublists = GenerateOverlappingExhaustiveSublists(
        limiter=CountLimit(3),
        base=list(range(10)),
        k=3,
        add_chance=0.8,
        min_representations=1,
        min_length=2
    )

    for sublist in generate_sublists:
        print(sublist)
