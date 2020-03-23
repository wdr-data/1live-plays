import numpy as np
import pygame
import sys
import math

# hallo

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

BOARD_OFFSET_X = 4.5
BOARD_OFFSET_Y = 3

wins_pink = 0
wins_white = 0
game_over = False
turn = 0
anz_turns = 0

width = 16 * SQUARESIZE
height = 9 * SQUARESIZE

size = (width, height)

pygame.init()

myfont = pygame.font.SysFont("monospace", int((SQUARESIZE/4)*3))

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

            xpos = int(c * SQUARESIZE + BOARD_OFFSET_X * SQUARESIZE)
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
        col_number = myfont.render(str(c+1), 1, GREY)
        
        xpos = int(SQUARESIZE * 0.28 + c * SQUARESIZE + BOARD_OFFSET_X * SQUARESIZE)
        ypos = int(BOARD_OFFSET_Y * SQUARESIZE - 0.8 * SQUARESIZE)
        
        screen.blit(col_number, (xpos,ypos))

def draw_player():

    if turn == 0:
        color = PINK
        text = "Pink ist dran"

    else:
        color = WHITE
        text = "Weiß ist dran"

    xpos = BOARD_OFFSET_X * SQUARESIZE
    ypos = SQUARESIZE

    pygame.draw.rect(screen, BLACK, (xpos, ypos, 7 * SQUARESIZE, SQUARESIZE))
    dran = myfont.render(text, 1, color)
    screen.blit(dran, (int(xpos + SQUARESIZE * 0.4), int(ypos + SQUARESIZE * 0.1)))

board = create_board()
print_board(board)

screen = pygame.display.set_mode(size)
draw_board(board)
draw_column_labels()
pygame.display.update()

while anz_turns < MAX_TURNS and not game_over:

    draw_player()

    pygame.display.update()

    for event in pygame.event.get():

        # Programm Exit
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Ask Player 1 Input
            if turn == 0:

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

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if anz_turns == MAX_TURNS-1:
                        label = myfont.render("Unentschieden!", 1, GREY)
                        screen.blit(label, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))

                    if winning_move(board, 1):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("Pink gewinnt!", 1, PINK)
                        wins_pink += 1
                        screen.blit(label, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))
                        game_over = True

                else:
                    turn -= 1
                    anz_turns -= 1

            # Ask Player 2 Input
            else:

                if event.type == pygame.KEYDOWN:
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

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if anz_turns == MAX_TURNS-1:
                        label = myfont.render("Unentschieden!", 1, GREY)
                        screen.blit(label, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))

                    if winning_move(board, 2):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("Weiß gewinnt!", 1, WHITE)
                        wins_white += 1
                        screen.blit(label, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))
                        game_over = True

                else:
                    turn -= 1
                    anz_turns -= 1

            print_board(board)
            draw_board(board)

            pygame.display.update()

            turn += 1
            turn = turn % 2
            anz_turns += 1

            if anz_turns == MAX_TURNS:
                pygame.time.wait(3000)

            if game_over:
                pygame.time.wait(3000)