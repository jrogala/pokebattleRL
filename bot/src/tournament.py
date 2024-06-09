import asyncio
from dataclasses import dataclass, field
from itertools import combinations
from poke_env import Player


@dataclass
class Tournament:
    agents: list[Player] = field(default_factory=list)
    amount_of_game: int = 1

    def __post_init__(self):
        if len(self.agents) < 2:
            raise ValueError("Tournament must have at least 2 agents")
        print(f"Making a tournament with agents: {self.agents}")

    async def battle(self, agent1: Player, agent2: Player, n_battles):
        await agent1.battle_against(agent2, n_battles=n_battles)

    async def arun(self):
        for agent1, agent2 in combinations(self.agents, 2):
            print(f"Battle between {agent1} and {agent2}")
            await self.battle(agent1, agent2, n_battles=self.amount_of_game)

    def run(self):
        asyncio.run(self.arun())
        winner = max(self.agents, key=lambda x: x.n_won_battles)
        print(
            f"winner is: {winner.username} with winrate: {winner.n_won_battles / winner.n_finished_battles}"
        )
        print(
            "others winrate: ",
            ", ".join(
                [
                    f"{agent.username}: {agent.n_won_battles / agent.n_finished_battles}"
                    for agent in self.agents
                    if agent != winner
                ]
            ),
        )


@dataclass
class HeadsUp:
    agent_1: Player
    agent_2: Player
    amount_of_game: int = 1

    def __post_init__(self):
        print(f"Making a heads up with agents: {self.agent_1} and {self.agent_2}")
        # self.agent_1.reset_battles()
        # self.agent_2.reset_battles()

    async def battle(self, n_battles):
        await self.agent_1.battle_against(self.agent_2, n_battles=n_battles)

    async def arun(self):
        await self.battle(n_battles=self.amount_of_game)

    def run(self):
        asyncio.run(self.arun())
        winner = (
            self.agent_1
            if self.agent_1.n_won_battles > self.agent_2.n_won_battles
            else self.agent_2
        )
        print(f"Battle finished, winner is: {winner}")
        print(f"Winner winrate: {winner.n_won_battles / winner.n_finished_battles}")
