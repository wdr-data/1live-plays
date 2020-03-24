import pygame
import numpy as np

import game_logic as game
from square_rect import SquareRect

SQUARESIZE = 50
HALF_SQUARE = int(SQUARESIZE / 2)
RADIUS = int(HALF_SQUARE - 5)

GREY = (137,149,155)
BLACK = (0,0,0)
PINK = (255,0,153)
WHITE = (225,225,225)

BOARD_OFFSET_X = 4.5
BOARD_OFFSET_Y = 3

screen_width = 16 * SQUARESIZE
screen_height = 9 * SQUARESIZE

size = (screen_width, screen_height)

status_font = pygame.font.SysFont("monospace", int((SQUARESIZE / 4) * 3))

screen = pygame.display.set_mode(size)

class Positions:
    CURRENT_PLAYER_PINK_LEFT = .5
    CURRENT_PLAYER_WHITE_LEFT = 12
    GAME_END = SquareRect(BOARD_OFFSET_X, 1, game.COLUMN_COUNT, 1)
    CURRENT_PLAYER = SquareRect(1, .5, 3.5, 1)

def draw_erase(square_rect):
    rect = square_rect.get_rect(SQUARESIZE)
    pygame.draw.rect(screen, BLACK, rect)

def draw_text(text, color, font, square_rect):
    rect = square_rect.get_rect(SQUARESIZE)
    draw_erase(square_rect)

    drawn_text = font.render(text, 1, color)
    text_rect = drawn_text.get_rect(center=(rect.left + int(rect.width / 2), rect.top + int(rect.height / 2)))
    screen.blit(drawn_text, text_rect)

def draw_board():
    flipped_board = np.flip(game.board, 0)

    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
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
    for c in range(game.COLUMN_COUNT):
        col_number = status_font.render(str(c+1), 1, GREY)

        xpos = int(SQUARESIZE * 0.28 + c * SQUARESIZE + BOARD_OFFSET_X * SQUARESIZE)
        ypos = int(BOARD_OFFSET_Y * SQUARESIZE - 0.8 * SQUARESIZE)

        screen.blit(col_number, (xpos,ypos))

def draw_game_end(turn, tie=False):
    if tie:
        color = GREY
        text = "Unentschieden!"
    elif turn == 0:
        color = PINK
        text = "Pink gewinnt!"
    else:
        color = WHITE
        text = "Weiß gewinnt!"

    draw_text(text, color, status_font, Positions.GAME_END)

def draw_current_player(turn):

    if turn == 0:
        color = PINK
        text = "Pink ist dran"
        text_left = Positions.CURRENT_PLAYER_PINK_LEFT
        erase_left = Positions.CURRENT_PLAYER_WHITE_LEFT
    else:
        color = WHITE
        text = "Weiß ist dran"
        text_left = Positions.CURRENT_PLAYER_WHITE_LEFT
        erase_left = Positions.CURRENT_PLAYER_PINK_LEFT

    square_rect_text = Positions.CURRENT_PLAYER.copy()
    square_rect_text.left = text_left

    square_rect_erase = Positions.CURRENT_PLAYER.copy()
    square_rect_erase.left = erase_left

    # erase old text
    draw_erase(square_rect_erase)
    draw_text(text, color, status_font, square_rect_text)