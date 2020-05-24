from graph_class import Vertex, Graph, Edge
from constants import SCALE, VERTEX_SIZE, HEIGHT, WIDTH


def check_position_on_canvas(_x, _y, _canvas, elements, _graph, CURRENT):
    """
    Checks if there is a graph component on [_x, _y]

    If there is a component, it gets focused / unfocused.
     Returns None if there is no component, False if component got unfocused and component itself if it got focus.
    """
    return_value = None
    element_index = _canvas.find_withtag(CURRENT)
    if len(_canvas.find_withtag(CURRENT)) > 0:
        element_index = _canvas.find_withtag(CURRENT)[0]
        if element_index in elements.keys():
            element = elements[element_index]
            if type(element) == Vertex:
                return_value = _graph.set_focus(element)
            elif type(element) == Edge:
                return_value = _graph.set_focus(element)
    if return_value is True:
        return_value = element_index
    return return_value


def update_canvas(canvas, elements, graph):
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


def draw_graph(_graph, _canvas, elements):
    """
    Canvas loop - clearing and drawing graph
    """
    for edge in _graph.edges:
        element_index = draw_edge(_canvas, edge)
        elements[element_index] = edge
    for vertex in _graph.vertices:
        element_index = draw_vertex(_canvas, vertex)
        elements[element_index] = vertex

    return elements


def draw_vertex(_canvas, _vertex, index=None):
    """
    Draws vertex on its position on canvas.
    Focused vertices have different color.
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
        return vertex_oval
    else:
        _canvas.coords(index,
                       _vertex.x - VERTEX_SIZE / 2, _vertex.y - VERTEX_SIZE / 2,
                       _vertex.x + VERTEX_SIZE / 2, _vertex.y + VERTEX_SIZE / 2
                       )
        _canvas.itemconfig(index, fill=_color)


def draw_edge(canvas, edge, index=None):
    vertex1 = edge.vertices[0]
    vertex2 = edge.vertices[1]
    if edge.focused:
        _color = "green"
    else:
        _color = "#000000"
    if index is None:
        line = canvas.create_line(vertex1.x, vertex1.y, vertex2.x, vertex2.y,
                                  width=3, activewidth=6, fill=_color
                                  )
        return line
    else:
        canvas.coords(index, edge.vertices[0].x, edge.vertices[0].y, edge.vertices[1].x, edge.vertices[1].y)
        canvas.itemconfig(index, fill=_color)


def add_vertex_from_click(_x, _y, widget, _graph):
    """
    Adds new vertex to grpah after mouse click on canvas.
    """
    vertex = Vertex("", x=_x, y=_y)
    _graph = _graph + vertex
    _graph.set_focus(vertex)
    index = draw_vertex(widget, vertex)
    return index, vertex


def remove_object(object_index, elements, _graph, canvas):
    """
    Removes component from graph object and from canvas
    """
    print(str(_graph))
    if object_index:
        print(object_index)
        canvas.delete(object_index)
        _graph = _graph - elements[object_index]

    return _graph
