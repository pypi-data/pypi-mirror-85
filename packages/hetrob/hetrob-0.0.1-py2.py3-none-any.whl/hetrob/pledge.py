from typing import List, Tuple, Dict, Type, Set, ClassVar
from abc import ABC, abstractmethod, abstractclassmethod

from hetrob.util import iterate_paths, to_snake_case


class Pledge(ABC):

    generalizes: ClassVar[Set[str]] = set()
    # specializes: ClassVar[Set[str]] = set()

    def pledges(self, *klasses: Type):
        for klass in klasses:
            if klass.__name__ not in self.generalizes:
                klass_names = map(lambda k: k.__name__, klasses)
                message = 'The following pledges are required {} but {} does not generalize {}'.format(
                    ', '.join(klass_names),
                    self.__class__.__name__,
                    klass.__name__
                )
                raise NotImplementedError(message)
        return True


def generalize(base_class: Type[Pledge]):

    def decorator(klass: Type[Pledge]):

        class NewKlass(base_class):
            pass

        NewKlass.__name__ = klass.__name__

        NewKlass.generalizes.add(base_class.__name__)
        NewKlass.generalizes.add(klass.__name__)

        # Dynamically add the method
        def from_base(cls, base: base_class) -> NewKlass:
            raise NotImplementedError()

        # TODO: this is not very understandable. Clean up
        method_name = 'from_' + to_snake_case(base_class.__name__).replace('_pledge', '_problem')
        method = abstractclassmethod(from_base)
        method.__name__ = method_name
        # print(method_name)
        setattr(NewKlass, method_name, method)

        return NewKlass

    return decorator


# THE ACTUAL PLEDGES
# ------------------


class NodePledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_nodes(self) -> List[int]:
        raise NotImplementedError()

    # UTILITY METHODS
    # ---------------

    def get_node_count(self) -> int:
        return len(self.get_nodes())


class VehiclePledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_vehicles(self) -> List[int]:
        raise NotImplementedError()

    # UTILITY METHODS
    # ---------------

    def get_vehicle_count(self) -> int:
        return len(self.get_vehicles())


@generalize(NodePledge)
class BasicGraphPledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_edge_weight(self, node1: int, node2: int) -> float:
        raise NotImplementedError()

    def get_node_profit(self, node: int) -> float:
        raise NotImplementedError()

    def get_node_cost(self, node: int) -> float:
        raise NotImplementedError()


@generalize(NodePledge)
class FleetPledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_vehicles(self) -> List[int]:
        raise NotImplementedError()

    # STANDARD IMPLEMENTATIONS
    # ------------------------

    def get_vehicle_count(self) -> int:
        return len(self.get_vehicles())


@generalize(FleetPledge)
@generalize(BasicGraphPledge)
class HeterogeneousGraphPledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_edge_weight(self, node1: int, node2: int, vehicle: int) -> float:
        raise NotImplementedError()

    def get_node_profit(self, node: int, vehicle: int) -> float:
        raise NotImplementedError()

    def get_node_cost(self, node: int, vehicle: int) -> float:
        raise NotImplementedError()


@generalize(BasicGraphPledge)
class BasicPrecedencePledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def precedes(self, node1: int, node2: int) -> bool:
        raise NotImplementedError()

    # STANDARD IMPLEMENTATIONS
    # ------------------------

    def get_precedences(self) -> List[List[int]]:
        nodes = self.get_nodes()
        precedences = [[] for _ in nodes]

        for node1 in nodes:
            for node2 in nodes:
                if self.precedes(node1, node2):
                    precedences[node2].append(node1)

        return precedences


@generalize(BasicPrecedencePledge)
class WindowedPrecedencePledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_precedence_window(self, node1: int, node2: int) -> Tuple[float, float]:
        raise NotImplementedError()

    # STANDARD IMPLEMENTATIONS
    # ------------------------

    def get_precedences(self) -> List[List[Tuple[int, float, float]]]:
        nodes = self.get_nodes()
        precedences = [[] for _ in nodes]

        for node1 in nodes:
            for node2 in nodes:
                if self.precedes(node1, node2):
                    start, end = self.get_precedence_window(node1, node2)
                    precedences[node2].append((node1, start, end))

        return precedences


@generalize(HeterogeneousGraphPledge)
class TimeWindowPledge(Pledge):

    # TO BE IMPLEMENTED
    # -----------------

    def get_time_window(self, node: int, vehicle: int) -> Tuple[float, float]:
        raise NotImplementedError()
