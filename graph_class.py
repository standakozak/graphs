from random import randint
from constants import VERTEX_SIZE, MAX_CANVAS_WIDTH, MAX_CANVAS_HEIGHT


class Graph:
    """
    Object representation of graphs
    """

    def __init__(self, name='', components=None):
        """
        Create graph object from tuple of vertex names

        Parameters:
            name - string
            components - tuple of strings
        """
        self.name = name

        self.vertices = []
        self.edges = []

        if components is not None:
            for component_name in components:
                vertex = Vertex(name=component_name, graph=self)
                self.vertices.append(vertex)

    def return_vertex(self, vertex_name):
        """
        Returns Vertex object by vertex name after searching in graph.

        If the graph does not contain the vertex, it is created
        Parameters:
            vertex_name - string
        """
        for vertex_search in self.vertices:
            if vertex_search.name == vertex_name:
                return vertex_search
        vertex = Vertex(vertex_name, graph=self)
        self.vertices.append(vertex)
        return vertex

    def add_from_neighbors_list(self, neighbors_list):
        """
        Add vertices and edges to graph object from list of neighbors

        Parameters:
            neighbors_list - dictionary of neighbors:
                (key = Vertex name): (value = list of neighboring Vertex names)
        """

        if neighbors_list is None:
            return None
        else:
            for vertex_name in neighbors_list.keys():
                for neighbor_name in neighbors_list[vertex_name]:
                    self.add_edge((vertex_name, neighbor_name))

    def add_edge(self, vertices, oriented=False, weight=None, name=''):
        """
        Add path to list, set vertices as neighbors

         Paramteres:
         vertices - tuple of two Vertex objects or their names
         oriented - edge is oriented from first vertex to second
         weight - int, weight of edge
         name - string
        """
        vertex1, vertex2 = vertices
        if type(vertex1) == str:
            vertex1 = self.return_vertex(vertices[0])
        if type(vertex2) == str:
            vertex2 = self.return_vertex(vertices[1])
        edge = Edge((vertex1, vertex2), oriented, weight, name, graph=self)
        self.edges.append(edge)
        edge.set_neighbors()

    def set_focus(self, component):
        """
        Sets graph components as focused (after clicking) - for visualization

        Parameters:
            component - Edge object / Vertex object
        """
        set_value = not component.focused
        for vertex in self.vertices:
            vertex.focused = False
        for edge in self.edges:
            edge.focused = False
        component.focused = set_value
        if set_value is True:  # Focus was set
            return True
        else:  # Focus was unset
            return False

    def __add__(self, other):
        """
        Returns new Graph object after it adds vertices and edges

        Parameters:
            other - Graph object / Vertex object / Edge object
        """

        new_graph = self
        if isinstance(other, Vertex):
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
                for _edge in other.edges:
                    if _edge not in new_graph.edges:
                        new_graph.edges.append(_edge)
        elif isinstance(other, Edge):
            new_graph.edges.append(other)
            other.set_neighbors()
        return new_graph

    def __sub__(self, other):
        """
        Returns new graph without component

        Parameters:
            other - Vertex object / Edge object to be removed from graph
        """

        new_graph = self
        if type(other) == Vertex:
            for index, vertex in enumerate(new_graph.vertices):
                if vertex == other:
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
    """
    Representation of vertex/node in graph object
    """
    def __init__(self, name, graph=None, x=None, y=None):
        """
        Creates Vertex object

        Parameters:
            name - string
            graph - Graph object
            x - horizontal position on canvas (for visualization)
            y - vertical position on canvas (for visualization)
        """
        self.name = name
        self.graph = graph
        self.neighbors = []
        self.x, self.y = x, y
        if self.x is None:
            self.x = randint(VERTEX_SIZE / 2, MAX_CANVAS_WIDTH - VERTEX_SIZE / 2)
        if self.y is None:
            self.y = randint(VERTEX_SIZE / 2, MAX_CANVAS_HEIGHT - VERTEX_SIZE / 2)
        self.focused = False

    def __str__(self):
        neighbors_text = [str(neighbor.name) for neighbor in self.neighbors]
        return f"Name: {self.name}, graph: {self.graph.name}\nNeighbors names: {str(neighbors_text)}"


class Edge:
    """
    Representation of edges between vertices in graph object
    """
    def __init__(self, vertex_objects, oriented=False, weight=None, name='', graph=None):
        """
        Creates Edge object

        Parameters:
            vertex_objects - tuple of two Vertex class instances
            oriented - bool; if True, the edge lead from first Vertex to the second
            weight - int; weight of edge
            graph - graph class instance
        """
        self.vertices = vertex_objects
        self.oriented = oriented
        self.weight = weight
        self.name = name
        self.graph = graph
        self.focused = False

    def set_neighbors(self):
        """
        Adds vertices in their list of neighbors, if they are not already there
        """
        vertex1, vertex2 = self.vertices
        if not self.oriented:
            if vertex1 not in vertex2.neighbors:
                vertex2.neighbors.append(vertex1)
        if vertex2 not in vertex1.neighbors:
            vertex1.neighbors.append(vertex2)

    def __str__(self):
        return f"Edge {self.name} connecting vertices {self.vertices[0].name} and {self.vertices[1].name} in graph " \
               f"{self.graph.name}\n Oriented: {self.oriented}, Weight: {self.weight}"


if __name__ == "__main__":
    # Example of using the classes
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
