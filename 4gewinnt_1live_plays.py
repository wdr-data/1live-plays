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
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

wins_pink = 0
wins_white = 0
game_over = False
turn = 0
anz_turns = 0

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+2) * SQUARESIZE

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
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GREY, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            if board[r][c] == 1:
                pygame.draw.circle(screen, PINK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

            elif board[r][c] == 2:
                pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    # Zeilenbeschriftung
    pygame.draw.rect(screen, BLACK, (0,int(1*SQUARESIZE), width, SQUARESIZE))
    col_one = myfont.render("1", 1, GREY)
    col_two = myfont.render("2", 1, GREY)
    col_three = myfont.render("3", 1, GREY)
    col_four = myfont.render("4", 1, GREY)
    col_five = myfont.render("5", 1, GREY)
    col_six = myfont.render("6", 1, GREY)
    col_seven = myfont.render("7", 1, GREY)
    # screen.blit(col_one, (int(SQUARESIZE*0.28,int((SQUARESIZE*0.2)+SQUARESIZE))))
    screen.blit(col_one, (28,120))
    screen.blit(col_two, (128,120))
    screen.blit(col_three, (228,120))
    screen.blit(col_four, (328,120))
    screen.blit(col_five, (428,120))
    screen.blit(col_six, (525,120))
    screen.blit(col_seven, (628,120))

    pygame.display.update()

board = create_board()
print_board(board)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while anz_turns < MAX_TURNS and not game_over:

    if turn != 0:
        pygame.draw.rect(screen, BLACK, (0,int(0*SQUARESIZE), width, SQUARESIZE))
        dran = myfont.render("Pink ist dran", 1, PINK)
        screen.blit(dran, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))

    else:
        pygame.draw.rect(screen, BLACK, (0,int(0*SQUARESIZE), width, SQUARESIZE))
        dran = myfont.render("Weiß ist dran", 1, WHITE)
        screen.blit(dran, (int(SQUARESIZE*0.4),int(SQUARESIZE*0.1)))

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

            turn += 1
            turn = turn % 2
            anz_turns += 1

            if anz_turns == MAX_TURNS:
                pygame.time.wait(3000)

            if game_over:
                pygame.time.wait(3000)