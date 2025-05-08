def load_words(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

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