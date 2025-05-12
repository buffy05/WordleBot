Overview
This project implements three distinct AI-based bots to solve Wordle puzzles, each leveraging a different algorithmic approach:

Monte Carlo Tree Search (MCTS) Bot

Constraint Satisfaction Problem (CSP) Bot

Bayesian Network Bot

Each bot is designed to autonomously play Wordle using a list of past solutions, simulating and displaying the solving process, performance statistics, and average guesses per solve.

Features
Automatically solves Wordle puzzles using different AI principles

Logs performance metrics such as:

Number of words solved

Average number of turns per solution

Modular and extensible design for adding additional solving strategies

Easy to run with separate folders and entry scripts for each bot

Technologies Used
Python 3.10+

Core libraries: random, math, itertools, collections

Algorithm-specific implementations built from scratch

Bot Descriptions
Monte Carlo Tree Search (MCTS) Bot
Uses simulation-based search and exploration vs. exploitation strategies to decide the next best word.

Constraint Satisfaction Problem (CSP) Bot
Applies constraint propagation and letter-position inference to systematically narrow down valid word candidates.

Bayesian Network Bot
Builds probabilistic models to update word likelihoods based on feedback from guesses.

How to Run
Each bot has its own folder and a dedicated entry script. To run, navigate to each folder and simply do python run_bot.py

Future Improvements: 
- Add user interface for interactive solving

- Train bots on broader word distributions

- Introduce reinforcement learning for adaptive guessing


