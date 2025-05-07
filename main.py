from game_simulator.wordle_game import WordleGame
from wordle_bots.mcst_bot import MCTSBot

def load_words(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f if len(line.strip()) == 5]

if __name__ == "__main__":
    word_list = load_words("words.txt")
    game = WordleGame(word_list, target_word="faint")
    bot = MCTSBot(word_list, num_simulations=200)  # You can tweak simulations!

    print(f"Target word: {game.target_word}\n")

    while not game.is_over():
        # Update candidates after feedback BEFORE choosing next move
        if game.guess_history:
            last_guess, last_feedback = game.guess_history[-1]
            bot.update_candidates(last_guess, last_feedback)

        move = bot.choose_move(game)
        feedback = game.make_guess(move)
        print(f"Guess: {move} -> {' '.join(feedback)}")

    if game.is_won():
        print("✅ Bot won!")
    else:
        print(f"❌ Bot lost. The word was '{game.target_word}'")
