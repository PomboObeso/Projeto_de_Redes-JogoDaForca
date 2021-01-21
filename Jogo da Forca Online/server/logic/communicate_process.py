from multiprocessing import Queue, Value
from utils.utils import check_type
from .process_all import ProcessAll
from .process_receive import ProcessReceive
from .process_send import ProcessSend


class CommunicateProcess:
    def __init__(self, socket, address, rooms):
        check_type(address, tuple)

        self.socket = socket
        self.address = address
        self.rooms = rooms

        self.process_list = []
        self.client_status = Value('i', True)
        self.queue_send = Queue()
        self.queue_receive = Queue()

        self.process_send = ProcessSend(self.queue_send, self.socket, self.client_status)
        self.process_receive = ProcessReceive(self.queue_receive, self.socket, self.client_status)
        self.process = ProcessAll(self.queue_send, self.queue_receive, self.address,
                                  self.client_status, self.rooms)

        self.process_list.append(self.process_send)
        self.process_list.append(self.process_receive)
        self.process_list.append(self.process)

    def terminate(self):
        for a in self.process_list:
            a.terminate()

    def start(self):
        for a in self.process_list:
            a.start()