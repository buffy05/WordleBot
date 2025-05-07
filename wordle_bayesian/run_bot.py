from wordle_game import WordleGame
from bayesian_wordle_bot import bayesian_wordle_bot, load_words

def evaluate_bot(word_list, max_words=None):
    total_attempts = 0
    total_wins = 0
    total_games = 0

    for i, target_word in enumerate(word_list):
        if max_words and i >= max_words:
            break

        game = WordleGame(word_list, target_word=target_word)
        print(f"\n--- Solving for target: {target_word} ---")
        
        bayesian_wordle_bot(game)

        total_games += 1
        if game.is_won():
            total_attempts += game.current_attempt
            total_wins += 1

    avg_attempts = total_attempts / total_wins if total_wins else float('inf')
    win_rate = (total_wins / total_games) * 100

    print(f"\n Evaluation complete!")
    print(f"Total games: {total_games}")
    print(f"Total wins: {total_wins}")
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Average number of attempts (only wins): {avg_attempts:.2f}")

if __name__ == "__main__":
    words = load_words("words.txt")
    # game = WordleGame(words)
    # bayesian_wordle_bot(game)
    evaluate_bot(words, max_words=100)
