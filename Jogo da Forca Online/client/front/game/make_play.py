import tkinter as tk


class MakePlay(tk.Frame):
    def __init__(self, inter_game, end_function, word_size, master):
        self.inter_game = inter_game
        self.end_function = end_function
        self.word_size = word_size
        self.master = master

        super().__init__(master)

        self.label = tk.Label(self, text="Answer: ")
        self.label.pack()

        self.input = tk.Text(self, height=1)
        self.input.pack()

        self.send_button = tk.Button(self, text="Ok", command=self._send)
        self.send_button.pack()

        super().pack()

    def _send(self):
        text = self.input.get("1.0", "end-1c")
        size = len(text)
        if size == 0:
            self.inter_game.queue_front.put(("alert", "Please the string don`t must be empty."))
        elif size > 1 and size != self.word_size:
            self.inter_game.queue_front.put(("alert", f"Please the string must be a size of 1 or {self.word_size}."))
        else:
            self.inter_game.make_play(text)
            self.end_function()
