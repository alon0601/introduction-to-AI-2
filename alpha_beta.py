import math
from heuristics import heuristic

h = heuristic


def alphabeta_max_h(current_game, id, depth=5):
    # add code here
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth, True, id)


def alphabeta_min_h(current_game, depth=5):
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth, False)


def minimax(current_game, alpha, beta, depth, maximize, id):
    best_move = "NO-OP"
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        # change this line according to graph
        return h(current_game, current_game.get_first_player()) - h(current_game, current_game.get_second_player()), current_game

    if maximize:
        v = -math.inf
        successors = current_game.get_moves(id)
        for successor, move in successors:
            mx, _ = minimax(successor, alpha, beta, depth - 1, False, 3-id)  # switch the id
            if v < mx:
                v = mx
                best_move = move
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_move

    else:
        v = math.inf
        successors = current_game.get_moves(id)
        for successor, move in successors:
            mx, _ = minimax(successor, alpha, beta, depth - 1, True, 3-id)
            if v > mx:
                v = mx
                best_move = move
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, best_move
