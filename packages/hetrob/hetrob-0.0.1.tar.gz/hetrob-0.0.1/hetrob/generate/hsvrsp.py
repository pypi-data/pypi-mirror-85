from typing import Callable, Generator

from hetrob.generate.util import (START_OF_TIME,
                                  END_OF_TIME,
                                  AbstractGenerate)


def generate_hsvrsp(generate_depot: AbstractGenerate,
                    generate_nodes: AbstractGenerate,
                    generate_vehicles: AbstractGenerate,
                    generate_cooperative_nodes: AbstractGenerate,
                    generate_precedence_nodes: AbstractGenerate):
    """
    lol
    """
    doc = "lol"

    vehicles = {}
    # Creating the vehicles
    for index, vehicle in enumerate(generate_vehicles):
        vehicles[str(index)] = vehicle

    # Generating the depot node
    depot_name, depot_node = next(generate_depot)
    nodes = {
        depot_name: depot_node
    }

    # Adding the "normal" nodes
    for name, node in generate_nodes:
        nodes[name] = node

    # Adding the cooperative nodes
    for name, node in generate_cooperative_nodes:
        nodes[name] = node

    # Adding the nodes connected by precedence constraints
    for name, node in generate_precedence_nodes:
        nodes[name] = node

    return {
        'nodes':    nodes,
        'vehicles': vehicles,
        'doc':      doc
    }
