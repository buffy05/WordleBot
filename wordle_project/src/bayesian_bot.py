import random
from collections import Counter

class BayesianBot:
    
    def __init__(self, game_state, word_list):
        self.state = game_state
        self.valid_words = [w.strip().lower() for w in word_list]
        self.probs = [1 / len(self.valid_words)] * len(self.valid_words)

    @staticmethod
    def generate_feedback(guess, true_word):
        feedback = [0] * len(guess)
        guess_chars = list(guess)
        true_chars = list(true_word)
        used = [False] * len(true_chars)
        # Greens
        for i, ch in enumerate(guess_chars):
            if ch == true_chars[i]:
                feedback[i] = 2
                used[i] = True
        # Yellows
        for i, ch in enumerate(guess_chars):
            if feedback[i] == 0:
                for j, tch in enumerate(true_chars):
                    if not used[j] and ch == tch:
                        feedback[i] = 1
                        used[j] = True
                        break
        return feedback

    def bayesian_update(self, guess, feedback):
        #update prob based on bayes theroum
        updated = []
        n = len(guess)
        for w, p in zip(self.valid_words, self.probs):
            fb = self.generate_feedback(guess, w)
            sim = sum(1 for x, y in zip(feedback, fb) if x == y)
            updated.append(p * (1 + sim / n))
        total = sum(updated)
        if total == 0:  # Avoid division by zero
            self.probs = [1 / len(self.valid_words)] * len(self.valid_words)
        else:
            self.probs = [u / total for u in updated]

    def make_guess(self, used_guesses):
        valid_candidates = [i for i, w in enumerate(self.valid_words) if w not in used_guesses]
        if not valid_candidates:
            return None
        idx = max(valid_candidates, key=lambda i: self.probs[i])
        return self.valid_words[idx]

    def update_constraints(self, guess, feedback):
        mapping = {'b': 0, 'y': 1, 'g': 2}
        numeric_fb = [mapping[f] for f in feedback]
        self.bayesian_update(guess, numeric_fb)