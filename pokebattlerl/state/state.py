from typing import Optional
import faust
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.battle import Battle


class PokemonMove(faust.Record, serializer="json"):
    move_id: str


class PokemonState(faust.Record, serializer="json"):
    pokemon_id: str
    hp: Optional[int]
    attack: Optional[int]
    defense: Optional[int]
    special_attack: Optional[int]
    special_defense: Optional[int]
    speed: Optional[int]
    status: Optional[str]
    level: Optional[int]
    moves: list[PokemonMove]
    ability: Optional[str]


class BattleState(faust.Record, serializer="json"):
    battle_id: str
    active_pokemon: PokemonState
    opponent_active_pokemon: PokemonState
    available_moves: list[PokemonMove]
    available_switches: list[PokemonState]


def get_pokemon_state(pokemon: Pokemon) -> PokemonState:
    return PokemonState(
        pokemon_id=pokemon.species,
        hp=pokemon.current_hp,
        attack=pokemon.stats["atk"],
        defense=pokemon.stats["def"],
        special_attack=pokemon.stats["spa"],
        special_defense=pokemon.stats["spd"],
        speed=pokemon.stats["spe"],
        status=str(pokemon.status),
        level=pokemon.level,
        moves=[PokemonMove(move_id=str(move.id)) for move in pokemon.moves.values()],
        ability=pokemon.ability,
    )


def get_battle_state(
    uuid: str,
    battle: Battle,
) -> dict:
    active_pokemon = battle.active_pokemon
    pokemon_opponent = battle.opponent_active_pokemon
    if active_pokemon is None:
        return b""
    if pokemon_opponent is None:
        return b""
    return BattleState(
        battle_id=battle.battle_tag,
        active_pokemon=get_pokemon_state(active_pokemon),
        opponent_active_pokemon=get_pokemon_state(pokemon_opponent),
        available_moves=[
            PokemonMove(move_id=str(move.id)) for move in active_pokemon.moves.values()
        ],
        available_switches=[
            get_pokemon_state(pokemon) for pokemon in battle.team.values()
        ],
    ).dumps()
