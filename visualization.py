import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tree import Node
from typing import Callable


def plot_2d(
    nodes: dict[int, Node],
    color_method: Callable[[Node], float] = Node.distance_from_root,
) -> None:
    """
    Plots the tree in 2D.

    Inputs:
    nodes: dict[int, Node]
        Mapping from node index to Node object outputted by dataframe_to_tree().
    color_method: Callable[[Node], float]
        Method to determine color of each segment. Should take a Node as input and output a float.
    """

    # needed to scale color method outputs
    max_value = max(color_method(node) for node in nodes.values())
    cmap = plt.colormaps["plasma"]  # choose a pretty colormap

    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        x_vals = [node._x, node._parent._x]
        y_vals = [node._y, node._parent._y]

        distance_from_root = color_method(node)

        # pick color in colormap using scaled color method output
        color = cmap(distance_from_root / max_value)

        # plot a 2D line from current node to its parent node
        # color using colormap value
        plt.plot(x_vals, y_vals, color=color)

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("Neuron Morphology 2D")
    plt.axis("equal")  # keeps scale of axes equal (not so 2D otherwise)

    # colorbar
    plt.colorbar(
        plt.cm.ScalarMappable(cmap=cmap),
        ax=plt.gca(),
        label=f"scaled {color_method.__name__}() value",
    )
    plt.show()
