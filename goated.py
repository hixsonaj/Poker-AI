import random
import numpy as np
from pypokerengine.players import BasePokerPlayer

class Goated(BasePokerPlayer):
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}  # Q-values for state-action pairs
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def declare_action(self, valid_actions, hole_card, round_state):
        state = self.__encode_state(round_state, hole_card, valid_actions)
        action = self.__choose_action(state, valid_actions)
        self.last_state = state
        self.last_action = action
        action_info = valid_actions[action]
        action, amount = action_info["action"], action_info["amount"]
        if action == "raise":
            amount = 1
        return action, amount   # action returned here is sent to the poker engine    
    
    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        reward = self.__calculate_reward(winners)
        self.__update_q_value(reward)
        pass

    def __encode_state(self, round_state, hole_card, valid_actions):
        # Simple encoding of the state (you can expand this)
        state = (tuple(hole_card), round_state["pot"]["main"]["amount"])
        return state

    def __choose_action(self, state, valid_actions):
        if random.uniform(0, 1) < self.epsilon:  # Exploration
            return random.choice(range(len(valid_actions)))
        else:  # Exploitation
            q_values = [self.q_table.get((state, a), 0) for a in range(len(valid_actions))]
            return np.argmax(q_values)

    def __update_q_value(self, reward):
        # Update Q-value using the Q-learning formula
        old_q_value = self.q_table.get((self.last_state, self.last_action), 0)
        best_next_q = max([self.q_table.get((self.last_state, a), 0) for a in range(len(self.q_table))], default=0)
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * best_next_q - old_q_value)
        self.q_table[(self.last_state, self.last_action)] = new_q_value

    def __calculate_reward(self, winners):
        # Assign reward based on outcome
        if self.uuid in winners:
            return 1  # Won
        else:
            return -1  # Lost
