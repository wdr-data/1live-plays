import math
import sys
import os
import json
from time import time, sleep
from enum import Enum
from queue import Queue

import pygame

pygame.init()

import game_logic as game
import ui
from bot import Bot, Event, DemocracyMode

class GameModes(Enum):
    DEMOCRACY = 'democracy'
    FIRST_COME_FIRST_SERVE = 'first_come_first_serve'

DEBUG = False
MODE = GameModes.DEMOCRACY
DEMOCRACY_TIMEOUT = 15

MAX_TURNS = game.ROW_COUNT * game.COLUMN_COUNT

score = {
    1: 0,
    2: 0,
}

game_over = False
turn = 'pink'
turn_count = 0

def get_current_player_number():
    global turn
    return 1 if turn == 'pink' else 2

def switch_turn():
    global turn
    turn = 'pink' if turn == 'white' else 'white'

def game_loop(event):
    global turn, turn_count, game_over

    if DEBUG:
        # Programm Exit
        number_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key in number_keys:
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

        else:
            return
    else:
        if event.bot.name != turn:
            return
        col = event.column

    player_number = get_current_player_number()

    if game.is_valid_location(col):
        row = game.get_next_open_row(col)
        game.drop_piece(row, col, player_number)

        if game.winning_move(player_number):
            score[player_number] += 1
            ui.draw_game_end(turn)
            ui.draw_scoreboard(score)
            game_over = True
        elif turn_count == MAX_TURNS - 1:
            ui.draw_game_end(turn, tie=True)
            game_over = True

        ui.draw_board()

        pygame.display.update()

        switch_turn()
        turn_count += 1

    if game_over:
        pygame.time.wait(3000)
        ui.draw_erase(ui.Positions.GAME_END)


pink_first = False
ui.draw_scoreboard(score)

if DEBUG:
    queue = pygame.event
else:
    print('Loading config...')
    try:
        with open('config.json', 'r') as fp:
            config = json.load(fp)
    except FileNotFoundError:
        print('Config file "config.json" not found.')
        sys.exit(1)

    print(f'Starting gamemode "{MODE.value}"...')

    if MODE is GameModes.FIRST_COME_FIRST_SERVE:
        print('Connecting bots...')
        queue = Queue()
        bots = {}
        for bot_name, bot_config in config.items():
            bots[bot_name] = Bot(bot_name, bot_config, queue)

        for bot in bots.values():
            bot.start_polling()
    elif MODE is GameModes.DEMOCRACY:
        print('Connecting bots...')

        democracies = {}
        for bot_name, bot_config in config.items():
            bot = Bot(bot_name, bot_config)
            democracies[bot_name] = DemocracyMode(bot)

        for democracy in democracies.values():
            democracy.start()

def mode_first_come_first_serve():
    global queue
    for event in queue.get():
        game_loop(event)
        if game_over:
            break

def mode_democracy():
    global turn, democracies, no_votes

    valid_locations = game.get_valid_locations()
    democracy = democracies[turn]
    democracy.reset_votes()

    for time_left in range(DEMOCRACY_TIMEOUT, -1, -1):
        current_vote = democracy.get_vote(valid_locations)

        if current_vote is not None:
            ui.draw_current_vote(current_vote, turn)

        ui.draw_countdown(turn, time_left, no_votes and time_left + 1 >= DEMOCRACY_TIMEOUT)
        pygame.display.update()
        if time_left:
            sleep(1)

    column = democracy.get_vote(valid_locations, reset=True)

    if column is None:
        no_votes = True
        return

    no_votes = False
    event = Event(democracy.bot, column)
    game_loop(event)
    ui.draw_erase(ui.Positions.CURRENT_VOTE)

while True:
    game.create_board()

    ui.draw_board()
    ui.draw_column_labels()
    pygame.display.update()

    pink_first = not pink_first
    game_over = False
    turn = 'pink' if pink_first else 'white'
    turn_count = 0
    no_votes = False

    while not game_over:

        ui.draw_current_player(turn)

        pygame.display.update()

        if MODE is GameModes.FIRST_COME_FIRST_SERVE:
            mode_first_come_first_serve()
        elif MODE is GameModes.DEMOCRACY:
            mode_democracy()
