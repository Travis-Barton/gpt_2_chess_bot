import pandas as pd
import numpy as np
import chess
import gpt_2_simple as gpt2
import random
import os
from chessboard import display
import sys
import argparse

# os.chdir('/Users/biscuit/Documents/GitHub/Personal-Projects/speed_test')
# os.chdir('/home/tbarton/machine_learning_scripts/speed_test')
RUN_NAME = 'new_run_large'
MODEL_NAME = None
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name=RUN_NAME)

chess_chrs = {
    'b_checker': u'\u25FB',
    'p': u'\u265F',
    'r': u'\u265C',
    'n': u'\u265E',
    'b': u'\u265D',
    'k': u'\u265A',
    'q': u'\u265B',
    'w_checker': u'\u25FC',
    'P': u'\u2659',
    'R': u'\u2656',
    'N': u'\u2658',
    'B': u'\u2657',
    'K': u'\u2654',
    'Q': u'\u2655'
}


def lets_play_chess(player_color='white', previous_moves=None, fancy_display=False):
    if player_color == 'white':
        player_color = True
    elif player_color == 'black':
        player_color = False
    else:
        player_color = None
    if fancy_display:
        display.start()
    board = chess.Board()
    game_so_far = '<#endofdoc#>'
    tries = 0
    turn_counter = 1
    while not board.is_game_over():
        if board.turn and game_so_far[-1] != '.':
            game_so_far += f' {board.fullmove_number}.'
        if board.turn == player_color:
            proposed_move = input(f'{"White" if player_color else "Black"}\'s turn: ')
            try:
                move_san = board.parse_san(proposed_move)
            except:
                print('that is not a legal move. Try again')
                continue
            if board.is_legal(move_san):
                board.push_san(proposed_move)
                game_so_far += ' ' + str(proposed_move)
                print(board.unicode(borders=True, empty_square=' '))
                if fancy_display:
                    display.update(board.fen())

            else:
                print('that is not a legal move. Try again')
                continue
        else:
            proposed_move, tries = predict_next_move(game_so_far, tries)
            try:
                move_san = board.parse_san(proposed_move)
                board.push_san(proposed_move)
                game_so_far += ' ' + str(proposed_move)
                print(f'The computer succeeded on attempt number {tries} to make a legal move.')
                print(board.unicode(borders=True, empty_square=' '))
                if fancy_display:
                    display.update(board.fen())

                tries = 0
            except:
                print(f'try #{tries}: {proposed_move}')
                if tries > 10:
                    print('Looks like I need a little help... lets move randomly and move on')
                    random_moves = random.sample(board.legal_moves.__str__().split(' ')[3:], 1)[0]
                    random_moves = random_moves.replace('(', '').replace(')', '').replace('>', '').replace(',', '')
                    board.push_san(random_moves)
                    game_so_far += ' ' + str(proposed_move)
                    print(board.unicode(borders=True, empty_square=' '))
                    if fancy_display:
                        display.update(board.fen())
                    tries = 0
                else:
                    continue
            # if board.is_legal(move_san):
            #
            # else:

        print(game_so_far)
        if fancy_display:
            display.checkForQuit()
    print(f'the game is over! congrats to {"white" if board.result() == "1-0" else "black" if board.result() == "0-1" else "both on the tie"}')
    if fancy_display:
        display.terminate()

def predict_next_move(game_so_far, tries=0):
    if tries > 0:
        temperature = .7 + .7**(10/tries)
    else:
        temperature = .7
    single_text = gpt2.generate(sess, prefix=game_so_far, return_as_list=True, run_name=RUN_NAME,
                                model_name=MODEL_NAME, temperature=temperature, length=100)[0]
    tries += 1
    return_text = single_text[len(game_so_far):].split(' ')
    if return_text[0] == '':
        return str(return_text[1]), tries
    else:
        return str(return_text[1]), tries


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('--player_color', action="store")
        parser.add_argument('--previous_moves', action="store")
        parser.add_argument('--fancy_display', action='store')
        args = parser.parse_args()
        lets_play_chess(player_color=args.player_color, previous_moves=args.previous_moves,
                        fancy_display=args.fancy_display)
    else:
        lets_play_chess()
