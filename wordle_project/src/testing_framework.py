import random
import os
from game_simulator import run_mcts_bot, run_csp_bot, run_bayesian_bot, load_words

# Configuration
NUM_RUNS = 100  # Number of test runs per bot
WORD_LIST_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordslist.txt')

def run_tests(bot_func, bot_name, target_words, words):
    successes = 0
    total_attempts = 0
    total_time = 0.0
    for target in target_words:
        success, attempts, time_taken = bot_func(target, words, verbose=False)
        if success:
            successes += 1
            total_attempts += attempts
        total_time += time_taken
    success_rate = (successes / NUM_RUNS) * 100
    avg_attempts = total_attempts / successes if successes > 0 else float('nan')
    avg_time = total_time / NUM_RUNS
    return success_rate, avg_attempts, avg_time

if __name__ == "__main__":
    # Load word list
    words = load_words(WORD_LIST_PATH)
    
    # Select a random set of target words for this run
    target_words = random.sample(words, NUM_RUNS)
    
    # Define bots to test
    bots = {
        "MCTS": run_mcts_bot,
        "CSP": run_csp_bot,
        "Bayesian": run_bayesian_bot
    }
    
    # Run tests and display results
    for bot_name, bot_func in bots.items():
        success_rate, avg_attempts, avg_time = run_tests(bot_func, bot_name, target_words, words)
        print(f"\n{bot_name} Bot Results:")
        print(f"  Success Rate: {success_rate:.2f}%")
        print(f"  Average Attempts (successful solves): {avg_attempts:.2f}")
        print(f"  Average Time per Game: {avg_time:.4f} seconds")