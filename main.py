import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from tree import Node



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
        names=column_names
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
    root_node = None
    for row in df.itertuples(index=False):  # each line is a node in swc files
        node = Node(
            index=int(row.Index),
            node_type=int(row.Type),
            x=float(row.X),
            y=float(row.Y),
            z=float(row.Z),
            radius=float(row.R),
            parent=int(row.Parent)
        )
        nodes[node._index] = node  # add new node to dictionary 

    # link parent-child relationships
    for node in nodes.values():
        if node._parent == -1:
            # root node
            if root_node is None:  # check that we've had no other root node
                root_node = node 
            else: 
                raise ValueError("swc file must contain only one root")
        else:  # normal node
            parent_node = nodes[node._parent]
            parent_node._children.append(node)

    if root_node is None:  # check we have a root node by the end
        raise ValueError("swc file must contain only one root")

    return root_node, nodes


def main():
    df = swc_to_dataframe('morphology/main.swc')
    root_node, nodes = dataframe_to_tree(df)
    print(root_node)
    print(nodes)

if __name__ == "__main__":
    main()
    


