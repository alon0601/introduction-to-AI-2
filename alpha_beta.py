import math

h = None


def alphabeta_max_h(current_game, _heuristic, depth=5):
    global h
    h = _heuristic
    # add code here
    alpha = -math.inf
    beta = math.inf
    return maximin(current_game, alpha, beta, depth)


def alphabeta_min_h(current_game, _heuristic, depth=5):
    global h
    h = _heuristic
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth)


def maximin(current_game, alpha, beta, depth):
    global h
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        return h(current_game, current_game.get_first_player()) - h(current_game, current_game.get_second_player()), current_game
    v = -math.inf
    moves = current_game.get_moves(current_game)
    for move in moves:
        mx, next_move = minimax(move, alpha, beta, depth - 1)
        if v < mx:
            v = mx
            best_move = move
        alpha = max(alpha, v)
        if alpha >= beta:
            return v, move
    return v, best_move


def minimax(current_game, alpha, beta, depth):
    global h
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        return h(current_game, current_game.get_first_player()) - h(current_game, current_game.get_second_player()), current_game
    v = math.inf
    moves = current_game.get_moves(current_game)
    for move in moves:
        mx, next_move = maximin(move, alpha, beta, depth - 1)
        if v > mx:
            v = mx
            best_move = move
        beta = min(beta, v)
        if alpha >= beta:
            return v, move
    return v, best_move
