from pokebattlerl.agent.loggingAgent import LoggingAgent


class RandomPlayer(LoggingAgent):
    def __init__(self):
        super().__init__()

    def choose_move(self, battle):
        super().log(battle)
        return self.choose_random_move(battle)
