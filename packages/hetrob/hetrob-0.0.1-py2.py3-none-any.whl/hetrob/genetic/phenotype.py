"""
A module, which contains different implementations for Individuals
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Dict
from collections import defaultdict
from hetrob.util import routes_add_depot, iterate_paths
from hetrob.problem import OrderedHeterogeneousSkillTimeConstraintProblem, ProblemType, AbstractProblem

from hetrob.genetic.fitness import FitnessMin
from hetrob.genetic.genotype import AbstractGenotype
from hetrob.genetic.util import StatefulQueue
from hetrob.genetic.evaluate import InfeasibilityPenalty, AbsoluteEndTimeObjective

# ABSTRACT BASE CLASSES
# =====================


class AbstractPhenotype(ABC):

    def __init__(self,
                 problem: ProblemType,
                 genotype: AbstractGenotype):
        self.problem = problem
        self.genotype = genotype

    @abstractmethod
    def evaluate(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def is_feasible(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_penalty(self) -> float:
        raise NotImplementedError()


# SPECIFIC INDIVIDUAL IMPLEMENTATIONS
# ===================================


class OrderedHeterogeneousSkillTimeConstraintPhenotype(AbstractPhenotype):

    # CLASS CONSTANTS
    # ---------------

    PROBLEM_CLASS = OrderedHeterogeneousSkillTimeConstraintProblem
    BIG_INTEGER = 1000000000000000000

    PENALTY_DISTANCE = 1000
    NODE_PENALTY_FUNCTION = lambda self, count: 5 * count ** 2
    TIME_WINDOW_PENALTY_FUNCTION = lambda self, diff: diff ** 2

    objective = InfeasibilityPenalty(
        AbsoluteEndTimeObjective(),
        PENALTY_DISTANCE
    )

    # THE CONSTRUCTOR
    # ---------------

    def __init__(self,
                 problem: PROBLEM_CLASS,
                 genotype: AbstractGenotype):
        AbstractPhenotype.__init__(self, problem, genotype)

        self.fitness = FitnessMin()
        # Here we need to be careful for the indices. The chromosomes themselves only describe the representation of
        # the actual tasks, which means they dont include the depot node. But they start at the index 0 nonetheless,
        # which means we have to convert between the index system of the chromosomes to the index system, which
        # includes the depot by incrementing all by 1. This gets rid of the 0 (depot) from the actual route assignments
        self.routes = []
        for route in self.genotype.decode():
            self.routes.append([node + 1 for node in route])

        # COMPUTED PROPERTIES
        # "full" routes refers to the fact, that these routes actually include the depot node as a start node. This
        # additional representation comes in handy for later calculations
        self.full_routes = routes_add_depot(self.routes, depot_node=0)

        self.feasible = True

        self.edges = self._create_route_edges()
        self.nodes = self._create_nodes()

        self.time_table = self._create_time_table()
        self.infeasible_count = 0
        self.penalty = self._create_penalty()

        self.cost = self.objective(self)

    # PUBLIC METHODS
    # -------------

    def evaluate(self) -> Any:
        return self.cost

    def is_feasible(self) -> bool:
        return self.feasible

    def get_penalty(self) -> Any:
        return self.penalty

    # PROTECTED METHODS
    # -----------------

    def _create_penalty(self):
        for node in self.nodes.values():
            if node['schedule'] is None or node['error']:
                self.infeasible_count += 1

        return self.NODE_PENALTY_FUNCTION(self.infeasible_count)

    def _create_cost(self):
        if self.feasible:
            # Actual process
            schedule_cost = max([end for start, end in self.time_table.values()])
            # time window penalties
            time_window_cost = self._get_time_window_penalty()

            return schedule_cost + time_window_cost
        else:
            return self.PENALTY_DISTANCE

    def _get_time_window_penalty(self):
        cost = 0

        for node in self.nodes.values():
            if node['index'] == 0:
                continue

            tw_start, tw_end = node['time_window'] if node['time_window'] is not None else (0, self.BIG_INTEGER)
            visit_start, visit_end = node['schedule']

            if not tw_start <= visit_start <= tw_end:
                diff = min(abs(visit_start - tw_start), abs(visit_start - tw_end))
                cost += self.TIME_WINDOW_PENALTY_FUNCTION(diff)

        return cost

    def _create_time_table(self):

        buffer = StatefulQueue(lambda edge: edge['to'])
        time_table = {}

        # Putting the initial starting points of all the routes into the buffer
        root = self.nodes[0]
        root['schedule'] = (0, 0)
        for edge in root['next']:
            buffer.add(edge)

        # Actually constructing the time table
        while not buffer.empty() and self.feasible:

            previous_state = hash(buffer)
            iterations = len(buffer)

            for i in range(iterations):

                edge = buffer.pop()
                node = self.nodes[edge['to']]
                previous = self.nodes[edge['from']]

                if edge['to'] == 0:
                    continue

                # Checking for skill matching
                if node['vehicle'] not in self.problem.qualified_vehicles[node['index']]:
                    self.feasible = False
                    self.nodes[node['index']]['error'] = True
                    break

                current_start_time = previous['schedule'][1] + edge['weight']

                _continue, _break = False, False
                for origin, target, delta_min, delta_max, same in node['succeeds']:
                    if self.nodes[origin]['schedule'] is None:
                        _continue = True
                        break

                    else:

                        if same and (self.nodes[origin]['vehicle'] != self.nodes[target]['vehicle']):
                            self.feasible = False
                            self.nodes[target]['error'] = True
                            _break = True
                            break

                        preceding_end_time = self.nodes[origin]['schedule'][1]

                        delta_min = delta_min if delta_min is not None else 0
                        delta_max = delta_max if delta_max is not None else self.BIG_INTEGER

                        if current_start_time < preceding_end_time + delta_min:
                            waiting_time = preceding_end_time + delta_min - current_start_time
                            current_start_time += waiting_time
                            node['waiting'] = waiting_time

                        elif current_start_time > preceding_end_time + delta_max:
                            #print('TOO LATE!')
                            self.feasible = False
                            _break = True
                            break

                if _continue:
                    buffer.add(edge)
                    continue
                if _break:
                    break

                node['schedule'] = (current_start_time, current_start_time + node['cost'])
                time_table[node['index']] = node['schedule']

                for edge in node['next']:
                    buffer.add(edge)

            if hash(buffer) == previous_state:
                # In this case there was no change in the buffer, so we did run into an unresolvable loop
                self.feasible = False
                break

        return time_table

    def _create_route_edges(self):
        edges = []

        for vehicle, route in enumerate(self.full_routes):
            for current, following in iterate_paths(route):
                edges.append({
                    'from':         current,
                    'to':           following,
                    'vehicle':      vehicle,
                    'weight':       self.problem.get_edge_weight(current, following, vehicle)
                })

        return edges

    def _create_nodes(self):
        nodes = defaultdict(lambda: {
            'index':                0,
            'vehicle':              0,
            'previous':             [],
            'next':                 [],
            'succeeds':             [],
            'precedes':             [],
            'time_window':          None,
            'cost':                 None,
            'schedule':             None,
            'waiting':              0,
            'error':                False,
        })

        for edge in self.edges:
            current = edge['from']
            following = edge['to']

            nodes[current]['index'] = current
            nodes[current]['time_window'] = self.problem.get_time_window(current, edge['vehicle'])
            nodes[current]['cost'] = self.problem.get_node_cost(current, edge['vehicle'])
            nodes[current]['next'].append(edge)
            nodes[current]['vehicle'] = edge['vehicle']

            nodes[following]['previous'].append(edge)

        for origin, precedences in enumerate(self.problem.get_precedences()):
            for target, start, end, same in precedences:
                nodes[target]['succeeds'].append((origin, target, start, end, same))
                nodes[origin]['precedes'].append((origin, target, start, end, same))

        return dict(nodes)


class BasicPhenotype(AbstractPhenotype):

    objective = AbsoluteEndTimeObjective()

    def __init__(self,
                 problem: AbstractProblem,
                 genotype: AbstractGenotype):
        AbstractPhenotype.__init__(self, problem, genotype)

        self.fitness = FitnessMin()
        # Here we need to be careful for the indices. The chromosomes themselves only describe the representation of
        # the actual tasks, which means they dont include the depot node. But they start at the index 0 nonetheless,
        # which means we have to convert between the index system of the chromosomes to the index system, which
        # includes the depot by incrementing all by 1. This gets rid of the 0 (depot) from the actual route assignments
        self.routes = []
        for route in self.genotype.decode():
            self.routes.append([node + 1 for node in route])

        # COMPUTED PROPERTIES
        # "full" routes refers to the fact, that these routes actually include the depot node as a start node. This
        # additional representation comes in handy for later calculations
        self.full_routes = routes_add_depot(self.routes, depot_node=0)
        self.nodes = self.create_nodes()

        self.calculate_schedule()

        self.cost = self.objective.evaluate(self)

    # IMPLEMENT "AbstractPhenotype"
    # -----------------------------

    def evaluate(self) -> Any:
        return self.cost

    def is_feasible(self) -> bool:
        return True

    def get_penalty(self) -> float:
        return 0

    # HELPER METHODS
    # --------------

    def create_nodes(self) -> Dict[int, dict]:
        nodes = defaultdict(lambda: {
            'index':                0,
            'vehicle':              0,
            'duration':             0.0,
            'previous':             0,
            'next':                 [],
            'schedule':             (0, 0),
        })

        for vehicle_id, route in enumerate(self.full_routes):

            for current_node, next_node in iterate_paths(route):
                nodes[current_node]['index'] = current_node
                nodes[current_node]['vehicle'] = vehicle_id
                nodes[current_node]['duration'] = self.problem.get_node_cost(current_node)
                nodes[current_node]['next'].append(next_node)

                nodes[next_node]['previous'] = current_node

        return nodes

    def calculate_schedule(self):

        # So to calculate the end times, we need to trace the path of every vehicle. Because obviously the end time of
        # a certain node depends on the node, which was visited before. Here we are collecting all the first nodes on
        # every vehicles path
        node_buffer = self.nodes[0]['next']

        while len(node_buffer) != 0:
            node_id = node_buffer.pop(0)
            previous_node = self.nodes[node_id]['previous']
            previous_end_time = self.nodes[previous_node]['schedule'][1]
            travel_time = self.problem.get_edge_weight(node_id, previous_node)
            node_duration = self.nodes[node_id]['duration']

            self.nodes[node_id]['schedule'] = (
                previous_end_time + travel_time,
                previous_end_time + travel_time + node_duration
            )

            if node_id != 0:
                node_buffer += self.nodes[node_id]['next']
