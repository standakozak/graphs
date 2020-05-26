from graph_class import Vertex, Edge
from constants import VERTEX_SIZE


def check_pos(canvas, elements, CURRENT):
    return_value = None
    if CURRENT is not None:
        index = canvas.find_withtag(CURRENT)
        if len(index) > 0:
            if index[0] in elements.keys():
                return_value = index[0]
    return return_value


def check_pos_set_focus(canvas, elements, graph, CURRENT):
    """
    Sets / unsets focus on CURRENT element from elements

     Returns None if CURRENT is None, False if component got unfocused and index of element from dictionary
     if it got focus.

    Parameters:
        canvas - tkinter.Canvas object
        elements - dictionary of elements on Canvas in form index : element object
        graph - Graph object
        CURRENT - tkinter.CURRENT (ID of element of canvas under the mouse)
    """

    element_index = check_pos(canvas, elements, CURRENT)
    return_value = None
    if element_index is not None:

        element = elements[element_index]
        if type(element) == Vertex or type(element) == Edge:
            return_value = graph.set_focus(element)

    if return_value is True:
        return_value = element_index
    return return_value


def update_canvas(canvas, elements, graph):
    """
    Draws elements of canvas, removes redundant elements from canvas

    Parameters:
        canvas - tkinter.Canvas object
        elements - dictionary of elements on canvas
        graph - Graph object
    Returns: modified dictionary of elements
    """
    indexes_to_delete = []
    for index, component in elements.items():
        if type(component) == Edge:
            if component not in graph.edges:
                canvas.delete(index)
                indexes_to_delete.append(index)
            else:
                draw_edge(canvas, component, index)
        elif type(component) == Vertex:
            if component not in graph.vertices:
                canvas.delete(index)
                indexes_to_delete.append(index)
            else:
                draw_vertex(canvas, component, index)
    for index in indexes_to_delete:
        del elements[index]

    return elements


def draw_graph(_graph, canvas, elements):
    """
    Initial drawing of graph

    Adds graph edges and vertices to dictionary
    Returns: modified dictionary
    """
    for edge in _graph.edges:
        element_index = draw_edge(canvas, edge)
        elements[element_index] = edge
    for vertex in _graph.vertices:
        element_index = draw_vertex(canvas, vertex)
        elements[element_index] = vertex

    return elements


def draw_vertex(_canvas, _vertex, index=None):
    """
    Draws vertex on its position on canvas.

    Draws vertex or modify drawn vertex by its index on canvas
    Returns: element index if it was created.
    """
    if _vertex.focused:
        _color = "#befc9a"
    else:
        _color = "#ffffff"
    if index is None:
        vertex_oval = _canvas.create_oval(_vertex.x - VERTEX_SIZE / 2, _vertex.y - VERTEX_SIZE / 2,
                                          _vertex.x + VERTEX_SIZE / 2, _vertex.y + VERTEX_SIZE / 2,
                                          width=2, fill=_color, activeoutline="green", activewidth=3
                                          )
        _canvas.tag_raise(vertex_oval)
        return vertex_oval
    else:
        _canvas.coords(index,
                       _vertex.x - VERTEX_SIZE / 2, _vertex.y - VERTEX_SIZE / 2,
                       _vertex.x + VERTEX_SIZE / 2, _vertex.y + VERTEX_SIZE / 2
                       )
        _canvas.itemconfig(index, fill=_color)
        _canvas.tag_raise(index)


def draw_edge(canvas, edge, index=None):
    """
    Draws edge on canvas or modifies a drawn one

    Returns: element index if it was created
    """
    vertex1 = edge.vertices[0]
    vertex2 = edge.vertices[1]
    if edge.focused:
        _color = "green"
    else:
        _color = "#000000"
    if index is None:
        line = canvas.create_line(vertex1.x, vertex1.y, vertex2.x, vertex2.y,
                                  width=4, activewidth=8, fill=_color
                                  )
        return line
    else:
        canvas.coords(index, edge.vertices[0].x, edge.vertices[0].y, edge.vertices[1].x, edge.vertices[1].y)
        canvas.itemconfig(index, fill=_color)


def add_vertex_from_click(x, y, canvas, graph):
    """
    Adds new vertex to graph after mouse click on canvas.
    """
    vertex = Vertex("", x=x, y=y)
    graph = graph + vertex
    graph.set_focus(vertex)
    index = draw_vertex(canvas, vertex)
    return index, vertex


def move_focused(x, y, element_index, elements):
    if element_index is None or element_index not in elements.keys():
        return None
    element = elements[element_index]
    if type(element) != Vertex:
        return None
    element.x = x
    element.y = y


def add_line(vertices, canvas, graph):
    vertex1, vertex2 = vertices
    if vertex1 is not None and vertex2 is not None:
        edge = Edge((vertex1, vertex2), graph=graph)
        graph = graph + edge
        graph.set_focus(edge)
        index = draw_edge(canvas, edge)
        return index, edge
    else:
        return None


def remove_object(object_index, elements, graph, canvas):
    """
    Removes component from graph object and from canvas
    """
    if object_index:
        canvas.delete(object_index)
        graph = graph - elements[object_index]

    return graph
