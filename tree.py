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

    def length(self): 
        """determines length of"""
