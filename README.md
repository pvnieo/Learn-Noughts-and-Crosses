# Tic Tac Toe
A simple implementation of the `tic-tac-toe` game using pygame interface, and multiple AI agents to play against. There is a possibility of a human vs human, human vs AI or AI vs AI match.

The available AIs are:

 - A random agent: plays each move randomly.
 - A minmax agent with levels: this is an implementation of the algorithm of minmax, one can choose the levels of the AI he is playing against, this represents the depth of the minmax shaft we are going to evaluate, the "easy" level corresponds to a depth of 1, "medium" to a depth of 2, "hard" to a depth of 9.
 - A Q learning agent, trained using the algorithm of tabular Q learning. This agent has the same difficulty as the "hard" minmax.

<div align="center">

![](image.png)

</div>

## Installation
This game runs on python >= 3.6, use pip to install dependencies:
```
pip3 install -r requirements.txt
```

## Usage
Use the `play_tic_tac_toe.py` script to play the game.
```
usage: play_tic_tac_toe.py [-h] [-l {easy,medium,hard}]
                           [-p1 {human,minmax,ql,random}]
                           [-p2 {human,minmax,ql,random}] [-w WIDTH] [-t TIME]
                           [-tg TOTAL_GAMES]

Implementation of a tic tac toe game with levels and multiple AIs.

optional arguments:
  -h, --help            show this help message and exit
  -l {easy,medium,hard}, --level {easy,medium,hard}
                        Level of the game, used only if minmax algorithm is selected.
                        Concretely, this represents the depth of the evaluated minmax tree:
                            * easy: depth = 1
                            * medium: depth = 2
                            * hard: depth = 9
  -p1 {human,minmax,ql,random}, --player1 {human,minmax,ql,random}
                        Controler of player 1, always plays with 'X'.
                        Player can be either:
                            * human: a human player gives the instruction
                            * minmax: a minmax with a depth of tree = level
                            * ql: a Q learning agent
                            * random: a random agent
  -p2 {human,minmax,ql,random}, --player2 {human,minmax,ql,random}
                        Controler of player 2, always plays with 'O'.
                        Player can be either:
                            * human: a human player gives the instruction
                            * minmax: a minmax with a depth of tree = level
                            * ql: a Q learning agent
                            * random: a random agent
  -w WIDTH, --width WIDTH
                        Width and height of the board
  -t TIME, --time TIME  Waiting time between two consecutive games in secondes
  -tg TOTAL_GAMES, --total_games TOTAL_GAMES
                        Maximum number of games that will be played
```

The script `train.py` is used to train the Q learning agent.
```
usage: train.py [-h] [-ni NITER] [-e EPSILON] [-a ALPHA] [-g GAMMA]

Training an RL agent to play Tic Tac Toe using Tabular Q Learning

optional arguments:
  -h, --help            show this help message and exit
  -ni NITER, --niter NITER
                        Number of training episodes
  -e EPSILON, --epsilon EPSILON
                        Exploration rate. Will be reduced to 0 as training
                        progresses.
  -a ALPHA, --alpha ALPHA
                        Learning rate of Q learning algorithm
  -g GAMMA, --gamma GAMMA
                        Discount factor
```