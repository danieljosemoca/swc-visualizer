import matplotlib.pyplot as plt
import plotly.graph_objects as go
from tree import Node
from typing import Callable


def plot_2d(
    nodes: dict[int, Node],
    color_method: Callable[[Node], float] = Node.length_from_root,
) -> None:
    """
    Plots the tree in 2D.

    Inputs:
    nodes: dict[int, Node]
        Mapping from node index to Node object outputted by dataframe_to_tree().
    color_method: Callable[[Node], float]
        Method to determine the color of each segment. Should take a Node as input and output a float.
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

    plt.xlabel("Relative X Position")
    plt.ylabel("Relative Y Position")
    plt.title("Neuron Morphology 2D")
    plt.axis("equal")  # keeps scale of axes equal (not so 2D otherwise)

    # colorbar
    plt.colorbar(
        plt.cm.ScalarMappable(cmap=cmap),
        ax=plt.gca(),
        label=f"scaled {color_method.__name__}() value",
    )
    plt.show()


def plot_3d(
    nodes: dict[int, Node],
    color_method: Callable[[Node], float] = Node.length_from_root,
) -> None:
    """
    Plots the tree in 3D.

    Inputs:
    nodes: dict[int, Node]
        Mapping from node index to Node object outputted by dataframe_to_tree().
    color_method: Callable[[Node], float]
        Method to determine color of each segment. Should take a Node as input and output a float.
    """

    # dictionary with output by the color method, for each node
    col_values = {node: color_method(node) for node in nodes.values()}
    max_col_value = max(col_values.values())  # to normalize color range later

    if max_col_value == 0:
        max_col_value = 1.0  # avoid zerodivisionerror when scaling

    # will store the two endpoints of each segment here,
    # in separate lists per dimension
    edge_x, edge_y, edge_z = [], [], []
    edge_colors = []
    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        # compute this segment's color, scaled to [0, 1]
        norm_col_val = col_values[node] / max_col_value

        # =endpoint 1 of this segment=
        edge_x.append(node._x)
        edge_y.append(node._y)
        edge_z.append(node._z)
        edge_colors.append(norm_col_val)

        # =endpoint 2 of this segment=
        edge_x.append(node._parent._x)
        edge_y.append(node._parent._y)
        edge_z.append(node._parent._z)
        edge_colors.append(norm_col_val)  # appended again so edge has uniform color

        # Separators so plotly knows we need a separate edge drawn next loop
        edge_x.append(None)
        edge_y.append(None)
        edge_z.append(None)
        edge_colors.append(0)

    # plot all the segments as a polyline
    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode="lines",
            line=dict(
                color=edge_colors,
                colorscale="agsunset",
                width=3,
                showscale=True,
                colorbar=dict(  # color scale in the legend
                    title=dict(
                        text=(f"scaled {color_method.__name__}() value"),
                        font=dict(size=15),
                        side="right",
                    ),
                ),
            ),
        )
    )
    fig.show()
