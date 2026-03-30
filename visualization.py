import matplotlib.pyplot as plt
from tree import Node


def plot_tree_2d(nodes: dict[int, Node]):
    root = next(node for node in nodes.values() if node._parent is None)

    # needed to normalize distance from root
    max_dist = max(node.distance(root) for node in nodes.values())
    cmap = plt.colormaps["copper"]

    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        x_vals = [node._x, node._parent._x]
        y_vals = [node._y, node._parent._y]

        distance_from_root = node.distance(root)

        # pick color in colormap using normalized distance from root
        color = cmap(distance_from_root / max_dist)

        # plot a 2D line from current node to its parent node
        # color from normalized distance from root
        plt.plot(x_vals, y_vals, color=color)

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("Neuron Morphology 2D")
    plt.axis("equal")  # keeps scale of axes equal (not so 2D otherwise)

    plt.show()
