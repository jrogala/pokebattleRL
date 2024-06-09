from agent.MoveAgent import HeuristicMove, MaxDamage, RandomMove
from agent.TeamAgent import MetaTeam, RandomTeam


class MetaMaxDamage(MaxDamage, MetaTeam):
    pass


class MetaRandomDamage(RandomMove, MetaTeam):
    pass


class RandomMaxDamage(MaxDamage, RandomTeam):
    pass


class Random(RandomMove, RandomTeam):
    pass


class Heuristic(HeuristicMove, MetaTeam):
    pass
