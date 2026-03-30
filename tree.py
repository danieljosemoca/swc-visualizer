import math

class Node:
    __slots__ = ('_index', '_type', '_x', '_y', '_z', '_radius', '_parent', '_children')
    def __init__(self, index: int, node_type: int, x: float, y: float, z: float, radius: float, parent: int):
        self._index = index
        self._type = node_type
        self._x = x
        self._y = y
        self._z = z
        self._radius = radius
        self._parent = parent
        self._children = []

    def distance(self, other: "Node | int" , nodes_dict = None) -> float: 
        """
        Outputs the distance in micrometers between current node and another.
        
        Input: 
        Other: Node object or index (integer)
        nodes_dict: dictionary of notes outputed by dataframe_to_tree(),
          needed if index of "other" node provided
        """
        if isinstance(other, int):  # 'other' was inputted as an index --> convert to node
            if nodes_dict is None:  # we're gonna need a dict[index, Node object]
                raise ValueError("please input the nodes dictionary when 'other' is an index.")
            if other not in nodes_dict:  # index doesn't exist
                raise ValueError(f"Node index {other} not found")
            other = nodes_dict[other]  # convert index to node object

        elif not isinstance(other, Node):   # 'other' was inputted as neither a Node or index for a node
            raise TypeError("'other' must be Node or int")

        # 3D distance formula
        return math.sqrt((other._x - self._x)**2 + (other._y - self._y)**2 + (other._z - self._z)**2)


    def length_to_root(self, nodes): 
        """determines the length of the branch from the current node to the root node, in micrometers."""
        node = self 
        distance_accumulator = 0
        while node._parent != -1: 
            distance_accumulator += node.distance(node._parent)
            node = nodes[node._parent]

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

