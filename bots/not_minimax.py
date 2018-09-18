from collections import defaultdict
from operator import itemgetter
import random

from botany_connectfour import game
from botany_core.tracer import get_opcode_count, get_opcode_limit


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


def can_make_4_horizontal(board, move_x, move_y, token):
    total = 1
    x = move_x
    while True:
        x += 1
        if x < 7 and (board[x][move_y] == token or board[x][move_y] == '.'):
            total += 1
        else:
            break
    x = move_x
    while True:
        x -= 1
        if x >= 0 and (board[x][move_y] == token or board[x][move_y] == '.'):
            total += 1
        else:
            break
    return total >= 4


def get_friendly_neighbours(board, move_x, move_y, token):
    total_neighbours = 0
    for delta_x in [-1, 0, 1]:
        x = move_x + delta_x
        if x < 0 or x > 6:
            continue
        for delta_y in [-1, 0, 1]:
            y = move_y + delta_y
            if y < 0 or y > 5:
                continue
            if board[x][y] == token:
                total_neighbours += 1
    return total_neighbours


def move_makes_3_horizontal_with_spaces(board, move_x, move_y, token, check_for_immediate_risk=True):
    left = move_x
    right = move_x
    x = move_x
    while True:
        x -= 1
        if x < 0 or board[x][move_y] != token:
            break
        left = x
    x = move_x
    while True:
        x += 1
        if x > 6 or board[x][move_y] != token:
            break
        right = x

    if right - left < 2 or left == 0 or right == 6:
        return False

    if check_for_immediate_risk:
        if board[left - 1][move_y] == '.' and board[right + 1][move_y] == '.':
            if move_y > 0:
                if board[left - 1][move_y - 1] != '.' and board[right + 1][move_y - 1] != '.':
                    return True
                else:
                    return False
            return True
    else:
        return True


