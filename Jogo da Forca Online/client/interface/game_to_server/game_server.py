from utils.utils import mount_message


class GameServer:
    def __init__(self, queue_send, queue_receive):
        self.queue_send = queue_send
        self.queue_receive = queue_receive

    def _return_function(self, send):
        def f():
            self.queue_send.put(send)

        return f

    def create_room(self, name_player, name_room, password):
        if name_player == "":
            return "Name Player must be a string no empty"
        elif name_room == "":
            return "Name Room must be a string no empty"

        self.queue_send.put(mount_message("menu_create", (name_player, name_room, password)))
        return None

    def enter_room(self, name_player, id_room, password):
        if name_player == "":
            return "Name Player must be a string no empty"
        elif id_room == "":
            return "Id Room must be a string no empty"

        self.queue_send.put(mount_message("menu_enter", (name_player, id_room, password)))
        return None

    def exit_room(self):
        send = {
            "type": "room",
            "subtype": "exit"
        }

        return self._return_function(send)

    def end(self):
        send = {
            "type": "menu",
            "subtype": "end"
        }

        self.queue_send.put(send)

        while not self.queue_send.empty():
            continue
