"""
Module for the visualization of results.
"""
import math
from typing import Tuple, List, Callable, Optional, Dict, Any, Sequence

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import ArrowStyle

from hetrob.util import d2

# VISUALIZATION OF GRAPHS
# =======================
# this section is about the visualization of network graphs(!). This includes for example the utilities needed to
# visualize the routing of the vehicles within an individual solution or the precedence relationships for
# problem instances etc.

# VISUALIZATION WITH MATPLOTLIB
# This section is specifically about the functions to make a visualization with matplotlib

# HELPER FUNCTIONS
# ----------------

def axes_scatter_coords(axes: plt.Axes, coords: Tuple[float, float], **kwargs) -> plt.Axes:
    """
    Modifies the given axes object by adding a single scatter point according to the given coordinates.

    :param axes:
    :param coords:
    :param kwargs:
    :return:
    """
    # Here we create two numpy arrays with each one element, because the "scatter" function expects numpy arrays.
    x = np.array([coords[0]])
    y = np.array([coords[1]])
    axes.scatter(x, y, **kwargs)

    return axes


def axes_arrow_between(axes: plt.Axes,
                       origin: Tuple[float, float],
                       target: Tuple[float, float],
                       **kwargs) -> plt.Axes:
    """
    Modifies the given axes object by adding an arrow between the given origin and target coordinates. The arrow
    can be further modified by passing keyword arguments.

    :param axes:
    :param origin:
    :param target:
    :param kwargs:
    :return:
    """
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    length = math.sqrt(dx ** 2 + dy ** 2)
    axes.arrow(
        x=origin[0],
        y=origin[1],
        dx=dx,
        dy=dy,
        length=length,
        **kwargs
    )

    return axes


def axes_descent_between(axes: plt.Axes,
                         origin: Tuple[float, float],
                         target: Tuple[float, float],
                         width: float,
                         **kwargs) -> plt.Axes:
    """
    Modifies the given axes object by adding a "descent" between the given origin and target coordinates. The arrow
    can be further modified by passing keyword arguments.

    A "descent" essentially is an arrow with out a body. It is just an arrow head, which starts with the full `width`
    at the `origin` and then narrows down along the path towards the `target`

    :param axes:
    :param origin:
    :param target:
    :param width:
    :param kwargs:
    :return:
    """
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    length = math.sqrt(dx ** 2 + dy ** 2)
    axes.arrow(
        x=origin[0],
        y=origin[1],
        dx=dx,
        dy=dy,
        head_length=length,
        length_includes_head=True,
        width=0.1 * width,
        head_width=width,
        **kwargs
    )

    return axes


def path_between(origin: Tuple[float, float],
                 target: Tuple[float, float]) -> Path:
    """
    Given two coordinate tuples for the origin and the destination of a path, this method will create a
    `matplotlib.path.Path` object between the two points on the axes.

    :param origin:          The tuple of two numeric values specifying the point in space where the path is to start
    :param target:          The tuple of two numeric values specifying the point in space where the path ends
    """
    vectors = [origin, target]
    codes = [Path.MOVETO, Path.LINETO]

    path = Path(vectors, codes)
    return path


def axes_line_between(axes: plt.Axes,
                      origin: Tuple[float, float],
                      target: Tuple[float, float],
                      **kwargs):
    """
    Given an `Axes` object and two points in the coordinate system, this method will draw a simple line between these
    points onto the axes.

    The additional keyword arguments of this function will be directly passed to the constructor of the
    `matplotlib.patches.PathPatch` object, which is used to draw the path onto the axes.

    :param axes:            The coordinate system onto which the line is to be drawn
    :param origin:          Tuple of two numeric values for the coordinates of the start of the line
    :param target:          Tuple of two numeric values for the coordinates of the end of the line
    """
    path = path_between(origin, target)

    patch = matplotlib.patches.PathPatch(path, **kwargs)
    axes.add_patch(patch)

    return axes


def axes_bracket_between(axes: plt.axes,
                         origin: Tuple[float, float],
                         target: Tuple[float, float],
                         width: float = 2.0,
                         **kwargs):
    """
    Given an `Axes` object and two points in the coordinate system, this method will draw a bracket between those
    two points. A bracket means a line between the two points with two orthogonal lines at the ends like this |----|

    The additional keyword arguments for this function are directly passed to the creation of the
    `matplotlib.patches.FancyArrowPatch` which is used to draw onto the axes.

    :param axes:            The coordinate system onto which to draw
    :param origin:          Tuple of two numeric values representing the starting point for the bracket
    :param target:          Tuple of two numeric values representing the end point of the bracket
    :param width:           The height of the two orthogonal lines at the ends of the bracket
    """
    path = path_between(origin, target)

    arrow_style = ArrowStyle.BarAB(widthA=width, widthB=width)
    patch = matplotlib.patches.FancyArrowPatch(path=path, arrowstyle=arrow_style, **kwargs)
    axes.add_patch(patch)

    return axes


