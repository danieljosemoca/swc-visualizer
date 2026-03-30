import matplotlib.pyplot as plt
from tree import Node


def plot_tree_2d(nodes: dict[int, Node]):
    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        x_vals = [node._x, node._parent._x]
        y_vals = [node._y, node._parent._y]

        plt.plot(x_vals, y_vals)  # plot a 2D line from current node to its parent node

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("Neuron Morphology 2D")

    plt.show()

