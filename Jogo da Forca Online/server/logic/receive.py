from utils.utils import check_type
from socket import socket
from .communicate_process import CommunicateProcess


class Receive:
    def __init__(self, ip, port, rooms):
        check_type(ip, str)
        check_type(port, int)

        self.address = (ip, port)
        self.server_socket = socket()
        self.server_socket.bind(self.address)
        self.rooms = rooms

    def start(self):
        print(f"Start server listen in: {self.address}")
        self.server_socket.listen(1000)

        while True:
            aux = self.server_socket.accept()
            print(f"\tNew connection with: {aux[1]}")

            lister = CommunicateProcess(aux[0], aux[1], self.rooms)
            lister.start()


