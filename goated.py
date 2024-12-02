import random
import numpy as np
from pypokerengine.players import BasePokerPlayer
import pypokerengine.utils.visualize_utils as U
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 1000

class Goated(BasePokerPlayer):

    

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        pot_size = round_state['pot']['main']['amount']
        # active_players = self.__get_active_players(round_state)

        seats = round_state['seats']
        active_players = sum(1 for seat in seats if seat['state'] in ['participating', 'allin'])

        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )
        
        # Default action is FOLD (index 0), overwritten later if better options exist
        action = valid_actions[0]['action']
        amount = valid_actions[0].get('amount', 0)
        
        # Check the win rate and decide the action
        if win_rate >= 1.1 / active_players:
            # Choose RAISE if win rate is high enough
            raise_amount = max(int(pot_size), valid_actions[2]['amount']['min'])
            raise_amount = min(raise_amount, valid_actions[2]['amount']['max'])  # Ensure valid range
            action = valid_actions[2]['action']
            amount = raise_amount
        elif win_rate >= 0.8 / active_players:
            # Choose CALL if win rate is moderate
            action = valid_actions[1]['action']
            amount = valid_actions[1]['amount']
        elif valid_actions[1]['amount'] == 0:
            # If FOLD action is essentially CHECK (amount is 0), choose it
            action = valid_actions[1]['action']
            amount = valid_actions[1]['amount']

        return action, amount

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