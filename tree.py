import math


class Node:
    __slots__ = ("_index", "_type", "_x", "_y", "_z", "_radius", "_parent", "_children")

    def __init__(
        self,
        index: int,
        node_type: int,
        x: float,
        y: float,
        z: float,
        radius: float,
        parent: "Node",
    ) -> None:
        self._index = index
        self._type = node_type
        self._x = x
        self._y = y
        self._z = z
        self._radius = radius
        self._parent = parent
        self._children = []

    def distance(self, other: "Node") -> float:
        """
        Outputs the distance in micrometers between current node and another.

        Input:
        Other: Node object or index (integer)
        nodes_dict: dictionary of notes outputed by dataframe_to_tree(),
          needed if index of "other" node provided
        """

        if isinstance(other, int):
            # 'other' was likely inputted as an index
            raise ValueError(
                "'other' must be a node. input nodes_dict[index] if input an index."
            )

        elif not isinstance(other, Node):
            # 'other' was inputted as neither a Node or index for a node
            raise TypeError("'other' must be Node.")

        # 3D distance formula
        return math.sqrt(
            (other._x - self._x) ** 2
            + (other._y - self._y) ** 2
            + (other._z - self._z) ** 2
        )

    def length_to_root(self, limit: int = 15000):
        """determines the length of the branch from the current node to the root node, in micrometers.

        Input:
        limit: max number of node traversals while attempting to find the root node until an Error is raised"""
        node = self
        count = 0
        distance_accumulator = 0

        while node._parent != -1 and count < limit:
            distance_accumulator += node.distance(node._parent)
            node = node._parent
            count += 1

        if count >= limit:
            raise NameError(
                "Root node not found. run validate(), and/or increase limit, and try again."
            )

        return distance_accumulator

    def validate(self):
        "checks tree integrity and fixes anything it can..."

    def branching_points(self):
        "computes the total number of branching points from the current node to all children nodes (bruv describe this better)"

    def dendritic_complexity(self):
        "whole neuron level"
        pass

    def branching_complexity(self):
        pass

    def tortuosity(self):
        pass

    def degeneration_score(self, other_rootnode: "Node"):
        """compares volume of two swc files."""
        pass

    def neuro_compare(self, other_rootnode: "Node"):
        """quantify spatial distribution changes between swc files"""
        # could make a cool graph
