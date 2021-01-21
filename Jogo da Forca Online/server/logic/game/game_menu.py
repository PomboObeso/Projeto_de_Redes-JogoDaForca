import tkinter as tk


class GameMenu(tk.Menu):
    def __init__(self, admin_test, end_game, master):
        self.master = master

        super().__init__(master)

        game_menu = tk.Menu(self, tearoff=0)

        if admin_test:
            game_menu.add_command(label="Delete Game", command=end_game)

        game_menu.add_command(label="Exit", command=end_game)
        super().add_cascade(label="Game", menu=game_menu)

    def set(self):
        self.master.config(menu=self)

    def unset(self):
        self.master.config(menu=None)
