import random

MAX_DEPTH = 15


def semi_max_value(state, current_game, h):
    if state.terminated or current_game.is_game_finished():
        return h(current_game, current_game.get_first_player()) - h(current_game, current_game.get_second_player()), None
    if state.g >= MAX_DEPTH:
        return eval(state)
    v = float('-inf')
    u = float('-inf')
    successors = current_game.get_moves()
    for s in successors:
        my_val, opponent_value = semi_max_value(s, current_game, h)
        if v == my_val:
            if opponent_value > u:
                u = opponent_value
        elif v < my_val:
            v = my_val
            u = opponent_value
    return v, u


def semi_maximax_decision(current_game, h):
    results = []
    val_action = float('-inf')
    opponent_val_score = float('-inf')
    for s in current_game.get_moves():
        my_value, opponent_value = semi_max_value(s, current_game, h)
        results.insert(0, (my_value,opponent_value, s.player2.node))
        if my_value > val_action:
            val_action = my_value
            opponent_val_score = opponent_value
        elif my_value == val_action:
            if opponent_value > opponent_val_score:
                opponent_val_score = opponent_value
    # if DEBAG:
    print("results: ", results)
    filtered_result = list(filter(lambda r: r[0] == val_action and r[1] == opponent_val_score, results))
    print("filtered results: ", filtered_result)
    action = filtered_result[random.randint(0, len(filtered_result)-1)][2]
    return action
