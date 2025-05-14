from utils import evaluate_guess

#helper function to simulate wordle feedback and validate against given feedback
def apply_feedback(guess, feedback, word):
    simulated_feedback = evaluate_guess(guess, word)
    return simulated_feedback == feedback

#gameState stores wordle game for each node in mcts
class GameState:
    def __init__(self, candidates, guess_history=None, depth=0):
        self.candidates = candidates
        self.guess_history = guess_history or []
        self.depth = depth

    #returns valid guesses but not the ones already used (prevents recycling/reusing old words)
    def get_possible_guesses(self, used_guesses=None):
        if used_guesses is None:
            return self.candidates
        return [w for w in self.candidates if w not in used_guesses]

    #create new gamestate post guess and feedback
    def next_state(self, guess, feedback):
        new_candidates = [w for w in self.candidates if apply_feedback(guess, feedback, w)]
        return GameState(new_candidates, self.guess_history + [(guess, feedback)], self.depth + 1)

    #if games is over, terminate (by this point have guesses or reached max depth)
    def is_terminal(self):
        return self.depth >= 6 or (self.guess_history and self.guess_history[-1][1] == 'ggggg')