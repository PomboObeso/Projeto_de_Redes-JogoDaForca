from front.game.game_front import GameFront
from front.menu.menu import Menu
from interface.game_to_server.game_server import GameServer
import tkinter as tk
from tkinter.messagebox import showerror
from utils.utils import mount_message


class InterGame:
    def __init__(self, queue_front, queue_send, queue_receive):
        self.queue_front = queue_front
        self.queue_send = queue_send

        self.game_to_server = GameServer(queue_send, queue_receive)

    def enter_room(self, data):
        if not data["status"]:
            self.queue_front.put(("end_game", None))
            self.queue_front.put(("alert", data["message"]))
        else:
            self.queue_front.put(("game_start", None))
            self.queue_send.put(mount_message("game_init", (data["id_room"],)))

    def make_play(self, text):
        self.queue_send.put(mount_message("game_make_play", (text,)))

    def end_game(self):
        self.queue_send.put(mount_message("game_end"))
        self.queue_send.put(mount_message("game_att_request"))

    def exit_room(self, test):
        if test:
            self.queue_send.put(mount_message("game_exit"))
            self.queue_send.put(mount_message("game_att_request"))
        else:
            self.queue_front.put(("end_game", None))

    def alert(self, alert=None):
        if alert is None:
            alert = "Error"

        self.queue_front.put(("alert", alert))

    def att_state(self, data):
        self.queue_front.put(("game_update", data))

    def _periodic_inter(self, root, page):
        def f():
            nonlocal page
            if self.queue_front.empty():
                self.queue_send.put(mount_message("game_att_request"))
                root.after(500, self._periodic_inter(root, page))
                return

            aux = self.queue_front.get()
            element = aux[0]
            data = aux[1]

            if element == "game_update":
                if type(page) == Menu:
                    page.destroy()
                    page = GameFront(self, data, root)
                page.data = data
                page.init()
            elif element == "game_start":
                page.destroy()
            elif element == "end_game":
                page.destroy()
                page = Menu(self, root)
            elif element == "end_all":
                root.destroy()
            elif element == "alert" and data is not None:
                showerror("Error", data)
            else:
                raise RuntimeError("Error in periodic inter front")

            root.after(500, self._periodic_inter(root, page))

        return f

    def start(self):
        root = tk.Tk()
        root.geometry("400x400")
        window = Menu(self, root)
        root.after(500, self._periodic_inter(root, window))
        root.mainloop()
