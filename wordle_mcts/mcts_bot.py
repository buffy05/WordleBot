import random
from mcts_node import MCTSNode
from game_state import GameState

#full, comprehensive mcts bot, prev version was faster and less buggy... but was not that accurate
#inspired by the github tutorial on mcts in python (will put link in sources) 
#still a little buggy 
class MCTSBot:
    def __init__(self, game_state, simulations=100):
        self.simulations = simulations
        self.root = MCTSNode(game_state)

    #buggy area: needs revising (sometimes works, sometimes returns AttributeError: 'NoneType' object has no attribute 'state')
    def search(self):
        for _ in range(self.simulations):
            node = self.select(self.root)
            reward = self.simulate(node.state)
            self.backpropagate(node, reward)
        best_child = self.root.best_child(c=0)
        if best_child is None:
            return random.choice(self.root.state.get_possible_guesses())
        return best_child.state.guess_history[-1][0]

    def select(self, node):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            node = node.best_child()
            if node is None:
                break
        return node

    def simulate(self, state):
        from wordle_game import WordleGame

        if not state.candidates:
            return 0

        solution = random.choice(state.candidates)
        game = WordleGame(state.candidates, target_word=solution)

        for _ in range(6 - state.depth):
            possible_guesses = state.get_possible_guesses()
            if not possible_guesses:
                return 0
            guess = random.choice(possible_guesses)
            feedback_list = game.make_guess(guess)
            feedback = ''.join(feedback_list)

            if feedback == 'ggggg':
                return 6 - (state.depth + game.current_attempt)

        return 0

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent
