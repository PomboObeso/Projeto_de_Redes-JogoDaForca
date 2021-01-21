from multiprocessing import Process, Manager
from interface.server_to_game.game_process import GameProcess
from interface.server_to_game.inter_game import InterGame
from interface.server_to_game.menu_process import MenuProcess
from time import sleep


class ProcessAll(Process):
    def __init__(self, queue_front, queue_send, queue_receive):
        self.queue_send = queue_send
        self.queue_receive = queue_receive

        self.intergame = InterGame(queue_front, self.queue_send, self.queue_receive)

        super().__init__(target=self._run)

    def _run(self):
        while True:
            if self.queue_receive.empty():
                sleep(0.1)
                continue

            aux = self.queue_receive.get()
            test = aux['type']

            if test == "menu":
                run = MenuProcess(self.intergame, aux, self.queue_send)
            elif test == "game":
                run = GameProcess(self.intergame, aux, self.queue_send)
            else:
                raise RuntimeError

            run.start()
