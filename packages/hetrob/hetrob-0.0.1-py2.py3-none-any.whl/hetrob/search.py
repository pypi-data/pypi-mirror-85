import random
from typing import List, Any

from hetrob.util import random_indices, two_point_reverse


def inter_route_single_move(routes: List[List[Any]], index1: int, index2: int, inplace=False):
    result = routes if inplace else routes.copy()

    try:
        i, = random_indices(result[index1], k=1)
        j, = random_indices(result[index2], k=1)
    except IndexError:
        return result

    if random.randint(0, 1):
        value = result[index1].pop(i)
        result[index2].insert(j, value)
    else:
        value = result[index2].pop(j)
        result[index1].insert(i, value)

    return result


def inter_route_single_swap(routes: List[List[Any]], index1: int, index2: int, inplace=False):
    result = routes if inplace else routes.copy()

    try:
        i, = random_indices(result[index1], k=1)
        j, = random_indices(result[index2], k=1)
    except IndexError:
        return result

    result[index1][i], result[index2][j] = result[index2][j], result[index1][i]

    return result


def intra_route_single_swap(route: [List[Any]], inplace=False):
    if len(route) < 2:
        return route

    result = route if inplace else route.copy()

    i, j = random_indices(result, k=2)
    result[i], result[j] = result[j], result[i]

    return result


def intra_route_two_point_reverse(route: List[Any], inplace=False):
    if len(route) < 2:
        return route

    result = route if inplace else route.copy()

    return two_point_reverse(result)



