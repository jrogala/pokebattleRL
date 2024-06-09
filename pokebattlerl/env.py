from poke_env import AccountConfiguration, Player
from poke_env.player import Gen8EnvSinglePlayer

# No authentication required
my_account_config = AccountConfiguration("agent", None)
player = Player(account_configuration=my_account_config)
