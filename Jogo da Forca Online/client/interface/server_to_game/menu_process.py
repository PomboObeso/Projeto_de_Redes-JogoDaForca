class MenuProcess:
    def __init__(self, intergame, data, queue):
        self.intergame = intergame
        self.data = data
        self.queue = queue

    def start(self):
        aux = self.data['subtype']

        if aux == "enter":
            self.intergame.enter_room(self.data)
        elif aux == "start":
            self.intergame.start()
        else:
            raise RuntimeError
