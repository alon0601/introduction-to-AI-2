import math

h = None


def alphabeta_max_h(current_game, _heuristic, depth=5):
    global h
    h = _heuristic
    # add code here
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth, True)


def alphabeta_min_h(current_game, _heuristic, depth=5):
    global h
    h = _heuristic
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth, False)


def minimax(current_game, alpha, beta, depth, maximize):
    global h
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        return h(current_game, current_game.get_first_player()) - h(current_game, current_game.get_second_player()), current_game

    if maximize:
        v = -math.inf
        moves = current_game.get_moves(current_game)
        for move in moves:
            mx, next_move = minimax(move, alpha, beta, depth - 1, False)
            if v < mx:
                v = mx
                best_move = move
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_move

    else:
        v = math.inf
        moves = current_game.get_moves(current_game)
        for move in moves:
            mx, next_move = minimax(move, alpha, beta, depth - 1, True)
            if v > mx:
                v = mx
                best_move = move
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, best_move