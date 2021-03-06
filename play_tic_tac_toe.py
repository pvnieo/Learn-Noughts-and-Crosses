# stdlib
import random
import time
import pickle
import argparse
from argparse import RawTextHelpFormatter
from collections import defaultdict
from itertools import cycle
# 3p
import pygame
import numpy as np


class Board:
    def __init__(self, w=900):
        self.w = w
        self.c = w // 3
        self.c2 = w // 6
        self.draw_board()

    def draw_board(self):
        self.screen = pygame.display.set_mode((self.w, self.w))
        self.screen.fill((0, 0, 125))
        pygame.display.set_caption("Tic Tac Toe")
        pygame.draw.line(self.screen, (255, 255, 255), (self.c, 0), (self.c, self.w))
        pygame.draw.line(self.screen, (255, 255, 255), (2*self.c, 0), (2*self.c, self.w))
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.c), (self.w, self.c))
        pygame.draw.line(self.screen, (255, 255, 255), (0, 2 * self.c), (self.w, 2 * self.c))
        pygame.display.flip()

    def draw_x(self, case_n):
        x, y = self.pos_to_coord(case_n)
        x, y = x // self.c * self.c, y // self.c * self.c
        pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x + self.c, y + self.c))
        pygame.draw.line(self.screen, (255, 255, 255), (x, y + self.c), (x + self.c, y))
        pygame.display.flip()

    def draw_o(self, case_n):
        x, y = self.pos_to_coord(case_n)
        pos = (x // self.c * self.c + self.c // 2, y // self.c * self.c + self.c // 2)
        pygame.draw.circle(self.screen, (255, 255, 255), pos, self.c // 2, 1)
        pygame.display.flip()

    def draw_win_line(self, pos1, pos2):
        pygame.draw.line(self.screen, (255, 0, 0), (self.c * (pos1 % 3) + self.c2, self.c * (pos1 // 3) + self.c2),
                                                   (self.c * (pos2 % 3) + self.c2, self.c * (pos2 // 3) + self.c2), 16)
        pygame.display.flip()

    def coord_to_pos(self, x, y):
        return (x // self.c) + 3 * (y // self.c)

    def pos_to_coord(self, pos):
        return (int(self.c * 1.2) * (pos % 3), int(self.c * 1.2) * (pos // 3))


class TicTacToe:
    def __init__(self, args):
        # set game argument
        self.w = args.width
        self.player1 = args.player1  # player 1 plays with "X"
        self.player2 = args.player2  # player 2 plays with "O"
        levels = {'easy': 1, 'medium': 2, 'hard': 9}
        self.level = levels[args.level]
        self.waiting_time = args.time

        # set properties
        self.count = {"1": 0, "2": 0, "0": 0}  # Counter of score of the game
        self.turns = cycle(["1", "2"])

        # function playing for players
        players = {"human": self.play_human, "minmax": self.play_minmax, "ql": self.play_ql, "random": self.play_random}
        self.play_func = {"1": players[self.player1], "2": players[self.player2]}

        # winning combinations
        self.wins = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]
        self.minmax_dict = {}  # store results of minmax algorithms to use later (improve speed)

        # load Q learning model
        with open("ql.pkl", "rb") as f:
            self.Q = pickle.load(f)

    def new_game(self):
        self.board = Board(self.w)
        self.state = ['.' for _ in range(9)]
        self.possible_movs = list(range(9))
        self.movs = {"1": set(), "2": set()}  # list of movs of each player
        winner = 0
        while True:
            turn_of = next(self.turns)
            winner = self.play_func[turn_of](turn_of)

            if winner != "0" or not self.possible_movs:
                self.count[winner] += 1
                time.sleep(self.waiting_time)
                break

        print(f'Player 1: {self.count["1"]} | Player 2: {self.count["2"]} | Tie: {self.count["0"]}\r', end='')

    def play_human(self, turn_of):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.board.coord_to_pos(*event.pos) not in self.possible_movs:
                        continue
                    case_n = self.board.coord_to_pos(*event.pos)
                    return self.do_step(turn_of, case_n)

    def play_minmax(self, turn_of):
        time.sleep(0.1)
        turn_op = "1" if turn_of == "2" else "2"
        case_n = self.minmax(self.movs[turn_of], self.movs[turn_op], depth=self.level, max_step=True)[1]
        return self.do_step(turn_of, case_n)

    def play_ql(self, turn_of):
        time.sleep(0.1)
        state_hash = "".join(self.state)
        if turn_of == "2":
            state_hash = state_hash.replace("1", "?").replace("2", "1").replace("?", "2")
        if state_hash in self.Q:
            case_n = np.argmax(self.Q[state_hash])
        else:
            case_n = random.choice(self.possible_movs)
        return self.do_step(turn_of, case_n)

    def play_random(self, turn_of):
        time.sleep(0.1)
        case_n = random.choice(self.possible_movs)
        return self.do_step(turn_of, case_n)

    def do_step(self, turn_of, case_n):
        self.state[case_n] = turn_of
        self.possible_movs.remove(case_n)
        self.draw_case(turn_of, case_n)
        self.movs[turn_of].add(case_n)
        is_win = self.is_win(self.movs[turn_of])
        if is_win:
            self.board.draw_win_line(min(is_win), max(is_win))
            return turn_of
        return "0"

    def draw_case(self, to_draw, case_n):
        self.board.draw_x(case_n) if to_draw == "1" else self.board.draw_o(case_n)

    def is_win(self, movs):
        for win in self.wins:
            if len(win.intersection(movs)) == 3:
                return win
        return False

    def minmax(self, my_moves, op_moves, depth=1, max_step=True):
        sign = 1 if max_step else -1
        if (tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign) in self.minmax_dict:
            return self.minmax_dict[(tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign)]

        if depth == 0 or (len(my_moves) + len(op_moves) == 9):
            if self.is_win(my_moves):
                M = 1 * sign
            else:
                M = -1 * sign if self.is_win(op_moves) else 0

            self.minmax_dict[(tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign)] = (M, -1)
            return (M, -1)

        if self.is_win(my_moves):
            self.minmax_dict[(tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign)] = (1 * sign, -1)
            return (1 * sign, -1)
        if self.is_win(op_moves):
            self.minmax_dict[(tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign)] = (-1 * sign, -1)
            return (-1 * sign, -1)

        d = defaultdict(list)
        for i in set(range(9)) - my_moves.union(op_moves):
            my_moves_copy = my_moves.copy()
            my_moves_copy.add(i)
            m = self.minmax(op_moves, my_moves_copy, depth - 1, not max_step)[0] * sign
            d[m].append(i)

        M, best_move = max(d.keys()), random.choice(d[max(d.keys())])

        self.minmax_dict[(tuple(sorted(my_moves)), tuple(sorted(op_moves)), depth, sign)] = (M * sign, best_move)
        return (M * sign, best_move)


def main(args):
    game = TicTacToe(args)
    for _ in range(args.total_games):
        game.new_game()
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Implementation of a tic tac toe game with levels and multiple AIs.",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("-l", "--level", choices=["easy", "medium", "hard"], default="medium",
                        help="""Level of the game, used only if minmax algorithm is selected.
Concretely, this represents the depth of the evaluated minmax tree:
    * easy: depth = 1
    * medium: depth = 2
    * hard: depth = 9""")
    parser.add_argument("-p1", "--player1", choices=["human", "minmax", "ql", "random"], default="human",
                        help="""Controler of player 1, always plays with 'X'.
Player can be either:
    * human: a human player gives the instruction
    * minmax: a minmax with a depth of tree = level
    * ql: a Q learning agent
    * random: a random agent""")
    parser.add_argument("-p2", "--player2", choices=["human", "minmax", "ql", "random"], default="minmax",
                        help="""Controler of player 2, always plays with 'O'.
Player can be either:
    * human: a human player gives the instruction
    * minmax: a minmax with a depth of tree = level
    * ql: a Q learning agent
    * random: a random agent""")
    parser.add_argument("-w", "--width", type=int, default=900,
                        help="Width and height of the board")
    parser.add_argument("-t", "--time", type=int, default=2,
                        help="Waiting time between two consecutive games in secondes")
    parser.add_argument("-tg", "--total_games", type=int, default=10,
                        help="Maximum number of games that will be played")

    args = parser.parse_args()
    main(args)
