class Graph:
    """
    Object representation of graphs
    """

    def __init__(self, components=None, name=''):
        """
        Create graph object from tuple of vertex names
        """
        self.name = name
        self.vertices = []
        self.edges = []
        if components is not None:
            for component_name in components:
                vertex = Vertex(name=component_name, graph_name=self.name)
                self.vertices.append(vertex)

    def add_from_neighbors_list(self, neighbors_list):
        """
        Add vertices and edges to graph object from list of neighbors

        Parameters:
            neighbors_list - dictionary - key = Vertex name: value = list of neighboring Vertex names
        """

        if neighbors_list is None:
            return None
        else:
            for vertex_name in neighbors_list.keys():
                for search_vertex in self.vertices:
                    if search_vertex.name == vertex_name:
                        break
                else:
                    self.vertices.append(Vertex(name=vertex_name, graph_name=self.name))
                for neighbor_name in neighbors_list[vertex_name]:
                    for search_vertex in self.vertices:
                        if search_vertex.name == vertex_name:
                            break
                    else:
                        self.vertices.append(Vertex(name=vertex_name, graph_name=self.name))
                    self.add_edge((vertex_name, neighbor_name))

    def add_edge(self, vertex_names, oriented=False, weight=None, name=''):
        """
        Add path to list, set vertices as neighbors

         Paramteres:
         vertices - tuple of two Vertex objects
         oriented - edge is oriented in order of mentioned vertices
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
        neighbors_text = [str(neighbor.name) for neighbor in self.neighbors]
        return f"Name: {self.name}, graph: {self.graph_name}\nNeighbors: {str(neighbors_text)}"


"""
test_graph = Graph(components=None, name="Testing graph")

_test_dict = {
    "A": ["B"],
    "B": ["D", "C"],
    "C": ["A"],
    "D": ["A", "C"]
}
test_graph.add_from_neighbors_list(_test_dict)

for _vertex in test_graph.vertices:
    print(str(_vertex))
"""
