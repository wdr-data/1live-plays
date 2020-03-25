import math
import sys
import os
import json
from queue import Queue

import pygame

pygame.init()

import game_logic as game
import ui
from bot import Bot, Event

DEBUG = os.environ.get('DEBUG', False)
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

        game.print_board()
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

    print('Connecting bots...')
    queue = Queue()
    bots = {}
    for bot_name, bot_config in config.items():
        video_id = input(f'Please enter video ID for bot "{bot_name}": ')
        bots[bot_name] = Bot(bot_name, bot_config, video_id, queue)

    for bot in bots.values():
        bot.start_polling()

while True:
    game.create_board()
    game.print_board()

    ui.draw_board()
    ui.draw_column_labels()
    pygame.display.update()

    pink_first = not pink_first
    game_over = False
    turn = 'pink' if pink_first else 'white'
    turn_count = 0

    while not game_over:

        ui.draw_current_player(turn)

        pygame.display.update()

        for event in queue.get():
            game_loop(event)
            if game_over:
                break
