from multiprocessing import Process
from json import loads


class ProcessReceive(Process):
    def __init__(self, queue, socket):
        self.queue = queue
        self.socket = socket

        super().__init__(target=self._process_receive)

    def _process_receive(self):
        while True:
            try:
                response = self.socket.recv(1024)
            except ConnectionResetError:
                break

            aux = response.decode('utf-8').replace("}{", "}\n{")
            aux = aux.split("\n")

            for a in aux:
                jdata = loads(a)
                self.queue.put(jdata)
