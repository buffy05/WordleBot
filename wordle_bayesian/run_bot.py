# run_bot.py
from wordle_game import WordleGame
from bayesian_bot import BayesianBot
def load_words(filename):
    with open(filename) as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5]

def main():
    word_list = load_words("words.txt")
    test_words = load_words("past_wordle_answers.txt")[1000:1200]  # use more later

    total_games = len(test_words)
    successes = 0
    total_turns = 0

    for idx, target in enumerate(test_words, 1):
        game = WordleGame(word_list, target_word=target)
        bot = BayesianBot(word_list)
        print(f"\n🔍 Test {idx}: Target word = {target}")

        while not game.is_over():
            guess = bot.choose_move(game)
            feedback = game.make_guess(guess)
            print(f"  ➤ Guess: {guess.upper()} -> Feedback: {feedback}")
            bot.update_constraints(guess, feedback)

        if game.is_won():
            successes += 1
            total_turns += game.current_attempt
            print("  ✅ Solved in", game.current_attempt, "turns.")
        else:
            print("  ❌ Failed to solve.")

    print("\n📊 Summary:")
    print(f"  Total Games: {total_games}")
    print(f"  Successful Solves: {successes}")
    print(f"  Success Rate: {successes / total_games:.2%}")
    if successes > 0:
        print(f"  Average Turns (successful games): {total_turns / successes:.2f}")
    else:
        print("  No successful games to report average turns.")

if __name__ == "__main__":
    main()
