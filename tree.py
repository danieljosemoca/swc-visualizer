import math


class Node:
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
        self._parent_index = parent_index  # always int
        self._parent: Node | None = None  # set later
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
            raise TypeError("'other' must be Node.")

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
        "checks tree integrity and fixes anything it can..."
        pass

    def branching_points(self, from_root: bool = False):
        "computes the total number of branching points from the current node to all children nodes (bruv describe this better)"
        pass

    def dendritic_complexity(self):
        "at whole neuron level. Based on length, branch points, and spine density."
        pass

    def branching_complexity(self):
        pass

    def tortuosity(self):
        pass

    def degeneration_score(self, other_root_node: "Node"):
        """compares volume of two swc files."""
        pass

    def neuro_compare(self, other_root_node: "Node"):
        """quantify spatial distribution changes between swc files"""
        # could make a cool graph
