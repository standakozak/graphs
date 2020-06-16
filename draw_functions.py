from graph_class import Vertex, Edge
from constants import VERTEX_SIZE, ALG_SPEED


def update_canvas(canvas, elements, graph):
    """
    Draws elements of canvas, removes redundant elements from canvas

    Objects from elements have to be in graph object to be drawn, otherwise they are deleted
    Returns: modified dictionary of elements
    Parameters:
        canvas - tkinter.Canvas object
        elements - dictionary of elements on canvas
        graph - Graph object
    """
    indexes_to_delete = []
    for index, component in elements.items():
        component.highlighted = False
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


def draw_graph(graph, canvas, elements):
    """
    Initial drawing of graph

    Adds edges and vertices from graph to dictionary
    Returns: modified dictionary
    Parameters:
        graph - instance of Graph class
        canvas - tkinter.Canvas object
        elements - dictionary of elements on canvas
    """
    for edge in graph.edges:
        element_index = draw_edge(canvas, edge)
        elements[element_index] = edge
        edge.canvas_index = element_index
    for vertex in graph.vertices:
        element_index = draw_vertex(canvas, vertex)
        elements[element_index] = vertex
        vertex.canvas_index = element_index

    return elements


def draw_vertex(canvas, vertex, index=None):
    """
    Draws vertex on its position on canvas.

    Draws vertex or modify drawn vertex by its index on canvas
    Returns: element index if it was created.
    Parameters:
        canvas - tkinter.Canvas object
        vertex - instance of Vertex class
        index - int, ID of element on canvas (if already created)

    """
    if vertex.highlighted:
        color = "#b6b6d6"
    elif vertex.focused:
        color = "#befc9a"
    else:
        color = "#ffffff"
    if index is None:
        vertex_oval = canvas.create_oval(vertex.x - VERTEX_SIZE / 2, vertex.y - VERTEX_SIZE / 2,
                                         vertex.x + VERTEX_SIZE / 2, vertex.y + VERTEX_SIZE / 2,
                                         width=2, fill=color, activeoutline="green", activewidth=3
                                         )
        canvas.tag_raise(vertex_oval)
        return vertex_oval
    else:
        canvas.coords(index,
                      vertex.x - VERTEX_SIZE / 2, vertex.y - VERTEX_SIZE / 2,
                      vertex.x + VERTEX_SIZE / 2, vertex.y + VERTEX_SIZE / 2
                      )
        canvas.itemconfig(index, fill=color)
        canvas.tag_raise(index)


def draw_edge(canvas, edge, index=None):
    """
    Draws edge on canvas or modifies a drawn one

    Returns: element index if it was created
    Parameters:
        canvas - tk.Canvas object
        edge - instance of Edge class
        index - int, ID of edge element on canvas (if None, it is created)
    """
    vertex1 = edge.vertices[0]
    vertex2 = edge.vertices[1]
    if edge.highlighted:
        color = "#b6b6d6"
    elif edge.focused:
        color = "green"
    else:
        color = "#000000"
    if index is None:
        line = canvas.create_line(vertex1.x, vertex1.y, vertex2.x, vertex2.y,
                                  width=4, activewidth=8, fill=color
                                  )
        return line
    else:
        canvas.coords(index, edge.vertices[0].x, edge.vertices[0].y, edge.vertices[1].x, edge.vertices[1].y)
        canvas.itemconfig(index, fill=color)


def add_vertex_from_click(x, y, canvas, graph):
    """
    Adds new vertex to graph after mouse click on canvas.

    Returns (ID of vertex element, new Vertex object)
    Parameters:
         x - horizonatal position on canvas (mouse position)
         y - vertical position on canvas (mouse pos)
         canvas - tkinter.Canvas object
         graph - instance of Graph class
    """
    vertex = Vertex("", x=x, y=y)
    graph = graph + vertex
    graph.set_focus(vertex)
    index = draw_vertex(canvas, vertex)
    return index, vertex


def add_edge(vertices, canvas, graph):
    """
    Adds connection between vertices after dragging by left button on mouse

    Creates Edge object, saves it to Graph and draws it
    Returns (ID of new edge, new Edge object)
    Parameters:
        vertices - tuple of Vertex class instances to be connected
        canvas - tkinter.Canvas object
        graph - instance of Graph class
    """
    vertex1, vertex2 = vertices
    if vertex1 is not None and vertex2 is not None:
        edge = Edge((vertex1, vertex2), graph=graph)
        graph = graph + edge
        graph.set_focus(edge)
        index = draw_edge(canvas, edge)
        return index, edge
    else:
        return None


def animation_step(canvas, queue):
    """
    Parameters:
        canvas - tkinter.canvas object
        queue - list of Edges and Vertices in the order they are higlighted
    """

    if len(queue) > 0:
        object_to_draw = queue.pop(0)
        if isinstance(object_to_draw, Vertex):
            draw_vertex(canvas, object_to_draw, object_to_draw.canvas_index)
        elif isinstance(object_to_draw, Edge):
            draw_edge(canvas, object_to_draw, object_to_draw.canvas_index)
        canvas.after(int(ALG_SPEED * 1000), lambda: animation_step(canvas, queue))


def draw_algorithm(func, canvas, graph, element):
    """
    Creates a seqence in which are objects highlighted start animation

    """
    object_queue = func(graph, element)
    for graph_object in object_queue:
        graph_object.highlighted = True

    animation_step(canvas, object_queue)

