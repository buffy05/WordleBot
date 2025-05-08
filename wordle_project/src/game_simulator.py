import random
import math
import os
from utils import load_words, evaluate_guess
from game_state import GameState
from mcts_node import MCTSNode
from csp_bot import CSPBot

# Define the path to the word list relative to the project root
WORD_LIST_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordslist.txt')

def play_wordle():
    """Allows a human player to play Wordle interactively."""
    words = load_words(WORD_LIST_PATH)
    target = random.choice(words)
    attempts_left = 6
    guesses_made = 0
    print("Welcome to Wordle! Guess a 5-letter word. You have 6 tries.")
    while guesses_made < attempts_left:
        guess = input("Enter guess: ").lower()
        if len(guess) != 5 or guess not in words:
            print("Must be a 5-letter word from the list. Try again.")
            continue
        feedback = evaluate_guess(guess, target)
        feedback_list = list(feedback.upper().replace('b', 'x'))
        print("Feedback:", feedback_list)
        guesses_made += 1
        if feedback == "ggggg":
            print(f"You won in {guesses_made} tries! The word was {target}")
            return
    print(f"Game over! The word was {target}")

class MCTSBot:
    """Monte Carlo Tree Search bot for solving Wordle."""
    def __init__(self, game_state, simulations=500, used_guesses=None):
        self.simulations = simulations
        self.root = MCTSNode(game_state)
        self.used_guesses = used_guesses.copy() if used_guesses else set()

    def search(self):
        for _ in range(self.simulations):
            node = self.select(self.root)
            if node is None:
                continue
            reward = self.simulate(node.state)
            self.backpropagate(node, reward)
        possible_guesses = [g for g in self.root.state.get_possible_guesses(self.used_guesses)]
        if not possible_guesses:
            print("No guesses available.")
            return None
        best_child = self.root.best_child(c=0)
        if best_child is None or best_child.state.guess_history[-1][0] in self.used_guesses:
            guess = random.choice(possible_guesses)
        else:
            guess = best_child.state.guess_history[-1][0]
        return guess

    def select(self, node):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand(self.used_guesses)
            node = node.best_child()
            if node is None:
                break
        return node

    def simulate(self, state):
        if not state.candidates:
            return 0
        solution = random.choice(state.candidates)
        current_state = state
        local_used = self.used_guesses.copy()
        for _ in range(6 - state.depth):
            possible_guesses = [g for g in current_state.get_possible_guesses(local_used)]
            if not possible_guesses:
                return 0
            guess = random.choice(possible_guesses)
            local_used.add(guess)
            feedback = evaluate_guess(guess, solution)
            if feedback == 'ggggg':
                return 6 - (state.depth + 1)
            current_state = current_state.next_state(guess, feedback)
        return 0

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

def run_mcts_bot():
    """Runs the MCTS bot to solve a Wordle puzzle."""
    words = load_words(WORD_LIST_PATH)
    target = random.choice(words)
    print(f"Target (for testing): {target}")
    state = GameState(words.copy())
    used_guesses = set()
    attempts = 0
    while attempts < 6:
        bot = MCTSBot(state, simulations=500, used_guesses=used_guesses)
        guess = bot.search()
        if guess is None:
            print(f"No valid guesses left after {attempts} tries.")
            break
        used_guesses.add(guess)
        feedback = evaluate_guess(guess, target)
        print(f"Guess #{attempts+1}: {guess} -> {list(feedback.upper().replace('b', 'x'))}")
        if feedback == "ggggg":
            print(f"Solved in {attempts+1} tries!")
            break
        state = state.next_state(guess, feedback)
        attempts += 1
    if attempts >= 6:
        print(f"Couldn't solve it. Word was {target}")

def run_csp_bot():
    """Runs the CSP bot to solve a Wordle puzzle."""
    words = load_words(WORD_LIST_PATH)
    target = random.choice(words)
    print(f"Target (for testing): {target}")
    state = GameState(words.copy())
    csp_bot = CSPBot(state, words)
    used_guesses = set()
    attempts = 0
    while attempts < 6:
        guess = csp_bot.make_guess(used_guesses)
        if guess is None:
            print(f"No valid guesses left after {attempts} tries.")
            break
        used_guesses.add(guess)
        feedback = evaluate_guess(guess, target)
        print(f"Guess #{attempts+1}: {guess} -> {list(feedback.upper().replace('b', 'x'))}")
        if feedback == "ggggg":
            print(f"Solved in {attempts+1} tries!")
            break
        csp_bot.update_constraints(guess, feedback)
        state = state.next_state(guess, feedback)
        attempts += 1
    if attempts >= 6:
        print(f"Couldn't solve it. Word was {target}")

if __name__ == "__main__":
    mode = input("Enter 'human' to play, 'mcts' for MCTS bot, or 'csp' for CSP bot: ").lower()
    if mode == 'human':
        play_wordle()
    elif mode == 'mcts':
        run_mcts_bot()
    elif mode == 'csp':
        run_csp_bot()
    else:
        print("Invalid mode. Use 'human', 'mcts', or 'csp'.")