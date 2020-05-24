import tkinter as tk
from tkinter import messagebox as messagebox
from sys import exit

from graph_class import Graph
from draw_functions import add_vertex_from_click, draw_graph, check_position_on_canvas, remove_object, update_canvas
from constants import VERTEX_SIZE, SCALE


def click(event):
    event.widget.focus_set()
    if type(event.widget) == tk.Canvas:
        global focused_object_index
        global element_indexes

        focused_object_index = check_position_on_canvas(event.x,event.y,graph_canvas,element_indexes,graph,tk.CURRENT)
        if focused_object_index is None:
            focused_object_index, new_vertex = add_vertex_from_click(event.x, event.y, event.widget, graph)
            element_indexes[focused_object_index] = new_vertex
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)


def key_press(event):
    if event.keysym == "Delete":
        global graph
        global element_indexes
        global focused_object_index

        graph = remove_object(focused_object_index, element_indexes, graph, graph_canvas)
        element_indexes = update_canvas(graph_canvas, element_indexes, graph)
        focused_object_index = None
    #print(str(event.keysym))
    #print(event.keycode)


def setup():
    _root = tk.Tk()

    frame = tk.Frame(_root, bg="#fdffed")

    frame.place(relheight=1, relwidth=1)

    global graph_canvas
    graph_canvas = tk.Canvas(frame, bg="#ffffff", bd=1.5, relief="sunken")
    graph_canvas.bind("<Button-1>", click)
    graph_canvas.bind("<Key>", key_press)
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
    tk.mainloop()


if __name__ == "__main__":
    focused_object_index = None
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
