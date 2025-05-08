import math
import random
from utils import evaluate_guess

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        # Limit expansion to 50 children for efficiency
        return len(self.children) >= 50

    def best_child(self, c=1.4):
        def ucb(node):
            if node.visits == 0:
                return float('inf')
            return node.value / node.visits + c * math.sqrt(math.log(self.visits) / node.visits)
        if self.children:
            return max(self.children.values(), key=ucb)
        return None

    def expand(self, used_guesses=None):
        # Get possible guesses, excluding those already used
        guesses = [g for g in self.state.get_possible_guesses() if g not in used_guesses]
        
        # Sample up to 50 guesses if there are more
        if len(guesses) > 50:
            guesses = random.sample(guesses, 50)
        
        # Iterate through sampled guesses
        for guess in guesses:
            # Sample up to 20 candidate solutions
            solutions = random.sample(self.state.candidates, min(20, len(self.state.candidates)))
            for solution in solutions:
                feedback = evaluate_guess(guess, solution)  # Assumes evaluate_guess returns a string
                key = (guess, feedback)
                if key not in self.children:
                    next_state = self.state.next_state(guess, feedback)
                    child = MCTSNode(next_state, parent=self)
                    self.children[key] = child
                    return child
        return None