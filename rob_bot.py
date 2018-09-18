import random
from botany_connectfour import game
from botany_core.tracer import get_opcode_count

import re


def test_make_board_from_string():
    board_string = """.	.	.	.	.	.	.
.	.	.	.	.	.	.
.	X	.	.	X	.	.
.	O	X	X	O	.	.
X	O	O	O	X	.	.
X	O	X	O	O	X	."""
    return make_board_from_string(board_string)


def make_test_board1():
    board_string = """.	.	.	.	.	.	.
.	.	.	.	.	.	.
.	.	.	X	O	.	.
.	.	.	O	O	.	.
.	.	.	X	X	.	.
.	.	.	X	O	.	."""
    return make_board_from_string(board_string)


def make_test_board2():
    board_string = """.	.	.	.	.	.	.
.	.	.	X	.	.	.
.	.	.	X	O	.	.
.	.	.	O	O	.	.
.	.	.	X	X	.	.
.	O	.	X	O	.	."""
    return make_board_from_string(board_string)


def make_test_board3():
    board_string = """.	.	.	.	.	.	.
.	.	.	.	.	.	.
.	.	.	O	.	.	.
.	.	.	O	.	.	.
.	.	.	X	X	.	.
.	.	O	X	X	X	O"""
    return make_board_from_string(board_string)


def make_test_board4():
    board_string = """. . . . . . .
. . . . . . .
. . . O . . .
. . X X . . .
. . X O O . .
. . O X X . ."""
    return make_board_from_string(board_string)


def make_test_board5():
    board_string = """.	.	.	X	X	O	.
.	.	.	O	X	O	.
X	X	.	X	O	X	.
O	O	.	X	X	X	.
O	X	.	O	X	O	.
O	O	X	X	O	O	."""
    return make_board_from_string(board_string)


def make_test_board6():
    board_string = """. . . X . . .
. . O X X . .
. . O O O . .
. . X X O . .
. O X O O X .
X X O X X O ."""
    return make_board_from_string(board_string)


def make_test_board7():
    board_string = """.	.	.	.	.	.	.
.	.	.	.	.	.	.
.	.	O	X	.	.	.
.	.	O	O	.	.	.
.	.	X	X	.	.	.
.	.	O	X	.	X	."""
    return make_board_from_string(board_string)


def make_string_from_board(board):
    return 'T'.join(''.join(x) for x in board)


def make_board_from_string(board_string):
    board = game.new_board()
    for i, line in enumerate(board_string.split('\n')):
        line = line.replace(' ', '')
        line = line.replace('\t', '')
        for j, char in enumerate(line):
            if j == 7:
                break
            board[j][5 - i] = char
    return board


def check_winner_regex(long_board_string, token, r=None):
    if r is None:
        if token == "X":
            r = re.compile(r'XXXX|X.{6}X.{6}X.{6}X|X.{7}X.{7}X.{7}X|X.{8}X.{8}X.{8}X')
        else:
            r = re.compile(r'OOOO|O.{6}O.{6}O.{6}O|O.{7}O.{7}O.{7}O|O.{8}O.{8}O.{8}O')
    return r.search(long_board_string)


def check_winner(board, move, position, ignore_vertical=False):
    token = board[move][position]

    # Horizontal
    total_count = 1
    x = move
    while True:
        x -= 1
        if x < 0 or board[x][position] != token:
            break
        total_count += 1
    x = move
    while True:
        x += 1
        if x > 6 or board[x][position] != token:
            break
        total_count += 1
    if total_count >= 4:
        return True

    # Vertical
    if not ignore_vertical:
        total_count = 1
        y = position
        while True:
            y -= 1
            if y < 0 or board[move][y] != token:
                break
            total_count += 1
        y = position
        if total_count >= 4:
            return True

    # Diag 1
    total_count = 1
    x = move
    y = position
    while True:
        x -= 1
        y -= 1
        if y < 0 or x < 0 or board[x][y] != token:
            break
        total_count += 1
    x = move
    y = position
    while True:
        y += 1
        x += 1
        if y > 5 or x > 6 or board[x][y] != token:
            break
        total_count += 1
    if total_count >= 4:
        return True

    # Diag 2
    total_count = 1
    x = move
    y = position
    while True:
        x += 1
        y -= 1
        if y < 0 or x > 6 or board[x][y] != token:
            break
        total_count += 1
    x = move
    y = position
    while True:
        x -= 1
        y += 1
        if y > 5 or x < 0 or board[x][y] != token:
            break
        total_count += 1
    if total_count >= 4:
        return True

    return False


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
        if column == 3:
            columns_with_space.append(column)
            continue
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


