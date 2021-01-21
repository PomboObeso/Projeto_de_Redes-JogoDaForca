import tkinter as tk


def front_page(size, close_function, master):
    page = tk.Toplevel()
    page.geometry(size)
    page.protocol("WM_DELETE_WINDOW", close_function)
    page.transient(master)
    page.focus_force()
    page.grab_set()

    return page
