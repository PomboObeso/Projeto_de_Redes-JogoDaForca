from multiprocessing import Process
from json import dumps
from time import sleep


class ProcessSend(Process):
    def __init__(self, queue, socket, client_status):
        self.queue = queue
        self.socket = socket
        self.client_status = client_status

        super().__init__(target=self._process_send)

    def _process_send(self, ):
        while True:
            if not bool(self.client_status.value):
                self.socket.close()
                print("\t\tEnd of Process Send")
                return

            if self.queue.empty():
                sleep(0.1)
                continue

            aux = self.queue.get()
            to_send = dumps(aux)
            to_send = to_send.encode()

            self.socket.send(to_send)