def axes_add_coordinates(axes: plt.Axes,
                         coordinates: List[Tuple[float, float]],
                         additional_kwargs: Callable = lambda index, coords: {},
                         additional_actions: Callable = lambda axes, index, coords: None):
    """
    Adds all the given coordinates to the given axes object. Also offers the option of passing the `additional_kwargs`
    callback, which accept the index and the coordinates to return a custom dict of additional kwargs for the call
    to the scatter function. Also the `additional_actions` callback is called for every coordinate with the axes object,
    the index and the coordinates to possible add additional elements to the plot.

    :param axes:
    :param coordinates:
    :param additional_kwargs:
    :param additional_actions:
    :return:
    """
    for node, coords in enumerate(coordinates):
        kwargs = additional_kwargs(node, coords)
        axes_scatter_coords(axes, coords, **kwargs)

        additional_actions(axes, node, coords)

    return axes


def get_false(*args, **kwargs):
    return False

def get_color_black(*args, **kwargs):
    return 'black'

def get_color_red(*args, **kwargs):
    return 'red'

def get_coords_string(coords: Tuple[float, float], *args, **kwargs):
    return '({}, {})'.format(*coords)


# THE PLOTTER CLASSES
# ===================

class ProblemPlotter:

    def plot_coordinates(self,
                         coordinates: List[Tuple[float, float]],
                         axes: Optional[plt.Axes] = None,
                         get_node_kwargs: Callable = lambda coords, index: {},
                         get_node_label: Callable = lambda coords, index: '',
                         plot_additional: Callable = lambda axes, coordinates, coords, index: None,):
        ax = plt.axes() if axes is None else axes

        for index, coords in enumerate(coordinates):
            # Drawing the actual node
            kwargs = get_node_kwargs(coords, index)
            axes_scatter_coords(ax, coords, **kwargs)

            # Drawing the label
            label = get_node_label(coords, index)
            if label:
                ax.text(coords[0], coords[1], label, fontsize=10, **kwargs)

            # Arbitrary additional actions
            plot_additional(ax, coordinates, coords, index)

        return ax

    def plot_coordinates_fancy(self,
                               coordinates: List[Tuple[float, float]],
                               axes: Optional[plt.Axes] = None,
                               get_node_kwargs: Callable = lambda coords, index: {},
                               get_node_label: Callable = lambda coords, index: ''):

        ax = plt.axes() if axes is None else axes

        default_kwargs = {
            'radius': 5
        }

        for index, coords in enumerate(coordinates):
            # Drawing the actual node
            kwargs = default_kwargs.copy()
            kwargs.update(get_node_kwargs(coords, index))
            circle = plt.Circle(coords, **kwargs)
            ax.add_artist(circle)

            if 'label' in kwargs:
                ax.text(
                    coords[0] + kwargs['radius'],
                    coords[1] + kwargs['radius'],
                    kwargs['label'],
                    fontsize=10
                )

        return ax

    def axes_add_precedences(self,
                             axes: plt.Axes,
                             coordinates: List[Tuple[float, float]],
                             precedences: List[List[Tuple[int, float, float, bool]]],
                             get_color: Callable = get_color_red,
                             get_label: Callable = get_false):

        for current, precedes in enumerate(precedences):
            current_coords = coordinates[current]

            for following, start, end, same in precedes:
                following_coords = coordinates[following]

                # Drawing the actual label
                color = get_color(current, current_coords, following, following_coords, start, end)
                axes_descent_between(axes, current_coords, following_coords, 1.2, color=color)

                # TODO: Draw the label

        return axes


