import math
import random
from wordle_game import WordleGame

#referenced/adapted github tutorial
def get_feedback(guess, solution):
    game = WordleGame([solution], target_word=solution)
    feedback_list = game.get_feedback(guess)
    return ''.join(feedback_list)

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}  
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_possible_guesses())

    def best_child(self, c=1.4):
        def ucb(node):
            if node.visits == 0:
                return float('inf')
            return node.value / node.visits + c * math.sqrt(math.log(self.visits) / node.visits)
        if self.children:
            return max(self.children.values(), key=ucb)
        return None

    def expand(self):
        guesses = self.state.get_possible_guesses()
        random.shuffle(guesses)
        for guess in guesses:
            for solution in random.sample(self.state.candidates, min(20, len(self.state.candidates))):
                feedback = get_feedback(guess, solution)
                key = (guess, feedback)
                if key not in self.children:
                    next_state = self.state.next_state(guess, feedback)
                    child = MCTSNode(next_state, parent=self)
                    self.children[key] = child
                    return child
        return None
