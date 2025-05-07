#have not incorporated entropy yet, will do so if time
from collections import defaultdict

#CSP PROBLEM: 
# variables: each leter position in five letter word (X0 to X4)
# domains: set of all lowercase letters a-z pruned at each iteration given feedback (domain gets smaller at each turn)
# constraints: letter must be in a position, letter cannot be in a position, letter must appear somewhere, letter must not appear, filtering words that meet all constraints
#HEURISTICS: 
#scoring words by letter frequency, information gain from elimiating words and will eliminate more words faster
#maximimizing score to choose a move (greedy heuristic, will always choose word with highest score (most frequent letters))
#better heuristics could be to use entropy maximization (will adopt if feasible by time)

#letter frequency in texts (how comman each letter is in the english language) from wikipedia 
#https://en.wikipedia.org/wiki/Letter_frequency
#should probably add this to all bots for more refined heuristics
#no exact, comprehensive for how common each word is in english dictionary, so this will have to do
#possible limitation: certain words comprised of high frequency letters 
# are less common that words with low frequency words (ex: jalop less common than crazy)
LETTER_FREQUENCY = {
    'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2,
    'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0,
    'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0,
    's': 6.3, 't': 9.1, 'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15,
    'y': 2.0, 'z': 0.074
}


#based on previous research on best word to use first try wordle
# 1: https://www.nytimes.com/2022/02/10/crosswords/best-wordle-tips.html
# 2: https://www.scientificamerican.com/article/information-theory-finds-the-best-wordle-starting-words1/
# 3: https://www.sfi.ie/research-news/news/wordle-data-analytics/#:~:text=For%20a%20one%20seed%20strategy,game%20length%20of%203.68%20rounds

#as per NYT wordle tips article: ADIEU, AUDIO, CANOE (words with many vowels) 
#as per scientific american article: SOARE, SLANE (high entropy words)
#as per data analytics research from the science foundation of ireland: TALES (if going by one seed strategy and not pre-deciding the second or third words)
#BEST_WORDS = {} (might fill this list in and make this adjustment)
#OR, for the sake of randomness, we could continue to just pick a random word to start with at each try
#current this just does the radnom 


class CSPBot:
    #word_list taken from github repo taken from nyt wordle source code
    def __init__(self, word_list):
        #given word_list only has valid five letter words, but if not, would adjust below line
        self.word_list = [word.strip().lower() for word in word_list]
        self.candidates = set(self.word_list) #currently all words are valid/none have been eliminated, at each turn will cut list down
        self.correct_positions = [None] * 5 #starts off with no current positions (constraint)
        self.wrong_positions = defaultdict(set) #set of values that are not in particlar position (constraint)
        self.must_have = set() #for yellow/green letters (constraint)
        self.cannot_have = set() #for black letters (not in word for sure) (constraint)

    #updates constraint given feedback and the current guessed word
    #will go through and add to sets above
    def update_constraints(self, guess, feedback):
        for i, (g_char, fb) in enumerate(zip(guess, feedback)):
            if fb == 'g':
                self.correct_positions[i] = g_char
                self.must_have.add(g_char)
            elif fb == 'y':
                self.wrong_positions[i].add(g_char)
                self.must_have.add(g_char)
            elif fb == 'b':
                if g_char not in self.must_have:
                    self.cannot_have.add(g_char)

    #goes through word, if current positions[i] is known, the word must have that letter at the index
    #if any incorrect letters are present OR letter is not in correct position, word is not valid
    #constraint satisifaction checker
    def is_valid(self, word):
        for i, c in enumerate(word):
            if self.correct_positions[i] and word[i] != self.correct_positions[i]:
                return False
            if c in self.wrong_positions[i]:
                return False
        for c in self.must_have:
            if c not in word:
                return False
        if any(c in self.cannot_have for c in word):
            return False
        return True

    #ranks word based on letter frequencies, will guess words with most common letters first
    #loops over unique letters in words and simply adds up their frequency values  
    #heuristic based
    def score_word(self, word):
        seen = set()
        score = 0
        for char in word:
            if char not in seen:
                score += LETTER_FREQUENCY.get(char, 0)
                seen.add(char)
        return score

    #chooses best word to guess next as per current constraints and scoring of words
    #filtering step to unique set of valid possible words
    def choose_move(self, game):
        self.candidates = {w for w in self.candidates if self.is_valid(w)}
        if not self.candidates:
            return "raise" #placeholder if no valid words left (don't want to exit immediately)
        return max(self.candidates, key=self.score_word) #greedy heuristic strategy always chooses the word with the highest score according to score_word
