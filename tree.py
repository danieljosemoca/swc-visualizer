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
        if isinstance(other, int):
            if nodes_dict is None: 
                raise ValueError("please input the nodes dictionary when 'other' is an index.")
            if other not in nodes_dict:
                raise ValueError(f"Node index {other} not found")
            other = nodes_dict[other]

        elif not isinstance(other, Node):
            raise TypeError("'other' must be Node or int")

        return math.sqrt((other._x - self._x)**2 + (other._y - self._y)**2 + (other._z - self._z)**2)


    def length_to_root(self, nodes): 
        """determines the length of the branch from the current node to the root node, in micrometers."""
        node = self 
        distance_accumulator = 0
        while node._parent != -1: 
            distance_accumulator += node.distance(nodes[node._parent])
            node = nodes[node._parent]

        return distance_accumulator

        

        

    def branching_points(self): 
        pass

    def dendritic_complexity(self):
        pass

    def tortuosity(self): 
        pass

    



