# Wordle Solver Project

This project contains a Wordle game simulator with three AI bots (MCTS, CSP, Bayesian) to solve Wordle puzzles, plus a testing framework to compare their performance.

# Directory Structure
- src/: Python scripts (game_simulator.py, testing_framework.py, etc.)
- data/: Word list (wordslist.txt)

# Requirements
- Python 3.x
- No external libraries are required

# How to Run

1. Navigate to the src/ directory:

2. Run a Single Bot:
- Use game_simulator.py to play Wordle or run a bot:
- At the prompt, enter:
- human: Play Wordle interactively.
- mcts: Run the Monte Carlo Tree Search bot.
- csp: Run the Constraint Satisfaction Problem bot.
- bayesian: Run the Bayesian bot.

3. Run the Testing Framework:
- Use testing_framework.py to compare bot performance over 100 runs:
- Output shows success rate, average attempts, and average time per bot:
- NUM_RUNS can be edited in testing_framework.py to change the number of runs.