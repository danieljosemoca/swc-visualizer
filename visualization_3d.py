import plotly.graph_objects as go
from tree import Node
from matplotlib import cm
from matplotlib.colors import to_hex
from typing import Callable


def plot_3d(nodes: dict[int, Node], color_method: Callable[[Node], float] = Node.distance_to_root):
    fig = go.Figure()
    root = next(node for node in nodes.values() if node._parent is None)

    # dictionary with values used for coloring
    values = {node: color_method(node) for node in nodes.values()}
    max_value = max(values.values())  # needed to normalize color range later

    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        # coordinates for segment from current node to its parent node
        x_vals = [node._x, node._parent._x]
        y_vals = [node._y, node._parent._y]
        z_vals = [node._z, node._parent._z]

        # computed color normalized to [0, 1]
        try: 
            norm_value = values[node] / max_value
        except ZeroDivisionError: 
            norm_value = values[node] / 1

        # now RGB color via colormap
        rgba = cm.get_cmap("cividis")(norm_value)
        color = to_hex(rgba)

        # plot time
        fig.add_trace(
            go.Scatter3d(
                x=x_vals,
                y=y_vals,
                z=z_vals,
                mode="lines",
                line=dict(color=color, width=3),
                showlegend=False,
            )
        )
    fig.show()
