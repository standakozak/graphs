from graph_class import Vertex, Edge


def check_pos(canvas, elements, CURRENT):
    """
    Checks elements on CURRENT position

    Returns ID of element on CURRENT position or None
    Parameters:
        canvas - tkinter.Canvas object
        elements - dictionary of elements on canvas
        CURRENT - tkinter.CURRENT
    """
    return_value = None
    if CURRENT is not None:
        index = canvas.find_withtag(CURRENT)
        if len(index) > 0:
            if index[0] in elements.keys():
                return_value = index[0]
    return return_value


def check_pos_set_focus(canvas, elements, graph, CURRENT):
    """
    Create / delete focus of CURRENT element from elements

     Returns None if CURRENT is None or if there is not any element on CURRENT position,
        False if component got unfocused and index of element from dictionary if it got focus.

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


def move_focused(x, y, element_index, elements):
    """
    Changes vertex coordinates

    Parameters:
        x - new horizontal position of vertex on canvas
        y - new vertical position of vertex on canvas
        element_index - ID of element (vertex) on canvas
        elements - dictionary of elements on canvas
    """
    if element_index is None or element_index not in elements.keys():
        return None
    element = elements[element_index]
    if type(element) != Vertex:
        return None
    element.x = x
    element.y = y


def remove_object(object_index, elements, graph, canvas):
    """
    Removes component from Graph object and from canvas

    Returns modified Graph object
    Parameters:
        object_index - ID of element on canvas to be removed
        element - dictionary of all elements on canvas
        graph - instance of Graph class
        canvas - tkinter.Canvas object
    """
    if object_index:
        canvas.delete(object_index)
        graph = graph - elements[object_index]

    return graph
