# stdlib
import random
import argparse
import pickle
from collections import defaultdict
from itertools import cycle
# 3p
import numpy as np


class TicTacToeTraining:
    def __init__(self, args):
        # RL params
        self.Q = defaultdict(lambda: [0 for _ in range(9)])  # Q function
        self.R = {"1": 1, "2": -1, "0": 0.5}  # reward
        self.epsilon = args.epsilon
        self.eps_step = (self.epsilon * 1.2) / args.niter
        self.alpha = args.alpha
        self.gamma = args.gamma
        self.niter = args.niter

        # function playing for players
        self.play_func = {"1": self.play_rl, "2": self.play_ai}

        # set properties of game
        self.count = {"1": 0, "2": 0, "0": 0}  # Counter of score of the game
        self.turns = cycle(["1", "2"])
        self.level = 1

        # winning combinations
        self.wins = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    def train(self):
        for i in range(self.niter):
            self.epsilon -= self.eps_step
            if i < (self.niter // 3):
                self.level = 1
            elif i < (2 * self.niter // 3):
                self.level = 2
            else:
                self.level = 9
            self.new_game()
        with open(f"ql_{self.niter}_{self.alpha}.pkl", "wb") as f:
            pickle.dump(dict(self.Q), f)

    def new_game(self):
        self.state = ['.' for _ in range(9)]
        self.transitions = []
        self.possible_movs = list(range(9))
        self.movs = {"1": set(), "2": set()}  # list of movs of each player
        winner = "0"
        while True:
            turn_of = next(self.turns)
            winner = self.play_func[turn_of](turn_of)

            # q iteration at the end of episode
            if winner != "0" or not self.possible_movs:
                s, a, *_ = self.transitions.pop(-1)
                self.Q[s][a] *= 1 - self.alpha
                self.Q[s][a] += self.alpha * self.R[winner]
                for s, a, sp in self.transitions[::-1]:
                    self.Q[s][a] *= 1 - self.alpha
                    self.Q[s][a] += self.alpha * self.gamma * max(self.Q[sp])

                self.count[winner] += 1
                break

        print(f'Player 1: {self.count["1"]} | Player 2: {self.count["2"]} | Tie: {self.count["0"]}\r', end='')

    def play_rl(self, turn_of):
        state_hash = "".join(self.state)
        for i in set(range(9)) - set(self.possible_movs):  # -inf for illegal movs
            self.Q[state_hash][i] = - float("inf")

        # epsilon-greedy policy
        if random.random() < self.epsilon:
            case_n = random.choice(self.possible_movs)
        else:
            case_n = np.argmax(self.Q[state_hash])
        self.state[case_n] = turn_of
        self.s, self.a = state_hash, case_n
        self.transitions.append([state_hash, case_n])
        return self.do_step(turn_of, case_n)

    def play_ai(self, turn_of):
        case_n = random.choice(self.possible_movs)
        self.state[case_n] = turn_of
        if self.transitions:
            self.transitions[-1].append("".join(self.state))
        return self.do_step(turn_of, case_n)

    def do_step(self, turn_of, case_n):
        self.possible_movs.remove(case_n)
        self.movs[turn_of].add(case_n)
        is_win = self.is_win(self.movs[turn_of])
        if is_win:
            return turn_of
        return "0"

    def is_win(self, movs):
        for win in self.wins:
            if len(win.intersection(movs)) == 3:
                return win
        return False


def main(args):
    game = TicTacToeTraining(args)
    game.train()
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Training an RL agent to play Tic Tac Toe using Tabular Q Learning"
    )
    parser.add_argument("-ni", "--niter", type=int, default=10000,
                        help="Number of training episodes")
    parser.add_argument("-e", "--epsilon", type=float, default=0.7,
                        help="Exploration rate. Will be reduced to 0 as training progresses.")
    parser.add_argument("-a", "--alpha", type=float, default=0.6,
                        help="Learning rate of Q learning algorithm")
    parser.add_argument("-g", "--gamma", type=float, default=0.95,
                        help="Discount factor")

    args = parser.parse_args()
    main(args)
