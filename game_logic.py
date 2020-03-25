import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

board = None

def create_board():
    global board
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))

def drop_piece(row, col, piece):
    global board
    board[row][col] = piece

def get_valid_locations():
    return [
        col
        for col in range(COLUMN_COUNT)
        if is_valid_location(col)
    ]

def is_valid_location(col):
    global board
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(col):
    global board
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board():
    global board
    print(np.flip(board, 0))

def winning_move(piece):
    global board
    # Check horizontal for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check ascending diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check descending diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
