import asyncio
import poke_env
from agent import RandomMaxDamage, MetaRandomDamage, MetaMaxDamage, Random, Heuristic
from tournament import HeadsUp, Tournament

battle_format = "gen9vgc2025regg"

# No authentication required
players: list[poke_env.Player] = [
    MetaMaxDamage(battle_format=battle_format, team=i) for i in range(1, 5)
]

# tournament = Tournament(players, 50)
# tournament.run()

heads_up = HeadsUp(
  Heuristic(battle_format=battle_format, max_concurrent_battles=1, team=1), 
  MetaMaxDamage(battle_format=battle_format, max_concurrent_battles=1, team=1), 
  100)
heads_up.run()


# def main():
#     player = Heuristic(battle_format=battle_format, team=1)
#     print(player.username)
#     asyncio.run(player.accept_challenges(opponent=None, n_challenges=1))
#     print(player.n_won_battles, player.n_lost_battles)


# if __name__ == "__main__":
#     main()
