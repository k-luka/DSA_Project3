from .node import Node
from graphtype import GraphType


class Graph(GraphType):
    nodes: set[Node]
    camera_position: tuple(float, float)
    camera_scale: float
