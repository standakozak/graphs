import tkinter as tk
from tkinter import messagebox as messagebox
from sys import exit

from graph_class import Graph, Vertex
from constants import vertex_size



def click_function(event):
    if type(event.widget) == tk.Canvas:
        vertex_oval = event.widget.create_oval(event.x - vertex_size / 2, event.y - vertex_size / 2,
                                               event.x + vertex_size / 2, event.y + vertex_size / 2,
                                               width=2, fill="#ffffff"
                                               )


def setup():
    _root = tk.Tk()

    frame = tk.Frame(_root,bg="#fdffed")
    frame.place(relheight=1,relwidth=1)

    graph_canvas = tk.Canvas(frame, bg="#ffffff", bd=1.5, relief="sunken")
    graph_canvas.bind("<Button-1>", click_function)
    graph_canvas.place(relheight=0.75, relwidth=0.8, relx=0.1, rely=0.075)

    _root.protocol("WM_DELETE_WINDOW", lambda: exit_window(_root))
    return _root


def exit_window(tkroot):
    tkroot.destroy()
    exit("Program closed!")
    """
    if messagebox.askokcancel(u"exit", u"Do you really want to exit?"):
        tkroot.destroy()
        exit()
    """

def loop(tkroot):

    tkroot.mainloop()


if __name__ == "__main__":
    root = setup()
    while True:
        loop(root)
