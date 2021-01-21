from logic.receive import Receive
from multiprocessing import Manager


class Interface:
    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.manager_process = Manager()
        self.rooms = self.manager_process.dict()

    def start_server(self):
        server = Receive(self.address, self.port, self.rooms)
        server.start()

    def edit_server(self):
        pass

    def end_server(self):
        pass
