from utils.utils import check_type, mount_message
from copy import deepcopy


class GameProcess:
    def __init__(self, data, game, address, queue_send, rooms):
        check_type(data, dict)
        self.data = data
        self.game = game
        self.address = address
        self.queue_send = queue_send
        self.rooms = rooms

    def _init_game(self):
        id_room = self.data["id_room"]
        room = self.rooms[id_room]

        test = False
        for i in room["players"]:
            if i["address"] == self.address:
                test = True
                break

        self.queue_send.put(mount_message("game_init", (test,)))
        self._send_state()

    def _exit_game(self):
        aux = self.game.remove_player(self.address)

        if aux is not None and aux:
            self.queue_send.put(mount_message("game_end"))

    def _end_game(self):
        self.game.end_game()

    def _send_state(self):
        id_room = self.game.actual_id
        if id_room is None:
            return

        try:
            room = self.rooms[id_room]
        except KeyError:
            self.game.actual_id = None
            self.queue_send.put(mount_message("game_end"))
            self.queue_send.put(mount_message("game_alert", ("The room no longer leaves.", )))

            return

        test = True
        for i in room["players"]:
            if i["address"] == self.address:
                test = False
                break

        if test and len(room["players"]) != 0:
            self.game.actual_id = None
            self.queue_send.put(mount_message("game_end"))
            self.queue_send.put(mount_message("game_alert", ("Leave the room!", )))
            return

        if room["word"] == room["word_discover"]:
            self.game.actual_id = None
            self.queue_send.put(mount_message("game_end"))

            if len(room["players"]) == 1:
                winner = 0
            else:
                winner = (room["rounds"] - 1) % len(room["players"])

            self.queue_send.put(mount_message(
                "game_alert", (f"The Game is End!\nThe Winner is {room['players'][winner]['name_player']}", )))
            return

        aux = deepcopy(room)
        aux["admin"] = aux["players"][0]["address"] == self.address
        _round = aux["rounds"] % len(aux["players"])
        aux["your"] = aux["players"][_round]["address"] == self.address
        del aux["word"]
        del aux["password"]
        for j in aux["players"]:
            del j["address"]

        aux["id_room"] = id_room

        self.queue_send.put(mount_message("game_att_state", (aux,)))

    def _make_play(self):
        aux = self.game.make_player(self.data["text"])

        if aux is None:
            self._send_state()
        else:
            self.queue_send.put(mount_message("game_alert", (aux, )))

    def start(self):
        aux = self.data["subtype"]
        if aux == "init":
            self._init_game()
        elif aux == "make_play":
            self._make_play()
        elif aux == "exit":
            self._exit_game()
        elif aux == "end":
            self._end_game()
        elif aux == "att_request":
            self._send_state()
        else:
            raise RuntimeError("Error game process.")