class RoutePlotter:
    """
    This class wraps various functions for plotting the routes of an optimization result using `matplotlib`
    """
    # STATIC FUNCTION CONSTANTS
    # -------------------------
    # These methods here are defined here, as the first methods even before the constructor because they are supposed
    # to be used as default parameters for other methods down the line. These other methods will require callable
    # objects as arguments and these arguments are supposed to be optional. We define whole functions here as sort of
    # "constants" to be used in the default case, because their behaviour is to complex for a simple lambda.
    # This is also the reason, why the functions are in upper case. They are more like class constants, than actual
    # methods.


    def GET_MARKER_CIRCLE(vehicle: int, current: int, following: int):
        return 'o'

    def GET_MARKER_DEPOT_SQUARE(vehicle: int, current: int, following: int):
        if current == 0:
            return 's'
        else:
            return 'o'

    def GET_COLOR_BLACK(vehicle: int, current: int, following: int):
        return 'black'

    def GET_ALPHA_ONE(vehicle: int, current: int, following: int):
        return 1.0

    def DRAW_DESCENT(axes: plt.Axes,
                     vehicle: int,
                     current_coords: Tuple[float, float],
                     following_coords: Tuple[float, float],
                     color):
        return axes_descent_between(axes, current_coords, following_coords, 0.4, color=color)

    # THE CONSTRUCTOR
    # ---------------

    def __init__(self):
        pass

    def plot_routes(self,
                    routes: List[List[int]],
                    coordinates: List[Tuple[float, float]],
                    axes: Optional[plt.Axes] = None,
                    return_start: bool = True,
                    get_node_marker: Callable = GET_MARKER_DEPOT_SQUARE,
                    get_node_color: Callable = GET_COLOR_BLACK,
                    get_node_alpha: Callable = GET_ALPHA_ONE,
                    get_label: Optional[Callable] = None,
                    draw_edge: Callable = DRAW_DESCENT):
        """
        Plots the given routes.

        Design Choice
        -------------
        This method has a very general implementation, considering all the custom functions, which can be passed in
        as arguments to customize behaviour. This makes this function server as a basis for all the more specialized
        functions, which this class offers. As every specific behaviour only presents some sort of specialization of
        the generic behaviour for this class. But is also serves the user; in case some special functionality is
        needed and not yet offered by other functions of this class, this method can be used.
        Although using it for everything is discouraged, as simple plots are not as straight forward as they could be.

        :param routes:                  A list of list of ints. Each sub list within this list represents a separate
                                        route. Each integer within this route is the ID of a node, which is visited as
                                        part of the route. The order of the integers in the list is the order of
                                        visits.
        :param coordinates:             A list of tuples of two numeric values. The tuples represent the coordinates of
                                        the nodes within a route. Each index in this list represents the integer ID
                                        of the node
        :param axes:                    Optionally an Axes object can be passed in. In this case the plot is drawn
                                        onto that axes. Otherwise a new one is created and returned.
        :param return_start:            A boolean flag, which indicates, whether or not to display a path, which leads
                                        from the last node in any of the routes back to the first node in the route
        :param get_node_marker:         Function, which accepts the parameters route index, current node ID, ID of the
                                        next node in the route. Is supposed to return a string which defines the
                                        look of the current node
        :param get_node_color:          Function, which accepts the parameters route index, current node ID, ID of the
                                        next node in the route. Returns a string which will define the color of the
                                        current node.
        :param get_node_alpha:          Function, which accepts the parameters route index, current node ID, ID of the
                                        next node in the route. Returns a float value between 0 and 1, which defines
                                        the alpha channel(opacity) for the display of the current node
        :param get_label:               Optional Function, which accepts the parameters route index, current node ID,
                                        ID of the next node in the route. Returns a string, which will be displayed
                                        next to the node within the coordinate system, acting as a label.
        :param draw_edge:               A function, which accepts the axes object, route index, current node ID,
                                        next node ID and color. This function is supposed to actually draw the edge
                                        between the two nodes, which are defined as current and next within the
                                        current route.
        """
        # In case an Axes object is passed in from the outside we will use that to draw on.
        ax = plt.axes() if axes is None else axes

        for vehicle, route in enumerate(routes):

            for current, following in zip(route, np.roll(route, -1)):

                current_coords = coordinates[current]
                following_coords = coordinates[following]

                # DRAWING THE POINT
                # marker and color for the node are generated by the corresponding functions.
                # The function "axes_scatter_coords" takes an axes object and applies a scatter plot to it with
                # exactly a single data point at the position of the given coordinates tuple.
                marker = get_node_marker(vehicle, current, following)
                color = get_node_color(vehicle, current, following)
                alpha = get_node_alpha(vehicle, current, following)
                axes_scatter_coords(ax, current_coords, marker=marker, color=color, alpha=alpha)
                # A "label" is an additional piece of text, which can be added to each node. The text would then appear
                # slightly beside the actual node.
                # The adding of a label is optional and only done if a function is passed for the "get_label" argument.
                # The text will then be generated according to this function.
                if get_label is not None:
                    label = get_label(vehicle, current, following)
                    axes.text(current_coords[0] + 0.2, current_coords[1] + 0.2, label, color=color, fontsize=10)

                # In the case that the next node (which is the route TO which a line would be drawn) is actually the
                # very first node in the route, that would mean that in this current iteration we would be drawing the
                # line, which would close the loop -> going back to the start.
                # This behaviour is controlled by the "return_start" flag. If this flag is false, we dont actually want
                # the path to return to the original node. In this case we are just going to skip the drawing process
                # of the line.
                if not return_start and following == route[0]:
                    continue

                # DRAWING THE CONNECTION
                # In drawing the edge there is the greatest freedom for the user
                ax = draw_edge(ax, vehicle, current_coords, following_coords, color)

        return ax


