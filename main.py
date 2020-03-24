import math
import sys

import pygame

pygame.init()

import game_logic as game
import ui

MAX_TURNS = game.ROW_COUNT * game.COLUMN_COUNT
wins = {
    1: 0,
    2: 0,
}

game_over = False
turn = 0
turn_count = 0


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

        if game.is_valid_location(col):
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, player_number)

            if game.winning_move(player_number):
                ui.draw_game_end(turn)
                wins[player_number] += 1
                game_over = True
            elif turn_count == MAX_TURNS - 1:
                ui.draw_game_end(turn, tie=True)
                game_over = True

            game.print_board()
            ui.draw_board()

            pygame.display.update()

            turn += 1
            turn = turn % 2
            turn_count += 1


pink_first = False

while True:
    game.create_board()
    game.print_board()

    ui.draw_board()
    ui.draw_column_labels()
    pygame.display.update()

    pink_first = not pink_first
    game_over = False
    turn = 0 if pink_first else 1
    turn_count = 0

    while not game_over:

        ui.draw_current_player(turn)

        pygame.display.update()

        for event in pygame.event.get():

            game_loop(event)

            if game_over:
                pygame.time.wait(3000)
                ui.draw_erase(ui.Positions.GAME_END)