import tkinter as tk
from front.menu.loading_page import LoadingPage
from utils.utils_front import front_page
from tkinter.messagebox import showwarning


class SubMenu(tk.Frame):
    def __init__(self, text, function, master):
        self.text = text
        self.function = function

        self.loading_page = None
        self.loading_frame = None

        super().__init__(master)

        self.title = tk.Label(self, text=text[0])
        self.title.pack()

        self.input_name_1 = tk.Label(self, text=text[1])
        self.input_name_1.pack()

        self.input_1 = tk.Text(self, height=1, padx=2, pady=2)
        self.input_1.pack()

        self.input_name_2 = tk.Label(self, text=text[2])
        self.input_name_2.pack()

        self.input_2 = tk.Text(self, height=1, padx=2, pady=2)
        self.input_2.pack()

        self.input_name_3 = tk.Label(self, text=text[3])
        self.input_name_3.pack()

        self.input_3 = tk.Text(self, height=1, padx=2, pady=2)
        self.input_3.pack()

        commit_button = tk.Button(self, text="Ok", command=self._aux_create)
        commit_button.pack()

        super().pack()

    @staticmethod
    def _alert_message(text):
        showwarning(title="Warning", message=text)

    def _aux_create(self):
        result_1 = self.input_1.get("1.0", "end-1c")
        result_2 = self.input_2.get("1.0", "end-1c")
        result_3 = self.input_3.get("1.0", "end-1c")

        aux = self.function(result_1, result_2, result_3)
        if aux is not None:
            self._alert_message(aux)
        else:
            self._create_loading()

    def _create_loading(self):
        if self.loading_page is not None:
            return

        self.loading_page = front_page("50x50", lambda: None, self)
        self.loading_frame = LoadingPage(self.loading_page)

    def close_loading(self):
        self.destroy()
        self.loading_page = None
        self.loading_frame = None

    def destroy(self):
        if self.loading_page is not None:
            self.loading_page.destroy()
            self.loading_page = None
            self.loading_frame = None

        super().destroy()
