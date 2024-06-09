import asyncio
import docker
import pytest
import pytest_asyncio
from pokebattlerl.agent import Random
from pokebattlerl.agent.loggingAgent import LoggingAgent
from pokebattlerl.scoring.tournament import FullTournament, Tournament
import requests

import logging

_logger = logging.getLogger(__name__)


# Example test function using the fixture
def test_docker_up():
    # Use the fixture data in your test
    try:
        client = docker.from_env()
    except Exception:
        pytest.exit("Docker is not running")
    if not any(
        (
            "pokebattlerl" in str(container.image)
            for container in client.containers.list()
        )
    ):
        pytest.exit(
            "pokebattlerl container is not running\nPlease run invoke docker --upd"
        )
    if requests.get("http://localhost:8000").status_code != 200:
        pytest.exit("Server is not up")


def test_single_battle():
    agent1 = Random.RandomPlayer()
    agent2 = Random.RandomPlayer()
    tournament = Tournament([agent1, agent2])
    tournament.start()


def test_round_robin():
    agents = [Random.RandomPlayer() for _ in range(4)]

    FullTournament(agents).start()
    for agent in agents:
        assert agent.n_finished_battles == 3
