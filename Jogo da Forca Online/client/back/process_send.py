from multiprocessing import Process
from json import dumps
from time import sleep


class ProcessSend(Process):
    def __init__(self, queue, queue_front, socket):
        self.queue = queue
        self.queue_front = queue_front
        self.socket = socket

        super().__init__(target=self._process_send)

    def _process_send(self):
        while True:
            if self.queue.empty():
                sleep(0.1)
                continue

            aux = self.queue.get()
            jdata = dumps(aux)

            try:
                self.socket.sendall(jdata.encode())
            except ConnectionResetError:
                self.queue_front.put(("end_all", None))
