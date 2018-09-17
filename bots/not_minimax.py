import random
from botany_connectfour import game
from botany_core.tracer import get_opcode_count


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


def get_next_move(board, token, state):
    board_columns_used = get_board_columns_used(board)
    available_moves = game.available_moves(board)
    preferred_locations = [3, 2, 4, 1, 5, 0, 6]
    priority_locations = get_columns_with_space(board, token, preferred_locations)
    losing_locations = set()

    if state is None:
        state = {'opening_trap': False}

    moves_played = get_moves_played(board)

    other_token = 'X' if token == 'O' else 'O'

    for move in available_moves:
        board[move][board_columns_used[move]] = token
        if check_winner(board, move, board_columns_used[move]):
            return move, state
        board[move][board_columns_used[move]] = '.'

    for move in available_moves:
        board[move][board_columns_used[move]] = other_token
        if check_winner(board, move, board_columns_used[move]):
            return move, state
        board[move][board_columns_used[move]] = '.'

    for move in available_moves:
        if board_columns_used[move] > 4:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = other_token

        if check_winner(board, move, board_columns_used[move] + 1):
            losing_locations.add(move)

        board[move][board_columns_used[move]] = '.'
        board[move][board_columns_used[move] + 1] = '.'

    skip_moves = set()

    for move in available_moves:
        if board_columns_used[move] > 4:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = token

        if check_winner(board, move, board_columns_used[move] + 1, ignore_vertical=True):
            skip_moves.add(move)

        board[move][board_columns_used[move]] = '.'
        board[move][board_columns_used[move] + 1] = '.'

    print(get_opcode_count())

    if moves_played == 1:
        # Don't go on top of the previous player
        losing_locations.add(find_enemy_location(board, other_token))

    if moves_played == 2:
        if board[3][1] == other_token:
            state['opening_trap'] = True
            return 2, state

    if moves_played == 4:
        if state['opening_trap']:
            if board[1][0] == '.' and board[4][0] == '.':
                return 4, state

    for move in priority_locations:
        if move not in available_moves or move in losing_locations or move in skip_moves:
            continue
        return move, state

    for move in preferred_locations:
        if move not in available_moves or move in losing_locations or move in skip_moves:
            continue
        return move, state

    for move in priority_locations:
        if move not in available_moves or move in losing_locations:
            continue
        return move, state

    for move in preferred_locations:
        if move not in available_moves or move in losing_locations:
            continue
        return move, state

    return random.choice(available_moves), state
