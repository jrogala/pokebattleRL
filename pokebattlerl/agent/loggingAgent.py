import json
from typing import Awaitable
import uuid
import faust
from poke_env import Player

from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
from poke_env.environment.battle import Battle
from pokebattlerl.state.state import (
    BattleState,
    PokemonState,
    PokemonMove,
    get_pokemon_state,
    get_battle_state,
)
from confluent_kafka import Producer
import logging
import warnings


logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class LoggingAgent(Player):
    def __init__(self):
        super().__init__(max_concurrent_battles=100)
        self.uuid = str(uuid.uuid4())
        conf = {
            "bootstrap.servers": "localhost:9092",
            "client.id": f"Agent_{self.uuid}",
        }
        self.producer = Producer(conf)

    def choose_move(
        self, battle: AbstractBattle
    ) -> BattleOrder | Awaitable[BattleOrder]:
        return self.choose_random_move(battle)

    def log(self, battle: Battle) -> BattleOrder | Awaitable[BattleOrder]:
        try:
            self.producer.produce(
                "battle",
                key=self.uuid,
                value=get_battle_state(self.uuid, battle),
            )
            self.producer.flush()
        except Exception as e:
            warnings.warn(f"Failed to log battle: {e}")
            pass
