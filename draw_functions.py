from graph_class import Vertex, Graph
from constants import scale, vertex_size
from math import sqrt


def check_position(_x, _y, _graph):
    return_value = None
    smallest_distance = None
    for vertex in _graph.vertices:

        distance = sqrt((_x - vertex.x) ** 2 + (_y - vertex.y) ** 2)
        if distance <= vertex_size * scale:
            if smallest_distance is None or distance < smallest_distance:
                smallest_distance = distance
                return_value = vertex

    # Setting / unsetting focus to Vertex
    if type(return_value) == Vertex:
        if smallest_distance <= vertex_size * scale / 2:
            _graph.set_focus(return_value)
    return return_value


def draw_graph(_graph, _canvas):
    _canvas.delete("all")
    for vertex in _graph.vertices:
        draw_vertex(_canvas, vertex)


def draw_vertex(_canvas, _vertex):
    if _vertex.focused:
        _color = "#befc9a"
    else:
        _color = "#ffffff"

    _canvas.create_oval(_vertex.x - vertex_size / 2, _vertex.y - vertex_size / 2,
                        _vertex.x + vertex_size / 2, _vertex.y + vertex_size / 2,
                        width=2, fill=_color
                        )


def add_vertex_from_click(_x, _y, widget, _graph):
    vertex = Vertex("", x=_x, y=_y)
    _graph.vertices.append(vertex)
    _graph.set_focus(vertex)
    draw_vertex(widget, vertex)
