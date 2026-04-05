import math


class Node:
    """"""
    __slots__ = (
        "_index",
        "_type",
        "_x",
        "_y",
        "_z",
        "_radius",
        "_parent_index",  # int (from SWC)
        "_parent",  # Node | None
        "_children",
    )

    def __init__(
        self,
        index: int,
        node_type: int,
        x: float,
        y: float,
        z: float,
        radius: float,
        parent_index: int,
    ) -> None:
        self._index = index
        self._type = node_type
        self._x = x
        self._y = y
        self._z = z
        self._radius = radius
        self._parent_index = parent_index
        self._parent: Node | None = None  # set later in dataframe_to_tree()
        self._children = []

    def distance(self, other: "Node") -> float:
        """
        Outputs the distance, in micrometers, between the current node and another.

        Input:
        Other: Node object to find distance from node method is used on
        """

        if isinstance(other, int):
            # 'other' was likely inputted as an index
            msg = "'other' must be a node. input nodes_dict[index] if input an index."
            raise ValueError(msg)

        elif not isinstance(other, Node):
            # 'other' was inputted as neither a Node or index for a node
            raise TypeError("'other' must be a Node.")

        # 3D distance formula
        return math.dist((self._x, self._y, self._z), (other._x, other._y, other._z))

    def get_root(self) -> "Node":
        """Returns the root node in the tree."""
        node = self
        while node._parent is not None:
            # this while loop finds the root node
            # which has no parent
            node = node._parent
        return node

    def distance_from_root(self) -> float:
        """
        Returns the distance, in micrometers, between the current node and the root node.
        """
        return self.distance(self.get_root())

    def length_from_root(self, limit: int = 15000) -> float:
        """
        Determines the length of the branch from the current node to the root node, in micrometers.

        Input:
        limit: max number of node traversals while attempting to find the root node until an Error is raised
        """
        node = self
        count = 0
        distance_accumulator = 0

        while node._parent is not None and count < limit:
            distance_accumulator += node.distance(node._parent)
            node = node._parent
            count += 1

        if count >= limit:
            msg = "Root node not found. run validate(), and/or increase limit, and try again."
            raise RuntimeError(msg)

        return distance_accumulator

    def validate(self):
        """
        Checks graph structure is a tree, ie acyclical and connected, using the rule:
        node number = edge number - 1.
        """
        node_count = 0 
        edge_count = 0


    def degree(self): 
        """outputs the number of trees attached to this node (ie the number of subtrees attached to it)."""
        

    def depth(self):
        """max(length_from_root())"""

    def dendritic_length(self):
        """
        Sum of lengths of all dendritic segments
        
        Depression and neurodegeneration have this low
        """

    def branching_points(self, from_root: bool = False):
        "computes the total number of branching points from the current node to all children nodes (bruv describe this better)"
        pass

    def dendritic_complexity(self):
        "at whole neuron level. Based on length, branch points, and spine density."
        pass

    def branching_complexity(self):
        pass

    def tortuosity(self):
        """path_length / straight_line_distance"""
        pass