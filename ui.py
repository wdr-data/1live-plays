from enum import Enum

import pygame
import pygame.gfxdraw
import pygame.ftfont
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

pygame.ftfont.init()
number_font = pygame.ftfont.SysFont("Arial", int((SQUARESIZE / 4) * 3))

score_font = pygame.ftfont.Font("fonts/WDRSans-ExtraBold.otf", int((SQUARESIZE / 4) * 3))
hack_font = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3))
countdown_font = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int(SQUARESIZE * 1.5))

status_font = pygame.ftfont.Font("fonts/WDRSans-Bold.otf", int((SQUARESIZE / 4) * 3))
status_font_large = pygame.ftfont.Font("fonts/WDRSans-ExtraBold.otf", int((SQUARESIZE / 4) * 5))

screen = pygame.display.set_mode(size)

class Positions:
    CURRENT_PLAYER_PINK_LEFT = .5
    CURRENT_PLAYER_WHITE_LEFT = 12
    GAME_END = SquareRect(BOARD_OFFSET_X, 1, game.COLUMN_COUNT, 1)
    CURRENT_VOTE = SquareRect(BOARD_OFFSET_X, 1, game.COLUMN_COUNT, 1)
    CURRENT_PLAYER = SquareRect(0, BOARD_OFFSET_Y, 3.5, 2)
    COUNTDOWN = SquareRect(0, 5.5, 3.5, 2)

class Align(Enum):
    CENTER = 'center'
    LEFT = 'left'
    RIGHT = 'right'


def draw_erase(square_rect, color=BLACK):
    rect = square_rect.get_rect(SQUARESIZE)
    pygame.draw.rect(screen, color, rect)

def draw_text(text, color, font, square_rect, align=Align.CENTER):
    rect = square_rect.get_rect(SQUARESIZE)
    draw_erase(square_rect)

    drawn_text = font.render(text, 1, color)

    text_rect = drawn_text.get_rect(center=(rect.left + int(rect.width / 2), rect.top + int(rect.height / 2)))

    if align is Align.LEFT:
        text_rect.left = rect.left
    if align is Align.RIGHT:
        text_rect.right = rect.right

    screen.blit(drawn_text, text_rect)

    return SquareRect(
        text_rect.left / SQUARESIZE,
        text_rect.top / SQUARESIZE,
        text_rect.width / SQUARESIZE,
        text_rect.height / SQUARESIZE,
    )

def draw_board():
    flipped_board = np.flip(game.board, 0)

    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
            xpos = int(c * SQUARESIZE + BOARD_OFFSET_X * SQUARESIZE)
            ypos = int(r * SQUARESIZE + BOARD_OFFSET_Y * SQUARESIZE)

            pygame.draw.rect(screen, GREY, (xpos, ypos, SQUARESIZE, SQUARESIZE))

            if flipped_board[r][c] == 1:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, PINK)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, PINK)

            elif flipped_board[r][c] == 2:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, WHITE)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, WHITE)

            else:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, BLACK)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, BLACK)

def draw_current_vote(vote, turn):
    if turn == 'pink':
        color = PINK
    else:
        color = WHITE

    left = int((BOARD_OFFSET_X + vote) * SQUARESIZE)
    top = int(Positions.CURRENT_VOTE.top * SQUARESIZE)

    draw_erase(Positions.CURRENT_VOTE)
    pygame.gfxdraw.filled_circle(screen, left + HALF_SQUARE, top + HALF_SQUARE, RADIUS, color)
    pygame.gfxdraw.aacircle(screen, left + HALF_SQUARE, top + HALF_SQUARE, RADIUS, color)

def draw_column_labels():
    for c in range(game.COLUMN_COUNT):
        square_rect = SquareRect(
            BOARD_OFFSET_X + c,
            BOARD_OFFSET_Y - 0.8,
            1,
            0.8,
        )
        draw_text(str(c + 1), GREY, number_font, square_rect)

def draw_game_end(turn, tie=False):
    if tie:
        color = GREY
        text = "Unentschieden!"
    elif turn == 'pink':
        color = PINK
        text = "Pink gewinnt!"
    else:
        color = WHITE
        text = "Weiß gewinnt!"

    draw_text(text, color, status_font, Positions.GAME_END)

def draw_current_player(turn):

    if turn == 'pink':
        color = PINK
        text = "PINK"
        text_left = Positions.CURRENT_PLAYER_PINK_LEFT
        erase_left = Positions.CURRENT_PLAYER_WHITE_LEFT
    else:
        color = WHITE
        text = "WEIß"
        text_left = Positions.CURRENT_PLAYER_WHITE_LEFT
        erase_left = Positions.CURRENT_PLAYER_PINK_LEFT

    square_rect_text = Positions.CURRENT_PLAYER.copy()
    square_rect_text.left = text_left

    square_rect_erase = Positions.CURRENT_PLAYER.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    draw_text(text, color, status_font_large, square_rect_text)

    square_rect_text.height = 1
    square_rect_erase.height = 1
    square_rect_text.top += 1.5
    square_rect_erase.top += 1.5
    draw_erase(square_rect_erase)
    draw_text('ist dran', color, status_font, square_rect_text)

def draw_countdown(turn, time_left, no_votes_message):

    if turn == 'pink':
        color = PINK
        text_left = Positions.CURRENT_PLAYER_PINK_LEFT
        erase_left = Positions.CURRENT_PLAYER_WHITE_LEFT
    else:
        color = WHITE
        text_left = Positions.CURRENT_PLAYER_WHITE_LEFT
        erase_left = Positions.CURRENT_PLAYER_PINK_LEFT

    square_rect_text = Positions.COUNTDOWN.copy()
    square_rect_text.left = text_left

    square_rect_erase = Positions.COUNTDOWN.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    square_rect_countdown = draw_text(str(time_left), color, countdown_font, square_rect_text)
    square_rect_countdown.top = square_rect_countdown.bottom - .15
    square_rect_countdown.height = .1
    draw_erase(square_rect_countdown)

    square_rect_text.top = square_rect_text.bottom
    square_rect_text.height = 1
    square_rect_text.left -= .5
    square_rect_text.width += 1
    draw_erase(square_rect_text, color=BLACK)

    if no_votes_message:
        draw_text('Keine Votes!', color, status_font, square_rect_text)

def draw_scoreboard(score):
    colon_rect = SquareRect(7.85, 0, .3, 1)
    draw_text(':', GREY, hack_font, colon_rect)

    pink_number_rect = SquareRect(0, 0, colon_rect.left, 1)
    pink_number_text_rect = draw_text(str(score[1]), PINK, hack_font, pink_number_rect, align=Align.RIGHT)
    pink_rect = SquareRect(0, 0, pink_number_text_rect.left, 1)
    draw_text('PINK ', PINK, score_font, pink_rect, align=Align.RIGHT)

    white_number_rect = SquareRect(colon_rect.right + .02, 0, 16, 1)
    white_number_text_rect = draw_text(str(score[2]), WHITE, hack_font, white_number_rect, align=Align.LEFT)
    white_rect = SquareRect(white_number_text_rect.right, 0, 16, 1)
    draw_text(' WEIß', WHITE, score_font, white_rect, align=Align.LEFT)

    draw_erase(SquareRect(0, 0.75, 16, .1))
