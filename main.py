from copy import deepcopy
import time
from enum import Enum

global PLAYER, STATIC_WEIGHTS

with open("input.txt", "r") as file:
    BOARD = []
    PLAYER = file.readline().rstrip()
    player_time, opp_time = file.readline().split()
    start_time = time.time()
    for _ in range(12):
        BOARD.append(list(file.readline().rstrip()))

class GameBoard:
    def __init__(self, board, player):
        self.board = board
        self.my_player = player
        self.my_opponent = 'X' if self.my_player == 'O' else 'O'
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.board_size = len(self.board)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # increment move
    @staticmethod
    def step_increase(step, direction):
        # print("step", step)
        # print("direction", direction)
        step = list(map(sum, zip(step, direction)))
        # print(step)
        # print(direction)
        while all(map(lambda i: 0 <= i < 12, step)):
            yield step
            step = list(map(sum, zip(step, direction)))


    # get_flips
    def find_flips(self, min_player, origin, direction, player):
        flips = [origin]
        for x, y in self.step_increase(origin, direction):
            if self.board[x][y] == min_player:
                flips.append((x, y))
            elif self.board[x][y] == ".":
                break
            elif self.board[x][y] == player and len(flips) > 1:
                return flips
        return []

    def flip_pieces(self, step, player):
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        # flip the pieces on the board
        flips = (flip for direction in self.directions
                 for flip in self.find_flips(opponent, step, direction, player))
        for x, y in flips:
            self.board[x][y] = player

    def isGameFinished(self):
        return not (self.hasAnyMoves(self.my_player) or self.hasAnyMoves(self.my_opponent))

    def hasAnyMoves(self, ply):
        return len(self.getAllPossibleMoves(ply)) > 0

    def getAllPossibleMoves(self, _player):
        result = []
        for a in range(12):
            for b in range(12):
                player_can_play = self.canPlay(_player, a, b)
                if player_can_play:
                    result.append((a, b))
                    # print("result", result)
        return result

    def get_possible_moves(self, _player):
        possible_moves = []

        for row in range(12):
            for col in range(12):
                if self.board[row][col] == '.':  # Empty position
                    # Check if placing a piece at this position would result in captures
                    if self.is_valid_move(board, row, col, player):
                        possible_moves.append((row, col))

        return possible_moves

    def is_valid_move(board, row, col, player):
        # Check if the position is valid for the given player
        if not self.is_valid_position(board, row, col):
            return False

        # Check if placing a piece at this position would result in captures
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if is_valid_direction(board, row, col, dr, dc, player):
                return True

        return False
    def is_valid_position(board, row, col):
        return 0 <= row < 12 and 0 <= col < 12
    def canPlay(self, _player, i, j):
        if self.board[i][j] != ".":
            return False
        if _player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        # Check in all 8 directions
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue

                mi, mj = i + di, j + dj
                c = 0

                while 0 <= mi < 8 and 0 <= mj < 8 and self.board[mi][mj] == opponent:
                    mi += di
                    mj += dj
                    c += 1

                if 0 <= mi < 8 and 0 <= mj < 8 and self.board[mi][mj] == _player and c > 0:
                    return True

        return False

    def getTotalStoneCount(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell != ".":
                    count += 1
        return count

    def getPlayerStoneCount(self, player):
        score = 0
        for i in range(12):
            for j in range(12):
                if self.board[i][j] == player:
                    score += 1
        return score

    def getStableDisks(self, player, i, j):
        stableDiscs = []

        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        # Define the eight possible directions
        directions_local = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for di, dj in directions_local:
            mi, mj = i + di, j + dj
            possibleStableDiscs = []

            while 0 <= mi < 12 and 0 <= mj < 12 and self.board[mi][mj] == opponent:
                possibleStableDiscs.append((mi, mj))
                mi += di
                mj += dj

            if 0 <= mi < 12 and 0 <= mj < 12 and self.board[mi][mj] == player and possibleStableDiscs:
                stableDiscs.extend(possibleStableDiscs)

        return stableDiscs

    def getFrontierSquares(self, player):
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        frontiers = []

        for i in range(12):
            for j in range(12):
                if self.board[i][j] == opponent:
                    possiblefrontiers = []

                    # Check 8 directions
                    # Up
                    if i > 0 and self.board[i - 1][j] == 0:
                        possiblefrontiers.append((i - 1, j))
                    # Down
                    if i < 11 and self.board[i + 1][j] == 0:
                        possiblefrontiers.append((i + 1, j))
                    # Right
                    if j < 11 and self.board[i][j + 1] == 0:
                        possiblefrontiers.append((i, j + 1))
                    # Left
                    if j > 0 and self.board[i][j - 1] == 0:
                        possiblefrontiers.append((i, j - 1))
                    # Up-left
                    if i > 0 and j > 0 and self.board[i - 1][j - 1] == 0:
                        possiblefrontiers.append((i - 1, j - 1))
                    # Up-right
                    if i > 0 and j < 11 and self.board[i - 1][j + 1] == 0:
                        possiblefrontiers.append((i - 1, j + 1))
                    # Down-left
                    if i < 11 and j > 0 and self.board[i + 1][j - 1] == 0:
                        possiblefrontiers.append((i + 1, j - 1))
                    # Down-right
                    if i < 11 and j < 11 and self.board[i + 1][j + 1] == 0:
                        possiblefrontiers.append((i + 1, j + 1))

                    for pf in possiblefrontiers:
                        if pf not in frontiers:
                            frontiers.append(pf)

        return frontiers

# Evaluation functions
def evalCorner(board, player):
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'

    myCorners = 0
    opCorners = 0

    if board[0][0] == player:
        myCorners += 1
    if board[11][0] == player:
        myCorners += 1
    if board[0][11] == player:
        myCorners += 1
    if board[11][11] == player:
        myCorners += 1

    if board[0][0] == opponent:
        opCorners += 1
    if board[11][0] == opponent:
        opCorners += 1
    if board[0][11] == opponent:
        opCorners += 1
    if board[11][11] == opponent:
        opCorners += 1

    return 100 * (myCorners - opCorners) // (myCorners + opCorners + 1)

def evalDiscDiff(board, player):
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'

    mySC = board.getPlayerStoneCount(player)
    opSC = board.getPlayerStoneCount(opponent)

    return 100 * (mySC - opSC) // (mySC + opSC + 1)

def stability(board, player):

    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'

    myS = 0
    opS = 0

    if board.board[0][0] == player:
        myS += len(board.getStableDisks(player, 0, 0))
    if board.board[0][11] == player:
        myS += len(board.getStableDisks(player, 0, 11))
    if board.board[11][0] == player:
        myS += len(board.getStableDisks(player, 11, 0))
    if board.board[11][11] == player:
        myS += len(board.getStableDisks(player, 11, 11))

    if board.board[0][0] == opponent:
        opS += len(board.getStableDisks(opponent, 0, 0))
    if board.board[0][11] == opponent:
        opS += len(board.getStableDisks(opponent, 0, 11))
    if board.board[11][0] == opponent:
        opS += len(board.getStableDisks(opponent, 11, 0))
    if board.board[11][11] == opponent:
        opS += len(board.getStableDisks(opponent, 11, 11))

    return 100 * (myS - opS) // (myS + opS + 1)

def frontier(board, player):
    myF = len(board.getFrontierSquares(player))
    opF = len(board.getFrontierSquares(player))

    return 100 * (myF - opF) // (myF + opF + 1)

def mobility(board, player):
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    myMoveCount = len(board.getAllPossibleMoves(player))
    opMoveCount = len(board.getAllPossibleMoves(opponent))

    return 100 * (myMoveCount - opMoveCount) // (myMoveCount + opMoveCount + 1)


# Main Game Function
class Game:
    def __init__(self, board):
        self.board = board

    def start(self, depth):
        return self.alpha_beta_search(self.board, depth)

    def alpha_beta_search(self, board, depth):
        return self.max(board, depth)

    def getGamePhase(self, board):
        sc = board.getTotalStoneCount()
        if sc < 48:     #early
            return 0
        elif sc <= 96:  #mid_game
            return 1
        else:           #late_game
            return 2

    def evaluation(self, board):

        phase = self.getGamePhase(board)
        if phase == 0:
            return 1000 * evalCorner(board.board, board.my_player) + 50 * mobility(board, board.my_player) \
                + 200 * stability(board, board.my_player) + 300 * frontier(board, board.my_player)
        elif phase == 1:
            return 1000 * evalCorner(board.board, board.my_player) \
                + 20 * mobility(board, board.my_player) \
                + 10 * evalDiscDiff(board, board.my_player) \
                + 200 * stability(board, board.my_player) \
                + 300 * frontier(board, board.my_player)
        else:  # LATE_GAME
            return 1000 * evalCorner(board.board, board.my_player) \
                + 100 * mobility(board,board.my_player) \
                + 500 * evalDiscDiff(board, board.my_player) \
                + 200 * stability(board, board.my_player) \
                + 300 * frontier(board, board.my_player)

    def max(self, board, depth):
        if depth == 0 or board.isGameFinished():
            e_val = self.evaluation(board)
            return e_val, None

        best_score = -float('inf')
        best_move = None

        moves = board.getAllPossibleMoves(self.board.my_player)


        for move in moves:
            new_board = deepcopy(board)
            new_board.flip_pieces(move, self.board.my_player)

            score, _move = self.min(new_board, depth - 1)

            # print('max', depth, score)
            if score > best_score:
                best_score = score
                best_move = move

            board.alpha = max(board.alpha, score)
            if board.alpha >= board.beta:
                break

        return best_score, best_move

    def min(self, board, depth):
        if depth == 0 or board.isGameFinished():
            e_val = self.evaluation(board)
            return e_val, None

        best_score = float('inf')
        best_move = None

        moves = board.getAllPossibleMoves(self.board.my_player)


        for move in moves:
            new_board = deepcopy(board)
            new_board.flip_pieces(move, self.board.my_player)

            score, _move = self.max(new_board, depth - 1)

            # print('min', depth, score)
            if score < best_score:
                best_score = score
                best_move = move

            board.beta = min(board.beta, score)
            if board.alpha >= board.beta:
                break

        return best_score, best_move

# Create new board state
current_board = GameBoard(BOARD, PLAYER)

# Create a new game
new_game = Game(current_board)
best_score, best_move = new_game.start(3)

def parse_move(row, col):
    column_letter = chr(ord('a') + col)
    row_number = row + 1
    return column_letter + str(row_number)

best_move = parse_move(best_move[1], best_move[0])
print(best_move)

# Print best move to output.txt
with open("output.txt", "w") as file:
    file.write(f"{best_move}\n")