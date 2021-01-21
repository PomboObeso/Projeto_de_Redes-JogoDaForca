from copy import deepcopy


class Game:
    def __init__(self, queue_send, queue_receive, rooms):
        self.queue_send = queue_send
        self.queue_receive = queue_receive
        self.rooms = rooms

        self.actual_id = None

    def _check_state(self):
        if not self.is_ready():
            raise RuntimeError("Game not set")

    def _get_room_data(self):
        self._check_state()
        return deepcopy(self.rooms[self.actual_id])

    def _set_room_data(self, data):
        self._check_state()
        self.rooms[self.actual_id] = data

    def remove_player(self, address):
        self._check_state()

        room = self._get_room_data()
        players = room["players"]

        test = True
        for i in range(0, len(players)):
            if players[i]["address"] == address:
                del players[i]
                test = False
                break

        if test:
            return None

        if len(players) == 0:
            self.end_game()
            return False

        self.rooms[self.actual_id] = room
        return True

    def end_game(self):
        self._check_state()
        del self.rooms[self.actual_id]

    def is_ready(self):
        return self.actual_id is not None

    def set_game(self, id_room):
        self.actual_id = id_room

    def end(self):
        try:
            self._check_state()
            del self.rooms[self.actual_id]
        finally:
            return

    def make_player(self, text):
        text = text.upper()

        room = self._get_room_data()
        word = room["word"]
        word_discover = room["word_discover"]

        word_len = len(word)
        text_len = len(text)

        count = 0
        if text_len == word_len:
            room["word_discover"] = word
            for i in word_discover:
                if i == "x":
                    count += 1
        elif text_len == 1:
            if text in word_discover:
                return "Please choice a new answer."
            aux = ""

            for i in range(0, word_len):
                if text == word[i]:
                    aux += word[i]
                    count += 1
                else:
                    aux += word_discover[i]
            room["word_discover"] = aux
        else:
            return "Problem in you answer!"

        if count == 0:
            room["attempts"] += 1
        room["rounds"] += 1

        size_players = len(room["players"])
        if size_players != 1:
            room["turn"] = room["rounds"] % size_players

        self._set_room_data(room)
