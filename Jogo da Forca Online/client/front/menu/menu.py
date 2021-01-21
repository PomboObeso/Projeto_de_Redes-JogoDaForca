import tkinter as tk
from front.menu.sub_menu import SubMenu
from utils.utils_front import front_page


class Menu(tk.Frame):
    def __init__(self, intergame, master):
        super().__init__(master)
        self.intergame = intergame

        self.label = tk.Label(self, text="Hangman Game Online (HGO)")
        self.label.pack()

        self.button_create = tk.Button(self, text="Create Room", command=self._button_create)
        self.button_create.pack()

        self.button_enter = tk.Button(self, text="Enter Room", command=self._button_enter)
        self.button_enter.pack()

        self.sub_window = None
        self.sub_menu = None

        master.focus_force()
        master.grab_set()

        super().pack()

    def _close_sub_janel(self):
        self.sub_window.destroy()
        self.sub_window = None
        self.sub_menu = None

    def _create_sub(self, text, function):
        if self.sub_window is not None:
            self.sub_window.lift()
        else:
            self.sub_window = front_page("200x200", self._close_sub_janel, self)
            self.sub_menu = SubMenu(text, function, self.sub_window)

    def _button_create(self):
        self._create_sub((
            "Create Room",
            "Name Player: ",
            "Name Room: ",
            "Password: "
        ), self.intergame.game_to_server.create_room)

    def _button_enter(self):
        self._create_sub((
            "Enter Room",
            "Name Player: ",
            "Id Room: ",
            "Password: "
        ), self.intergame.game_to_server.enter_room)

    def destroy(self):
        if self.sub_window is not None:
            self.sub_window.destroy()

        self.label = self.button_create = self.button_enter \
            = self.sub_window = self.sub_menu = None

        super().destroy()
