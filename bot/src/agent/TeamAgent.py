from glob import glob
from pathlib import Path
from random import choice
from poke_env import Player
from poke_env.teambuilder import Teambuilder


class FileBuilder(Teambuilder):
    def __init__(self, folder: str):
        self.folder = folder
        super().__init__()

    def yield_team(self):
        teams = choice(glob(self.folder))
        with open(teams) as f:
            return self.join_team(self.parse_showdown_team(f.read()))


class MetaTeam(Player):
    def __init__(self, team: int = 1, *args, **kwargs):
        super().__init__(
            team=FileBuilder(folder=f"src/agent/teams/meta/{team}.txt"), **kwargs
        )


class RandomTeam(Player):
    def __init__(self, *args, **kwargs):
        print(Path("./").absolute())
        super().__init__(team=FileBuilder(folder="src/agent/teams/*/*.txt"), **kwargs)
