class Graph:
    """
    Object representation of graphs
    """

    def __init__(self, components=None, name=''):
        """
        Create graph object from set of vertex names
        """
        self.name = name
        self.vertices = []
        self.edges = []
        for component_name in components:
            vertex = Vertex(name=component_name, graph_name=self.name)
            self.vertices.append(vertex)

    def add_edge(self, vertex_names, oriented=False, weight=None, name=''):
        """
        Add path to list, set vertices as neighbors

         Paramteres:
         vertices - tuple of two Vertex objects
         oriented = edge is oriented in order of mentioned vertices
        """

        if vertex_names[0] is None or vertex_names[1] is None:
            return None
        else:
            vertex1, vertex2 = None, None
            for vertex_search in self.vertices:
                if vertex_names[0] == vertex_search.name:
                    vertex1 = vertex_search
                if vertex_names[1] == vertex_search.name:
                    vertex2 = vertex_search
            if vertex1 is None or vertex2 is None:
                return None
            else:
                self.edges.append((vertex1, vertex2, oriented, weight, name))
                if oriented is False:
                    vertex2.neighbors.append(vertex1)

                vertex1.neighbors.append(vertex2)


class Vertex:
    def __init__(self, name, graph_name=None):
        self.name = name
        self.graph_name = graph_name
        self.neighbors = []

    def __str__(self):
        return f"Vertex {self.name} of graph {self.graph_name}\nNeighbors: {str(self.neighbors)}"

"""
test_vertices = {"TestA", "Q", "Vertex120"}
test_graph = Graph(test_vertices, "Testing graph")
for _vertex in test_graph.vertices:
    print(str(_vertex))
print()
test_graph.add_edge(("TestA", "Q"), oriented=True, weight=2, name="Edge_1")
for _vertex in test_graph.vertices:
    print(str(_vertex))
"""
