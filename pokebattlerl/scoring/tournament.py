import asyncio
from dataclasses import dataclass, field
from itertools import combinations
from pokebattlerl.agent.loggingAgent import LoggingAgent


@dataclass
class Tournament:
    agents: list[LoggingAgent] = field(default_factory=list)

    def start(self):
        for agent1, agent2 in combinations(self.agents, 2):
            asyncio.run(agent1.battle_against(agent2, n_battles=1))


@dataclass
class FullTournament(Tournament):
    """
    Make every player play against every other player
    """

    def start(self):
        for agent1, agent2 in combinations(self.agents, 2):
            asyncio.run(agent1.battle_against(agent2, n_battles=1))

    def start_sync(self):
        self.loop.run_until_complete(self.start())
