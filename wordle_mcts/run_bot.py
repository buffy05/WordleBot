from game_state import GameState
from mcts_bot import MCTSBot
from wordle_game import WordleGame

def play_mcts_game(solution, simulations=500):
    with open("words.txt") as f:
        word_list = [line.strip() for line in f if len(line.strip()) == 5]

    print(f"target word: {solution}")
    state = GameState(word_list.copy())
    attempts = 0
    while attempts < 6:
        bot = MCTSBot(state, simulations=simulations)
        guess = bot.search()
        game = WordleGame(word_list, target_word=solution)
        feedback = ''.join(game.get_feedback(guess))
        print(f"guess #{attempts+1}: {guess} -> {feedback}")
        if feedback == 'ggggg':
            print("solved it")
            return attempts + 1
        state = state.next_state(guess, feedback)
        attempts += 1
    print("couldn't solve it")
    return None

#will adapt this later to go over a whole list of test words (from prev wordles) 
#will also get solved/unsolved statisics and time avergaes 
#so far been testing on individual words given a certain number of simulations (1-300)
if __name__ == "__main__":
    play_mcts_game("crate", simulations=100)
