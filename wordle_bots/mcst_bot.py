import random
from collections import defaultdict

class MCTSBot:
    def __init__(self, word_list, num_simulations=100):
        self.word_list = word_list
        self.num_simulations = num_simulations
        self.candidates = word_list.copy()  # Start with all words

    def choose_move(self, game):
        """
        Choose the next move based on current game state.
        """
        if game.current_attempt == 0:
            return random.choice(["slate", "crane", "adieu", "roast", "later"])

        best_guess = None
        best_score = -1

        # **Only consider candidate words as guesses**
        for guess in self.candidates:
            score = self.evaluate_guess(guess)
            if score > best_score:
                best_score = score
                best_guess = guess

        return best_guess

    def evaluate_guess(self, guess):
        """
        Use Monte Carlo simulations to score a guess.
        """
        feedback_buckets = defaultdict(list)

        # **Sample from candidates, not full list**
        sample_size = min(self.num_simulations, len(self.candidates))
        if sample_size == 0:
            return 0  # fallback

        sample = random.sample(self.candidates, sample_size)

        for target in sample:
            feedback = self.simulate_feedback(guess, target)
            feedback_key = ''.join(feedback)
            feedback_buckets[feedback_key].append(target)

        score = 0
        for feedback, group in feedback_buckets.items():
            score += (len(self.candidates) - len(group))

        return score / sample_size

    def simulate_feedback(self, guess, target):
        """
        Simulate Wordle feedback.
        """
        result = ["b"] * 5
        target_chars = list(target)
        guess_chars = list(guess)

        for i in range(5):
            if guess_chars[i] == target_chars[i]:
                result[i] = "g"
                target_chars[i] = None
                guess_chars[i] = None

        for i in range(5):
            if guess_chars[i] is not None and guess_chars[i] in target_chars:
                result[i] = "y"
                target_index = target_chars.index(guess_chars[i])
                target_chars[target_index] = None

        return result

    def update_candidates(self, last_guess, feedback):
        """
        Prune candidates based on feedback.
        """
        new_candidates = []
        for word in self.candidates:
            if self.simulate_feedback(last_guess, word) == feedback:
                new_candidates.append(word)
        self.candidates = new_candidates
