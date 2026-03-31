import plotly.graph_objects as go
from tree import Node
from matplotlib import cm
from matplotlib.colors import to_hex


def plot_3d(nodes: dict[int, Node]):
    fig = go.Figure()
    root = next(node for node in nodes.values() if node._parent is None)

    # dict[node: distance in micrometers from the root node]
    distances = {node: node.distance(root) for node in nodes.values()}
    max_dist = max(distances.values())  # needed to normalize distance from root

    for node in nodes.values():
        if node._parent is None:
            continue  # skip root node

        # coordinates for segment from current node to its parent node
        x_vals = [node._x, node._parent._x]
        y_vals = [node._y, node._parent._y]
        z_vals = [node._z, node._parent._z]

        # normalized distance from the root (for color)
        norm_dist = (distances[node] / max_dist)

        # specific color based on that distance value
        rgba = cm.get_cmap("cividis")(norm_dist)
        color = to_hex(rgba)

        # plot time
        fig.add_trace(go.Scatter3d(
                x=x_vals,
                y=y_vals,
                z=z_vals,
                mode='lines',
                line=dict(
                    color=color,
                    width=3
                ),
                showlegend=False
            ))
    fig.show()