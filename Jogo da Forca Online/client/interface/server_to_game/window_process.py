from multiprocessing import Process


class WindowProcess(Process):
    def __init__(self, window, client_status):
        self.window = window
        self.client_status = client_status

        super().__init__(target=self.process)

    def process(self):
        self.window.mainloop()
        self.client_status.value = False
