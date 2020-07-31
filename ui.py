from enum import Enum
import os

import pygame
import pygame.gfxdraw
import pygame.ftfont
import pygame.image
import pygame.transform
import numpy as np

import game_logic as game
from square_rect import SquareRect
from config import config

SQUARESIZE = 100
HALF_SQUARE = int(SQUARESIZE / 2)
RADIUS = int(HALF_SQUARE - 5)

COLOR_BOARD = (137, 149, 155)
BLACK = (0, 0, 0)
COLOR_LEFT_PLAYER = config["players"]["left_player"]["color"]
COLOR_RIGHT_PLAYER = config["players"]["right_player"]["color"]

BOARD_OFFSET_X = 4.5
BOARD_OFFSET_Y = 3

screen_width = 16 * SQUARESIZE
screen_height = 9 * SQUARESIZE

size = (screen_width, screen_height)

pygame.ftfont.init()

if os.environ.get("FULLSCREEN"):
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)


class Fonts:
    VOFFSET = {"left_player": 0.08 / SQUARESIZE, "right_player": -0.035 / SQUARESIZE}
    HOFFSET = {"left_player": 0, "right_player": 0.05 / SQUARESIZE}

    SCORE = {
        "left_player": pygame.ftfont.Font(
            "fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3)
        ),
        "right_player": pygame.ftfont.Font(
            "fonts/Barlow-Bold.otf", int((SQUARESIZE / 4) * 2.9)
        ),
    }
    NUMBERS = pygame.ftfont.Font(
        "fonts/WDRSansUL-ExtraBold.otf", int((SQUARESIZE / 4) * 3)
    )
    GAME_END = SCORE
    COUNTDOWN = {
        "left_player": pygame.ftfont.Font(
            "fonts/WDRSansUL-ExtraBold.otf", int(SQUARESIZE * 1.5)
        ),
        "right_player": pygame.ftfont.Font(
            "fonts/Barlow-Bold.otf", int(SQUARESIZE * 1.5)
        ),
    }
    STATUS = {
        "left_player": pygame.ftfont.Font(
            "fonts/WDRSans-Bold.otf", int((SQUARESIZE / 5) * 3)
        ),
        "right_player": pygame.ftfont.Font(
            "fonts/Barlow-Bold.otf", int((SQUARESIZE / 5) * 3)
        ),
    }
    STATUS_LARGE = {
        "left_player": pygame.ftfont.Font(
            "fonts/WDRSansUL-ExtraBold.otf",
            int(
                (SQUARESIZE / 4)
                * 5
                * (5 / len(config["players"]["left_player"]["name"]))
            ),
        ),
        "right_player": pygame.ftfont.Font(
            "fonts/Barlow-Bold.otf",
            int(
                (SQUARESIZE / 4)
                * 5
                * (5 / len(config["players"]["right_player"]["name"]))
            ),
        ),
    }


class Images:
    LOGOS = {
        player: pygame.image.load(f"images/logo_{player}.png").convert_alpha()
        for player in config["players"]
    }
    SCORE_LOGOS = {
        player: pygame.transform.smoothscale(
            surf, (int(surf.get_width() * SQUARESIZE / surf.get_height()), SQUARESIZE)
        )
        for player, surf in LOGOS.items()
    }
    STATUS_LOGOS = {
        player: pygame.transform.smoothscale(
            surf,
            (
                int(4 * SQUARESIZE),
                int(surf.get_height() * 4 * SQUARESIZE / surf.get_width()),
            ),
        )
        for player, surf in LOGOS.items()
    }


class Positions:
    SCORE_HEIGHT = 1.0
    CURRENT_PLAYER_LEFT_PLAYER_LEFT = 0.25
    CURRENT_PLAYER_RIGHT_PLAYER_LEFT = 11.75
    CURRENT_PLAYER = SquareRect(0, BOARD_OFFSET_Y - 1, 4, 3)
    GAME_END = SquareRect(0, 1, 16, 1)
    CURRENT_VOTE = SquareRect(BOARD_OFFSET_X, 1, game.COLUMN_COUNT, 1)
    COUNTDOWN = SquareRect(0, 6, 4, 2)


class Align(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


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
        height_offset_umlaut = font.get_ascent() - max(
            *[metric[3] for metric in font.metrics(text)]
        )

    height_offset_umlaut = min(0, height_offset_umlaut)

    text_rect = drawn_text.get_rect(
        center=(rect.left + int(rect.width / 2), rect.top + int(rect.height / 2))
    )
    text_rect.top += height_offset_umlaut / 2

    if align is Align.LEFT:
        text_rect.left = rect.left
    if align is Align.RIGHT:
        text_rect.right = rect.right

    screen.blit(drawn_text, text_rect)

    return SquareRect.from_rect(text_rect, SQUARESIZE)


def draw_hack_text(text, color, font, square_rect, align=Align.CENTER):
    """
    We need this for the WDRSansUL font, because that is the only font with correct numbers,
    but also has weird underlines baked into the font.
    So we draw the text and then erase the underline as a hack.
    """
    text_rect = draw_text(text, color, font, square_rect, align=align)
    erase_rect = text_rect.copy()
    erase_rect.top = erase_rect.bottom - 0.11 * text_rect.height
    erase_rect.height = 0.07 * text_rect.height
    erase_rect.left -= 0.05 * text_rect.height
    erase_rect.width += 0.1 * text_rect.height
    draw_erase(erase_rect)
    return text_rect


def draw_piece(left, top, color, scale=1):
    pygame.gfxdraw.filled_circle(
        screen,
        int(left * SQUARESIZE) + HALF_SQUARE,
        int(top * SQUARESIZE) + HALF_SQUARE,
        int(RADIUS * scale),
        color,
    )
    for _ in range(2):
        pygame.gfxdraw.aacircle(
            screen,
            int(left * SQUARESIZE) + HALF_SQUARE,
            int(top * SQUARESIZE) + HALF_SQUARE,
            int(RADIUS * scale),
            color,
        )


def draw_image(source, rect, vertical_align="top", horizontal_align="left"):
    draw_erase(rect)

    rect = rect.get_rect(SQUARESIZE)

    if vertical_align == "center":
        rect.top += int((rect.height - source.get_height()) / 2)
    elif vertical_align == "bottom":
        rect.top += int(rect.height - source.get_height())

    if horizontal_align == "center":
        rect.left += int((rect.width - source.get_width()) / 2)
    elif horizontal_align == "right":
        rect.left += int(rect.width - source.get_width())

    return SquareRect.from_rect(screen.blit(source, rect), SQUARESIZE,)


def draw_board():
    flipped_board = np.flip(game.board, 0)

    for c in range(game.COLUMN_COUNT):
        for r in range(game.ROW_COUNT):
            left = c + BOARD_OFFSET_X
            top = r + BOARD_OFFSET_Y

            pygame.draw.rect(
                screen,
                COLOR_BOARD,
                (int(left * SQUARESIZE), int(top * SQUARESIZE), SQUARESIZE, SQUARESIZE),
            )

            if flipped_board[r][c] == 1:
                draw_piece(left, top, COLOR_LEFT_PLAYER)

            elif flipped_board[r][c] == 2:
                draw_piece(left, top, COLOR_RIGHT_PLAYER)

            else:
                draw_piece(left, top, BLACK)


def draw_current_vote(vote, turn):
    color = config["players"][turn]["color"]

    left = BOARD_OFFSET_X + vote
    top = Positions.CURRENT_VOTE.top

    draw_erase(Positions.CURRENT_VOTE)
    draw_piece(left, top, color)


def draw_column_labels():
    for c in range(game.COLUMN_COUNT):
        square_rect = SquareRect(BOARD_OFFSET_X + c, BOARD_OFFSET_Y - 0.8, 1, 0.8,)
        draw_hack_text(str(c + 1), COLOR_BOARD, Fonts.NUMBERS, square_rect)


def draw_game_end(turn, tie=False):
    if tie:
        color = COLOR_BOARD
        text = "Unentschieden!".upper()
    else:
        color = config["players"][turn]["color"]
        text = f"{config['players'][turn]['name']} gewinnt!".upper()

    draw_hack_text(text, color, Fonts.GAME_END[turn], Positions.GAME_END)


def draw_current_player(turn):
    color = config["players"][turn]["color"]
    text = config["players"][turn]["name"]

    if turn == "left_player":
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

    square_rect_logo = Positions.CURRENT_PLAYER.copy()
    square_rect_logo.left = text_left

    square_rect_erase = Positions.CURRENT_PLAYER.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    draw_image(Images.STATUS_LOGOS[turn], square_rect_logo, vertical_align="center")

    font = Fonts.STATUS[turn]
    font_voffset = font.get_height() * Fonts.VOFFSET[turn]

    square_rect_text = square_rect_logo.copy()

    square_rect_text.height = 1
    square_rect_erase.height = 1
    square_rect_text.top += 3 + font_voffset
    square_rect_erase.top += 3
    draw_erase(square_rect_erase)
    draw_text("ist dran", color, font, square_rect_text)


def draw_countdown(turn, time_left, no_votes_message):
    color = config["players"][turn]["color"]

    if turn == "left_player":
        text_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
    else:
        text_left = Positions.CURRENT_PLAYER_RIGHT_PLAYER_LEFT
        erase_left = Positions.CURRENT_PLAYER_LEFT_PLAYER_LEFT

    font = Fonts.COUNTDOWN[turn]
    font_voffset = font.get_height() * Fonts.VOFFSET[turn]

    square_rect_text = Positions.COUNTDOWN.copy()
    square_rect_text.left = text_left
    square_rect_text.top += font_voffset

    square_rect_erase = Positions.COUNTDOWN.copy()
    square_rect_erase.left = erase_left

    draw_erase(square_rect_erase)
    square_rect_countdown = draw_text(str(time_left), color, font, square_rect_text)
    square_rect_countdown.top = square_rect_countdown.bottom - 0.15
    square_rect_countdown.height = 0.1
    draw_erase(square_rect_countdown)

    # No votes text
    font = Fonts.STATUS[turn]
    font_voffset = font.get_height() * Fonts.VOFFSET[turn]

    square_rect_text.top = 8 + font_voffset
    square_rect_text.height = 1
    draw_erase(square_rect_text, color=BLACK)

    if no_votes_message:
        draw_text("Keine Votes!", color, font, square_rect_text)


def draw_scoreboard(score):
    player = "left_player"
    font = Fonts.SCORE[player]
    font_voffset = font.get_height() * Fonts.VOFFSET[player]
    font_hoffset = font.get_height() * Fonts.HOFFSET[player]

    colon_rect = SquareRect(7.85, font_voffset, 0.3, Positions.SCORE_HEIGHT)
    draw_hack_text(":", COLOR_BOARD, font, colon_rect)

    left_player_rect = SquareRect(
        0, font_voffset, colon_rect.left, Positions.SCORE_HEIGHT,
    )
    left_player_rect.right = colon_rect.left - font_hoffset
    left_text_rect = draw_hack_text(
        f"{config['players'][player]['name']} {score[player]}",
        COLOR_LEFT_PLAYER,
        Fonts.SCORE[player],
        left_player_rect,
        align=Align.RIGHT,
    )
    draw_piece(left_text_rect.left - 1, 0, COLOR_LEFT_PLAYER, scale=0.75)

    player = "right_player"
    font = Fonts.SCORE[player]
    font_voffset = font.get_height() * Fonts.VOFFSET[player]
    font_hoffset = font.get_height() * Fonts.HOFFSET[player]
    right_player_rect = SquareRect(
        colon_rect.right + 0.01 + font_hoffset,
        font_voffset,
        colon_rect.left,
        Positions.SCORE_HEIGHT,
    )
    right_text_rect = draw_hack_text(
        f"{score[player]} {config['players'][player]['name']}",
        COLOR_RIGHT_PLAYER,
        font,
        right_player_rect,
        align=Align.LEFT,
    )
    draw_piece(right_text_rect.right, 0, COLOR_RIGHT_PLAYER, scale=0.75)
