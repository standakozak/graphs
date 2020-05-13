class Graph:
    """
    Representation of graphs
    """

    def __init__(self, components=None):
        """
        Create graph object from set of vertex names
        """

        self.vertices = []
        self.edges = []

        for component in components:
            vertex = Vertex(component)
            self.vertices.append(vertex)


class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
