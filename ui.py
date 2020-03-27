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

class Fonts:
    SCORE = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3))
    NUMBERS = SCORE
    GAME_END = SCORE
    COUNTDOWN = pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int(SQUARESIZE * 1.5))
    STATUS = pygame.ftfont.Font("fonts/WDRSans-Bold.otf", int((SQUARESIZE / 4) * 3))
    STATUS_LARGE = {
        name: pygame.ftfont.Font("fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 5 * (5 / len(player['name']))))
        for name, player in config['players'].items()
    }

if os.environ.get('FULLSCREEN'):
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

class Positions:
    SCORE_HEIGHT = 1.0
    CURRENT_PLAYER_LEFT_PLAYER_LEFT = .1
    CURRENT_PLAYER_RIGHT_PLAYER_LEFT = 11.6
    CURRENT_PLAYER = SquareRect(0, BOARD_OFFSET_Y, 4.4, 2)
    GAME_END = SquareRect(0, 1, 16, 1)
    CURRENT_VOTE = SquareRect(BOARD_OFFSET_X, 1, game.COLUMN_COUNT, 1)
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

    if not text:
        height_offset_umlaut = 0
    elif len(text) == 1:
        height_offset_umlaut = font.get_ascent() - font.metrics(text)[0][3]
    else:
        height_offset_umlaut = font.get_ascent() - max(*[metric[3] for metric in font.metrics(text)])

    height_offset_umlaut = min(0, height_offset_umlaut)

    text_rect = drawn_text.get_rect(center=(rect.left + int(rect.width / 2), rect.top + int(rect.height / 2)))
    text_rect.top += height_offset_umlaut / 2

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

def draw_hack_text(text, color, font, square_rect, align=Align.CENTER):
    text_rect = draw_text(text, color, font, square_rect, align=align)
    erase_rect = text_rect.copy()
    erase_rect.top = erase_rect.bottom - .11 * text_rect.height
    erase_rect.height = .07 * text_rect.height
    erase_rect.left -= .05 * text_rect.height
    erase_rect.width += .1 * text_rect.height
    draw_erase(erase_rect)
    return text_rect

def draw_piece(left, top, color):
    pygame.gfxdraw.filled_circle(
        screen,
        int(left * SQUARESIZE) + HALF_SQUARE,
        int(top * SQUARESIZE) + HALF_SQUARE,
        RADIUS,
        color,
    )
    pygame.gfxdraw.aacircle(
        screen,
        int(left * SQUARESIZE) + HALF_SQUARE,
        int(top * SQUARESIZE) + HALF_SQUARE,
        RADIUS,
        color,
    )

def draw_board():
    flipped_board = np.flip(game.board, 0)

    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
            left = c + BOARD_OFFSET_X
            top = r + BOARD_OFFSET_Y

            pygame.draw.rect(
                screen,
                COLOR_BOARD,
                (int(left * SQUARESIZE), int(top * SQUARESIZE), SQUARESIZE, SQUARESIZE)
            )

            if flipped_board[r][c] == 1:
                draw_piece(left, top, COLOR_LEFT_PLAYER)

            elif flipped_board[r][c] == 2:
                draw_piece(left, top, COLOR_RIGHT_PLAYER)

            else:
                draw_piece(left, top, BLACK)

def draw_current_vote(vote, turn):
    color = config['players'][turn]['color']

    left = BOARD_OFFSET_X + vote
    top = Positions.CURRENT_VOTE.top

    draw_erase(Positions.CURRENT_VOTE)
    draw_piece(left, top, color)

def draw_column_labels():
    for c in range(game.COLUMN_COUNT):
        square_rect = SquareRect(
            BOARD_OFFSET_X + c,
            BOARD_OFFSET_Y - 0.8,
            1,
            0.8,
        )
        draw_hack_text(str(c + 1), COLOR_BOARD, Fonts.NUMBERS, square_rect)

def draw_game_end(turn, tie=False):
    if tie:
        color = COLOR_BOARD
        text = "Unentschieden!"
    else:
        color = config['players'][turn]['color']
        text = f"{config['players'][turn]['name']} gewinnt!"

    draw_hack_text(text, color, Fonts.GAME_END, Positions.GAME_END)

def draw_current_player(turn):
    color = config['players'][turn]['color']
    text = config['players'][turn]['name']

    if turn == 'left_player':
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

    square_rect_text = Positions.CURRENT_PLAYER.copy()
    square_rect_text.left = text_left

    square_rect_erase = Positions.CURRENT_PLAYER.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    draw_hack_text(text, color, Fonts.STATUS_LARGE[turn], square_rect_text)

    square_rect_text.height = 1
    square_rect_erase.height = 1
    square_rect_text.top += 1.5
    square_rect_erase.top += 1.5
    draw_erase(square_rect_erase)
    draw_text('ist dran', color, Fonts.STATUS, square_rect_text)

def draw_countdown(turn, time_left, no_votes_message):
    color = config['players'][turn]['color']

    if turn == 'left_player':
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

    square_rect_text = Positions.COUNTDOWN.copy()
    square_rect_text.left = text_left

    square_rect_erase = Positions.COUNTDOWN.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    square_rect_countdown = draw_text(str(time_left), color, Fonts.COUNTDOWN, square_rect_text)
    square_rect_countdown.top = square_rect_countdown.bottom - .15
    square_rect_countdown.height = .1
    draw_erase(square_rect_countdown)

    square_rect_text.top = square_rect_text.bottom
    square_rect_text.height = 1
    square_rect_text.left -= .5
    square_rect_text.width += 1
    draw_erase(square_rect_text, color=BLACK)

    if no_votes_message:
        draw_text('Keine Votes!', color, Fonts.STATUS, square_rect_text)

def draw_scoreboard(score):
    colon_rect = SquareRect(7.85, 0, .3, Positions.SCORE_HEIGHT)
    draw_hack_text(':', COLOR_BOARD, Fonts.SCORE, colon_rect)

    left_player_rect = SquareRect(0, 0, colon_rect.left, Positions.SCORE_HEIGHT)
    left_player_rect.right = colon_rect.left
    draw_hack_text(
        f"{config['players']['left_player']['name']} {score['left_player']}",
        COLOR_LEFT_PLAYER,
        Fonts.SCORE,
        left_player_rect,
        align=Align.RIGHT
    )

    right_player_rect = SquareRect(
        colon_rect.right + 0.01, 0,
        colon_rect.left, Positions.SCORE_HEIGHT,
    )
    draw_hack_text(
        f"{score['right_player']} {config['players']['right_player']['name']}",
        COLOR_RIGHT_PLAYER,
        Fonts.SCORE,
        right_player_rect,
        align=Align.LEFT
    )
