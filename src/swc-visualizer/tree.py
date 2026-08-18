import math


class Node:
    """"""

    __slots__ = (  # __slots__ reduces memory overhead
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
        Other: Node object to find the current node's distance from.
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

    def validate(self) -> None:
        """Checks tree is valid, ie. acyclical and complete."""
        # Find the root of the tree containing this node
        root = self.get_root()

        visited = set()
        node_count = 0
        edge_count = 0
        stack = [root]  # a stack can be  implemented as a python list

        while stack:  # condition false once whole tree traversed
            node = stack.pop()  # node checked this iteration
            if node in visited:
                msg = f"Cycle detected: node {node._index} visited twice."
                raise RuntimeError(msg)
            visited.add(node)
            node_count += 1

            for child in node._children:
                edge_count += 1
                stack.append(child)  # an iteration of this while loop per tree node

        # Tree structure rule: edges = nodes - 1
        if edge_count != node_count - 1:
            msg = f"Invalid tree: edges={edge_count}, nodes={node_count}. "
            raise RuntimeError(msg)

        # if no errors raised, tree is valid
        print("Tree is valid!")

    def depth(self) -> float:
        """Returns the maximum length from the root to any node in the tree."""
        root = self.get_root()
        max_depth = 0.0
        # stack holds (node, accumulated_length_from_root)
        stack = [(root, 0.0)]
        while stack:
            node, accum = stack.pop()
            # Update max depth for this node
            if accum > max_depth:
                max_depth = accum
            for child in node._children:
                # Add edge length to accumulated length
                edge_len = node.distance(child)
                stack.append((child, accum + edge_len))
        return max_depth

    def total_length(self) -> float:
        """
        Returns the sum of lengths of all edges in the neuron.
        """
        total = 0.0
        stack = [self.get_root()]
        while stack:
            node = stack.pop()
            for child in node._children:
                total += node.distance(child)
                stack.append(child)
        return total

    def branching_points(self) -> int:
        """
        Computes the total number of branching points from the current node
        to all children nodes, ie number of nodes with 2+ children.
        """
        count = 0
        stack = [self]
        while stack:
            node = stack.pop()
            if len(node._children) >= 2:
                count += 1
            stack.extend(node._children)
        return count

    def neuron_summary(self) -> None:
        print("Tree validation check:")
        self.validate()
        print(f"Number of branching points: {self.branching_points()}")
        print(f"Total length: {round(self.total_length(), 3)} micrometers")
        print(f"Tree depth: {round(self.depth(), 3)} micrometers")