class SchedulePlotter:
    """
    This class wraps various functions for plotting the schedules of an optimization result using `matplotlib`
    """
    # STATIC FUNCTION CONSTANTS
    # -------------------------
    # These methods here are defined here, as the first methods even before the constructor because they are supposed
    # to be used as default parameters for other methods down the line. These other methods will require callable
    # objects as arguments and these arguments are supposed to be optional. We define whole functions here as sort of
    # "constants" to be used in the default case, because their behaviour is to complex for a simple lambda.
    # This is also the reason, why the functions are in upper case. They are more like class constants, than actual
    # methods.

    def GET_COLOR_BLACK(vehicle: int, node: int, start: float, end: float):
        return 'black'

    def GET_LABEL_VEHICLE(vehicle: int):
        return str(vehicle)

    def GET_TEXT_NODE(vehicle: int, node: int, start: float, end: float):
        return str(node)

    # THE CONSTRUCTOR
    # ---------------

    def __init__(self):
        pass

    # PUBLIC METHODS
    # --------------

    def increment_vertically(self,
                             items: Sequence[Any],
                             y_start: float = 2,
                             y_step: float = 2):
        """
        Iterates a list of given `items` while also simultaneously incrementing a y variable in each iteration.
        The method works as a generator, which during each iteration yields a tuple of the item of the given sequence
        and the current value of the y variable

        Explanation
        -----------
        So what is the purpose of this function? The general problem with creating Gantt chart style plots for the
        visualization of timing/schedules is that they are organized in fixed rows on the y-axis usually. Creating
        these discrete rows from continuous coordinates is a task which all the of the schedule plots will have in
        column. So this function provides a means of simplifying the overhead for keeping track of the vertical row
        position.

        :param items:               The sequence of items to be iterated for each row
        :param y_start:             The float value for the initial value of the y variable
        :param y_step:              The float value for the step size of the y variable
        """
        y = y_start
        for item in items:
            yield item, y
            y += y_step

    def plot_schedules(self,
                       time_table: Dict[int, Tuple[float, float]],
                       full_routes: List[List[int]],
                       include_first: bool = False,
                       get_color: Callable = GET_COLOR_BLACK,
                       get_label: Callable = GET_LABEL_VEHICLE,
                       get_text: Optional[Callable] = None,
                       min_length: float = 1,
                       plot_additional: Optional[Callable] = None):
        """
        Plots the schedules of the given `full_routes` into a Gantt chart like plot.

        :param time_table:              A dict, whose keys are the integer ID's of the nodes and the values are tuples,
                                        where the first value is the absolute start time of the job and the second value
                                        the absolute end time of the job.
        :param full_routes:             A list of list of ints. Each sub list within this list represents a separate
                                        route. Each integer within this route is the ID of a node, which is visited as
                                        part of the route. The order of the integers in the list is the order of
                                        visits.
        :param include_first:           A boolean flag, which indicates, whether or not the very first node in each
                                        of the routes is supposed to be included in the plot or not. (If the routes
                                        use the depot assumption it is better to not include the first node (=depot))
        :param get_color:               A Function, which accepts the current route index, the current node ID and its
                                        float start and end times. Returns a string which defines the color of the line
                                        of the current node.
        :param get_label:               A function which accepts the current route index and returns a string, which
                                        is supposed to be describe the current route and thus the row in the schedule
                                        plot. The label will be used to label the y-axis of the plot
        :param get_text:                A Function, which accepts the current route index, the current node ID and its
                                        float start and end times. Returns a string, which will be displayed as a label
                                        for each schedule line lightly beneath it.
        :param plot_additional:         A function, which will accept the axes object, the current route index, the
                                        current node ID, the float start and end time of the node and the current
                                        y position value for the row. Can draw any additional custom content to
                                        the axes object.
        """
        ax = plt.axes()

        y_start = 0
        y_step = 1

        y_lim = 0
        x_lim = 0

        # The y axis will be discretely partitioned into the individual rows. Each row represents the time line of
        # one schedule.
        # This list will contain the labels, which are being put onto the y axis to describe the individual rows.
        # These names will be generated within the loop.
        labels = []

        for vehicle, (route, y) in enumerate(self.increment_vertically(full_routes,
                                                                       y_start=y_start,
                                                                       y_step=y_step)):
            # The "get_label" function is supposed to return a descriptive string label for each of routes, which
            # is then saved within the "labels" list so this list can later be used to set the axis labels of the
            # axes object.
            label = get_label(vehicle)
            labels.append(label)

            # In case the "include_first" flag is true that indicates that the first node in every route is supposed
            # to be included in the schedule, if it is false, that means we leave out the first node.
            for node in (route if include_first else route[1:]):

                # To draw the line, which symbolizes the visit of a node within the plot, an origin and destination
                # coordinate tuple are required. On the y axis the coordinate obviously is the same, but on the x
                # axis (which is the time line) it is equal to start and end time.
                start, end = time_table[node]
                duration = end - start
                origin = (start, y)
                target = (max(start + duration, start + min_length), y)

                color = get_color(vehicle, node, start, end)

                ax = axes_line_between(ax, origin, target, lw=10, color=color)

                # In case the optional "get_text" function is not none, it is used to retrieve a descriptive string
                # for each node visit. This string will then be added to the plot slightly below the line, which
                # represents the corresponding visit
                if get_text is not None:
                    text = get_text(vehicle, node, start, end)
                    x_text = (start + end) / 2
                    y_text = y - y_step * 0.2
                    ax.text(x_text, y_text, text, color=color, fontsize=10)

                # The "plot_additional" arg is an optional function, which gets passed all the relevant values of the
                # current state and the axes object itself to add some custom objects to the plot
                if plot_additional is not None:
                    plot_additional(ax, vehicle, node, start, end, y)

                x_lim = end if end > x_lim else x_lim

            y_lim = y if y > y_lim else y_lim

        ax.set_xlim(0, x_lim * 1.05)
        ax.set_ylim(y_start - 0.5 * y_step, y_lim + 0.5 * y_step)

        # This will set the custom labels for the vertical rows
        ax.set_yticks(range(y_start, y_lim + y_step, y_step))
        ax.set_yticklabels(labels)

        return ax


