#might not need this/could take out...?
def apply_feedback(guess, feedback, word):
    used = [False] * 5
    for i in range(5):
        if feedback[i] == 'g':
            if word[i] != guess[i]:
                return False
            used[i] = True
    for i in range(5):
        if feedback[i] == 'y':
            if guess[i] == word[i] or guess[i] not in word:
                return False
            if sum((guess[i] == word[j]) and not used[j] for j in range(5)) == 0:
                return False
        elif feedback[i] == 'b':
            if any((guess[i] == word[j]) and not used[j] for j in range(5)):
                return False
    return True

class GameState:
    def __init__(self, candidates, guess_history=None, depth=0):
        self.candidates = candidates
        self.guess_history = guess_history or []
        self.depth = depth

    def get_possible_guesses(self):
        return self.candidates

    def next_state(self, guess, feedback):
        new_candidates = [w for w in self.candidates if apply_feedback(guess, feedback, w)]
        return GameState(new_candidates, self.guess_history + [(guess, feedback)], self.depth + 1)

    def is_terminal(self):
        return self.depth >= 6 or (self.guess_history and self.guess_history[-1][1] == 'ggggg')
