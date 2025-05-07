from game_state import GameState
from mcts_bot import MCTSBot
from wordle_game import WordleGame

def play_mcts_game(solution, simulations=500, verbose=True):
    with open("words.txt") as f:
        word_list = [line.strip() for line in f if len(line.strip()) == 5]

    if verbose:
        print(f"\ntarget word: {solution}")
    state = GameState(word_list.copy())
    attempts = 0
    while attempts < 6:
        bot = MCTSBot(state, simulations=simulations)
        guess = bot.search()
        if guess is None:
            if verbose:
                print("No valid guesses left. Failed to solve.")
            return None
        game = WordleGame(word_list, target_word=solution)
        feedback = ''.join(game.get_feedback(guess))
        if verbose:
            print(f"guess #{attempts+1}: {guess} -> {feedback}")
        if feedback == 'ggggg':
            if verbose:
                print("solved it")
            return attempts + 1
        state = state.next_state(guess, feedback)
        attempts += 1
    if verbose:
        print("couldn't solve it")
    return None

if __name__ == "__main__":
    simulations = 100  # adjust as needed
    max_words = 50     # adjust to full list later

    with open("past_wordle_answers.txt") as f:
        test_words = [line.strip() for line in f if len(line.strip()) == 5][:max_words]

    solved_count = 0
    total_turns = 0
    for i, word in enumerate(test_words, start=1):
        print(f"\n=== Test {i}: {word} ===")
        result = play_mcts_game(word, simulations=simulations, verbose=False)
        if result is not None:
            print(f"Solved {word} in {result} turns.")
            solved_count += 1
            total_turns += result
        else:
            print(f"Failed to solve {word}.")

    print("\n========== SUMMARY ==========")
    print(f"Total words tested: {len(test_words)}")
    print(f"Solved: {solved_count}/{len(test_words)}")
    if solved_count > 0:
        avg_turns = total_turns / solved_count
        print(f"Average turns (only successful games): {avg_turns:.2f}")
    else:
        print("No words were solved.")
