from random import choice
from poke_env import Player
from poke_env.data.replay_template import f
from poke_env.environment import DoubleBattle, Move, MoveCategory, ObservedPokemon, Pokemon, Target
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player import BattleOrder, DoubleBattleOrder
import logging

_logger = logging.getLogger(__name__)


class MaxDamage(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def choose_move(self, battle) -> DoubleBattleOrder | BattleOrder:
        if isinstance(battle, DoubleBattle):
            # 1st pokemon
            best_move_1 = None
            best_move_2 = None
            if battle.available_moves[0]:
                best_move_1 = max(
                    battle.available_moves[0], key=lambda move: move.base_power
                )
            if battle.available_moves[1]:
                best_move_2 = max(
                    battle.available_moves[1], key=lambda move: move.base_power
                )
            if best_move_1 and best_move_2:
                return DoubleBattleOrder(
                    BattleOrder(best_move_1), BattleOrder(best_move_2)
                )
            else:
                return self.choose_random_move(battle)
        else:
            if battle.available_moves:
                best_move = max(
                    battle.available_moves, key=lambda move: move.base_power
                )
                return self.create_order(best_move)
            else:
                return self.choose_random_move(battle)


class RandomMove(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def choose_move(self, battle):
        return self.choose_random_move(battle)


class HeuristicMove(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def _compute_score(self, battle: DoubleBattle, mon: Pokemon, move: Move, target: Pokemon, *, _is_target_opponent=True) -> float:
        score = 0
        multiplicator: float = 1 if _is_target_opponent else -1
        if move.category == MoveCategory.PHYSICAL:
            if mon.stats["atk"] is not None and target.base_stats["def"] is not None:
                multiplicator *= mon.stats["atk"] / target.base_stats["def"]
        elif move.category == MoveCategory.SPECIAL:
            if mon.stats["spa"] is not None and target.base_stats["spd"] is not None:
                multiplicator *= mon.stats["spa"] / target.base_stats["spd"]
        if move.base_power:
            score += move.base_power * multiplicator
        # if move.drain:
        #     score += move.drain * move.base_power
        if move.boosts:
            score += sum(move.boosts.values()) * multiplicator
        self_boost = move.self_boost if move.self_boost else {}
        if self_boost:
            score += sum(self_boost.values()) * 100
        # if move.heal:
        #     score += move.heal * mon.max_hp
        if move.status:
            score += 50 * multiplicator
        return max(0.01, score)

    def choose_move(self, battle: AbstractBattle) -> BattleOrder | DoubleBattleOrder:
        if not isinstance(battle, DoubleBattle):
            return self.choose_random_move(battle)
        orderBattle = []
        # List all possible moves for each pokemon
        possible_moves = []
        for pokemon_id in range(2):
            pokemon = battle.active_pokemon[pokemon_id]
            if not pokemon:
                _logger.warning("No pokemon found for %s", pokemon_id)
                continue
            for move in battle.available_moves[pokemon_id]:
                # Opponent
                if move.target in [Target.NORMAL, Target.FOE_SIDE]:
                    for target_pos, target in enumerate(battle.opponent_active_pokemon):
                        if target is None:
                            _logger.warning("No target found for %s", pokemon)
                            continue
                        possible_moves.append((pokemon_id, move, target_pos, target))
                # Ally
                elif move.target in [Target.ADJACENT_ALLY, Target.ADJACENT_ALLY_OR_SELF, Target.ALLY_SIDE]:
                    for target_pos, target in enumerate(battle.active_pokemon):
                        if target is None:
                            _logger.warning("No target found for %s", pokemon)
                            continue
                        possible_moves.append((pokemon_id, move, target_pos, target))
                # Self
                elif move.target in [Target.SELF]:
                    possible_moves.append((pokemon_id, move, pokemon_id, pokemon))
                # All TODO: Implement
                elif move.target in [Target.ALL, Target.ALL_ADJACENT, Target.ALL_ADJACENT_FOES, Target.ALLIES, Target.ALLY_TEAM]:
                    _logger.warning("Move %s with target %s not implemented", move, move.target)
        print(possible_moves)
        # Check if we have to return a DoubleBattleOrder or a BattleOrder
        if len(orderBattle) == 2:
            return DoubleBattleOrder(orderBattle[0], orderBattle[1])
        elif len(orderBattle) == 1:
            return DoubleBattleOrder(orderBattle[0], None)
        return self.choose_random_doubles_move(battle)
