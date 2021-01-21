import tkinter as tk
from tkinter.messagebox import showwarning
from front.game.make_play import MakePlay
from utils.utils_front import front_page


class GameFront(tk.Frame):
    def __init__(self, inter_game, data, master):
        self.inter_game = inter_game
        self.data = data
        self.master = master
        self.sub_window = None
        self.sub_menu = None

        super().__init__(master)

        self.menu_bar = tk.Menu(self)
        master.config(menu=self.menu_bar)

        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self._init_game_menu()
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)

        self.name_room = tk.Label(self)
        self.name_room.grid(row=0, column=0)

        self.id_room = tk.Label(self)
        self.id_room.grid(row=0, column=1)

        self.round = tk.Label(self)
        self.round.grid(row=0, column=2)

        self.times = tk.Label(self)
        self.times.grid(row=1, column=0)

        self.word = tk.Label(self)
        self.word.grid(row=1, column=1)

        self.exit = tk.Button(self, text="Make Your Play")
        self.exit.grid(row=2)

        self.players_time = []
        for i in range(3, 5):
            aux = []
            for j in range(0, 2):
                label = tk.Label(self)
                label.grid(row=i, column=j)
                aux.append(label)
            self.players_time.append(aux)

        self.init()
        super().pack()

    def _init_game_menu(self):
        if self.data["admin"]:
            self.game_menu.add_command(label="Delete Game", command=self._end_game)

        self.game_menu.add_command(label="Exit", command=self._exit_game)

    def _init_times(self):
        aux = ""
        i = 0
        for i in range(0, self.data["total_attempts"] - self.data["attempts"]):
            aux += "O"

        for i in range(i, self.data["total_attempts"] - 1):
            aux += "X"

        return aux

    def _init_players_time(self):
        count = 0

        for i in self.players_time:
            for j in i:
                if count < len(self.data["players"]):
                    if count == self.data["turn"]:
                        j.config(text=self.data["players"][count]["name_player"], background='yellow')
                    else:
                        j.config(text=self.data["players"][count]["name_player"], background="white")

                    count += 1
                else:
                    j.config(text="", background="white")

    def init(self):
        self.name_room.config(text=f'Name Room: {self.data["name_room"]}')
        self.id_room.config(text=f'Id Room: {self.data["id_room"]}')
        self.round.config(text=f'Rounds: {self.data["rounds"]}')
        self.times.config(text=f'Attempts: {self._init_times()}')
        self.word.config(text=f'Word: {self.data["word_discover"]}')
        self.exit.config(command=self._make_move(self.data["your"]))

        self._init_players_time()

    def _close_function(self):
        self.sub_window.destroy()
        self.sub_window = None
        self.sub_menu = None

    def _end_sub(self):
        if self.sub_window is not None:
            self.sub_window.destroy()

        self.sub_window = \
            self.sub_menu = None

    def _make_move(self, test):
        def f():
            if test:
                self.sub_window = front_page("200x200", self._close_function, self)
                self.sub_window.protocol("WM_DELETE_WINDOW", self._end_sub)
                self.sub_menu = MakePlay(self.inter_game, self._end_sub, len(self.data["word_discover"]), self.sub_window)
            else:
                showwarning("Warning", "It's Not Your Turn!")

        return f

    def _exit_game(self):
        self.inter_game.exit_room(True)

    def _end_game(self):
        self.inter_game.end_game()

    def destroy(self):
        self.master.config(menu=None)
        self._end_sub()
        super().destroy()
