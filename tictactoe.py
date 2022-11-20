"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count to keep track of moves made on the board
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != None:
                count += 1
    # Determines that player O will be odd of count and player X will be even
    if board == initial_state():
        return X
    if count % 2 == 1:
        return O
    else:
        return X
            


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Creates set that stores available moves left
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                moves.add((i,j))
    return moves
                


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Error exception for invalid action
    if action not in actions(board):
        raise Exception("Invalid Action")

    #Creates copy of board based on action made
    i,j =action
    boardCopy = copy.deepcopy(board)
    boardCopy[i][j] = player(board)
    
    return boardCopy

    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Checks if a winner is from row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            else:
                return None

    #Checks if a winner is from column
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
            else:
                return None

    #Checks if a winner from first diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        else:
            return None

    #Checks if a winner from second diagonal
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
        else:
            return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Returns True for winners or if tie and False for if the board has empty spaces
    if winner(board) == X:
        return True

    if winner(board) == O:
        return True

    for i in range (3):
        for j in range(3):
            if board[i][j]== None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #Assigns values for player X, 0 and for a tie
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    else:
        return 0


def Max_value(board):
    #Algorithm for max value:
    #Declares most possible smallest number
    #Checks if board is Terminal i.e. game is finished , and then returns utility
    #Loops to determine possible maximum value based off of the action of the Min_value algorithm.
    maxValue = -math.inf
    if terminal(board):
        return (utility(board))
    for action in actions(board):
        maxValue = max(maxValue, Min_value(result(board, action)))
    return maxValue


def Min_value(board):
    #Algorithm for min value:
    #The process is the same for Max_value except it is esentially the opposite operattion
    minValue = math.inf
    if terminal(board):
        return (utility(board))
    for action in actions(board):
        minValue = min(minValue, Max_value(result(board, action)))
    return minValue


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #Checks if the game is finished
    if terminal(board) == True:
        return None
    
    #Determines the action for player X using Min_value and reverse to get what action to take
    elif player(board) == X:
        playsForX = []
        for action in actions(board):
            playsForX.append([Min_value(result(board,action)),action])

        return sorted(playsForX, key=lambda x: x[0], reverse=True)[0][1]

    #Determines the action for player O using Max_value to get what action to take
    elif player(board) == O:
        playsForO = []
        for action in actions(board):
            playsForO.append([Max_value(result(board,action)),action])

        return sorted(playsForO, key=lambda x: x[0])[0][1]
                         
    
