import numpy as np
import pygame
import sys
import math

GREY = (137,149,155)
BLACK = (0,0,0)
PINK = (255,0,153)
WHITE = (225,225,225)

ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_TURNS = ROW_COUNT * COLUMN_COUNT
SQUARESIZE = 50
HALF_SQUARE = int(SQUARESIZE / 2)
RADIUS = int(HALF_SQUARE - 5)

BOARD_text_center_x = 4.5
BOARD_OFFSET_Y = 3

wins = {
    1: 0,
    2: 0,
}

game_over = False
turn = 0
turn_count = 0

width = 16 * SQUARESIZE
height = 9 * SQUARESIZE

size = (width, height)

pygame.init()

status_font = pygame.font.SysFont("monospace", int((SQUARESIZE / 4) * 3))

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # check horizontal for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check aufsteigende Diagonalen
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check absteigende Diagonalen
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):

    flipped_board = np.flip(board, 0)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            xpos = int(c * SQUARESIZE + BOARD_text_center_x * SQUARESIZE)
            ypos = int(r * SQUARESIZE + BOARD_OFFSET_Y * SQUARESIZE)

            pygame.draw.rect(screen, GREY, (xpos, ypos, SQUARESIZE, SQUARESIZE))

            if flipped_board[r][c] == 1:
                pygame.draw.circle(screen, PINK, (xpos + HALF_SQUARE, ypos + HALF_SQUARE), RADIUS)

            elif flipped_board[r][c] == 2:
                pygame.draw.circle(screen, WHITE, (xpos + HALF_SQUARE, ypos + HALF_SQUARE), RADIUS)

            else:
                pygame.draw.circle(screen, BLACK, (xpos + HALF_SQUARE, ypos + HALF_SQUARE), RADIUS)

def draw_column_labels():
    for c in range(COLUMN_COUNT):
        col_number = status_font.render(str(c+1), 1, GREY)

        xpos = int(SQUARESIZE * 0.28 + c * SQUARESIZE + BOARD_text_center_x * SQUARESIZE)
        ypos = int(BOARD_OFFSET_Y * SQUARESIZE - 0.8 * SQUARESIZE)

        screen.blit(col_number, (xpos,ypos))

def draw_game_end(tie=False):
    if tie:
        color = GREY
        text = "Unentschieden!"
    elif turn == 0:
        color = PINK
        text = "Pink gewinnt!"
    else:
        color = WHITE
        text = "Weiß gewinnt!"


    xpos = BOARD_text_center_x * SQUARESIZE
    ypos = SQUARESIZE
    width = COLUMN_COUNT * SQUARESIZE
    height = SQUARESIZE

    pygame.draw.rect(screen, BLACK, (xpos, ypos, width, height))
    drawn_text = status_font.render(text, 1, color)
    text_rect = drawn_text.get_rect(center=(int(xpos + width / 2), ypos + int(height / 2)))
    screen.blit(drawn_text, text_rect)

def draw_current_player():
    
    pygame.draw.rect(screen, BLACK, (xpos, ypos, width, height))
    
    if turn == 0:
        color = PINK
        text = "Pink ist dran"
        text_center_x = 2.25
    else:
        color = WHITE
        text = "Weiß ist dran"
        text_center_x = 13.75

    xpos = text_center_x * SQUARESIZE
    ypos = SQUARESIZE
    width = 4 * SQUARESIZE
    height = SQUARESIZE

    drawn_text = status_font.render(text, 1, color)
    text_rect = drawn_text.get_rect(center=(int(xpos + width / 2), ypos + int(height / 2)))
    screen.blit(drawn_text, text_rect)

def game_loop(event):
    
    global turn, turn_count, game_over

    # Programm Exit
    if event.type == pygame.QUIT:
        sys.exit()

    number_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]
    if event.type == pygame.KEYDOWN and event.key in number_keys:

        if event.key == pygame.K_1:
            col = int(0)
        elif event.key == pygame.K_2:
            col = int(1)
        elif event.key == pygame.K_3:
            col = int(2)
        elif event.key == pygame.K_4:
            col = int(3)
        elif event.key == pygame.K_5:
            col = int(4)
        elif event.key == pygame.K_6:
            col = int(5)
        elif event.key == pygame.K_7:
            col = int(6)

        # Ask Player 1 Input
        if turn == 0:
            player_number = 1
        else:
            player_number = 2

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, player_number)

            if winning_move(board, player_number):
                draw_game_end()
                wins[player_number] += 1
                game_over = True
            elif turn_count == MAX_TURNS - 1:
                draw_game_end(tie=True)
                game_over = True

            print_board(board)
            draw_board(board)

            pygame.display.update()

            turn += 1
            turn = turn % 2
            turn_count += 1

screen = pygame.display.set_mode(size)

pink_first = False

while True:
    board = create_board()
    print_board(board)

    draw_board(board)
    draw_column_labels()
    pygame.display.update()

    pink_first = not pink_first
    game_over = False
    turn = 0 if pink_first else 1
    turn_count = 0

    while not game_over:

        draw_game_end()

        pygame.display.update()

        for event in pygame.event.get():

            game_loop(event)
            
            if game_over:
                pygame.time.wait(3000)