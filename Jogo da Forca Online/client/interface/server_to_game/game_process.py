class GameProcess:
    def __init__(self, intergame, data, queue):
        self.intergame = intergame
        self.data = data
        self.queue = queue

    def _init_game(self):
        if not self.data["status"]:
            self.intergame.exit_room(False)
            self.intergame.alert("Problems with room, please create another.")

    def _att_state(self):
        self.intergame.att_state(self.data["state"])

    def _end_game(self):
        self.intergame.exit_room(False)

    def _alert(self):
        self.intergame.alert(self.data["message"])

    def start(self):
        aux = self.data["subtype"]

        if aux == "init":
            self._init_game()
        elif aux == "att_state":
            self._att_state()
        elif aux == "end":
            self._end_game()
        elif aux == "alert":
            self._alert()
        else:
            raise RuntimeError("Error in GameProcess")
