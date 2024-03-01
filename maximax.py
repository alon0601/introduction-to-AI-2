import random

MAX_DEPTH = 15


def max_value(state, current_game, h):
    if state.terminated or current_game.is_game_finished():
        return  h(current_game, current_game.get_first_player()) + h(current_game, current_game.get_second_player()), None
    if state.g >= MAX_DEPTH:
        return eval(state)
    v = float('-inf')
    successors = current_game.get_moves()
    for s in successors:
        min_val = max_value(s, current_game, h)
        v = max(v, min_val)
    return v


def maximax_decision(state, current_game, h):
    results = []
    val_action = float('-inf')
    for s in current_game.get_moves():
        temp_value = max_value(s, current_game, h)
        results.insert(0, (temp_value, s.player2.node))
        if temp_value > val_action:
            val_action = temp_value
    print("results: ", results)
    filtered_result = list(filter(lambda r: r[0] == val_action, results))
    print("filtered results: ", filtered_result)
    action = filtered_result[random.randint(0, len(filtered_result)-1)][1]  # choose an action with max value randomly
    return action