class EvolutionPlotter:
    """
    This class wraps various functions for plotting the evolution of an optimization process using `matplotlib`
    """
    def __init__(self):
        pass

    def plot_fitness(self,
                     data: Sequence[float],
                     axes: Optional[plt.Axes] = None,
                     **kwargs):
        ax = plt.axes() if axes is None else axes

        length = len(data)
        x = np.linspace(0, length, num=length)
        y = np.array(list(data))

        ax.plot(x, y, **kwargs)

        return ax

    def plot_fitness_absolute(self,
                              data: Sequence[float],
                              axes: Optional[plt.Axes] = None,
                              compare: Callable = min,
                              **kwargs):
        ax = plt.axes() if axes is None else axes

        length = len(data)
        x = np.linspace(0, length, num=length)
        y = np.zeros(shape=length)

        min_fitness = data[0]
        for index, value in enumerate(data):
            min_fitness = compare(min_fitness, value)
            y[index] = min_fitness

        ax.plot(x, y, **kwargs)

        return ax


# PLOTTING EXPERIMENT STATISTICS
# ==============================


class StatisticsPlotter(object):

    def __init__(self):
        pass

    # CLASS METHODS
    # -------------

    @classmethod
    def plot_plain(cls,
                   data: Dict[str, Dict[str, Dict[str, float]]],
                   key: str,
                   axes: Optional[plt.Axes] = None,
                   colors: Optional[Dict[str, str]] = None):
        ax = plt.axes() if axes is None else axes

        for algorithm_name, instance_data in data.items():
            instances = list(instance_data.keys())
            x = cls.calc_x_from_instances(instances)
            ax.set_xticks(x)
            y = np.array([stats[key] for instance_name, stats in instance_data.items()])

            if colors is None:
                line, = ax.plot(x, y)
            else:
                line, = ax.plot(x, y, color=colors[algorithm_name])

            line.set_label(algorithm_name)

        return ax

    @classmethod
    def plot_fancy(cls,
                   data: Dict[str, Dict[str, Dict[str, float]]],
                   axes: Optional[plt.Axes] = None):
        ax = plt.axes() if axes is None else axes



    # UTILITY METHODS
    # ---------------

    @classmethod
    def calc_x_from_instances(cls, instances: List[str]) -> np.array:
        return np.array(range(1, len(instances) + 1))


