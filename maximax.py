import math
import random

from heuristics import heuristic

h = heuristic


def max_value(current_game, id, depth=5):
    best_move = "NO-OP"
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        return h(current_game, id) + h(current_game, 3 - id), best_move  # switch the id
    v = float('-inf')
    successors = current_game.get_moves(id)
    for s, move in successors:
        mx, _ = max_value(s, 3 - id, depth - 1)
        if v < mx:
            v = mx
            best_move = move
    return v, best_move


def maximax_decision(current_game, id):
    results = []
    val_action = float('-inf')
    for s, move in current_game.get_moves(id):
        temp_value, _= max_value(s, 3 - id)
        results.insert(0, (temp_value, move))
        if temp_value > val_action:
            val_action = temp_value
    print("results: ", results)
    filtered_result = list(filter(lambda r: r[0] == val_action, results))
    print("filtered results: ", filtered_result)
    action = filtered_result[random.randint(0, len(filtered_result)-1)][1]  # choose an action with max value randomly
    return action
