#should fix bugs from previous mcts wordle bot (in wordle_mcts folder)
#loads words from file into list
def load_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

#eval a guess against target word and return feedback (like get feedback)
def evaluate_guess(guess, target):
    feedback = []
    for i in range(5):
        if guess[i] == target[i]:
            feedback.append('g')
        elif guess[i] in target:
            feedback.append('y')
        else:
            feedback.append('b')
    return ''.join(feedback)