def get_board_columns_used(board):
    all_columns = [0, 0, 0, 0, 0, 0, 0]
    for x in range(7):
        board_column = board[x]
        for y in range(6):
            if board_column[y] == '.':
                all_columns[x] = y
                break
            all_columns[x] = 6
    return all_columns


def board_walk(board, board_columns, move, token):
    board[move][board_columns[move]] = token
    board_columns[move] += 1


def board_unwalk(board, board_columns, move):
    board_columns[move] -= 1
    board[move][board_columns[move]] = '.'


def get_next_move(board, token):

    test_board = test_make_board_from_string()

    print(f'Before check_winner:{get_opcode_count()}')
    game.check_winner(test_board)
    print(f'After check_winner:{get_opcode_count()}')

    board_columns_used = get_board_columns_used(board)

    print(f'Before available moves:{get_opcode_count()}')
    all_available_moves = game.available_moves(board)
    print(f'After available moves:{get_opcode_count()}')

    preferred_locations = [3, 2, 4, 1, 5, 0, 6]

    print(f'Before preferred locations:{get_opcode_count()}')
    priority_locations = get_columns_with_space(board, token, preferred_locations)
    print(f'After preferred locations:{get_opcode_count()}')

    losing_locations = set()
    # if state is None:
    #     state = {'opening_trap': False}

    print(f'Before board walk: {get_opcode_count()}')
    board[3][board_columns_used[3]] = token
    board[3][board_columns_used[3]] = '.'
    print(f'After board walk: {get_opcode_count()}')


    new_board = game.new_board()
    new_board[0][0] = 'X'
    new_board[1][1] = 'X'
    new_board[2][2] = 'X'
    new_board[3][3] = 'X'

    print(f'Before game.check_winner:{get_opcode_count()}')
    game.check_winner(new_board)
    print(f'After game.check_winner:{get_opcode_count()}')

    print(f'Before check_winner:{get_opcode_count()}')
    check_winner(board, 3, 3)
    print(f'After check_winner:{get_opcode_count()}')

    rO = re.compile(r'OOOO|O.{6}O.{6}O.{6}O|O.{7}O.{7}O.{7}O|O.{8}O.{8}O.{8}O')
    rX = re.compile(r'XXXX|X.{6}X.{6}X.{6}X|X.{7}X.{7}X.{7}X|X.{8}X.{8}X.{8}X')
    board_string = make_string_from_board(board)
    print(f'Before check_winner_regex:{get_opcode_count()}')
    board_string = board_string[:2 * 7 + 2] + 'X' + board_string[2 * 7 + 2:]
    check_winner_regex(board_string, 'X', r=rX)
    print(f'After check_winner_regex:{get_opcode_count()}')

    moves_played = get_moves_played(board)

    # best_value = float('-inf')
    # best_move = random.choice(available_moves)

    other_token = 'X' if token == 'O' else 'O'

    for move in all_available_moves:
        board[move][board_columns_used[move]] = token
        if check_winner(board, move, board_columns_used[move]):
            return move
        board[move][board_columns_used[move]] = '.'

    print(get_opcode_count())

    for move in all_available_moves:
        board[move][board_columns_used[move]] = other_token
        if check_winner(board, move, board_columns_used[move]):
            return move
        board[move][board_columns_used[move]] = '.'

    print(get_opcode_count())

    available_moves = set(all_available_moves)

    for move in all_available_moves:
        if board_columns_used[move] > 4:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = other_token

        if check_winner(board, move, board_columns_used[move] + 1):
            losing_locations.add(move)

        board[move][board_columns_used[move]] = '.'
        board[move][board_columns_used[move] + 1] = '.'

    print(get_opcode_count())

    skip_moves = set()

    for move in all_available_moves:
        if board_columns_used[move] > 4:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = token

        if check_winner(board, move, board_columns_used[move] + 1, ignore_vertical=True):
            skip_moves.add(move)

        board[move][board_columns_used[move]] = '.'
        board[move][board_columns_used[move] + 1] = '.'

    # for move in all_available_moves:
    #     board[move][board_columns_used[move]] = token
    #     if move_makes_opportunity(board, move, board_columns_used[move], token):
    #         return move


    print(get_opcode_count())

    if moves_played == 1:
        # Don't go on top of the previous player
        losing_locations.add(find_enemy_location(board, other_token))

    if moves_played == 2:
        if board[3][1] == other_token:
            return 2

    if moves_played == 4:
        if board[3][1] == other_token and board[1][0] == '.' and board[4][0] == '.':
            return 4

    priority_locations = [x for x in priority_locations if x not in skip_moves]

    for move in priority_locations:
        if move in losing_locations:
            continue
        return move

    for move in preferred_locations:
        if move in losing_locations:
            continue
        return move

    return random.choice(all_available_moves)

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


