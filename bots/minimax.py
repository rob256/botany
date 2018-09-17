import random

from botany_connectfour import game


def copy_board(board):
    return [x[:] for x in board]


def get_board_value(board, player):
    winner = game.check_winner(board)
    if winner is None:
        return 0
    elif winner == player:
        return float('inf')
    else:
        return float('-inf')


def get_next_move(board, token):
    available_moves = game.available_moves(board)
    preferred_locaitons = [3, 2, 4, 1, 5, 0, 6]

    best_value = float('-inf')
    best_move = random.choice(available_moves)

    other_token = 'X' if token == 'O' else 'O'

    for move in available_moves:
        new_board = copy_board(board)
        game.make_move(new_board, move, token)
        if game.check_winner(new_board):
            return move

    for move in available_moves:
        new_board = copy_board(board)
        game.make_move(new_board, move, other_token)
        if game.check_winner(new_board):
            return move

    for move in preferred_locaitons:
        if move not in available_moves:
            continue
        return move

        # move_value = minimax(new_board, 0, False, token, other_token)
        # if move_value > best_value:
        #     best_move = move

    return best_move


def minimax(board, depth, maxplayer, token, other_token):
    if depth == 0:
        return get_board_value(board, token)
    if maxplayer:
        value = float('-inf')
        for move in game.available_moves(board):
            new_board = copy_board(board)
            game.make_move(new_board, move, token)
            if game.check_winner(new_board):
                return float('inf')
            value = max(value, minimax(new_board, depth - 1, False, token, other_token))
        return value
    else:
        value = float('inf')
        for move in game.available_moves(board):
            new_board = copy_board(board)
            game.make_move(new_board, move, other_token)
            if game.check_winner(new_board):
                return float('-inf')
            value = min(value, minimax(new_board, depth - 1, True, token, other_token))
        return value


