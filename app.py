import tkinter as tk
from tkinter import messagebox as messagebox
from sys import exit

from graph_class import Graph
from draw_functions import add_vertex_from_click, draw_graph, check_position
from constants import vertex_size, scale


def click(event):
    if type(event.widget) == tk.Canvas:
        hovered_object = check_position(event.x, event.y, graph)
        if hovered_object is None:
            add_vertex_from_click(event.x, event.y, event.widget, graph)
        print(str(graph.vertices))
        for vertex in graph.vertices:
            print(str(vertex.focused))


def setup():
    _root = tk.Tk()

    frame = tk.Frame(_root, bg="#fdffed")
    frame.place(relheight=1, relwidth=1)

    global graph_canvas
    graph_canvas = tk.Canvas(frame, bg="#ffffff", bd=1.5, relief="sunken")
    graph_canvas.bind("<Button-1>", click)
    graph_canvas.place(relheight=0.75, relwidth=0.8, relx=0.1, rely=0.075)

    _root.protocol("WM_DELETE_WINDOW", lambda: exit_window(_root))
    return _root


def exit_window(tkroot):
    #if messagebox.askokcancel(u"exit", u"Do you really want to exit?"):
    tkroot.destroy()
    exit("Program closed!")


def loop(tkroot):

    tkroot.update()
    draw_graph(graph, graph_canvas)



if __name__ == "__main__":
    graph = Graph()
    root = setup()

    while True:
        loop(root)
