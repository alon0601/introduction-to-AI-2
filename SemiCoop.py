import math
import random

from heuristics import heuristic

h = heuristic


def max_h_coop(current_game, id, depth=6):
    # add code here
    results = []
    player_val = float('-inf')
    op_val = float('-inf')
    for s, move in current_game.get_moves(id):
        value, state = minimax_coop(s, depth, 3 - id)
        results.insert(0, (value, move))
        if player_val < value[id-1]:
            player_val = value[id-1]
            op_val = value[2-id]
        elif player_val == value[id-1] and op_val < value[2-id]:
            op_val = value[2-id]

    filteredresult = list(filter(lambda r: r[0][2-id] == op_val and r[0][id-1] == player_val, results))
    action = filteredresult[random.randint(0, len(filteredresult)-1)][1]
    return action


# def alphabeta_min_h(current_game, depth=5):
#       alpha = -math.inf
#     beta = math.inf
#     return minimax(current_game, alpha, beta, depth, False)


def minimax_coop(current_game, depth, id):
    best_move = "NO-OP"
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        game_value = (h(current_game, 1), h(current_game, 2))  # switch the id
        return game_value, best_move

    player_val = -math.inf
    op_val = -math.inf
    successors = current_game.get_moves(id)
    for successor, move in successors:
        game_value, _ = minimax_coop(successor, depth - 1, 3-id)
        if game_value[id-1] == player_val:
            if game_value[2-id] > op_val:
                op_val = game_value[2-id]
                best_move = move
        elif game_value[id-1] > player_val:
            player_val = game_value[id-1]
            op_val = game_value[2-id]
            best_move = move
    if id == 1:
        return (player_val, op_val), best_move
    else:
        return (op_val, player_val), best_move