import math
import random
from wordle_game import WordleGame 

# English letter frequency (Wikipedia)
LETTER_FREQUENCY = {
    'a': 8.167, 
    'b': 1.492, 
    'c': 2.782, 
    'd': 4.253, 
    'e': 12.702,
    'f': 2.228, 
    'g': 2.015, 
    'h': 6.094, 
    'i': 6.966, 
    'j': 0.153,
    'k': 0.772, 
    'l': 4.025, 
    'm': 2.406, 
    'n': 6.749, 
    'o': 7.507,
    'p': 1.929, 
    'q': 0.095, 
    'r': 5.987, 
    's': 6.327, 
    't': 9.056,
    'u': 2.758, 
    'v': 0.978, 
    'w': 2.360, 
    'x': 0.150, 
    'y': 1.974, 
    'z': 0.074
}

def load_words(filename):
    with open(filename) as f:
        return [line.strip() for line in f if len(line.strip()) == 5]

def mcmc_sample(beliefs, num_samples=500):
    """Sample words according to their probabilities (MCMC resampling)."""
    words = list(beliefs.keys())
    probs = [beliefs[word] for word in words]
    samples = random.choices(words, weights=probs, k=num_samples)
    sampled_beliefs = {}
    for word in samples:
        if word not in sampled_beliefs:
            sampled_beliefs[word] = 0
        sampled_beliefs[word] += 1
    total = sum(sampled_beliefs.values())
    for word in sampled_beliefs:
        sampled_beliefs[word] /= total
    return sampled_beliefs

def update_beliefs(beliefs, guess, feedback):
    """Bayesian update: keep only consistent words."""
    new_beliefs = {}
    for word in beliefs:
        if simulate_feedback(guess, word) == feedback:
            new_beliefs[word] = beliefs[word]
    total = sum(new_beliefs.values())
    if total == 0:
        # Avoid division by zero if no words match (rare)
        uniform_prob = 1 / len(beliefs)
        return {word: uniform_prob for word in beliefs}
    for word in new_beliefs:
        new_beliefs[word] /= total
    return new_beliefs

def simulate_feedback(guess, target):
    """Simulate WordleGame feedback format for given guess and target."""
    result = ["b"] * 5
    target_chars = list(target)
    guess_chars = list(guess)

    # First pass: green
    for i in range(5):
        if guess_chars[i] == target_chars[i]:
            result[i] = "g"
            target_chars[i] = None
            guess_chars[i] = None

    # Second pass: yellow
    for i in range(5):
        if guess_chars[i] is not None and guess_chars[i] in target_chars:
            result[i] = "y"
            target_index = target_chars.index(guess_chars[i])
            target_chars[target_index] = None

    return result

def word_letter_score(word):
    """Score a word based on unique letter frequencies."""
    unique_letters = set(word)
    return sum(LETTER_FREQUENCY.get(c, 0) for c in unique_letters)

def pick_initial_guess(candidates):
    """Pick the best starting word based on letter frequency."""
    return max(candidates, key=word_letter_score)

def entropy_of_guess(guess, candidates):
    """Expected information gain if we guess this word."""
    feedback_buckets = {}
    for word in candidates:
        feedback = tuple(simulate_feedback(guess, word))  # Feedback must be hashable
        if feedback not in feedback_buckets:
            feedback_buckets[feedback] = 0
        feedback_buckets[feedback] += 1
    total = sum(feedback_buckets.values())

    entropy = 0
    for count in feedback_buckets.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def pick_next_guess(beliefs):
    """Pick the guess that maximizes expected information gain."""
    candidates = list(beliefs.keys())
    best_guess = None
    best_entropy = -1
    for guess in candidates:
        ent = entropy_of_guess(guess, candidates)
        if ent > best_entropy:
            best_entropy = ent
            best_guess = guess
    return best_guess

def bayesian_wordle_bot(game, samples_per_round=500):
    word_list = game.word_list
    beliefs = {word: 1/len(word_list) for word in word_list}

    while not game.is_over():
        sampled_beliefs = mcmc_sample(beliefs, num_samples=samples_per_round)

        if game.current_attempt == 0:
            guess = pick_initial_guess(list(sampled_beliefs.keys()))
        else:
            guess = pick_next_guess(sampled_beliefs)

        try:
            feedback = game.make_guess(guess)
        except ValueError as e:
            print(f"Error: {e}")
            return

        print(f"Attempt {game.current_attempt}: {guess} -> {feedback}")

        beliefs = update_beliefs(beliefs, guess, feedback)

    if game.is_won():
        print(f"Solved in {game.current_attempt} attempts! 🎉 Target word: {game.target_word}")
    else:
        print(f"Failed to solve. Target word was: {game.target_word}")
