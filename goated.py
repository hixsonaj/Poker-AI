import random
import numpy as np
from pypokerengine.players import BasePokerPlayer
import pypokerengine.utils.visualize_utils as U
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from sklearn.linear_model import LinearRegression


NB_SIMULATION = 1000

class Goated(BasePokerPlayer):

    def __init__(self, nb_player=2):
        super().__init__()
        self.nb_player = nb_player
        self.model_raise = LinearRegression()  # Model for predicting raise threshold
        self.model_call = LinearRegression()  # Model for predicting call threshold
        self.training_data = []  # Collect features and targets for training
        self.raise_threshold = random.uniform(0.6, 1.6)  # Default raise threshold
        self.call_threshold = random.uniform(0.3, 1.3)  # Default call threshold
        self.models_trained = False  # Flag to indicate if models are trained


    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        pot_size = round_state['pot']['main']['amount']
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
        
        # Adjust thresholds based on agent's historical performance
        self.__update_thresholds(pot_size, active_players, len(community_card), win_rate)

        # Check the win rate and decide the action
        if win_rate >= self.raise_threshold / self.nb_player:
            # Choose RAISE with different bet percentages for each street
            if len(community_card) == 0:  # Pre-flop
                random_num = random.uniform(1.1, 2.7)
            elif len(community_card) == 3:  # Flop
                random_num = random.uniform(0.39, 1.4)
            elif len(community_card) == 4:  # Turn
                random_num = random.uniform(0.65, 1.1)
            else:  # River
                random_num = random.uniform(0.9, 2.2)

            raise_amount = max((random_num * int(pot_size)), valid_actions[2]['amount']['min'])
            raise_amount = min(raise_amount, valid_actions[2]['amount']['max'])  # Ensure valid range
            action = valid_actions[2]['action']
            amount = int(raise_amount)  # Convert bet size to integer
        elif win_rate >= self.call_threshold / self.nb_player:
            # Choose CALL if win rate is moderate
            action = valid_actions[1]['action']
            amount = valid_actions[1]['amount']
        elif valid_actions[1]['amount'] == 0:
            # If FOLD action is essentially CHECK (amount is 0), choose it
            action = valid_actions[1]['action']
            amount = valid_actions[1]['amount']

        self.__collect_training_data(pot_size, active_players, len(community_card), win_rate)


        return action, amount
    
    def __update_thresholds(self, pot_size, active_players, street, win_rate):
        """
        Predict thresholds using the regression models or use defaults if not trained.
        """
        features = np.array([[pot_size, active_players, street, win_rate]])
        if self.models_trained:
            try:
                self.raise_threshold = self.model_raise.predict(features)[0]
                self.call_threshold = self.model_call.predict(features)[0]
            except NotFittedError:
                print("Models are not fitted yet. Using default thresholds.")

    def __collect_training_data(self, pot_size, active_players, street, win_rate):
        """
        Collects training data for the regression models.
        """
        self.training_data.append([pot_size, active_players, street, win_rate, self.raise_threshold, self.call_threshold])

        # Train the models periodically
        if len(self.training_data) > 10 and len(self.training_data) % 5 == 0:
            data = np.array(self.training_data)
            features = data[:, :4]  # First 4 columns are features
            raise_targets = data[:, 4]  # 5th column is the raise threshold
            call_targets = data[:, 5]  # 6th column is the call threshold

            self.model_raise.fit(features, raise_targets)
            self.model_call.fit(features, call_targets)
            self.models_trained = True  # Mark models as trained

            # Log model training
            print("Trained regression models on collected data.")

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        print(U.visualize_round_start(round_count, hole_card, seats, self.uuid))
        active_players = sum(1 for seat in seats if seat['state'] in ['participating', 'allin'])
        baseline_win_rate = 1 / active_players + 1  # Calculate baseline win rate
        # self.__update_thresholds(baseline_win_rate)

        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass