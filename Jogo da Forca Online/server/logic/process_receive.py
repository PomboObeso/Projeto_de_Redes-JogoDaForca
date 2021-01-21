from multiprocessing import Process
from json import loads
from json.decoder import JSONDecodeError
from time import sleep


class ProcessReceive(Process):
    def __init__(self, queue, socket, client_status):
        self.queue = queue
        self.socket = socket
        self.client_status = client_status

        super().__init__(target=self._process_receive)

    def _process_receive(self):
        while True:
            if not bool(self.client_status.value):
                self.socket.close()
                print("\t\tEnd of Process Receive")
                return

            try:
                response = self.socket.recv(1024)
            except ConnectionResetError:
                break

            if response is None:
                continue

            aux = response.decode('utf-8')

            try:
                jdata = loads(aux)
            except JSONDecodeError:
                continue

            self.queue.put(jdata)
