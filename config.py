from pypokerengine.api.game import setup_config, start_poker
from default_agents import FishPlayer, FoldMan, RandomPlayer, HonestPlayer
from console_player import ConsolePlayer
from goated import Goated

config = setup_config(max_round=1000, initial_stack=1000, small_blind_amount=1)

#Default Agents
# config.register_player(name="Fish Player", algorithm=FishPlayer())              #Call machine
# config.register_player(name="Fold Man", algorithm=FoldMan())                    #Extremely tight
# config.register_player(name="Random Player", algorithm=RandomPlayer())          #Possibly intoxicated
# config.register_player(name="Honest Player", algorithm=HonestPlayer())          #Dudes trying his best

#User Input
# config.register_player(name="Console Player", algorithm=ConsolePlayer())        #I'm taking their money

#Goated Poker AI
config.register_player(name="Goated Poker-AI1", algorithm=Goated())              #Goated
config.register_player(name="Goated Poker-AI2", algorithm=Goated())              #Goated
config.register_player(name="Goated Poker-AI3", algorithm=Goated())              #Goated
config.register_player(name="Goated Poker-AI4", algorithm=Goated())              #Goated




game_result = start_poker(config, verbose=1)