def move_opens_opportunities(board, move_x, move_y, token):
    total_opportunities_count = 0

    # Check left
    count = 0
    if move_x > 2:
        for delta_x in [-1, -2, -3]:
            target = board[move_x + delta_x][move_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    # Check right
    count = 0
    if move_x < 4:
        for delta_x in [1, 2, 3]:
            target = board[move_x + delta_x][move_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    # Check diag-down-left
    count = 0
    if move_x > 2 and move_y > 2:
        for delta in [-1, -2, -3]:
            delta_x = delta
            delta_y = delta
            target = board[move_x + delta_x][move_y + delta_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    # Check diag-up-left
    count = 0
    if move_x > 2 and move_y < 3:
        for delta in [-1, -2, -3]:
            delta_x = delta
            delta_y = -delta
            target = board[move_x + delta_x][move_y + delta_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    # Check diag-down-right
    count = 0
    if move_x < 4 and move_y > 2:
        for delta in [1, 2, 3]:
            delta_x = delta
            delta_y = -delta
            target = board[move_x + delta_x][move_y + delta_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    # Check diag-up-right
    count = 0
    if move_x < 4 and move_y < 3:
        for delta in [1, 2, 3]:
            delta_x = delta
            delta_y = delta
            target = board[move_x + delta_x][move_y + delta_y]
            if target == '.':
                continue
            elif target == token:
                count += 1
            else:
                break
            if count == 3:
                total_opportunities_count += 1

    return total_opportunities_count


def results_in_a_winner(board, board_columns, token, other_token):
    # Make the move
    for i in range(7):
        if board_columns[i] == 6:
            continue
        # Check if other can win
        board[i][board_columns[i]] = other_token
        if check_winner(board, i, board_columns[i]):
            return other_token
        board[i][board_columns[i]] = '.'

    for i in range(7):
        if board_columns[i] == 6:
            continue
        # Check if other can win
        board[i][board_columns[i]] = token
        if check_winner(board, i, board_columns[i]):
            board_columns[i] += 1
            return results_in_a_winner(board, board_columns, other_token, token)
        board[i][board_columns[i]] = '.'


def get_next_move(board, token):
    board_columns_used = get_board_columns_used(board)
    available_moves = game.available_moves(board)
    preferred_locations = [3, 2, 4, 1, 5, 0, 6]
    preferred_locations = [x for x in preferred_locations if x in available_moves]
    priority_locations = get_columns_with_space(board, token, preferred_locations)
    opcode_limit = get_opcode_limit()
    losing_locations = set()
    skip_moves = set()

    # if state is None:
    #     state = {'opening_trap': False}

    moves_played = get_moves_played(board)

    other_token = 'X' if token == 'O' else 'O'

    for move in available_moves:
        board[move][board_columns_used[move]] = token
        if check_winner(board, move, board_columns_used[move]):
            print('MOVE: winning move')
            return move
        board[move][board_columns_used[move]] = '.'

    for move in available_moves:
        board[move][board_columns_used[move]] = other_token
        if check_winner(board, move, board_columns_used[move]):
            print('MOVE: blocking enemy win')
            return move
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

    # Opening book
    if moves_played == 1:
        if board[3][0] == other_token:
            losing_locations.add(3)

    if moves_played == 2:
        if board[3][1] == other_token:
            # state['opening_trap'] = True
            return 2
        if board[2][0] == other_token:
            return 2
        if board[4][0] == other_token :
            return 4

    if moves_played == 4:
        if board[3][1] == other_token and board[1][0] == '.' and board[4][0] == '.':
            return 4

    # Take the move if you see a open-ended 3 way opportunity
    for move in available_moves:
        if move in losing_locations:
            continue
        if move_makes_3_horizontal_with_spaces(board, move, board_columns_used[move], token):
            print('MOVE: 3-way opportunity')
            return move

    # Block 2 adjacent tokens for the enemy
    for move in available_moves:
        if move_makes_3_horizontal_with_spaces(board, move, board_columns_used[move], other_token):
            print('MOVE: block 3-way opportunity')
            return move

    for move in available_moves:
        if move in losing_locations or board_columns_used[move] > 4:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = token

        if check_winner(board, move, board_columns_used[move] + 1, ignore_vertical=True):
            skip_moves.add(move)

        board[move][board_columns_used[move]] = '.'
        board[move][board_columns_used[move] + 1] = '.'

    print(get_opcode_count())

    # Look for forced wins
    for move in skip_moves:
        if move in losing_locations or board_columns_used[move] > 2:
            continue
        board[move][board_columns_used[move]] = token
        board[move][board_columns_used[move] + 1] = other_token
        board[move][board_columns_used[move] + 2] = token

        if check_winner(board, move, board_columns_used[move] + 2):
            print('MOVE: Force WIN')
            return move

        board[move][board_columns_used[move] + 2] = '.'
        board[move][board_columns_used[move] + 1] = '.'
        board[move][board_columns_used[move]] = '.'

    # # Look for a sure win:
    # for move in available_moves:
    #     print(f'sure {move}')
    #     if move in losing_locations or board_columns_used[move] > 2:
    #         continue
    #     copy_board = [x[:] for x in board]
    #     copy_board_columns_used = board_columns_used[:]
    #     copy_board[move][copy_board_columns_used[move]] = token
    #     # copy_board[move][copy_board_columns_used[move] + 1] = token
    #
    #     # if not check_winner(copy_board, move, board_columns_used[move] + 1):
    #     #     continue
    #
    #     # copy_board[move][copy_board_columns_used[move] + 1] = '.'
    #     copy_board_columns_used[move] += 1
    #
    #     result = results_in_a_winner(copy_board, copy_board_columns_used, token, other_token)
    #     print(f'sure result: {result}')
    #
    #     if result == token:
    #         print('MOVE: Sure WIN')
    #         return move
    #     elif result == other_token:
    #         losing_locations.add(move)

    # Look for opening opportunities
    for move in preferred_locations:
        move_score = {}
        if move in skip_moves or move in losing_locations or board_columns_used[move] == 0:
            continue

        score = move_opens_opportunities(board, move, board_columns_used[move], token)
        if score > 0:
            move_score[move] = score

        if move_score:
            sorted_score = sorted(move_score.items(), key=itemgetter(1))
            print('MOVE: making opportunities')
            return sorted_score[0][0]

    # # Look for blocking opening opportunities
    # for move in preferred_locations:
    #     move_score = {}
    #     if move in skip_moves or move in losing_locations or board_columns_used[move] == 0:
    #         continue
    #
    #     score = move_opens_opportunities(board, move, board_columns_used[move], other_token)
    #     if score > 0:
    #         move_score[move] = score
    #
    #     if move_score:
    #         sorted_score = sorted(move_score.items(), key=itemgetter(1))
    #         print('MOVE: blocking enemy opportunities')
    #         return sorted_score[0][0]

    sorted_friendly_neighbours_score = None
    friendly_neighbours_score = {}

    for move in preferred_locations:
        if move in skip_moves or move in losing_locations or board_columns_used[move] == 0 or board_columns_used[move] == 0:
            continue
        friendly_neighbours = get_friendly_neighbours(board, move, board_columns_used[move], token)
        if friendly_neighbours > 1:
            friendly_neighbours_score[move] = friendly_neighbours

    if friendly_neighbours_score:
        sorted_friendly_neighbours_score = sorted(friendly_neighbours_score.items(), key=itemgetter(1))
        if sorted_friendly_neighbours_score[0][1] >= 3:
            print('MOVE: good friendlies')
            return sorted_friendly_neighbours_score[0][0]

    for move in preferred_locations:
        if move in skip_moves or move in losing_locations or board_columns_used[move] == 0 or board_columns_used[move] > 3:
            continue
        if not can_make_4_horizontal(board, move, board_columns_used[move], token):
            continue
        if move > 0:
            if board[move - 1][board_columns_used[move]] == token:
                print('MOVE: pair left')
                return move
        if move < 6:
            if board[move + 1][board_columns_used[move]] == token:
                print('MOVE: pair right')
                return move

    if sorted_friendly_neighbours_score:
        print('MOVE: weak neighbours')
        return sorted_friendly_neighbours_score[0][0]

    print(get_opcode_count())

    for move in priority_locations:
        if move not in available_moves or move in losing_locations or move in skip_moves:
            continue
        return move

    for move in preferred_locations:
        if move not in available_moves or move in losing_locations or move in skip_moves:
            continue
        return move

    for move in priority_locations:
        if move not in available_moves or move in losing_locations:
            continue
        return move

    for move in preferred_locations:
        if move not in available_moves or move in losing_locations:
            continue
        return move

    return random.choice(available_moves)
