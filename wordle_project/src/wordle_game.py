import random

#basic wordle game class, provides feedback (for bot), tested it by playing manually
class WordleGame:
    def __init__(self, word_list, target_word=None, max_attempts=6):
        self.word_list = word_list
        self.max_attempts = max_attempts
        self.target_word = target_word or random.choice(word_list)
        self.current_attempt = 0
        self.game_over = False
        self.guess_history = []

    def make_guess(self, guess):
        guess = guess.lower()
        if self.game_over:
            raise ValueError("Game is over. Please reset to play again.")
        if guess not in self.word_list:
            raise ValueError("Invalid guess: Not in word list.")
        if len(guess) != 5:
            raise ValueError("Invalid guess: Must be 5 letters.")

        feedback = self.get_feedback(guess)
        self.guess_history.append((guess, feedback))
        self.current_attempt += 1

        if guess == self.target_word or self.current_attempt >= self.max_attempts:
            self.game_over = True

        return feedback

    def get_feedback(self, guess):
        result = ["b"] * 5 
        target_chars = list(self.target_word)
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

    def is_won(self):
        return self.guess_history and self.guess_history[-1][0] == self.target_word

    def is_over(self):
        return self.game_over

    def reset(self, new_target=None):
        self.target_word = new_target or random.choice(self.word_list)
        self.current_attempt = 0
        self.game_over = False
        self.guess_history = []

    def get_state(self):
        return {
            "attempts": self.current_attempt,
            "history": self.guess_history,
            "is_over": self.game_over,
            "is_won": self.is_won(),
        }