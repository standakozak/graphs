from random import randint
from constants import VERTEX_SIZE, WIDTH, HEIGHT


class Graph:
    """
    Object representation of graphs
    """

    def __init__(self, name='', components=None):
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
        edge = Edge((vertex1, vertex2), oriented, weight, name, graph=self)
        self.edges.append(edge)
        if oriented is False:
            vertex2.neighbors.append(vertex1)

        vertex1.neighbors.append(vertex2)

    def set_focus(self, component):
        _set_value = not component.focused
        for _vertex in self.vertices:
            _vertex.focused = False
        for _edge in self.edges:
            _edge.focused = False
        component.focused = _set_value
        if _set_value is True:  # Focus was set
            return True
        else:  # Focus was unset
            return False

    def __add__(self, other):
        """
        Returns new Graph object after it adds vertices and edges from second Graph object to the first
        """

        new_graph = self
        if isinstance(other, Vertex):
            if other.neighbors is not None:
                for neighbor in other.neighbors:
                    new_graph.add_edge((other, neighbor))
            new_graph.vertices.append(other)

        elif isinstance(other, Graph):
            if other.vertices is not None:
                for _vertex in other.vertices:
                    _vertex.graph_name = new_graph.name
                    new_graph.vertices.append(_vertex)

            if other.edges is not None:
                for _edge in other.edges:
                    if _edge not in new_graph.edges:
                        new_graph.edges.append(_edge)
        return new_graph

    def __sub__(self, other):
        new_graph = self
        if type(other) == Vertex:
            for index, _vertex in enumerate(new_graph.vertices):
                if _vertex == other:
                    del new_graph.vertices[index]
                    break

            indexes_to_delete = []
            for index, edge in enumerate(new_graph.edges):
                if other in edge.vertices:
                    indexes_to_delete.append(index)
            for index in reversed(indexes_to_delete):
                del new_graph.edges[index]

        elif type(other) == Edge:
            for index, edge in enumerate(new_graph.edges):
                if edge == other:
                    del new_graph.edges[index]
                    break
        return new_graph


class Vertex:
    def __init__(self, name, graph_name=None, x=None, y=None):
        self.name = name
        self.graph_name = graph_name
        self.neighbors = []
        self.x, self.y = x, y
        if self.x is None:
            self.x = randint(VERTEX_SIZE / 2, WIDTH)
        if self.y is None:
            self.y = randint(VERTEX_SIZE / 2, HEIGHT)
        self.focused = False

    def __str__(self):
        neighbors_text = [str(neighbor.name) for neighbor in self.neighbors]
        return f"Name: {self.name}, graph: {self.graph_name}\nNeighbors: {str(neighbors_text)}"


class Edge:
    def __init__(self, vertex_objects, oriented=False, weight=None, name='', graph=None):
        self.vertices = vertex_objects
        self.oriented = oriented
        self.weight = weight
        self.name = name
        self.graph = graph
        self.focused = False

    def __str__(self):
        return f"Edge {self.name} connecting vertices {self.vertices[0].name} and {self.vertices[1].name} of graph " \
               f"{self.graph.name}\n Oriented: {self.oriented}, Weight: {self.weight}"


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

    for vertex in result_graph.vertices:
        print(str(vertex))

