from back.server_connection import ServerConnection


class Interface:
    def __init__(self, address, port):
        self.server_connection = ServerConnection(address, port)

    def start(self):
        print("Starting Client")
        self.server_connection.start()
