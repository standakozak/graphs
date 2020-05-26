import tkinter as tk
from tkinter import messagebox as messagebox
from sys import exit

from graph_class import Graph
from draw_functions import *


def click(event):
    """
    Tkinter event - pressing mouse button - setting focus to element, creating new vertex

    Checks and changes focus of objects, creates new vertex if mouse was not above any alement, visualizes changes
    """
    event.widget.focus_set()
    if type(event.widget) == tk.Canvas:
        global focused_object_index, element_indexes

        focused_object_index = check_pos_set_focus(graph_canvas, element_indexes, graph, tk.CURRENT)
        if focused_object_index is None:
            focused_object_index, new_vertex = add_vertex_from_click(event.x, event.y, event.widget, graph)
            element_indexes[focused_object_index] = new_vertex
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)


def mouse_motion(event, mouse_num=1):
    """
    Moving with vertices (righ button) / creating edges (left button)

    Tkinter event - mouse motion, mouse button released (for end of event)
    Modifies elements by adding edge, checks / change focus of elements, visualizes changes

    Parameters:
        mouse_num - int, number of mouse button (1-left, 2-middle, 3-right)
    """
    global dragged_object_index, element_indexes, graph, focused_object_index

    if str(event.type) == "Motion":
        if mouse_num == 1:
            if dragged_object_index is None:
                dragged_object_index = check_pos(graph_canvas, element_indexes, tk.CURRENT)
        elif mouse_num == 3:
            if not focused_object_index:
                focused_object_index = check_pos_set_focus(graph_canvas, element_indexes, graph, tk.CURRENT)
            if focused_object_index:
                move_focused(event.x, event.y, focused_object_index, element_indexes)
                update_canvas(graph_canvas, element_indexes, graph)

    elif str(event.type) == "ButtonRelease":  # End of motion
        if event.num == 1:
            if dragged_object_index:
                end_object_index = check_pos(graph_canvas, element_indexes, tk.CURRENT)
                if end_object_index is not None and end_object_index != dragged_object_index:
                    # Creating new edge
                    new_edge_index, edge = add_line((element_indexes[dragged_object_index],
                                                     element_indexes[end_object_index]), event.widget, graph)
                    element_indexes[new_edge_index] = edge
                    focused_object_index = new_edge_index
                    element_indexes = update_canvas(graph_canvas, element_indexes, graph)
            dragged_object_index = None


def key_press(event):
    """
    Tkinter event - pressing key

    Key:
        delete - deletes focused element
    Modifies elements, visualizes changes
    """
    if event.keysym == "Delete":
        global graph, element_indexes, focused_object_index

        graph = remove_object(focused_object_index, element_indexes, graph, graph_canvas)
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)
        focused_object_index = None


def setup():
    """
    Creates window and widgets, binds events to functions
    Returns root - Tk object
    """
    root = tk.Tk()

    frame = tk.Frame(root, bg="#fdffed")

    frame.place(relheight=1, relwidth=1)

    global graph_canvas
    graph_canvas = tk.Canvas(frame, bg="#ffffff", bd=1.5, relief="sunken")
    graph_canvas.bind("<Button-1>", click)
    graph_canvas.bind("<Button-3>", click)
    graph_canvas.bind("<Key>", key_press)
    graph_canvas.bind("<B1-Motion>", mouse_motion)
    graph_canvas.bind("<B3-Motion>", lambda event: mouse_motion(event, 3))
    graph_canvas.bind("<ButtonRelease-1>", mouse_motion)
    graph_canvas.place(relheight=0.75, relwidth=0.8, relx=0.1, rely=0.075)

    root.protocol("WM_DELETE_WINDOW", lambda: exit_window(root))
    return root


def exit_window(tkroot):
    """
    Prints dialog window, shuts down the program
    """
    if messagebox.askokcancel(u"Exit", u"Do you really want to exit?"):
        tkroot.destroy()
        exit("Program closed!")


def loop(tkroot):
    """
    Main loop of program
    """
    global element_indexes
    element_indexes = draw_graph(graph, graph_canvas, element_indexes)
    tkroot.mainloop()


if __name__ == "__main__":
    focused_object_index = None  # For deleting elements and moving vertices
    dragged_object_index = None  # For creating edges
    element_indexes = dict()  # Dictionary of IDs of elements on canvas and object instances of graph components
    graph = Graph()  # Main graph instance for visualization

    # Example of adding components to graph
    _test_dict = {
        "A": ["B"],
        "B": ["D"],
        "C": [],
        "D": ["A", "C"]
    }
    graph.add_from_neighbors_list(_test_dict)

    root = setup()
    loop(root)
