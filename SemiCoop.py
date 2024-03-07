import math
import random

from heuristics import heuristic

h = heuristic


def max_h_coop(current_game, id, depth=5):
    # add code here
    results = []
    player_val = float('-inf')
    op_val = float('-inf')
    for s, move in current_game.get_moves(id):
        value, state = minimax_coop(s, depth, 3 - id)
        results.insert(0, (value, move))
        if player_val < value[1]:
            player_val = value[1]
            op_val = value[0]
        elif player_val == value[1] and op_val < value[0]:
            op_val = value[0]

    # print("results: ", results)

    filteredresult = list(filter(lambda r: r[0][0] == op_val and r[0][1] == player_val, results))
    # print("filtered results: ", filteredresult)
    action = filteredresult[random.randint(0, len(filteredresult)-1)][1]
    return action


# def alphabeta_min_h(current_game, depth=5):
#       alpha = -math.inf
#     beta = math.inf
#     return minimax(current_game, alpha, beta, depth, False)


def minimax_coop(current_game, depth, id):
    best_move = "NO-OP"
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        game_value = (h(current_game, id), h(current_game, 3 - id))  # switch the id
        return game_value, best_move

    player_val = -math.inf
    op_val = -math.inf
    successors = current_game.get_moves(id)
    # debugging:
    # print("depth: "+ str(depth))
    # print("player: " + str(id))
    # print("successors: " + str([mov for suc, mov in successors]))
    # for suc, mov in successors:
    #     print("move: " + mov)
    #     print("h: " + str(h(suc, id)))
    for successor, move in successors:
        game_value, _ = minimax_coop(successor, depth - 1, 3-id)
        if player_val < game_value[1]:
            player_val = game_value[1]
            op_val = game_value[0]
            best_move = move
        elif player_val == game_value[1] and op_val < game_value[0]:
            op_val = game_value[0]
            best_move = move
    return (player_val, op_val), best_move
