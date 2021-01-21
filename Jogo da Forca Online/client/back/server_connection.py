from socket import socket
from multiprocessing import Queue
from utils.utils import check_type
from .process_all import ProcessAll
from .process_receive import ProcessReceive
from .process_send import ProcessSend


class ServerConnection:
    def __init__(self, ip, port):
        self.address = (ip, port)
        self.process_list = []
        self.socket = socket()
        a = 0
        while True:
            try:
                self.socket.connect(self.address)
                break
            except ConnectionRefusedError:
                if a == 5:
                    raise ConnectionRefusedError
                a += 1
                continue

        self.queue_send = Queue()
        self.queue_receive = Queue()
        self.queue_front = Queue()

        self.process_send = ProcessSend(self.queue_send, self.queue_front, self.socket)
        self.process_receive = ProcessReceive(self.queue_receive, self.socket)
        self.process = ProcessAll(self.queue_front, self.queue_send, self.queue_receive)

        self.process_list.append(self.process_send)
        self.process_list.append(self.process_receive)
        self.process_list.append(self.process)

    def send(self, jdata):
        check_type(jdata, dict)
        self.queue_send.put(jdata)

    def terminate(self):
        for a in self.process_list:
            a.terminate()

    def start(self):
        for a in self.process_list:
            a.start()

        self.process.intergame.start()
        self.process.intergame.game_to_server.end()
        self.terminate()
        self.socket.shutdown(1)
