from enum import Enum
import os

import pygame
import pygame.gfxdraw
import pygame.ftfont
import numpy as np

import game_logic as game
from square_rect import SquareRect
from config import config

SQUARESIZE = 100
HALF_SQUARE = int(SQUARESIZE / 2)
RADIUS = int(HALF_SQUARE - 5)

COLOR_BOARD = (137,149,155)
BLACK = (0,0,0)
COLOR_LEFT_PLAYER = config['players']['left_player']['color']
COLOR_RIGHT_PLAYER = config['players']['right_player']['color']

BOARD_OFFSET_X = 4.5
BOARD_OFFSET_Y = 3

screen_width = 16 * SQUARESIZE
screen_height = 9 * SQUARESIZE

size = (screen_width, screen_height)

pygame.ftfont.init()
number_font = pygame.ftfont.SysFont("Arial", int((SQUARESIZE / 4) * 3))

score_font = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3))
hack_font = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3))
countdown_font = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int(SQUARESIZE * 1.5))

status_font = pygame.ftfont.Font("fonts/WDRSans-Bold.otf", int((SQUARESIZE / 4) * 3))
status_font_large = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 5))

if os.environ.get('FULLSCREEN'):
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

class Positions:
    CURRENT_PLAYER_LEFT_PLAYER_LEFT = .5
    CURRENT_PLAYER_RIGHT_PLAYER_LEFT = 12
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

            pygame.draw.rect(screen, COLOR_BOARD, (xpos, ypos, SQUARESIZE, SQUARESIZE))

            if flipped_board[r][c] == 1:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, COLOR_LEFT_PLAYER)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, COLOR_LEFT_PLAYER)

            elif flipped_board[r][c] == 2:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, COLOR_RIGHT_PLAYER)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, COLOR_RIGHT_PLAYER)

            else:
                pygame.gfxdraw.filled_circle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, BLACK)
                pygame.gfxdraw.aacircle(screen, xpos + HALF_SQUARE, ypos + HALF_SQUARE, RADIUS, BLACK)

def draw_current_vote(vote, turn):
    if turn == 'left_player':
        color = COLOR_LEFT_PLAYER
    else:
        color = COLOR_RIGHT_PLAYER

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
        draw_text(str(c + 1), COLOR_BOARD, number_font, square_rect)

def draw_game_end(turn, tie=False):
    if tie:
        color = COLOR_BOARD
        text = "Unentschieden!"
    elif turn == 'left_player':
        color = COLOR_LEFT_PLAYER
        text = "1LIVE gewinnt!"
    else:
        color = COLOR_RIGHT_PLAYER
        text = "2LIVE gewinnt!"

    draw_text(text, color, status_font, Positions.GAME_END)

def draw_current_player(turn):

    if turn == 'left_player':
        color = COLOR_LEFT_PLAYER
        text = "1LIVE"
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        color = COLOR_RIGHT_PLAYER
        text = "2LIVE"
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

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

    if turn == 'left_player':
        color = COLOR_LEFT_PLAYER
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        color = COLOR_RIGHT_PLAYER
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

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
    draw_text(':', COLOR_BOARD, hack_font, colon_rect)

    left_player_number_rect = SquareRect(0, 0, colon_rect.left, 1)
    left_player_number_text_rect = draw_text(str(score['left_player']), COLOR_LEFT_PLAYER, hack_font, left_player_number_rect, align=Align.RIGHT)
    left_player_rect = SquareRect(0, 0, left_player_number_text_rect.left, 1)
    draw_text('1LIVE ', COLOR_LEFT_PLAYER, score_font, left_player_rect, align=Align.RIGHT)

    right_player_number_rect = SquareRect(colon_rect.right + .02, 0, 16, 1)
    right_player_number_text_rect = draw_text(str(score['right_player']), COLOR_RIGHT_PLAYER, hack_font, right_player_number_rect, align=Align.LEFT)
    right_player_rect = SquareRect(right_player_number_text_rect.right, 0, 16, 1)
    draw_text(' 2LIVE', COLOR_RIGHT_PLAYER, score_font, right_player_rect, align=Align.LEFT)

    draw_erase(SquareRect(0, 0.75, 16, .1))
