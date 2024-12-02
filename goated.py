import random
import numpy as np
from pypokerengine.players import BasePokerPlayer
import pypokerengine.utils.visualize_utils as U
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 1000

class Goated(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        
        print(str(win_rate) + " BRUH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        choice = self.__choice_action(valid_actions)
        amount = choice["amount"]
        print(amount)


        if win_rate >= 2.0 / self.nb_player:
            action = valid_actions[2]
            amount = 10
        elif win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]  # fetch CALL action info
        elif amount == 0:
            action = valid_actions[1]
        else:
            action = valid_actions[0]



        # if win_rate >= 1.0 / self.nb_player:
        #     action = valid_actions[1]  # fetch CALL action info
        # elif win_rate >= 2.0 / self.nb_player:
        #     action = valid_actions[2]
        #     amount = 10
        # else:
        #     action = valid_actions[0]  # fetch FOLD action info
        return action['action'], amount

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        print(U.visualize_round_start(round_count, hole_card, seats, self.uuid))

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass