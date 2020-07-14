import random
from time import sleep
import sys
from copy import deepcopy

class AgentScoreCells:
    def __init__(self, player):
        self.player = player
        self.node_count = 0

    def evaluate(self, game):
        score = game.score()
        return len(self.get_empty_cells(game)) + score[str(self.player)]

    def get_empty_cells(self, game):
        board = game.get_board()
        if self.player == 1:
            idxs = game.p1_idxs
        else:
            idxs = game.p2_idxs
        return [board[idx] for idx in idxs if board[idx][self.player] == 0]

    def possible_moves(self, game):
        board = game.get_board()
        if self.player == 1:
            idxs = game.p1_idxs
        else:
            idxs = game.p2_idxs
        moves = [idx for idx in idxs if board[idx][self.player] > 0]
        return moves

    def min_max(self, depth, game, move, alpha, beta):
        self.node_count +=1
        clone = game.clone()
        clone.move(move)

        maximizer = clone.turn == self.player

        if depth == 0:
            return self.evaluate(clone)

        move_options = self.possible_moves(clone)
        best_move = -sys.maxsize if maximizer else sys.maxsize

        for move_slot in move_options:
            current_value = self.min_max(
                depth - 1,
                clone,
                move_slot,
                alpha,
                beta
            )

            if maximizer:
                best_move = max(current_value, best_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(current_value, best_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move

    def get_move(self, game):
        """Min max should be implemented here."""
        clone = game.clone()
        possible_moves = self.possible_moves(clone)
        available_scores = list(
            map(lambda move_slot:
                self.min_max(
                    3,
                    clone,
                    move_slot,
                    -sys.maxsize,
                    sys.maxsize
                ),
                possible_moves))
        if available_scores:
            score_max = max(available_scores)
            final_options = [move for score, move in
                             zip(available_scores, possible_moves)
                             if score == score_max]
            return random.choice(final_options)
        else:
            return -1



class AgentScore:
    def __init__(self, player):
        self.player = player
        self.node_count = 0

    def evaluate(self, game):
        score = game.score()
        return score[str(self.player)]

    def get_empty_cells(self, game):
        board = game.get_board()
        if self.player == 1:
            idxs = game.p1_idxs
        else:
            idxs = game.p2_idxs
        return [board[idx] for idx in idxs if board[idx][self.player] == 0]

    def possible_moves(self, game):
        board = game.get_board()
        if self.player == 1:
            idxs = game.p1_idxs
        else:
            idxs = game.p2_idxs
        moves = [idx for idx in idxs if board[idx][self.player] > 0]
        return moves

    def min_max(self, depth, game, move, alpha, beta):
        self.node_count += 1
        clone = game.clone()
        clone.move(move)

        maximizer = clone.turn == self.player

        if depth == 0:
            return self.evaluate(clone)

        move_options = self.possible_moves(clone)
        best_move = -sys.maxsize if maximizer else sys.maxsize

        for move_slot in move_options:
            current_value = self.min_max(
                depth - 1,
                clone,
                move_slot,
                alpha,
                beta
            )

            if maximizer:
                best_move = max(current_value, best_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(current_value, best_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move

    def get_move(self, game):
        """Min max should be implemented here."""
        clone = game.clone()
        possible_moves = self.possible_moves(clone)
        available_scores = list(
            map(lambda move_slot:
                self.min_max(
                    3,
                    clone,
                    move_slot,
                    -sys.maxsize,
                    sys.maxsize
                ),
                possible_moves))
        if available_scores:
            score_max = max(available_scores)
            final_options = [move for score, move in
                             zip(available_scores, possible_moves)
                             if score == score_max]
            return random.choice(final_options)
        else:
            return -1




class ManqalaGame:
    def __init__(self, n, board, turn=None):
        self._board = board
        self.n = n #number of stones per cell
        self.p1_manqala_idx = [0, 12]
        self.p2_manqala_idx = [6, 18]
        self.p1_idxs = [1, 2, 9, 10, 11, 13, 14, 21, 22, 23]
        self.p2_idxs = [3, 4, 5,  7,  8, 15, 16, 17, 19, 20]
        self.turn = random.randrange(1, 3, 1) if turn is None else turn
        self.p1_adjacencies = {'2': [3],
                              '9': [15,3],
                              '21':[15,3],
                              '14':[15]}
        self.p2_adjacencies = {'20':[21],
                               '3':[9,21],
                               '15':[9,21],
                               '8':[9]}

    def get_board(self):
        return self._board

    def clone(self):
        return deepcopy(self)

    def render_board(self):

        result = '{0:>25}|{1:>1}|{2:>1}\n'.format(
            self._board[12][0], self._board[12][1], self._board[12][2])
        result += '{0: >21}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}\n'.format(
            self._board[13][0], self._board[13][1], self._board[13][2],
            self._board[11][0], self._board[11][1], self._board[11][2])
        result += '{0: >21}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}\n'.format(
            self._board[14][0], self._board[14][1], self._board[14][2],
            self._board[10][0], self._board[10][1], self._board[10][2])
        result += '{0: >1}|{1: >1}'.format(
            self._board[18][0], self._board[18][1])
        result += '{0: >3}|{1: >1}|{2:>1}'.format(
            self._board[17][0], self._board[17][1], self._board[17][2])
        result += '{0: >3}|{1: >1}|{2:>1}'.format(
            self._board[16][0], self._board[16][1], self._board[16][2])
        result += '{0: >3}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}'.format(
            self._board[15][0], self._board[15][1], self._board[15][2],
            self._board[9][0], self._board[9][1], self._board[9][2])
        result += '{0: >3}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}'.format(
            self._board[8][0], self._board[8][1], self._board[8][2],
            self._board[7][0], self._board[7][1], self._board[7][2])
        result += '{0:>3}|{1:>1}\n'.format(self._board[6][0], self._board[6][1])
        result += '{0:>3}'.format(self._board[18][2])
        result += '{0: >4}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}'.format(
            self._board[19][0], self._board[19][1], self._board[19][2],
            self._board[20][0], self._board[20][1], self._board[20][2])
        result += '{0: >3}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}'.format(
            self._board[21][0], self._board[21][1], self._board[21][2],
            self._board[3][0], self._board[3][1], self._board[3][2])
        result += '{0: >3}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}'.format(
            self._board[4][0], self._board[4][1], self._board[4][2],
            self._board[5][0], self._board[5][1], self._board[5][2])
        result += '{0:>4}\n'.format(self._board[6][2])
        result += '{0: >21}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}\n'.format(
            self._board[22][0], self._board[22][1], self._board[22][2],
            self._board[2][0], self._board[2][1], self._board[2][2])
        result += '{0: >21}|{1: >1}|{2:>1}{3:>3}|{4:>1}|{5:>1}\n'.format(
            self._board[23][0], self._board[23][1], self._board[23][2],
            self._board[1][0], self._board[1][1], self._board[1][2])
        result += '{0:>25}|{1:>1}|{2:>1}\n'.format(
            self._board[0][0], self._board[0][1], self._board[0][2])

        return result

    def move(self, idx):
        curr_stones = self._board[idx][2]
        i = (idx+1) % 24
        while curr_stones != 0:
            # skip over other palyer's manqalas
            if (self.turn == 1 and i in self.p2_manqala_idx) or (self.turn == 2 and i in self.p1_manqala_idx):
                i = (i + 1) % 24
                continue
            self._board[i][2] += 1
            if curr_stones == 1:
                """
                If this is the last stone in hand and will be placed in palyer's manqala then toggle player here
                so that the next toggle lets the player plays again
                """
                if (self.turn == 1 and i in self.p1_manqala_idx) or (self.turn == 2 and i in self.p2_manqala_idx):
                    self.toggle_player()

            #if you land on an empty cell take adjacent cells if exists
            # if curr_stones == 1 and self._board[i][2] == 1:
            #     if self.turn == 1:
            #         to_collect = 0
            #         if str(i) in self.p1_adjacencies:
            #             for adj in self.p1_adjacencies[str(i)]:
            #                 to_collect += self._board[adj][2]
            #                 self._board[adj][2] = 0
            #             to_collect += 1
            #             self._board[i][2] = 0
            #         self._board[0][2] += to_collect
            #     elif self.turn == 2:
            #         to_collect = 0
            #         if str(i) in self.p2_adjacencies:
            #             for adj in self.p1_adjacencies[str(i)]:
            #                 to_collect += self._board[adj][2]
            #                 self._board[adj][2] = 0
            #             to_collect += 1
            #             self._board[i][2] = 0
            #         self._board[6][2] += to_collect
            curr_stones -= 1
            i = (i + 1) % 24
        self._board[idx][2] = 0


    def score(self):
        return {"1": self._board[0][2] + self._board[12][2],
                "2": self._board[6][2] + self._board[18][2]}

    def done(self):
        winning_score = self.n * 10 + 1

        p1_score = self._board[0][2] + self._board[12][2]
        p2_score = self._board[6][2] + self._board[18][2]

        p1_cells = 0
        p1_cells += self._board[1][2] + self._board[2][2] + self._board[3][2] + self._board[4][2] + self._board[5][2]
        p1_cells += self._board[7][2] + self._board[8][2] + self._board[9][2] + self._board[10][2] + self._board[11][2]

        p2_cells = 0
        p2_cells += self._board[13][2] + self._board[14][2] + self._board[15][2] + self._board[16][2] + self._board[17][2]
        p2_cells += self._board[19][2] + self._board[20][2] + self._board[21][2] + self._board[22][2] + self._board[23][2]

        return p1_cells == 0 or p2_cells == 0 or p1_score >= winning_score or p2_score >= winning_score

    def winner(self):
        if self._board[0][2] + self._board[12][2] > self._board[6][2] + self._board[18][2]:
            return 1
        elif self._board[0][2] + self._board[12][2] < self._board[6][2] + self._board[18][2]:
            return 2
        else:
            return 0

    def toggle_player(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        return self.turn

def clear_screen():
    """Screen clearing *hack*"""
    print("\n" * 4)

def get_board():
    print("Enter number of stones per cell (Min 4 and Max 6, default is 4)?")
    n = int(input())
    if int(n) < 4 or int(n) > 6:
        n = 4
    board = [
        [0, 1, 0], [1, 1, n], [2, 1, n], [3, 2, n], [4, 2, n], [5, 2, n],
        [6, 2, 0], [7, 2, n], [8, 2, n], [9, 1, n], [10, 1, n], [11, 1, n],
        [12, 1, 0], [13, 1, n], [14, 1, n], [15, 2, n], [16, 2, n], [17, 2, n],
        [18, 2, 0], [19, 2, n], [20, 2, n], [21, 1, n], [22, 1, n], [23, 1, n]
    ]
    return n, board


def play_computer_computer():
    """
    TODO: This needs more work
    :return:
    """
    n, board = get_board()
    game = ManqalaGame(n, board)
    computer1 = AgentScore(1)
    computer2 = AgentScoreCells(2)
    while not game.done():
        print("Computer 1 | Computer 2")
        score = game.score()
        print("{0: >10} | {1: >10}".format(
            score[str(1)], score[str(2)]))
        print(game.render_board())
        print("Player {0}'s Turn".format(game.turn))
        sleep(0.2)
        if game.turn == 1:
            computer1_move = computer1.get_move(game)
            if computer1_move == -1:
                game.toggle_player()
                continue
            game.move(computer1_move)
            print("Computer 1 played {}".format(str(computer1_move)))
            print("Node Count for Computer 1: {}".format(str(computer1.node_count)))
        elif game.turn == 2:
            computer2_move = computer2.get_move(game)
            if computer2_move == -1:
                game.toggle_player()
                continue
            game.move(computer2_move)
            print("Computer 2 played {}".format(str(computer2_move)))
            print("Node Count for Computer 2: {}".format(str(computer2.node_count)))
        game.toggle_player()
    if game.done():
        winner = game.winner()
        if winner == 0:
            print("It's a Draw")
        else:
            print("The winner is:", str(game.winner()))

def play_computer_human(human, computer):
    print("Human Player:", str(human))
    print("Computer Player:", str(computer))
    n, board = get_board()
    game = ManqalaGame(n, board)
    computer_agent = AgentScore(computer)
    while not game.done():
        print("Computer: Player {} | Human: Player {}".format(computer, human))
        score = game.score()
        print("{0: >18} | {1: >15}".format(
            score[str(computer)], score[str(human)]))
        print(game.render_board())
        print("Player {0}'s Turn".format(game.turn))
        print("Node Count for Computer : {}".format(str(computer_agent.node_count)))
        sleep(1)
        if game.turn == computer:
            computer_move = computer_agent.get_move(game)
            game.move(computer_move)
            print("Computer played: {}".format(str(computer_move)))
        elif game.turn == human:
            print("Please enter the cell number to play, q to quit")
            i = input()
            if i == "q":
                break
            game.move(int(i))
            print("You played: {}".format(i))
        game.toggle_player()

    if game.done():
        winner = game.winner()
        if winner == 0:
            print("It's a Draw")
        else:
            print("The winner is:", str(game.winner()))
    else:
        print("Thank you, please play again!")
def play_human_human():
    pass

def play():
    print("Enter 1 for Human vs Computer and 2 for Computer vs Computer")
    c = input()
    if c == "2":
        play_computer_computer()
    else:
        play_computer_human(human=1, computer=2)



def test_manqala():
    print("test_manqala")
    board = [
        [0, 1, 0], [1, 1, 1], [2, 1, 6], [3, 2, 1], [4, 2, 0], [5, 2, 0],
        [6, 2, 0], [7, 2, 0], [8, 2, 0], [9, 1, 0], [10, 1, 0], [11, 1, 0],
        [12, 1, 0], [13, 1, 0], [14, 1, 0], [15, 2, 1], [16, 2, 0], [17, 2, 0],
        [18, 2, 0], [19, 2, 0], [20, 2, 0], [21, 1, 0], [22, 1, 0], [23, 1, 0]
    ]
    game = ManqalaGame(board, 1)
    print(game.render_board())
    game.move(2)
    print(game.render_board())


if __name__ == "__main__":
    play()
