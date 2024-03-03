import math
from heuristics import heuristic

h = heuristic


def alphabeta_max_h(current_game, id, depth=5):
    # add code here
    alpha = -math.inf
    beta = math.inf
    return minimax(current_game, alpha, beta, depth, True, id)


# def alphabeta_min_h(current_game, depth=5):
#     alpha = -math.inf
#     beta = math.inf
#     return minimax(current_game, alpha, beta, depth, False)


def minimax(current_game, alpha, beta, depth, maximize, id):
    best_move = "NO-OP"
    if current_game.is_terminal() or current_game.is_game_finished() or depth == 0:
        game_value = h(current_game, id) - h(current_game, 3 - id)  # switch the id
        if not maximize:
            game_value = -game_value
        return game_value, best_move

    if maximize:
        v = -math.inf
        successors = current_game.get_moves(id)
        # debugging:
        # print("depth: "+ str(depth))
        # print("player: " + str(id))
        # print("successors: " + str([mov for suc, mov in successors]))
        # for suc, mov in successors:
        #     print("move: " + mov)
        #     print("h: " + str(h(suc, id)))
        for successor, move in successors:
            mx, _ = minimax(successor, alpha, beta, depth - 1, False, 3-id)
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
