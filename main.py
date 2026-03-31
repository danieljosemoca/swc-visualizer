import pandas as pd

from tree import Node
from visualization import plot_tree_2d, plot_tree_3d
from visualization_3d import plot_3d


# == Helper functions ==


def swc_to_dataframe(filepath, column_names=None):
    """
    Convert an SWC file to a pandas DataFrame.
    Column names is a possible input in case some swc files we stumble upon aren't standardized.
    """
    if column_names is None:
        column_names = ["Index", "Type", "X", "Y", "Z", "R", "Parent"]

    df = pd.read_csv(
        filepath,
        sep=r"\s+",  # whitespace separation
        comment="#",  # swc files have a header
        header=None,
        names=column_names,
    )
    if df.shape[1] != 7:
        raise ValueError(f"Expected 7 columns, but found {df.shape[1]}.")

    return df


def dataframe_to_tree(df: pd.DataFrame) -> tuple[Node, dict[int, Node]]:
    """
    Convert an SWC DataFrame into a tree of Node objects.

    Returns:
    root_node: Node
    nodes: dict[int, Node]
        Mapping from node index to Node object.
    """

    nodes = {}
    for row in df.itertuples(index=False):
        # each line corresponds to a single node in swc files
        node = Node(
            index=int(row.Index),
            node_type=int(row.Type),
            x=float(row.X),
            y=float(row.Y),
            z=float(row.Z),
            radius=float(row.R),
            parent_index=int(row.Parent),
            # parent Node assigned later
        )
        nodes[node._index] = node  # add new node to dictionary

    # =add parent reference using parent index attribute=
    root_node = None
    for node in nodes.values():
        if node._parent_index == -1:  # root node check
            if root_node is not None:
                # looks like we've had a root node already
                raise ValueError("swc file must contain only one root")
            root_node = node
            continue  # root node needs no parent node

        if node._parent_index not in nodes:
            msg = f"Parent index {node._parent_index} not found (error in swc)."
            raise ValueError(msg)

        # get reference to the parent node object using nodes dictionary
        parent_node = nodes[node._parent_index]

        #  assign the parent node to current node's parent node attribute
        node._parent = parent_node

        # append current node as item in parent node's children list
        parent_node._children.append(node)

    # final checks
    if root_node is None:  # check we have a root node
        msg = "No root found. swc file must contain a root."
        raise ValueError(msg)
    if root_node._parent is not None:  # check root node has no parent
        raise ValueError("Root node should not have a parent")

    return root_node, nodes


def main():
    df = swc_to_dataframe("morphology/main.swc")
    root_node, nodes = dataframe_to_tree(df)
    plot_3d(nodes)

if __name__ == "__main__":
    main()
