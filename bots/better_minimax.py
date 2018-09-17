# This is just a lightly better implementation over minimax.py. It
# checks to see where the enemy placed its first piece and places
# a piece somewhere else.

from botany_connectfour import game


def copy_board(board):
    return [x[:] for x in board]


def get_moves_played(board, max_move=10):
    number_of_moves = 0
    for column in board:
        for row in column:
            if row == '.':
                break
            else:
                number_of_moves += 1
        if number_of_moves >= max_move:
            return number_of_moves
    return number_of_moves


def find_enemy_location(board, enemy_token):
    for i, column in enumerate(board):
        if column[0] == enemy_token:
            return i


# def get_board_value(board, player):
#     winner = game.check_winner(board)
#     if winner is None:
#         return 0
#     elif winner == player:
#         return float('inf')
#     else:
#         return float('-inf')


def get_columns_with_space(board, token, preferred_locations):
    columns_with_space = []
    for column in preferred_locations:
        space_count = 0
        board_column = board[column]
        for row in board_column[::-1]:
            if row == '.' or row == token:
                space_count += 1
            else:
                break
        if space_count >= 4:
            columns_with_space.append(column)
    return columns_with_space


def get_next_move(board, token):
    available_moves = game.available_moves(board)
    preferred_locations = [3, 2, 4, 1, 5, 0, 6]
    priority_locations = get_columns_with_space(board, token, preferred_locations)
    avoid_locations = []

    moves_played = get_moves_played(board)

    # best_value = float('-inf')
    # best_move = random.choice(available_moves)

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

    if moves_played == 1:
        # Don't go on top of the previous player
        avoid_locations.append(find_enemy_location(board, other_token))

    for move in priority_locations:
        if move not in available_moves or move in avoid_locations:
            continue
        return move

    for move in preferred_locations:
        if move not in available_moves or move in avoid_locations:
            continue
        return move

        # move_value = minimax(new_board, 0, False, token, other_token)
        # if move_value > best_value:
        #     best_move = move

    # return best_move


# def minimax(board, depth, maxplayer, token, other_token):
#     if depth == 0:
#         return get_board_value(board, token)
#     if maxplayer:
#         value = float('-inf')
#         for move in game.available_moves(board):
#             new_board = copy_board(board)
#             game.make_move(new_board, move, token)
#             if game.check_winner(new_board):
#                 return float('inf')
#             value = max(value, minimax(new_board, depth - 1, False, token, other_token))
#         return value
#     else:
#         value = float('inf')
#         for move in game.available_moves(board):
#             new_board = copy_board(board)
#             game.make_move(new_board, move, other_token)
#             if game.check_winner(new_board):
#                 return float('-inf')
#             value = min(value, minimax(new_board, depth - 1, True, token, other_token))
#         return value


