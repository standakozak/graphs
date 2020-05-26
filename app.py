import tkinter as tk
from tkinter import messagebox as messagebox
from sys import exit

from graph_class import Graph
from draw_functions import *


def click(event):
    event.widget.focus_set()
    if type(event.widget) == tk.Canvas:
        global focused_object_index, element_indexes

        focused_object_index = check_pos_set_focus(graph_canvas, element_indexes, graph, tk.CURRENT)
        if focused_object_index is None:
            focused_object_index, new_vertex = add_vertex_from_click(event.x, event.y, event.widget, graph)
            element_indexes[focused_object_index] = new_vertex
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)


def mouse_motion(event, mouse_num=1):
    global dragged_object_index, element_indexes, graph, focused_object_index

    if str(event.type) == "Motion":
        if mouse_num == 1:
            if dragged_object_index is None:
                dragged_object_index = check_pos(graph_canvas, element_indexes, tk.CURRENT)
                if dragged_object_index is None:
                    dragged_object_index = False
        elif mouse_num == 3:
            if not focused_object_index:
                focused_object_index = check_pos_set_focus(graph_canvas, element_indexes, graph, tk.CURRENT)
            if focused_object_index:
                move_focused(event.x, event.y, focused_object_index, element_indexes)
                update_canvas(graph_canvas, element_indexes, graph)

    elif str(event.type) == "ButtonRelease":
        if event.num == 1:
            if dragged_object_index:
                end_object_index = check_pos(graph_canvas, element_indexes, tk.CURRENT)
                if end_object_index is not None and end_object_index != dragged_object_index:
                    new_edge_index, edge = add_line((element_indexes[dragged_object_index],
                                                     element_indexes[end_object_index]), event.widget, graph)
                    element_indexes[new_edge_index] = edge
                    focused_object_index = new_edge_index
            element_indexes = update_canvas(graph_canvas, element_indexes, graph)
            dragged_object_index = None


def key_press(event):
    if event.keysym == "Delete":
        global graph, element_indexes, focused_object_index

        graph = remove_object(focused_object_index, element_indexes, graph, graph_canvas)
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)
        focused_object_index = None


def setup():
    _root = tk.Tk()

    frame = tk.Frame(_root, bg="#fdffed")

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

    _root.protocol("WM_DELETE_WINDOW", lambda: exit_window(_root))
    return _root


def exit_window(tkroot):
    if messagebox.askokcancel(u"Exit", u"Do you really want to exit?"):
        tkroot.destroy()
        exit("Program closed!")


def loop(tkroot):
    global element_indexes
    element_indexes = draw_graph(graph, graph_canvas, element_indexes)
    tkroot.mainloop()


if __name__ == "__main__":
    focused_object_index = None
    dragged_object_index = None

    element_indexes = dict()
    graph = Graph()
    _test_dict = {
        "A": ["B"],
        "B": ["D"],
        "C": [],
        "D": ["A", "C"]
    }
    graph.add_from_neighbors_list(_test_dict)

    root = setup()

    while True:
        loop(root)
