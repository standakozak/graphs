class Graph:
    """
    Object representation of graphs
    """

    def __init__(self, name='', components=None, parent_graph=None):
        """
        Create graph object from tuple of vertex names
        """
        self.name = name

        if parent_graph is None:
            self.vertices = []
            self.edges = []
        else:
            self.vertices = parent_graph.vertices
            self.edges = parent_graph.edges

        if components is not None:
            for component_name in components:
                vertex = Vertex(name=component_name, graph_name=self.name)
                self.vertices.append(vertex)

    def return_vertex(self, vertex_name):
        """
        Returns Vertex object from searching in graph by vertex name.

        If the graph does not contain the vertex, it is created
        """
        for _vertex_search in self.vertices:
            if _vertex_search.name == vertex_name:
                return _vertex_search
        _vertex = Vertex(vertex_name, graph_name=self.name)
        self.vertices.append(_vertex)
        return _vertex

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
                for neighbor_name in neighbors_list[vertex_name]:
                    self.add_edge((vertex_name, neighbor_name))

    def add_edge(self, vertex_names, oriented=False, weight=None, name=''):
        """
        Add path to list, set vertices as neighbors

         Paramteres:
         vertices - tuple of two Vertex objects
         oriented - edge is oriented in order of mentioned vertices
        """

        vertex1 = self.return_vertex(vertex_names[0])
        vertex2 = self.return_vertex(vertex_names[1])

        self.edges.append((vertex1, vertex2, oriented, weight, name))
        if oriented is False:
            vertex2.neighbors.append(vertex1)

        vertex1.neighbors.append(vertex2)

    def __add__(self, other, name=None):
        """
        Returns new Graph object after it adds vertices and edges from second Graph object to the first
        """
        if name is None:
            name = self.name

        new_graph = Graph(name, parent_graph=self)
        if isinstance(other, Vertex):
            other.name = new_graph.name
            if other.neighbors is not None:
                for neighbor in other.neighbors:
                    new_graph.add_edge((other, neighbor))
            new_graph.vertices.append(other)

        elif isinstance(other, Graph):
            if other.vertices is not None:
                for vertex in other.vertices:
                    vertex.graph_name = new_graph.name
                    new_graph.vertices.append(vertex)

            if other.edges is not None:
                for edge in other.edges:
                    if edge not in new_graph.edges:
                        new_graph.edges.append(edge)
        return new_graph


class Vertex:
    def __init__(self, name, graph_name=None):
        self.name = name
        self.graph_name = graph_name
        self.neighbors = []

    def __str__(self):
        neighbors_text = [str(neighbor.name) for neighbor in self.neighbors]
        return f"Name: {self.name}, graph: {self.graph_name}\nNeighbors: {str(neighbors_text)}"


if __name__ == "__main__":
    graph1 = Graph("graph 1")
    graph2 = Graph("graph 2")

    _test_dict = {
        "A": ["B"],
        "B": ["D"],
        "C": [],
        "D": ["A", "C"]
    }
    graph1.add_from_neighbors_list(_test_dict)

    graph2.return_vertex("Q")
    graph2.return_vertex("X")
    graph2.add_edge(("Q", "X"), oriented=True, weight=12)

    result_graph = graph2 + graph1

    for _vertex in result_graph.vertices:
        print(str(_vertex))
