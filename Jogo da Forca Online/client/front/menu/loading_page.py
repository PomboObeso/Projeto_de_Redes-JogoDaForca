import tkinter as tk


class LoadingPage(tk.Frame):
    def __init__(self, master):
        self.master = master

        super().__init__(master)

        self.ok_label = tk.Label(master, text="Loading...")
        self.ok_label.pack()

        super().pack()
