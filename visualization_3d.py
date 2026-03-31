import plotly.graph_objects as go
from tree import Node
from typing import Callable


def plot_3d(
    nodes: dict[int, Node],
    color_method: Callable[[Node], float] = Node.distance_to_root,
):

    # dictionary with values used for coloring
    values = {node: color_method(node) for node in nodes.values()}
    max_value = max(values.values())  # needed to normalize color range later

    # will store the two endpoints of each segment here,
    # in separate lists per dimension
    # and "None" separating each segment
    edge_x, edge_y, edge_z = [], [], []
    edge_colors = []
    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        # endpoint 1 of this segment
        edge_x.append(node._x)
        edge_y.append(node._y)
        edge_z.append(node._z)

        # endpoint 2 of this segment
        edge_x.append(node._parent._x)
        edge_y.append(node._parent._y)
        edge_z.append(node._parent._z)

        # computed color normalized to [0, 1]
        try:
            edge_colors.append(values[node] / max_value)
            edge_colors.append(values[node] / max_value)
        except ZeroDivisionError:
            edge_colors.append(1)
            edge_colors.append(1)

        # at end of loop we append None to separate each segment
        edge_x.append(None)
        edge_y.append(None)
        edge_z.append(None)
        # colors does not accept None so we use 0 as placeholder
        edge_colors.append(0)

    # plot time
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
                colorbar=dict(
                    title=dict(
                        text=(f"scaled {color_method.__name__} output"),
                        font=dict(size=15),
                        side="right",
                    ),
                ),
            ),
        )
    )
    fig.show()
