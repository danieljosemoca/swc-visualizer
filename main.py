import os
import glob
import pandas as pd
from tree import Node
from visualization import plot_2d
from visualization_3d import plot_3d


# == Helper functions ==


def swc_to_dataframe(filepath, column_names=None):
    """
    Convert an SWC file to a pandas DataFrame.
    Column names is a possible input in case some swc files we stumble upon aren't standardized.
    """
    if column_names is None:
        column_names = ["Index", "Type", "X", "Y", "Z", "R", "Parent"]  # as per swc file structure

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


def main() -> None:
    """Main function to run the program."""
    # locate all swc files in the 'morphology' folder
    swc_files = glob.glob("morphology/*.swc")
    if not swc_files:
        print("No .swc files found in the 'morphology' folder.")
        return

    # ask user which visualization(s) they want
    print("Which visualization(s) would you like?")
    print("1: 2D only")
    print("2: 3D only")
    print("3: Both 2D and 3D")
    choice = input("Enter 1, 2, or 3: ").strip()
    do_2d = (choice == "1" or choice == "3")
    do_3d = (choice == "2" or choice == "3")

    # process each file
    for filepath in swc_files:
        print(f"\n--- Processing: {os.path.basename(filepath)} ---")
        try:
            df = swc_to_dataframe(filepath)
            root_node, nodes = dataframe_to_tree(df)  # tree construction
            root_node.neuron_summary()  # validation + basic stats

            if do_2d:
                plot_2d(nodes)
            if do_3d:
                plot_3d(nodes)
        except Exception as e:  # catch any error that happens during file processing
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
