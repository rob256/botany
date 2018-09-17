# This is just random bot. Nothing smart.

import random

from botany_connectfour import game


def get_next_move(board, token):
    return random.choice(game.available_moves(board))
